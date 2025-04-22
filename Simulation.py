from sympy.matrices.expressions.matexpr import MatrixElement
from SimulationMessage import (
    Message,
    SystemTimeMessage,
    SwitchMessage,
    VoltageCurrentMessage,
    OversamplingMessage
)
import copy
import math
from Element import ExternalSwitch, Diode, VoltageCurrentSource, Element, Voltmeter, Ammeter
from FormNetworkMatrix import NetworkMatrix
import scipy
from sympy import Matrix
import sympy as sp
import sympy.logic as sp_logic
from util import (print_matrix,is_rise_edge, retrieveSystemMatrix,
                  get_backward_euler_integartion, get_trapezoid_integration, 
                  update_system_matrix_to_reflect_dependency,retrieve_Zsw_hat,get_tustin_integration, radau_integration_step,
                  get_pade_03_integeration, int_to_binary_list,
                  get_pade_0_2_matrix, state_iteration,get_radau_integration, get_forward_euler_integration
                  )
from typing import Tuple
import pandas as pd
import numpy as np
import numpy.typing as npt
from functools import total_ordering
import matplotlib.pyplot as plt
import matplotlib.ticker as plt_ticker
from matplotlib.widgets import CheckButtons
from visualize import on_pick, toggle_visibility
from matplotlib.widgets import CheckButtons
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv
import warnings

@total_ordering
class SimulationModule:
    def __init__(self):
        self.cur_system_time  = None
        self.publish_message = None
    
        self.message_level_dependent = 0
        
    def __eq__(self, other):
        return self.message_level_dependent == other.message_level_dependent
    
    def __lt__(self, other):
        return self.message_level_dependent < other.message_level_dependent

    def update(self, message):
        pass
    
    def publish(self):
        pass


class SystemClockSimulationModule:
    def __init__(
        self, systen_clock_frequency: float, system_clock_message: SystemTimeMessage
    ):
        super().__init__()
        self.system_clock_frequency = systen_clock_frequency
        self.system_clock_message = system_clock_message

    
        self.module_level_depend_map:dict[int, list[SimulationModule]] = {}
        
        
    def update_list_of_node_module(self, list_of_node_modules:list[SimulationModule]):
 
        # sort by their levels
        list_of_node_modules.sort()
        for i in range(len(list_of_node_modules)):
            mod = list_of_node_modules[i]
            if mod.message_level_dependent not in self.module_level_depend_map.keys():
                self.module_level_depend_map[mod.message_level_dependent] = [mod]
            else:
                self.module_level_depend_map[mod.message_level_dependent].append(mod)
        
        
    def start_simuation(self, end_simulation_time: float):
        stop_step_size = int(
            math.ceil(end_simulation_time * self.system_clock_frequency)
        )

        
        # now, regular clock
        for step in range( stop_step_size):
            

            
            self.system_clock_message.set_time(step * (1 / self.system_clock_frequency))
            for level in self.module_level_depend_map.keys():
                self.system_clock_message.message_manager.publish_message(level)
                #TODO: invoke module calculation
                
                for mod in self.module_level_depend_map[level]:
                    mod.publish()


class VoltageCurrentSimulationModule(SimulationModule):
    def __init__(
        self,
        source: VoltageCurrentSource,
        voltage_current_source_message: VoltageCurrentMessage,
    ):
        super().__init__()
        self.source = source
        self.voltage_current_source_message = voltage_current_source_message
        self.cur_source_value = 0
        self.message_level_dependent = 1


    def sinewave_at_time_t(self, time_t):
        """
        Computes the value of a sine wave at a specific time.

        Parameters:
        - time_t (float): Time in seconds to evaluate the sine wave.

        Returns:
        - float: Value of the sine wave at the given time.
        """

        
        # Angular frequency (omega) in radians per second
        angular_frequency = 2 * math.pi * self.source.frequency

        # Sine wave value
        
        return self.source.amplitude * math.sin(angular_frequency * time_t) if self.source.frequency > 0 else self.source.amplitude

    
    def update(self, message):
        
        # only receive SystemTimeMEssage
        assert isinstance(message, SystemTimeMessage)
        
        self.cur_system_time = message.get_time()
        

        self.cur_source_value = self.sinewave_at_time_t(message.get_time())
        # print(message.get_time(),   self.cur_source_value)
    def publish(self):

        if self.source.is_voltage_source:
            self.voltage_current_source_message.set_value(
                self.cur_source_value, self.source.element_voltage_name, 
                self.cur_system_time
            )
        else:
            self.voltage_current_source_message.set_value(
                self.cur_source_value, self.source.element_current_name,
                  self.cur_system_time
            )



class SwitchSimulationModule(SimulationModule):
    def __init__(self, switch: ExternalSwitch, switch_message: SwitchMessage, system_clock_frequency:float):
        super().__init__()
        self.switch: ExternalSwitch = switch

        assert self.switch.duty_cycle <= 1.0
        self.cur_switch_status = switch.initial_switch_state
        self.switch_message = switch_message
        self.message_level_dependent = 1
        self.sampling_frequency = system_clock_frequency
    def pwm_at_time_t(self, time_t, delay=0) -> bool:
        period = 1 / self.switch.switch_frequency
        adjusted_time = time_t - delay

        # Numerically stable modulo operation
        time_in_period = adjusted_time - period * math.floor(adjusted_time / period)

        # Round to the nearest step of time_t if iteration step dt is known
        dt = 1 / self.sampling_frequency  # Known discrete time step
        time_in_period = round((time_in_period) / dt, 9) * dt  

        high_duration = self.switch.duty_cycle * period

        if self.switch.duty_cycle == 0.0:
            return False
        if self.switch.duty_cycle == 1.0:
            return True
        val =time_in_period + dt <= high_duration or (time_in_period+dt) >= period 
        #val = time_in_period < high_duration
        return val if self.switch.pwm_value_at_each_new_cycle else not val   
    def update(self, message):
        # only accept systemtime message
        assert isinstance(message, SystemTimeMessage)
        self.cur_system_time = message.get_time()
        
    def publish(self):
        
        if self.cur_system_time == 0:
            self.cur_switch_status = self.switch.initial_switch_state
        else:
            self.cur_switch_status = self.pwm_at_time_t(self.cur_system_time, self.switch.time_delay)
        self.switch_message.set_switch_status(
            self.cur_switch_status, self.switch.element_voltage_name, self.cur_system_time
        )
        






class SwitchOversampleModule(SimulationModule):
    def __init__(self, sample_frequency: float, network_matrix: NetworkMatrix, oversample_message:OversamplingMessage):
        super().__init__()
        self.message_level_dependent = 2
        self.oversample_message = oversample_message
        
        self.sample_frequency = sample_frequency
        self.network_matrix = network_matrix

        # dictionary of both current/voltage label of switch to a list[] contain the switch states
        
        self.switch_state_dict: dict[str,int] = {}  # switch_voltage_label map to index in array
        self.switch_states_receive:list[bool | None] = [None] * len(self.network_matrix.external_switch_labels)
        
        for i in range(len(self.network_matrix.external_switch_labels)):
            s_lab = self.network_matrix.s_labels[i]
            s_ele = self.network_matrix.m_column_labels_to_obj_map[s_lab]
            self.switch_state_dict[ s_ele.element_voltage_name  ] = i
         
        self._switch_update_count = 0

    def update(self, message: Message):
    
        
        if isinstance(message, SystemTimeMessage):
            self.cur_system_time = message.get_time()
        elif isinstance(message, SwitchMessage):
            can_receive_switch = is_rise_edge(self.sample_frequency, self.cur_system_time) or self.cur_system_time ==0
            assert self.cur_system_time == message.system_time
            if can_receive_switch:
                index = self.switch_state_dict[message.switch_voltage_label]
                if self.cur_system_time  ==  0:
                    # initialize stage
                    self.switch_states_receive[index] = message.is_switch_on()
                else:
                    # normal stage
                    self.switch_states_receive[index] = message.is_switch_on()

    def publish(self, ):
        
        can_publish = self.cur_system_time ==0 or is_rise_edge(self.sample_frequency, self.cur_system_time)
        

        if can_publish:
            self.oversample_message.notify_result(self.switch_state_dict, self.switch_states_receive.copy(), self.cur_system_time)

        


class StateSpaceSimulationModule(SimulationModule):
    def __init__(self, network_matrix: NetworkMatrix, iteration_frequency: float):
        super().__init__()
        self.network_matrix = network_matrix

        self.iteration_frequency = iteration_frequency
        self.message_level_dependent = 3
        
        
        self.u_label_map = {u_lab: i for i, u_lab in enumerate(self.network_matrix.u_labels)}
        self.u_size = len(self.network_matrix.u_labels)
        self.u = np.ndarray( ( 1, self.u_size ), dtype=np.float32 )

        # element label resemble in the order of s_label in self.network_matrix
        self.switch_label_index_map:dict[str, int] = {}
        self.switch_index_label_map:dict[int, (str,str)] ={}
        # self.switch_mask:npt.NDArray[np.bool_] =  None
        self.diode_index:list[int] = []
        self.external_switch_index:list[int] = []
        self.switch_state:list[bool] = None
        self.switch_triggered:list[bool] = None
        
        
        # the iteration process
        self.number_of_state_variable = len(self.network_matrix.x_labels)
        self.__x_cur_ind = np.ndarray((self.number_of_state_variable,1), dtype=np.float32, )
        self.__x_cur_ind[:,:] = 0
        
        self.x_with_dep = np.ndarray((self.number_of_state_variable,1), dtype=np.float32, )
        self.x_with_dep[:,:] = 0

        self.y_cur = np.ndarray(  (self.network_matrix.u_label_size, 1), dtype=np.float32)
        self.y_cur[:, 0] = 0


        # from the paper by antonio
        # y= C1*X_hat + C*x + D*u
        # but here, we did some analysis and simplfiy out the stuff 
        # If see update_system_matrix_to_reflect_dependency()
        # C1 -> C_impulse and D_impulse
        # C -> C_nonimpulse
        # D-> D_nonimpulse
        self.Q:npt.NDArray = None
        self.C: npt.NDArray =None
        self.C1:npt.NDArray = None
        self.D :npt.NDArray = None
        self.M0 :npt.NDArray = None
        self.A :npt.NDArray = None
        self.B :npt.NDArray = None
        self.M_pivots: Tuple=None
        
        self.diode_index_y_index_mapping: dict[int, int] = {}
        self.C_impulse:npt.NDArray = None
        self.C_non_impulse:npt.NDArray= None
        self.D_impulse:npt.NDArray = None
        self.D_non_impulse:npt.NDArray = None
        self.A_dependent:npt.NDArray = None
        self.B_dependent:npt.NDArray =  None

        #states related to switch changes
        self.C1_diode_sw:npt.NDArray = None
        self.C_diode_sw:npt.NDArray = None
        self.D_diode_sw: npt.NDArray = None
        self.C_mult_A : npt.NDArray = None  # x_hat 
        self.C_mult_B :npt.NDArray = None
        
        # The pre-comuated matrix used for switch changes
        self.C_diode_impulse_sw: npt.NDArray = None
        self.C_diode_natural_sw: npt.NDArray = None
        self.D_diode_natural_sw: npt.NDArray = None
        self.C_diode_explicit_der_mult_delta_t_sw: npt.NDArray = None
        self.D_diode_explicit_der_mult_delta_t_sw: npt.NDArray = None

    
        self.x_next_with_dep_A: npt.NDArray = None
        self.X_next_with_dep_B: npt.NDArray = None
        
        self.independent_state_labels:list[str] = []
        self.dependent_state_labels:list[str] = []
        self.y_dep_labels:list[str] = []
        self.forced_switch_mapping:dict[Element, list[Element]] = {}
        
        self.M_cache :dict[str, Matrix] = {}
        
        
        # ouput and debug record
        self.time_t:list[float] = []
        self.y_output:list[list[float]] = []
        self.x_output:list[list[float]] = []
        
        self.switch_state_output:list[list[int]] = []
        self.switch_triggered_output:list[list[int]] = []
        

        self.solver_zero_input_res:npt.NDArray = None
        self.solver_zero_state_res:npt.NDArray = None

        self.switch_last_output = np.zeros(self.network_matrix.s_labels_size)
        self.use_impulse_in_y_output = False
        self.initialize_data()
    
    def generate_M_cache_key(self,key_list:list[bool|int], value_type="" )->str:
        
        if value_type == "": # assume is bool type in list
            return ''.join(['T' if state else 'F' for state in key_list])
        else:
            return ''.join(['T' if state==1 else 'F' for state in key_list])
    def force_triggered_events(self )->dict[ExternalSwitch, list[Diode]]:
        # see if network inconsistent could cause by switch events
        inconsistent_row_len = len(self.y_dep_labels)
        if inconsistent_row_len == 0:
            return {}
        
        start_row = self.network_matrix.M.rows -inconsistent_row_len
        
        forced_switch_diode_mapping= {}  # each swithc can map to 1 or more diode
                                        # but not switch map to other switch
        
        for row in range(start_row, self.network_matrix.M.rows):
            row_in_m = self.network_matrix.M[row, :]
            diode_list= []
            switch_list = []
            for i in range( len(row_in_m)):
                if row_in_m[i] != 0:
                    lab = self.network_matrix.m_column_labels[i]
                    ele = self.network_matrix.m_column_labels_to_obj_map[lab]
                    if isinstance(ele, Diode):
                        diode_list.append(ele)
                    elif isinstance(ele, ExternalSwitch):
                        switch_list.append(ele)
            
            if len(switch_list) >0 and len(diode_list) > 0:
                assert len(switch_list) == 1
                forced_switch_diode_mapping[switch_list[0]] = diode_list
        
        return forced_switch_diode_mapping

    def swap_difference(self, bool_states:list[bool])->list[str]:
        # given list of T/F states for switch/diode in self.network_matrix.s_labels
        # update curent switch and network matrix to given states in 'bool_states'
        list_to_swap = []
        for idx, cur_switch_state in enumerate(self.switch_state):
            if cur_switch_state != bool_states[idx]:
                self.switch_state[idx] = bool_states[idx]
                list_to_swap.append(  self.switch_index_label_map[idx][0])

        self.swap_col_and_update(list_to_swap)
        # sanity check after swapping
        for idx, state in enumerate(self.switch_state):
            assert bool_states[idx] == state

            if state:
                assert self.switch_index_label_map[idx][1] == self.network_matrix.s_labels[idx]
            else:
                assert self.switch_index_label_map[idx][0] == self.network_matrix.s_labels[idx]
                
    def iterative_all_possible_switch_scenarion(self):
        current_switch_states = self.switch_state.copy()
        total_switch_case = 2**(self.network_matrix.s_labels_size)
        
        
        for case in range(total_switch_case):
            bool_states, _ = int_to_binary_list(case, self.network_matrix.s_labels_size)
            # now, go ahead and    
            self.swap_difference(bool_states)
            
        # now, swap back to initial states 
        self.swap_difference(current_switch_states)
        
        assert [ x== y for x,y in zip(current_switch_states, self.switch_state)]
        
    def diode_interest_index_in_y_labels(
        self
    ):
        # recall for diode soft-switch(when not affect by the impulse), 
        # from Antonio Massarini(An efficient algorithm for xxx)
        # when diode is on, we look at the current, when off, look at the voltage
        # if diode's current <0(when on) or diode voltage >0(off), a soft switch happen
        
        
        
        # however, for our y_labels, we have a list of y_output, we need to know the index of diode's voltage or current
        
        diode_index_to_y_label_index:dict[int, int] = {}
        
        for diode_ind,  diode_i in enumerate(self.diode_index):
            
            if self.switch_state[diode_i]:  # look at current  
                sw_ele:Diode = self.network_matrix.m_column_labels_to_obj_map[   self.switch_index_label_map[diode_i][1]  ]
                
            else:
                sw_ele:Diode = self.network_matrix.m_column_labels_to_obj_map[   self.switch_index_label_map[diode_i][0]  ]
             
            assert isinstance(sw_ele, Diode)
            if(self.switch_state[diode_i]):
                assert sw_ele.element_current_name == self.switch_index_label_map[diode_i][1] 
                diode_ammeter = self.network_matrix.element_name_obj_map[sw_ele.diode_ammeter_name]
                y_index = self.network_matrix.y_labels.index(diode_ammeter.element_current_name)
            else:
                assert sw_ele.element_voltage_name == self.switch_index_label_map[diode_i][0] 
                diode_voltmeter = self.network_matrix.element_name_obj_map[sw_ele.diode_voltmeter_name]
                y_index = self.network_matrix.y_labels.index(diode_voltmeter.element_voltage_name)

            diode_index_to_y_label_index[diode_ind ] = y_index
        return diode_index_to_y_label_index    
    
    def get_Y_hat_A_B(self,A: Matrix, B: Matrix, C: Matrix):
        
        # from the 2021 paper by DSPACE
        # want to predict the voltage/current of diode in next step to reduce numerical oscillation scenario
        
        # recall Y = C_final *x+ D_final*u
        # Y_hat = C_final *X_hat + D_final * u_hat
        # If assume u_hat to be 0 for a very small iteration interval
        #Y_hat = C_final * X_hat = C_Final *(A*X + B*u)        
        Y_hat_A = C @A
        Y_hat_B = C @ B
        return Y_hat_A, Y_hat_B
        
    def get_diode_softswitch_interest_matrix(self, diode_ind_to_y_ind:dict[int, int],
                                            C1: Matrix, 
                                            A:Matrix, B: Matrix, C: Matrix, D: Matrix, 
                                            C_impulse_matrix:Matrix, C_nonimpulse_matrix:Matrix, 
                                            D_impulse_matrix:Matrix, D_nonimpulse_matrix:Matrix
                                       
                                             ):

        
        Y_hat_A, Y_hat_B = self.get_Y_hat_A_B(A, B,C)
        
        C1_diode_sw = sp.zeros( len(diode_ind_to_y_ind), self.network_matrix.x_hat_label_size )
        C_diode_sw = sp.zeros(len(diode_ind_to_y_ind), self.network_matrix.x_hat_label_size )
        D_diode_sw= sp.zeros(len(diode_ind_to_y_ind), self.network_matrix.u_label_size)
        
        C_impulse_sw=sp.zeros(len(diode_ind_to_y_ind), self.network_matrix.x_hat_label_size)
        D_impulse_sw=sp.zeros(len(diode_ind_to_y_ind), self.network_matrix.u_label_size)
        
        
        C_nonimpulse_sw=sp.zeros(len(diode_ind_to_y_ind), self.network_matrix.x_hat_label_size)
        D_nonimpulse_sw = sp.zeros(len(diode_ind_to_y_ind), self.network_matrix.u_label_size)
        

        
        Y_hat_A_sw = sp.zeros(len(diode_ind_to_y_ind),  self.network_matrix.x_hat_label_size)
        Y_hat_B_sw = sp.zeros(len(diode_ind_to_y_ind), self.network_matrix.u_label_size)
        
        for diode_idx, y_lab_idx in diode_ind_to_y_ind.items():
            C1_diode_sw[diode_idx, :] = C1[y_lab_idx, :]
            C_diode_sw[diode_idx,:] = C[y_lab_idx, :]
            D_diode_sw[diode_idx, :] = D[y_lab_idx, :]
            C_impulse_sw[diode_idx, :] = C_impulse_matrix[y_lab_idx, :]
            D_impulse_sw[diode_idx, :] = D_impulse_matrix[y_lab_idx, :]
            
            C_nonimpulse_sw[diode_idx, :] = C_nonimpulse_matrix[y_lab_idx, :]
            D_nonimpulse_sw[diode_idx, :] = D_nonimpulse_matrix[y_lab_idx, :]
            
            Y_hat_A_sw[diode_idx, :] = Y_hat_A[y_lab_idx, :]   
            Y_hat_B_sw[diode_idx, :] = Y_hat_B[y_lab_idx, :]
        
        
        return sp.matrix2numpy(C1_diode_sw, dtype=np.float32), \
            sp.matrix2numpy(C_diode_sw, dtype=np.float32), sp.matrix2numpy(D_diode_sw, dtype=np.float32),\
                sp.matrix2numpy(C_impulse_sw,dtype=np.float32), sp.matrix2numpy(C_nonimpulse_sw, dtype=np.float32), \
                    sp.matrix2numpy(D_impulse_sw, dtype=np.float32) , sp.matrix2numpy(D_nonimpulse_sw,dtype=np.float32),\
                        sp.matrix2numpy(Y_hat_A_sw,dtype=np.float32), sp.matrix2numpy(Y_hat_B_sw,dtype=np.float32)   
        
        
    def swap_col_and_update(self, label_to_Swap:list[str], assert_no_cache=False, assert_cache=False):
        if len(label_to_Swap) >0:
            for lab in label_to_Swap:
                self.network_matrix.swap_M_matrix_columns(lab)
        # do a cache
        

        if None in self.switch_state:
            # means from the init srage
            key = ""
        else:
            key =self.generate_M_cache_key(self.switch_state)    #= ",".join(self.switch_state)
        if key not in self.M_cache.keys():
            assert not assert_no_cache
            self.network_matrix.rref_update()
            self.Q, self.C1, self.C, self.D, self.M0, self.A, self.B, self.y_dep_labels,M_offset_info = retrieveSystemMatrix(
                M=self.network_matrix.M,
                m_pivots=self.network_matrix.M_pivots,
                m_labels=self.network_matrix.m_column_labels,
                s_labels_size=self.network_matrix.s_labels_size,
                y_labels_size=self.network_matrix.y_label_size,
                x_hat_labels_size=self.network_matrix.x_hat_label_size,
                x_labels_size=self.network_matrix.x_label_size,
                y_zero_labels_size=self.network_matrix.y_zero_label_size,
                s_zero_labels_size=self.network_matrix.s_zero_label_size,
                capacitor_size=self.network_matrix.capacitor_size,
                inductor_size=self.network_matrix.inductor_size,
                voltage_source_size=self.network_matrix.voltage_source_size,
                current_source_size=self.network_matrix.current_source_Size,
                redundant_offset=self.network_matrix.redundant_size
            )
            
            self.forced_switch_mapping = self.force_triggered_events()
            
            
            # filter out inconsistent labels from y _labels
            M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final, \
                self.C_impulse, self.C_non_impulse, self.D_impulse, self.D_non_impulse, \
                self.independent_state_labels, self.dependent_state_labels, C1_final= update_system_matrix_to_reflect_dependency(
                M0=self.M0.copy(),
                Q =self.Q.copy(),
                C1 = self.C1.copy(),
                A=self.A.copy(), B=self.B.copy(), C=self.C.copy(), D=self.D.copy(),
                m_pivots=self.network_matrix.M_pivots,
                u_labels=self.network_matrix.u_labels,
                y_labels= self.network_matrix.y_labels,
                y_dependent_labels=self.y_dep_labels,
                x_hat_labels=self.network_matrix.x_hat_labels,
                x_hat_col_offset_in_m_pivots=M_offset_info["x_hat_col_offset"],
                x_hat_label_to_obj_map=self.network_matrix.m_column_labels_to_obj_map,
                symbol_to_value_map=self.network_matrix.symbolic_to_value_map,
                element_name_to_obj_map=self.network_matrix.element_name_obj_map
            )
                
            self.C1 = C1_final[:, :]
            self.M0= M0_final[:,:]
            self.A = A_final[:,:]
            self.B = B_final[:,:]
            self.C = C_final[:,:]
            self.D = D_final[:,:]
            self.A_dependent = A_dependent_final[:,:]
            self.B_dependent = B_dependent_final[:,:]


            
            
            # diode_column_label = [] # if diode is on, give I_D, if diode is off, give V_D
            
            # for diode_i in self.diode_index:
                
            #     if self.switch_state[diode_i]:
            #         diode_column_label.append(self.switch_index_label_map[diode_i][1])
            #     else:
            #         diode_column_label.append(self.switch_index_label_map[diode_i][0])
            
            
            # self.C1_SW, self.C_SW, self.D_SW, self.C_impulse_SW, self.D_impulse_SW, self.C_non_impulse_SW, self.D_non_impulse_SW,  self.Z_hat_SW_A, self.Z_hat_SW_B = retrieve_Zsw_hat(  
            #                     A=self.A, B=self.B, C=self.C, D=self.D, C1=self.C1, 
            #                 C_impulse_matrix=self.C_impulse, C_nonimpulse_matrix=self.C_non_impulse,
            #                 D_impulse_matrix=self.D_impulse, D_nonimpulse_matrix=self.D_non_impulse,
            #                 x_hat_labels=self.network_matrix.x_hat_labels, u_labels=self.network_matrix.u_labels,
            #                 diode_column_labels=diode_column_label, y_labels=self.network_matrix.y_labels,
                      
            #                 element_name_obj_map=self.network_matrix.element_name_obj_map,
            #                 m_column_labels_to_obj_map=self.network_matrix.m_column_labels_to_obj_map
            #                 )
    
            self.diode_index_y_index_mapping = self.diode_interest_index_in_y_labels()

            # check if they are the same or not
            
            

            # now, Cache all the matrix that relateds to swicth state changing
            
            self.C1_diode_sw, self.C_diode_sw, self.D_diode_sw, \
                _, _, _, _, self.C_mult_A, self.C_mult_B = self.get_diode_softswitch_interest_matrix(
                    C1 = Matrix(self.C1), A = Matrix(self.A), B= Matrix(self.B), C= Matrix(self.C), D= Matrix(self.D),
                    C_impulse_matrix=Matrix(self.C_impulse), C_nonimpulse_matrix=Matrix(self.C_non_impulse),
                    D_impulse_matrix=Matrix(self.D_impulse), D_nonimpulse_matrix=Matrix(self.D_non_impulse),
                    diode_ind_to_y_ind = self.diode_index_y_index_mapping
                )
            
            I_A_dependent = sp.eye( self.A_dependent.shape[0] )
            self.C_diode_impulse_sw = np.matmul(  self.C1_diode_sw, (self.A_dependent - I_A_dependent ))  # for finding C_impulse, just multiply x_cur with this matrix
            self.C_diode_natural_sw = self.C_diode_sw.copy()
            self.D_diode_natural_sw = self.D_diode_sw.copy()
            self.C_diode_explicit_der_mult_delta_t_sw = self.C_diode_natural_sw + np.multiply(self.C_mult_A, 1/self.iteration_frequency)
            self.D_diode_explicit_der_mult_delta_t_sw  = self.D_diode_natural_sw + np.multiply(self.C_mult_B, 1/self.iteration_frequency)
 
            
            # discretized A,B,C,D
            
            self.A = sp.matrix2numpy(self.A.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.B = sp.matrix2numpy(self.B.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C = sp.matrix2numpy(self.C.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.D = sp.matrix2numpy(self.D.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C1 = sp.matrix2numpy(self.C1.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.solver_zero_input_res, self.solver_zero_state_res = get_pade_03_integeration(self.A, self.B, 1/self.iteration_frequency)
            #self.solver_zero_input_res, self.solver_zero_state_res = get_pade_0_2_matrix(self.A, self.B, 1/self.iteration_frequency)
            #self.solver_zero_input_res, self.solver_zero_state_res = get_trapezoid_integration(self.A, self.B, 1/self.iteration_frequency)   
            # self.solver_zero_input_res, self.solver_zero_state_res = get_tustin_integration(self.A, self.B, 1/self.iteration_frequency)    
            # self.solver_zero_input_res, self.solver_zero_state_res = get_radau_integration(self.A, self.B, 1/self.iteration_frequency)         
            #self.solver_zero_input_res, self.solver_zero_state_res = get_backward_euler_integartion(self.A, self.B, 1/self.iteration_frequency)
            self.A_dependent = sp.matrix2numpy(self.A_dependent.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.B_dependent = sp.matrix2numpy(self.B_dependent.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C_impulse = sp.matrix2numpy(self.C_impulse.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C_non_impulse = sp.matrix2numpy(self.C_non_impulse.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.D_impulse = sp.matrix2numpy(self.D_impulse.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.D_non_impulse = sp.matrix2numpy(self.D_non_impulse.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.x_next_with_dep_A  = np.matmul(self.A_dependent,  self.solver_zero_input_res)
            self.X_next_with_dep_B = np.matmul(self.A_dependent, self.solver_zero_state_res)
            cache_Data = [
                self.network_matrix.M.copy(), 
                self.C1.copy(), self.C.copy(), self.D.copy(),
                self.M0.copy(), self.A.copy(), self.B.copy(),

                self.y_dep_labels.copy(),
                self.A_dependent.copy(),
                self.B_dependent.copy(),

                self.forced_switch_mapping.copy(),
                self.C_impulse.copy(),
                self.C_non_impulse.copy(),
                self.D_impulse.copy(),
                self.D_non_impulse.copy(),


                self.Q.copy(),
                self.independent_state_labels.copy(),
                self.dependent_state_labels.copy(),
                self.solver_zero_input_res.copy(),
                self.solver_zero_state_res.copy(),
                self.diode_index_y_index_mapping.copy(),
                self.C1_diode_sw.copy(),
                self.C_diode_sw.copy(),
                self.D_diode_sw.copy(),
                self.C_mult_A.copy(),
                self.C_mult_B.copy(),
                self.C_diode_impulse_sw.copy(),
                self.C_diode_natural_sw.copy(),
                self.D_diode_natural_sw.copy(),
                self.C_diode_explicit_der_mult_delta_t_sw.copy(),
                self.D_diode_explicit_der_mult_delta_t_sw.copy(),
                self.x_next_with_dep_A.copy(),
                self.X_next_with_dep_B.copy()
            ]

            self.M_cache[key] = cache_Data
                        
            
        else:
            cache_Data = self.M_cache[key]
            self.network_matrix.M = cache_Data[0].copy()
            self.C1 = cache_Data[1].copy()
            self.C = cache_Data[2].copy()
            self.D = cache_Data[3].copy()
            self.M0 = cache_Data[4].copy()
            self.A = cache_Data[5].copy()
            self.B = cache_Data[6].copy()

            self.y_dep_labels = cache_Data[7].copy()
            self.A_dependent = cache_Data[8].copy()
            self.B_dependent = cache_Data[9].copy()

            self.forced_switch_mapping = cache_Data[10].copy()
            self.C_impulse = cache_Data[11].copy()
            self.C_non_impulse = cache_Data[12].copy()
            self.D_impulse = cache_Data[13].copy()
            self.D_non_impulse = cache_Data[14].copy()


            self.Q = cache_Data[15].copy()
            self.independent_state_labels = cache_Data[16].copy()
            self.dependent_state_labels = cache_Data[17].copy()
            self.solver_zero_input_res = cache_Data[18].copy()
            self.solver_zero_state_res = cache_Data[19].copy()
            self.diode_index_y_index_mapping = cache_Data[20].copy()
            self.C1_diode_sw = cache_Data[21].copy()
            self.C_diode_sw = cache_Data[22].copy()
            self.D_diode_sw = cache_Data[23].copy()
            self.C_mult_A = cache_Data[24].copy()
            self.C_mult_B = cache_Data[25].copy()
            self.C_diode_impulse_sw = cache_Data[26].copy()
            self.C_diode_natural_sw = cache_Data[27].copy()
            self.D_diode_natural_sw = cache_Data[28].copy()
            self.C_diode_explicit_der_mult_delta_t_sw = cache_Data[29].copy()
            self.D_diode_explicit_der_mult_delta_t_sw = cache_Data[30].copy()
            self.x_next_with_dep_A = cache_Data[31].copy()
            self.X_next_with_dep_B = cache_Data[32].copy()

    def initialize_data(self):
        
        
        s_size = len(self.network_matrix.s_labels)
        
        self.switch_state = [False] * s_size
        self.switch_triggered = [False] * s_size 

        
        for i in range(s_size):
            s_lab = self.network_matrix.s_labels[i]
            ele = self.network_matrix.m_column_labels_to_obj_map[s_lab]
            
            
            ind = i
            self.switch_label_index_map[ele.element_current_name] = ind
            self.switch_label_index_map[ele.element_voltage_name] = ind
            self.switch_index_label_map[ind] = (ele.element_voltage_name, ele.element_current_name)
            if isinstance(ele, Diode):

                self.switch_state[ind]  =ele.initial_switch_state
                self.switch_triggered[ind] =  False 
                self.diode_index.append(ind)
            else:
                assert isinstance(ele, ExternalSwitch)
                self.switch_state[ind] =  None
                self.switch_triggered[ind] = False
  
                self.external_switch_index.append(ind)
                
        self.swap_col_and_update([])

        
    def update(self, message:Message):
        
        if isinstance(message, SystemTimeMessage):
            self.cur_system_time = message.get_time()
        else:
            assert self.cur_system_time == message.system_time
            can_receive = self.cur_system_time == 0 or is_rise_edge(self.iteration_frequency, self.cur_system_time)
            if not can_receive:
                return
            # means can receive
            
            if isinstance(message, VoltageCurrentMessage):
                if message.source_column_label not in self.u_label_map.keys():
                    ind = len(self.u_label_map)
                    self.u_label_map[message.source_column_label]  = ind
                    self.u[0,ind] = message.value
                else:
                    ind = self.u_label_map[message.source_column_label]
                    self.u[0,ind] = message.value
                    

                    
            elif isinstance(message, OversamplingMessage):

                
                if message.system_time  == 0:
                    for key, value in message.switch_states_map.items():
                        
                        ind = self.switch_label_index_map[key]
                        self.switch_state[ind] = True if value else False
                        self.switch_triggered[ind] = False

                    # sanity check switch initial state in alignment with the state it received initially
                
                    for lab in self.network_matrix.s_labels:
                        ele = self.network_matrix.m_column_labels_to_obj_map[lab]
                        sw_ind = self.switch_label_index_map[lab]
                        
                        if self.switch_state[sw_ind] is False:
                            assert ele.element_voltage_name == lab
                        else:
                            assert self.switch_state[sw_ind] is True
                            assert ele.element_current_name == lab
                    
                    # self.build_truth_table_for_impulse_response()
                    if len(self.switch_state) > 0:
                        self.iterative_all_possible_switch_scenarion()
                        
                
                else:
                    for key, value in message.switch_states_map.items():
                        ind = self.switch_label_index_map[key]
                        if value != self.switch_state[ind]:
                            self.switch_triggered[ind] = True
                        else:
                            self.switch_triggered[ind] = False
                        self.switch_state[ind] = True if value else False
                        
       
            else:
                raise ValueError("Unexpected case occurred")
            
    def publish(self):
        can_process = self.cur_system_time == 0 or is_rise_edge(self.iteration_frequency, self.cur_system_time)
        if can_process:
            self.iteration()
            


    def plot_switch_graph(self):
        time_np_array = np.array(self.time_t)
        switch_state_np_array = np.array(self.switch_state_output)
        switch_triggered_np_array = np.array(self.switch_triggered_output)

        # Create subplots
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            subplot_titles=("Switch Triggered Signals", "Switch State Signals"))
        
        for i in range(self.network_matrix.s_labels_size):
            lab = self.network_matrix.s_labels[i]
            ele = self.network_matrix.m_column_labels_to_obj_map[lab]
            if isinstance(ele, ExternalSwitch):
                # Add triggered signals
                fig.add_trace(
                    go.Scatter(x=time_np_array, y=switch_triggered_np_array[:, i],
                            mode='lines', name=f"{ele.name} Triggered"),
                    row=1, col=1
                )
                
                # Add state signals
                fig.add_trace(
                    go.Scatter(x=time_np_array, y=switch_state_np_array[:, i],
                            mode='lines', name=f"{ele.name} State"),
                    row=2, col=1
                )
        
        # Update layout for better visualization
        fig.update_layout(
            title="Switch State and Triggered Signals",
            xaxis_title="Time",
            yaxis_title="State",
            # height=600,
            # width=900,
            template="plotly_white"
        )
        
        fig.show()


    def plot_output_graph(self, ax1_y_ticks=None, ax2_y_ticks=None, outputfile_name="output.csv"):
        time_np_array = np.array(self.time_t)
        y_output_np_array = np.array(self.y_output, dtype=np.float32).squeeze()

        y_output_column_names = ["time"]
        # Create subplots for current and voltage
        # Create subplots for current and voltage
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            subplot_titles=("Voltage", "Current"))

        # Add lines to the plot
        for i in range(self.network_matrix.y_label_size):
            lab = self.network_matrix.y_labels[i]
            ele = self.network_matrix.m_column_labels_to_obj_map[lab]

            if isinstance(ele, Voltmeter):
                y_data = y_output_np_array if len(y_output_np_array.shape) == 1 else y_output_np_array[:, i]
                fig.add_trace(
                    go.Scatter(x=time_np_array, y=y_data, 
                            mode='lines', name=f"Voltage: {ele.name}"),
                    row=1, col=1
                )
                y_output_column_names.append(f"Voltage: {ele.name}")
            else:
                y_data = y_output_np_array if len(y_output_np_array.shape) == 1 else y_output_np_array[:, i]
                fig.add_trace(
                    go.Scatter(x=time_np_array, y=y_data, 
                            mode='lines', name=f"Current: {ele.name}"),
                    row=2, col=1
                )
                y_output_column_names.append(f"Current: {ele.name}")
        # Update layout for grids and legends
        fig.update_layout(
            title="Output Graph",
    
            showlegend=True, 
        )

        # Set axis titles and tick intervals
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Voltage", row=1, col=1)
        fig.update_yaxes(title_text="Current", row=2, col=1)

        if ax1_y_ticks is not None:
            fig.update_yaxes(tickmode="linear", dtick=ax1_y_ticks, row=1, col=1)
        if ax2_y_ticks is not None:
            fig.update_yaxes(tickmode="linear", dtick=ax2_y_ticks, row=2, col=1)

        # Display the figure
        fig.show()  
        
        time_np_array = time_np_array.reshape(-1, 1)
        # for outputing
        combined_array = np.hstack((time_np_array, y_output_np_array))
        df = pd.DataFrame(combined_array, columns=y_output_column_names)
        df.to_csv(outputfile_name, index=False)

    def get_x_hat(self,):
        warnings.warn("old_function is deprecated", DeprecationWarning, stacklevel=2)
        return  np.matmul(self.A, self.get_x_cur_with_dep()) +np.matmul(self.B, self.u)
    def handle_external_switch(self, x_at_t0 ):
        
        switch_triggere_labels = []
        
        list_to_swap = []
        for i in range(len(self.switch_triggered)):
            if self.switch_triggered[i] :
                sw_volt_lab, sw_I_lab = self.switch_index_label_map[i]
                if self.switch_state[i]:
                    list_to_swap.append(sw_volt_lab)
                    assert self.network_matrix.s_labels[i] == sw_volt_lab  # because switch is on, get the I labe
                else:
                    list_to_swap.append(sw_I_lab)
                    assert self.network_matrix.s_labels[i] == sw_I_lab
                switch_triggere_labels.append(sw_volt_lab)  
        
        self.swap_col_and_update(list_to_swap, assert_no_cache=True)     
        # if len(list_to_swap) > 0:
        #     impulse_val = np.matmul( self.C_diode_impulse_sw, x_at_t0)

        # else:
        #     impulse_val = np.zeros(  ( len(self.diode_index), 1), dtype=np.float32)

        # return len(switch_triggere_labels) , impulse_val
        return len(switch_triggere_labels)
    def handle_diode_soft_switch(self, x_for_update):
        # non_impulse_val_tmp = np.matmul( non_impulse_C ,x_for_update, dtype=np.float32) +  np.matmul( non_impulse_D ,self.u, dtype=np.float32)
        # z_prime_tmp =  np.matmul(Z_hat_SW_A, x_for_update) + np.matmul(Z_hat_SW_B, self.u)
        # z_next_tmp = z_prime_tmp*(1/self.iteration_frequency) + non_impulse_val_tmp  # predice next step diode current/value
        
        
        
        non_impulse_val = np.matmul(self.C_diode_natural_sw, x_for_update, dtype=np.float32) + np.matmul(self.D_diode_natural_sw, self.u)
        z_next = np.matmul(self.C_diode_explicit_der_mult_delta_t_sw,x_for_update) + np.matmul(self.D_diode_explicit_der_mult_delta_t_sw, self.u)
        # np.testing.assert_almost_equal(non_impulse_val_tmp, non_impulse_val, decimal=5)
        # # np.testing.assert_almost_equal(z_prime, z_prime_tmp, decimal=5)
        # np.testing.assert_almost_equal(z_next, z_next_tmp, decimal=3)
        
        return non_impulse_val, z_next
    
    

    def update_both_impulse_non_impulse(self, impulse_val, non_impulse_val, z_next
                                        ):
        
        # the impulse_val, non_impulse_val, and z_next all in Dimension (diode_number x 1)

        swapped_flag = False
    
    

        
        labels_to_swap = []

        for diode_idx,  i in enumerate(self.diode_index):
            volt_lab, I_lab = self.switch_index_label_map[i]
            diode_state = self.switch_state[i]
            volt_nonimpulse = current_nonimpulse = non_impulse_val[diode_idx]
            volt_impulse = current_impulse = impulse_val[diode_idx]

            if volt_impulse > 0 or (  diode_state is False and volt_nonimpulse>0  and  z_next[diode_idx] > 0 ):
                self.switch_state[i] = True
                labels_to_swap.append(volt_lab)

            elif current_impulse <0 or ( diode_state is True and current_nonimpulse < 0   and z_next[diode_idx] < 0):
                self.switch_state[i] = False
                labels_to_swap.append(I_lab)
 
            else:
                pass
                

        
        if len(labels_to_swap) > 0:
            self.swap_col_and_update(labels_to_swap, assert_no_cache=True)
            swapped_flag = True

            
        return swapped_flag


    
    def update_y_cur(self, use_impulse, x_for_update, u_for_update, C_impulse, D_impulse, C_nonimpulse, D_nonimpulse):

        
        imp_c = np.matmul(C_impulse, x_for_update, dtype=np.float32) 
        imp_D = np.matmul(D_impulse, u_for_update, dtype=np.float32)
        non_imp = np.matmul(C_nonimpulse, x_for_update, dtype=np.float32) + np.matmul(D_nonimpulse, u_for_update, dtype=np.float32)
        
        imp = imp_c + imp_D

        if use_impulse:
            
            self.y_cur = non_imp + imp
        else:

            self.y_cur = non_imp 
            


    def get_x_cur_with_dep(self):

        return self.x_with_dep




    def iterative_x(self, x_for_iteration, zero_input, zero_state):
        x_before = x_for_iteration.copy()
        x_t = state_iteration(x_before, zero_input,zero_state, self.u)
        self.__x_cur_ind = x_t.copy()
        

    def update_x_cur_with_dep(self, A_dependent, B_dependent):
        self.x_with_dep =  np.matmul(A_dependent,  self.__x_cur_ind.copy(), dtype=np.float32)
    
        

    def iteration(self):
        x_cur_before = self.get_x_cur_with_dep().copy()
        u_cur_before = self.u.copy()
        # if update x at this stage, it work for parallel all other iteration except the x_state iteration
        if(self.cur_system_time == 0.0):
            self.swap_col_and_update([])

        switch_change_occur = self.handle_external_switch(x_at_t0=x_cur_before) # update matrixs when external switches being toggled

        # demonstrate parallel of nonimpulse and impulse switch evalulation
        diode_number = len(self.diode_index)
        state_number = x_cur_before.shape[0]
        input_number = self.u.shape[0]
        combined_matrix = np.zeros( (diode_number*3, state_number + input_number ), dtype=np.float32  )
        if(switch_change_occur > 0):
            combined_matrix[0:diode_number, 0:state_number] = self.C_diode_impulse_sw
        combined_matrix[ diode_number: diode_number*2, :] =  np.concat((self.C_diode_natural_sw, self.D_diode_natural_sw), axis=1)
        combined_matrix [diode_number*2:, :] = np.concat((self.C_diode_explicit_der_mult_delta_t_sw, self.D_diode_explicit_der_mult_delta_t_sw), axis=1)
            
        
        m_v_value = np.matmul(combined_matrix, np.concat((x_cur_before, self.u), axis=0))
        
        impulse_value =   m_v_value[0:diode_number]
        non_impulse_value = m_v_value[diode_number: diode_number*2]
        z_next = m_v_value[diode_number*2: ]
        
        # update diodes states accordingly
        diode_change_occur = self.update_both_impulse_non_impulse(impulse_val=impulse_value, non_impulse_val=non_impulse_value, z_next=z_next) # merge logic for finalize diode switching
        
        self.use_impulse_in_y_output = switch_change_occur or (not diode_change_occur)
        

        #update x
        self.x_with_dep = np.matmul(self.x_next_with_dep_A, x_cur_before) + np.matmul(self.X_next_with_dep_B, self.u)

        
        self.update_y_cur(
            use_impulse=self.use_impulse_in_y_output,
            x_for_update=x_cur_before,
            u_for_update=u_cur_before,
            C_impulse=self.C_impulse,
            D_impulse=self.D_impulse,
            C_nonimpulse=self.C_non_impulse,
            D_nonimpulse=self.D_non_impulse,
        )
        

        self.time_t.append(self.cur_system_time)
        # cur_switch_state =[]
        # cur_switch_trigger =[]
        
        # for i, val in self.switch_index_label_map.items():
        #     if i not in self.diode_index:
        #         cur_switch_state.append(self.switch_state[i])
        #         cur_switch_trigger.append(self.switch_triggered[i])
        # self.switch_state_output.append (  cur_switch_state)
        # self.switch_triggered_output.append( cur_switch_trigger)
        
        self.y_output.append(self.y_cur[:,0].tolist())
        

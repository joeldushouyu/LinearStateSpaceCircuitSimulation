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

        self.Q:npt.NDArray = None
        self.C: npt.NDArray =None
        self.C1:npt.NDArray = None
        self.D :npt.NDArray = None
        self.M0 :npt.NDArray = None
        self.A :npt.NDArray = None
        self.B :npt.NDArray = None
        self.M_pivots: Tuple=None
        self.integration_strategy:str=""
        
        
        
        self.C_impulse:npt.NDArray = None
        self.C_non_impulse:npt.NDArray= None
        self.D_impulse:npt.NDArray = None
        self.D_non_impulse:npt.NDArray = None
        self.A_dependent:npt.NDArray = None
        self.B_dependent:npt.NDArray =  None

        self.C_SW:npt.NDArray = None
        self.D_SW:npt.NDArray = None
        self.C_impulse_SW:npt.NDArray = None
        self.D_impulse_SW:npt.NDArray = None
        self.C_non_impulse_SW:npt.NDArray = None
        self.D_non_impulse_SW:npt.NDArray = None
        self.Z_hat_SW_A:npt.NDArray = None
        self.Z_hat_SW_B:npt.NDArray = None
        self.C1_SW:npt.NDArray = None

        
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
        
        self.boolean_symbol_to_element_name_map:dict[sp.Symbol:str] = {}
        
        
        self.solver_zero_input_res:npt.NDArray = None
        self.solver_zero_state_res:npt.NDArray = None
        self.fig_count = 1
        
        self.switch_last_output = np.zeros(self.network_matrix.s_labels_size)
        self.use_impulse_in_y_output = False
        self.initialize_data()
    

        self.diode1_map:dict[float, int] = {}
        self.diode2_map:dict[float, int]  = {}
        self.diode_1_change = 0
        self.diode_2_change = 0
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
        
    
    # def _retrieve_min_terms_of_each_states(self ):
        
    #     # truth table is input is divided into two part
    #     # [All current switch/diode states, next possible switch case]
    #     # the output is logic 1 if caused impulse to switch state, logic zero other wise
        
    #     # first, get all minterms (boolean input thage generate True output) 
        
    #     # minterms happen if the state is independent in one, but dependent in other. Likewise if is dependent in one but independent in other.
    #     min_terms_dict:dict[str:list[list[int]]] = {}
        
    #     switch_number = self.network_matrix.s_labels_size
        
    #     external_switch_number = len(self.network_matrix.external_switch_labels)
    #     for state_id in range( 2**self.network_matrix.s_labels_size):
            
        
    #         _, current_state = int_to_binary_list(state_id,switch_number)
            
    #         cur_state_cache_key = self.generate_M_cache_key(current_state,1)
    #         cur_state_ind_labels = self.M_cache[cur_state_cache_key][31].copy()
    #         cur_state_dep_labels = self.M_cache[cur_state_cache_key][32].copy()
    #         for external_switch_id in range(2** external_switch_number):
    #             _, next_state_external_switch = int_to_binary_list(external_switch_id, external_switch_number)
    #             next_state = current_state.copy()
                
    #             # update the external switch in next state
    #             for ind, ex_idx in enumerate(self.external_switch_index):
    #                 next_state[ex_idx] = next_state_external_switch[ind]

    #             next_state_cache_key = self.generate_M_cache_key(next_state,1)
    #             # now determine if it is a min_term 
    #             next_state_ind_labels = self.M_cache[next_state_cache_key][31].copy()
    #             next_state_dep_labels = self.M_cache[next_state_cache_key][32].copy()
                
    #             for state_lab in self.network_matrix.x_hat_labels:
    #                 if (state_lab in cur_state_ind_labels and state_lab in next_state_dep_labels) :
    #                     # means is a state label become dependent in the next iteration
                        
    #                     # this means it might create a spike in any diode that depends on this output
                        
    #                     if state_lab not in min_terms_dict:
    #                         min_terms_dict[state_lab] = [ current_state + next_state_external_switch   ]
    #                     else:
    #                         min_terms_dict[state_lab].append( current_state + next_state_external_switch   )
    #     # this should give minterms of list 
        
    #     return min_terms_dict
            
            
    # def build_truth_table_for_impulse_response(self):
    #     # truth table is input is divided into two part
    #     # [All current switch/diode states, next possible switch/diode state]
    #     # the output is logic 1 if caused impulse to switch state, logic zero other wise
    #     self.iterative_all_possible_switch_scenarion()
        
    #     # for prediction of impulse response, the state of diode is the same between two state, only the external switches changes state
    #     input_symbols_part_1 = []
    #     input_symbols_part_2 = []
        
    #     for idx, s_lab in enumerate(self.network_matrix.s_labels):
    #         ele = self.network_matrix.m_column_labels_to_obj_map[s_lab]
            
    #         element_name_sp = sp.symbols(ele.name)
    #         input_symbols_part_1.append(element_name_sp)
    #         self.boolean_symbol_to_element_name_map[element_name_sp] = ele.name
            
    #         if isinstance(ele, ExternalSwitch):
    #             assert idx in self.external_switch_index # sanity check
    #             ele_inp_sp = sp.symbols(f"{ ele.name}-input")
    #             input_symbols_part_2.append(ele_inp_sp)
    #             self.boolean_symbol_to_element_name_map[ele_inp_sp] = ele.name
                
    #     min_terms_dict = self._retrieve_min_terms_of_each_states()
        
    #     min_term_pos_dict = {}
        
        
    #     for x_hat_labels, min_term_list in min_terms_dict.items():
    #         min_term_pos_dict[x_hat_labels] = sp_logic.POSform(  input_symbols_part_1+input_symbols_part_2,
    #                                                            min_term_list
    #                                                            )
            
    #     p = 200
        
    def choose_intergation_strategy(self):
        # numerical oscillation (not system oscillation) will always occur for any real eigenvalue < 0
        
        # use trapezoidal  by default
        # use backward euler if real eigenvalue < -2 
        # temp = self.A.copy()
        # temp = temp* (1/self.iteration_frequency)

        
        # # Step 2: Check stability (eigenvalues within [-1, 1])
        # eigenvalues = np.linalg.eigvals(temp)
        # stability = all(abs(eig) <= 1 for eig in eigenvalues)

        # # Step 3: Check stiffness (large spread of eigenvalue magnitudes)
        # min_eig = min(eigenvalues)
        # max_eig = max(eigenvalues)
        # min_eig_mag = min(np.abs(eigenvalues))
        # max_eig_mag = max(np.abs(eigenvalues))
        # stiffness = True if min_eig_mag==0 else  (max_eig_mag / min_eig_mag) > 10

        # # Output results
        # if all(abs(eig) <= 1 for eig in eigenvalues):
        #     print("Stable")
        #     self.integration_strategy= "Trapezoidal"
        # else:
        #     print("Unstable")
        #     self.integration_strategy= "BackwardEuler"
        # self.integration_strategy= "Trapezoidal"
        # print("Eigenvalues:", eigenvalues)
        # print("Stiffness:", stiffness)
        pass
        
    def swap_col_and_update(self, label_to_Swap:list[str], assert_no_cache=False):
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


            
            
            diode_column_label = [] # if diode is on, give I_D, if diode is off, give V_D
            
            for diode_i in self.diode_index:
                
                if self.switch_state[diode_i]:
                    diode_column_label.append(self.switch_index_label_map[diode_i][1])
                else:
                    diode_column_label.append(self.switch_index_label_map[diode_i][0])
            
            
            self.C1_SW, self.C_SW, self.D_SW, self.C_impulse_SW, self.D_impulse_SW, self.C_non_impulse_SW, self.D_non_impulse_SW,  self.Z_hat_SW_A, self.Z_hat_SW_B = retrieve_Zsw_hat(  
                                A=self.A, B=self.B, C=self.C, D=self.D, C1=self.C1, 
                            C_impulse_matrix=self.C_impulse, C_nonimpulse_matrix=self.C_non_impulse,
                            D_impulse_matrix=self.D_impulse, D_nonimpulse_matrix=self.D_non_impulse,
                            x_hat_labels=self.network_matrix.x_hat_labels, u_labels=self.network_matrix.u_labels,
                            diode_column_labels=diode_column_label, y_labels=self.network_matrix.y_labels,
                            number_of_inductor=self.network_matrix.inductor_size, number_of_current_source=self.network_matrix.current_source_Size,
                            element_name_obj_map=self.network_matrix.element_name_obj_map,
                            m_column_labels_to_obj_map=self.network_matrix.m_column_labels_to_obj_map
                            )
         
            # discretized A,B,C,D
            
            self.A = sp.matrix2numpy(self.A.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.B = sp.matrix2numpy(self.B.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C = sp.matrix2numpy(self.C.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.D = sp.matrix2numpy(self.D.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C1 = sp.matrix2numpy(self.C1.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.solver_zero_input_res, self.solver_zero_state_res = get_pade_03_integeration(self.A, self.B, 1/self.iteration_frequency)
            self.solver_zero_input_res, self.solver_zero_state_res = get_pade_0_2_matrix(self.A, self.B, 1/self.iteration_frequency)
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
            
            self.C_SW = sp.matrix2numpy(self.C_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.D_SW = sp.matrix2numpy(self.D_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C_impulse_SW = sp.matrix2numpy(self.C_impulse_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.D_impulse_SW = sp.matrix2numpy(self.D_impulse_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C_non_impulse_SW = sp.matrix2numpy(self.C_non_impulse_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.D_non_impulse_SW= sp.matrix2numpy(self.D_non_impulse_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.Z_hat_SW_A = sp.matrix2numpy(self.Z_hat_SW_A.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.Z_hat_SW_B = sp.matrix2numpy(self.Z_hat_SW_B.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            self.C1_SW = sp.matrix2numpy(self.C1_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
            
            #TODO: also cache the ode solver matrix
            cache_Data = [
                            self.network_matrix.M[:,:], 
                            self.C1[:,:], self.C[:,:], self.D[:,:],
                            self.M0[:,:], self.A[:,:], self.B[:,:],
         
                            self.y_dep_labels.copy(),
                            self.A_dependent[:,:],
                            self.B_dependent[:,:],
            
                            self.forced_switch_mapping.copy(),
                            self.C_impulse.copy(),
                            self.C_non_impulse.copy(),
                            self.D_impulse.copy(),
                            self.D_non_impulse.copy(),
                            
                            self.C_SW.copy(),
                            self.D_SW.copy(),
                            self.C_impulse_SW.copy(),
                            self.D_impulse_SW.copy(),
                            self.C_non_impulse_SW.copy(),
                            self.D_non_impulse_SW.copy(),
                            self.Z_hat_SW_A.copy(),
                            self.Z_hat_SW_B.copy(),
                            self.C1_SW.copy(),
                            self.Q.copy(),
                            self.independent_state_labels.copy(),
                            self.dependent_state_labels.copy(),
                            self.solver_zero_input_res,
                            self.solver_zero_state_res
                            ]

            self.M_cache[key] = cache_Data
            
            
        else:
            cache_Data = self.M_cache[key]
            
            self.network_matrix.M = cache_Data[0][:,:]
            self.C1 = cache_Data[1][:,:]
            self.C = cache_Data[2][:,:]
            self.D = cache_Data[3][:,:]
            self.M0 = cache_Data[4][:,:] 
            self.A = cache_Data[5][:,:]   
            self.B = cache_Data[6][:,:]   

            self.y_dep_labels = cache_Data[7].copy()
            self.A_dependent = cache_Data[8][:,:]
            self.B_dependent = cache_Data[9][:,:]

            self.forced_switch_mapping = cache_Data[10].copy()
            self.C_impulse = cache_Data[11].copy()
            self.C_non_impulse = cache_Data[12].copy()
            self.D_impulse = cache_Data[13].copy()
            self.D_non_impulse = cache_Data[14].copy()

            
            self.C_SW=cache_Data[15].copy()
            self.D_SW=cache_Data[16].copy()
            self.C_impulse_SW=cache_Data[17].copy()
            self.D_impulse_SW=cache_Data[18].copy()
            self.C_non_impulse_SW=cache_Data[19].copy()
            self.D_non_impulse_SW=cache_Data[20].copy()
            self.Z_hat_SW_A=cache_Data[21].copy()
            self.Z_hat_SW_B=cache_Data[22].copy()
            self.C1_SW = cache_Data[23].copy()
            self.Q = cache_Data[24].copy()
            self.independent_state_labels = cache_Data[25].copy()
            self.dependent_state_labels = cache_Data[26].copy()
            self.solver_zero_input_res = cache_Data[27].copy()
            self.solver_zero_state_res = cache_Data[28].copy()
        
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

        
        self.choose_intergation_strategy()
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
                        
                        if self.switch_state[sw_ind] == False:
                            assert ele.element_voltage_name == lab
                        else:
                            assert self.switch_state[sw_ind] == True
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
        return  np.matmul(self.A, self.get_x_cur_with_dep()) +np.matmul(self.B, self.u)
    def handle_external_switch(self, x_cur_before_t0 ):
        
        switch_triggere_labels = []
        
        list_to_swap = []
        for i in range(len(self.switch_triggered)):
            if self.switch_triggered[i] :
                sw_volt_lab, sw_I_lab = self.switch_index_label_map[i]
                if self.switch_state[i]:
                    list_to_swap.append(sw_volt_lab)
                else:
                    list_to_swap.append(sw_I_lab)
                switch_triggere_labels.append(sw_volt_lab)  
        if len(list_to_swap) > 0:
            self.swap_col_and_update(list_to_swap, assert_no_cache=True)
            new_x_temp =np.matmul(self.A_dependent, x_cur_before_t0, dtype=np.float32) + np.matmul( self.B_dependent ,self.u, dtype=np.float32)
            # impulse response of internal diode
            
            impulse_difference = (new_x_temp- x_cur_before_t0)
            impulse_val = np.matmul(self.C1_SW, impulse_difference, dtype=np.float32) # use C1_sw, because the effect of E already applied on x_cur during the normal iteration update

        else:
            impulse_val = np.zeros(  (self.C1_SW.shape[0], 1), dtype=np.float32)
            impulse_difference = np.zeros(  (self.A.shape[0], 1), dtype=np.float32)
        return len(switch_triggere_labels) , impulse_val, impulse_difference

    def handle_diode_soft_switch(self,non_impulse_C, non_impulse_D, x_for_update, Z_hat_SW_A, Z_hat_SW_B):
        non_impulse_val = np.matmul( non_impulse_C ,x_for_update, dtype=np.float32) +  np.matmul( non_impulse_D ,self.u, dtype=np.float32)
        z_prime =  np.matmul(Z_hat_SW_A, x_for_update) + np.matmul(Z_hat_SW_B, self.u)
        z_next = z_prime*(1/self.iteration_frequency) + non_impulse_val
        return non_impulse_val, z_next
    
    

    def update_both_impulse_non_impulse(self, impulse_val, non_impulse_val, z_next
                                        ):
        
    

        swapped_flag = False
    
    
        diode_count = 0
        
        labels_to_swap = []
        # consistent = True
        # for indx, i in enumerate(self.diode_index):
        #     if  (z_next[indx] < 0 and non_impulse_val[indx] > 0) or  (z_next[indx] > 0 and non_impulse_val[indx] < 0):
        #         consistent = False
        # if not consistent:
        #     return True
        for i in self.diode_index:
            volt_lab, I_lab = self.switch_index_label_map[i]
            diode_state = self.switch_state[i]
            volt_nonimpulse = current_nonimpulse = non_impulse_val[diode_count]
            volt_impulse = current_impulse = impulse_val[diode_count]

            if volt_impulse > 0 or (  diode_state==False and volt_nonimpulse>0  and  z_next[diode_count] > 0 ):
                self.switch_state[i] = True
                labels_to_swap.append(volt_lab)
                self.diode_1_change += 1
                self.diode1_map[self.cur_system_time] = self.diode_1_change

            elif current_impulse <0 or ( diode_state == True and current_nonimpulse < 0   and z_next[diode_count] < 0):
                self.switch_state[i] = False
                labels_to_swap.append(I_lab)
                self.diode_2_change += 1
                self.diode2_map[self.cur_system_time] = self.diode_2_change
            else:
                pass
                
            diode_count +=1
        
        if len(labels_to_swap) > 0:
            self.swap_col_and_update(labels_to_swap, assert_no_cache=True)
            swapped_flag = True

            
        return swapped_flag


    
    def update_y_cur(self, use_impulse, x_for_update, u_for_update, C_impulse, D_impulse, C_nonimpulse, D_nonimpulse, dependent_state_labels):
        y_before = self.y_cur.copy()
        
        
        # # how about try to filter output from any states that became dependent?
        
        # # or even use the impulse for dependent?
        
        y_affect_by_dependent:set[int] = set()
        
        
        for lab in dependent_state_labels:
            x_hat_index = self.network_matrix.x_hat_labels.index(lab)
            
            x_for_update[x_hat_index] = 0
            for y_row_idx in range(self.network_matrix.y_label_size):
            
                if not np.isclose( self.C1[y_row_idx,x_hat_index], 0.0):
                    y_affect_by_dependent.add(y_row_idx)
            
        
        
        imp_c = np.matmul(C_impulse, x_for_update, dtype=np.float32) 
        imp_D = np.matmul(D_impulse, u_for_update)
        # impulse_v = np.matmul(self.C_impulse, impulse_difference)*self.iteration_frequency
        non_imp = np.matmul(C_nonimpulse, x_for_update, dtype=np.float32) + np.matmul(D_nonimpulse, u_for_update)
        
        imp = imp_c + imp_D
        # for i in y_affect_by_dependent:
        #     imp[i] = 0

        # self.y_cur = imp + non_imp

        if use_impulse:
            
            self.y_cur = non_imp + imp
        else:

            self.y_cur = non_imp 
            
            # self.y_cur = (1/2)*(non_imp+y_before)              
        # self.y_cur = np.matmul(self.C, x_for_update) + np.matmul(self.D, self.u)


    def get_x_cur_with_dep(self):

        return self.x_with_dep




    def iterative_x(self, x_for_iteration, zero_input, zero_state):
        x_before = x_for_iteration.copy()
        x_t = state_iteration(x_before, zero_input,zero_state, self.u)
        self.__x_cur_ind = x_t.copy()
        

    def update_x_cur_with_dep(self, A_dependent, B_dependent):
        self.x_with_dep =  np.matmul(A_dependent,  self.__x_cur_ind.copy(), dtype=np.float32) + np.matmul(B_dependent, self.u)
    
        

    def iteration(self):
        x_raw = self.__x_cur_ind.copy()
        x_cur_before = self.get_x_cur_with_dep().copy()

        # if update x at this stage, it work for parallel all other iteration except the x_state iteration
        
        hash_key = self.generate_M_cache_key(self.switch_state)
        non_impulse_C = self.M_cache[hash_key][15].copy() #buck example does not allow it to be, but can be prefetched
        non_impulse_D = self.M_cache[hash_key][16].copy()  
        Z_SW_A = self.M_cache[hash_key][21].copy()
        Z_SW_B = self.M_cache[hash_key][22].copy()
    

        # demonstrate parallel of nonimpulse and impulse switch evalulation
        non_impulse_value, z_next = self.handle_diode_soft_switch(non_impulse_C=non_impulse_C, 
                                                                  non_impulse_D=non_impulse_D,
                                                                  x_for_update=x_cur_before.copy(),
                                                                  Z_hat_SW_A=Z_SW_A,
                                                                  Z_hat_SW_B=Z_SW_B) # can process in parallel
        
        switch_change_occur, impulse_value, impulse_difference = self.handle_external_switch(x_cur_before_t0=x_cur_before.copy())

        diode_change_occur = self.update_both_impulse_non_impulse(impulse_val=impulse_value, non_impulse_val=non_impulse_value, z_next=z_next) # merge logic for finalize diode switching
        
        self.use_impulse_in_y_output = switch_change_occur or (not diode_change_occur)
        
        
        # dependency
        self.iterative_x(x_for_iteration=x_cur_before, zero_input=self.solver_zero_input_res, zero_state=self.solver_zero_state_res)
        self.update_x_cur_with_dep(A_dependent=self.A_dependent, B_dependent=self.B_dependent)
        
        self.update_y_cur(
            use_impulse=self.use_impulse_in_y_output,
            x_for_update=x_cur_before,
            u_for_update=self.u,
            C_impulse=self.C_impulse,
            D_impulse=self.D_impulse,
            C_nonimpulse=self.C_non_impulse,
            D_nonimpulse=self.D_non_impulse,
            dependent_state_labels=self.dependent_state_labels
        )
        

        self.time_t.append(self.cur_system_time)
        cur_switch_state =[]
        cur_switch_trigger =[]
        
        for i, val in self.switch_index_label_map.items():
            if i not in self.diode_index:
                cur_switch_state.append(self.switch_state[i])
                cur_switch_trigger.append(self.switch_triggered[i])
        self.switch_state_output.append (  cur_switch_state)
        self.switch_triggered_output.append( cur_switch_trigger)
        
        self.y_output.append(self.y_cur[:,0].tolist())
        
    def save_diode_debug_info_to_csv(self, filename: str):
        # Get all unique times from both dictionaries
        times = sorted(set(self.diode1_map.keys()).union(set(self.diode2_map.keys())))

        # Open the CSV file for writing
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header
            writer.writerow(['time', 'diode1_map_value', 'diode2_map_value'])
            
            # Write the data rows
            for time in times:
                diode1_value = self.diode1_map.get(time, None)  # Get value or None if key doesn't exist
                diode2_value = self.diode2_map.get(time, None)  # Get value or None if key doesn't exist
                writer.writerow([time, diode1_value, diode2_value])
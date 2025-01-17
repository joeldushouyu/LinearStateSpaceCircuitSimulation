from SimulationMessage import (
    Message,
    SystemTimeMessage,
    SwitchMessage,
    VoltageCurrentMessage,
    OversamplingMessage
)
import math
from Element import ExternalSwitch, Diode, VoltageCurrentSource, Element, Voltmeter, Ammeter
from FormNetworkMatrix import NetworkMatrix

from sympy import Matrix
import sympy as sp
from util import (is_rise_edge, retrieveSystemMatrix,
                  determine_dependent_state_vars, print_matrix_for_matlab_format,stiffSolver,
                  backwardEulerIntegration, trapezoidalIntegration, 
                  detemrminte_matrix_for_dependent_state_vars
                  )
from typing import Tuple
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
            if step == 12 or step==13:
                p = 20

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
    def __init__(self, switch: ExternalSwitch, switch_message: SwitchMessage):
        super().__init__()
        self.switch: ExternalSwitch = switch

        assert self.switch.duty_cycle <= 1.0
        self.cur_switch_status = switch.initial_switch_state
        self.switch_message = switch_message
        self.message_level_dependent = 1
        
    def pwm_at_time_t(self, time_t) -> bool:
        period = 1 / self.switch.switch_frequency  # Period of the PWM signal
        time_in_period =  math.fmod( time_t , period)  # Time within the current PWM period
        high_duration = (
            self.switch.duty_cycle * period
        )  # Duration of the "high" state in one period

        val =  time_in_period < high_duration
        if self.switch.pwm_value_at_each_new_cycle:
            return val
        else:
            return not val


    def update(self, message):
        # only accept systemtime message
        assert isinstance(message, SystemTimeMessage)
        self.cur_system_time = message.get_time()
        
    def publish(self):
        
        if self.cur_system_time == 0:
            self.cur_switch_status = self.switch.initial_switch_state
        else:
            self.cur_switch_status = self.pwm_at_time_t(self.cur_system_time)
        # print("switch origin publish")
        # print(self.cur_system_time, self.cur_switch_status)
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
        # self.switch_state_send:list[bool|None] = [None] * len(self.network_matrix.external_switch_labels)
        
        # need to have two list of switch state. Because it is not possible to have signal reflected
        # instantly at the rise edge 
        
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
                    # self.switch_state_send[index] = [message.is_switch_on()]
                else:
                    # normal stage
                    self.switch_states_receive[index] = message.is_switch_on()
                # print("oversample receive")
                # print( self.cur_system_time, self.switch_states_receive)
    def publish(self, ):
        
        can_publish = self.cur_system_time ==0 or is_rise_edge(self.sample_frequency, self.cur_system_time)
        

        if can_publish:
            self.oversample_message.notify_result(self.switch_state_dict, self.switch_states_receive.copy(), self.cur_system_time)
            # self.switch_state_send = self.switch_states_receive.copy()
        


class StateSpaceSimulationModule(SimulationModule):
    def __init__(self, network_matrix: NetworkMatrix, iteration_frequency: float):
        super().__init__()
        self.network_matrix = network_matrix

        self.iteration_frequency = iteration_frequency
        self.message_level_dependent = 3
        
        
        self.u_label_map = {u_lab: i for i, u_lab in enumerate(self.network_matrix.u_labels)}
        self.u_size = len(self.network_matrix.u_labels)
        self.u = np.ndarray( ( 1, self.u_size ), dtype=np.float64 )
        #       sp.Matrix(  1, self.u_size, [0 for k in range(self.u_size)] )


        
        # self.switch_lab_map:dict[str,int] = {} # switch-label map to [is_switch_on, is_switch_triggered]
        # self.switch_state:list[bool] = []
        # self.switch_triggered:list[bool] = []
        
        # # the diode state 
        # self.diode_lab_map: dict[str, int] = {}
        # self.diode_state:list[bool ] = []
        
        
        # element label resemble in the order of s_label in self.network_matrix
        self.switch_label_index_map:dict[str, int] = {}
        self.switch_index_label_map:dict[int, (str,str)] ={}
        self.switch_mask:npt.NDArray[np.bool_] =  None
        self.diode_index:list[int] = []
        self.external_switch_index:list[int] = []
        self.switch_state:npt.NDArray[np.bool_] = None
        self.switch_triggered:npt.NDArray[np.bool_] = None
        
        
        # the iteration process
        self.number_of_state_variable = len(self.network_matrix.x_labels)
        self.x_cur = np.ndarray((self.number_of_state_variable,1), dtype=np.float64, )
        self.x_cur[:,:] = 0
        
        #sp.Matrix( self.number_of_state_variable, 1,  [0 for k in range(self.number_of_state_variable)])  # assume initial value of zero in the beginning
        
        self.number_of_output = len(self.network_matrix.y_labels)
        self.y_cur = np.ndarray(  (self.number_of_output, 1), dtype=np.float64)
        #self.y_cur = sp.Matrix(self.number_of_output, 1, [0 for k in range(self.number_of_output)]) 
    
        self.C: Matrix =None
        self.C1:Matrix = None
        self.D :Matrix = None
        self.M0 :Matrix = None
        self.A :Matrix = None
        self.B :Matrix = None
        self.S_dxdt:Matrix = None
        self.Sx:Matrix = None
        self.Su:Matrix = None
        self.C_SW:Matrix = None
        self.D_SW:Matrix = None
        self.M_size = 0
        self.M_pivots: Tuple=None
        self.integration_strategy:str=""
        
        self._A_iteration:npt.NDArray = None
        self._B_iteration:npt.NDArray  =None
        self._C_iteration:npt.NDArray   = None
        self._D_iteration:npt.NDArray  = None
        self._S_dxdt:npt.NDArray  = None
        self._Sx:npt.NDArray  = None
        self._Su:npt.NDArray  = None
        self._C_SW:npt.NDArray =None
        self._D_SW:npt.NDArray =None
        self._A_dependent:npt.NDArray  = None
        self._B_dependent:npt.NDArray  = None
        
        
        # self.Add_inv:Matrix = None
        # self.Adi:Matrix = None
        # self.Bd:Matrix = None
        self.A_dependent:Matrix = None
        self.B_dependent:Matrix =  None
        self.A_x_independent_filter:Matrix = None
        self.network_inconsistent_labels:list[str] = []
        self.independent_state_var_labels:list[str] = []
        self.dependent_state_var_labels:list[str] = []
        # self.network_pivots_cols:list[int] = []
        # self.independent_row_col_map:dict[str, list[int]] = {}
        # self.dependent_row_col_map:dict[str, list[int]] = {}
        
        self.forced_switch_mapping:dict[Element, list[Element]] = {}
        
        self.M_cache :dict[str, Matrix] = {}
        
        
        # ouput and debug record
        
        self.time_t:list[float] = []
        self.y_output:list[list[float]] = []
        self.x_output:list[list[float]] = []
        
        self.switch_state_output:list[list[int]] = []
        self.switch_triggered_output:list[list[int]] = []
        self.u_output:list[list[float]] = []
        
        
        self.fig_count = 1
        self.initialize_data()
    
    
    def update_dependent_in_xcur(self):
        
        
        part_1  =  np.matmul(self.A_x_independent_filter, self.x_cur)
        res =   part_1    +   np.matmul( self._A_dependent, self.x_cur) +  np.matmul( self._B_dependent ,  self.u)
        
        # add back with original self.x_cir
        res += self.x_cur
        #TODO: remove later
        
        for lab in self.dependent_state_var_labels:
            ind = self.network_matrix.x_hat_labels.index(lab)
            assert part_1[ind,0] == -self.x_cur[ind, 0]
        for lab in self.independent_state_var_labels:
            ind = self.network_matrix.x_hat_labels.index(lab)
            assert res[ind,0] == self.x_cur[ind,0]
            
        return res
        
    def force_triggered_events(self )->dict[ExternalSwitch, list[Diode]]:
        # see if network inconsistent could cause by switch events
        inconsistent_row_len = len(self.network_inconsistent_labels)
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
    
    # def determine_dependency_state(self):
    #     # independent_state_vars_labels = []
    #     # dependent_state_vars_labels = []
        
    #     # independent_state_vars_cols = []
    #     independent_state_vars_rows = []
    #     # dependent_state_vars_cols = []
    #     dependent_state_vars_rows = []


        
    #     # mapping
    #     independent_row_col_map:dict[str, list[int]] = {}
    #     dependent_row_col_map:dict[str, list[int]] = {}
    
    #     # recall rref form
    #     # 1. if pivot row means the first nonzero value in the row
    #     # for any non pivot column, the rows start with the max(pivot_row) +1

    #     cols = self.M0.cols
    #     self.M0, pivots = self.M0.rref()
    #     # pivot_rows = [next(row for row in range(self.M0.shape[0]) if self.M0[row, col] != 0) for col in pivots]
        
    #     dependent_row_start = 0
    #     for i in range(len(pivots)):
    #         col = pivots[i]
    #         ind_label =  self.network_matrix.x_hat_labels[col] 
       
            
    #         independent_row_col_map[ind_label] = [i , col   ]  # by def, ith pivor correspond to ith row
    #         independent_state_vars_rows.append(i)
            
    #     dependent_row_start = max(independent_state_vars_rows) +1
    #     assert dependent_row_start == len(pivots) 
        
    #     for col in range(self.M0.cols):
    #         if col not in pivots:
                
    #             dep_label = self.network_matrix.x_hat_labels[col]
                
    #             # find a zero row, from dependent_row_start
                
    #             for r in range(dependent_row_start, self.M0.rows):
    #                 if self.M0[r, col] == 0 and r not in dependent_state_vars_rows:
    #                     dependent_state_vars_rows.append(r)
                        
    #                     dependent_row_col_map[dep_label] = [r, col]
    #                     break
            
    #     # j = 0
    #     # for col in range(cols):
    #     #     is_independent = j  < len(pivots)  and pivots[j] == col
    #     #     if is_independent:
    #     #         independent_state_vars_labels.append( self.network_matrix.x_hat_labels[col] )  
    #     #         independent_state_vars_cols.append(col)
    #     #         first_non_zero_row = next((row for row in range(self.M0.shape[0]) if self.M0[row, col] != 0), None)
    #     #         # find max of this row
    #     #         independent_state_vars_rows.append(first_non_zero_row)
    #     #         j += 1
    #     #     else:
    #     #         dependent_state_vars_labels.append(self.network_matrix.x_hat_labels[col])
    #     #         dependent_state_vars_cols.append(col) 
                
    #     #         # find a row that is all zero in M0
                
        
        
    #     zero_rows = []
        
    #     for i in range(self.M0.rows):
    #         if self.M0[i,:].is_zero_matrix:
    #             zero_rows.append(i)
    #     zero_count = len(zero_rows)
    #     # independent_count= len(independent_state_vars_labels)
    #     # dependent_count = len(dependent_state_vars_labels)
        
    #     A_dependent =  Matrix(self.A.rows, self.A.cols, [0]*(self.A.rows *self.A.cols ))   
    #     B_dependent = Matrix(self.B.rows, self.B.cols, [0]*(self.B.rows *self.B.cols ) )     
        
    #     if zero_count == 0:
    #         return independent_row_col_map, dependent_row_col_map, A_dependent, B_dependent
        
    #     x_hat_labels_orders = self.network_matrix.x_hat_labels
    #     # update M0, A, B
    #     A_temp = self.A[:,:]
    #     B_temp = self.B[:,:]
    #     M0_temp = self.M0[:,:]
    #     zero_row_A = Matrix(1, self.A.cols, [0]*self.A.cols)
    #     zero_row_B = Matrix(1, self.B.cols, [0]*self.B.cols)
    #     zero_row_M0 = Matrix(1, self.M0.cols, [0]*self.M0.cols)
        
    #     #TODO: is M0 always correctly reflected in transformer model?
    #     for row_ind in range( M0_temp.rows ):
    #         label = x_hat_labels_orders[row_ind]
    #         if label in independent_row_col_map:
            
    #             original_row = independent_row_col_map[label][0]
    #             assert row_ind == independent_row_col_map[label][1]
    #             self.M0[row_ind,:] = M0_temp[ original_row   ,:]
    #             self.A[row_ind, :] = A_temp[original_row, :]
    #             self.B[row_ind, :] = B_temp[original_row, :]

                
                
    #             #update back
    #             independent_row_col_map[label] = [row_ind, row_ind]
    #         else:
    #             # means is an dependent variable
    #             # use 8-58 of chua
                
    #             original_row = dependent_row_col_map[label][0]
    #             original_col = dependent_row_col_map[label][1]
    #             assert row_ind == original_col
    #             self.M0[row_ind, :] = zero_row_M0[:,:]
    #             self.A[row_ind, :] = zero_row_A[:,:]  
    #             self.B[row_ind, :] = zero_row_B[:,:]

                
    #             # j = row_ind
    #             # k = row_ind
                
    #             a_j_k = A_temp[original_row, original_col]
    #             A_temp[original_row, original_col] = 0
    #             A_dependent[row_ind, :] = A_temp[original_row, :]
    
    #             B_dependent[row_ind, :] = B_temp[original_row, :]
                
    #             A_dependent[row_ind, :] *= -1/a_j_k
    #             B_dependent[row_ind, :] *= -1/a_j_k
                
                
    #             # update back
    #             dependent_row_col_map[label] = [row_ind, row_ind]
    #     return independent_row_col_map, dependent_row_col_map, A_dependent, B_dependent     
                
            
               
    
    def choose_intergation_strategy(self):
        # numerical oscillation (not system oscillation) will always occur for any real eigenvalue < 0
        
        # use trapezoidal  by default
        # use backward euler if real eigenvalue < -2 
        temp = self.A.subs(self.network_matrix.symbolic_to_value_map)
        eigen_value_dict = temp.eigenvals()
        
        
        min_eig = min(  [  sp.re(x.subs(self.network_matrix.symbolic_to_value_map))  * (1/self.iteration_frequency) for x  in eigen_value_dict.keys()])
        max_eig =  max(  [  sp.re(x.subs(self.network_matrix.symbolic_to_value_map))  * (1/self.iteration_frequency) for x  in eigen_value_dict.keys()])
        
        max_abs = max([  abs(sp.re(x.subs(self.network_matrix.symbolic_to_value_map))  * (1/self.iteration_frequency)) for x  in eigen_value_dict.keys()])
        min_abs = min([  abs(sp.re(x.subs(self.network_matrix.symbolic_to_value_map))  * (1/self.iteration_frequency)) for x  in eigen_value_dict.keys()])
        
        # if max_abs/min_abs > 1000:
        #     # means stiff system encounter
        #     # ration equation: https://en.wikipedia.org/wiki/Stiff_equation
        #     # stiffness ratio is negotiable to change
        #     self.integration_strategy = "stiff"
        if min_eig <= -2:
            self.integration_strategy = "BackwardEuler"
        else:
            self.integration_strategy = "Trapezoidal"
            
        print(f"***********using {self.integration_strategy} *****************")
        
        
    def swap_col_and_update(self, label_to_Swap:str):
        if label_to_Swap != "":
            self.network_matrix.update_M_matrix(label_to_Swap, False)
        # do a cache
        

        
        key  = "".join(self.network_matrix.m_column_labels)
        if key not in self.M_cache.keys():
            
            self.network_matrix.rref_update()
            self.S_dxdt, self.Sx, self.Su, self.C1, self.C, self.D, self.M0, self.A, self.B, self.C_SW, self.D_SW, self.network_inconsistent_labels = retrieveSystemMatrix(
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
            
            # at here, determine any force-triggered events, dependent variables, and so forth before turn into numpy array
            M0_new, A_new, B_new, A_x_ind_filter, A_dep, B_dep, ind_lab, dep_lab = detemrminte_matrix_for_dependent_state_vars(self.M0, self.A, self.B, self.network_matrix.x_hat_labels)
            self.M0 = M0_new.copy()
            self.B = B_new.copy()
            self.A = A_new.copy()
            self.A_x_independent_filter = A_x_ind_filter.copy()
            self.A_dependent = A_dep.copy()
            self.B_dependent = B_dep.copy()
            self.independent_state_var_labels = ind_lab.copy()
            self.dependent_state_var_labels = dep_lab.copy()
            
            
            self._A_iteration = sp.matrix2numpy(self.A.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._B_iteration = sp.matrix2numpy(self.B.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._C_iteration = sp.matrix2numpy(self.C.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._D_iteration = sp.matrix2numpy(self.D.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._S_dxdt = sp.matrix2numpy(self.S_dxdt.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._Sx = sp.matrix2numpy(self.Sx.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._Su = sp.matrix2numpy(self.Su.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._C_SW = sp.matrix2numpy(self.C_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._D_SW = sp.matrix2numpy(self.D_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._A_dependent = sp.matrix2numpy(self.A_dependent.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._B_dependent = sp.matrix2numpy(self.B_dependent.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            
            cache_Data = [
                            self.network_matrix.M[:,:], self.S_dxdt[:,:], self.Sx[:,:],
                            self.Su[:,:], self.C1[:,:], self.C[:,:], self.D[:,:],
                            self.M0[:,:], self.A[:,:], self.B[:,:],
                            self.C_SW[:,:], self.D_SW[:,:],
                            self._A_iteration[:,:],
                            self._B_iteration[:,:],
                            self._C_iteration[:,:],
                            self._D_iteration[:,:],
                            self._S_dxdt[:,:],
                            self._Sx[:,:],
                            self._Su[:,:],
                            self._C_SW[:,:],
                            self._D_SW[:,:],
                            self.network_inconsistent_labels.copy(),
                            self.A_dependent[:,:],
                            self.B_dependent[:,:],
                            self._A_dependent[:,:],
                            self._B_dependent[:,:],
                            self.A_x_independent_filter[:,:],
                            self.forced_switch_mapping.copy(),
                            self.independent_state_var_labels.copy(),
                            self.dependent_state_var_labels.copy()
                            ]

            self.M_cache[key] = cache_Data
            
            
        else:
            cache_Data = self.M_cache[key]
            
            self.network_matrix.M = cache_Data[0][:,:]
            self.S_dxdt = cache_Data[1][:,:]
            self.Sx = cache_Data[2][:,:]
            self.Su = cache_Data[3][:,:]
            self.C1 = cache_Data[4][:,:]
            self.C = cache_Data[5][:,:]
            self.D = cache_Data[6][:,:]
            self.M0 = cache_Data[7][:,:]  # Was missing
            self.A = cache_Data[8][:,:]    # Was missing
            self.B = cache_Data[9][:,:]    # Was missing
            self.C_SW = cache_Data[10][:,:]
            self.D_SW = cache_Data[11][:,:]
            self._A_iteration = cache_Data[12][:,:]
            self._B_iteration = cache_Data[13][:,:]
            self._C_iteration = cache_Data[14][:,:]
            self._D_iteration = cache_Data[15][:,:]
            self._S_dxdt = cache_Data[16][:,:]
            self._Sx = cache_Data[17][:,:]
            self._Su = cache_Data[18][:,:]
            self._C_SW = cache_Data[19][:,:]
            self._D_SW = cache_Data[20][:,:]
            self.network_inconsistent_labels = cache_Data[21].copy()
            self.A_dependent = cache_Data[22][:,:]
            self.B_dependent = cache_Data[23][:,:]
            self._A_dependent = cache_Data[24][:,:]
            self._B_dependent = cache_Data[25][:,:]
            self.A_x_independent_filter = cache_Data[26][:,:]
            self.forced_switch_mapping = cache_Data[27].copy()
            self.independent_state_var_labels = cache_Data[28].copy()
            self.dependent_state_var_labels = cache_Data[29].copy()

            

        
        
        
        
    def initialize_data(self):
        
        # the diode state
        
        s_size = len(self.network_matrix.s_labels)
        
        self.switch_state = np.ndarray((s_size, 1), dtype=np.bool_ )
        self.switch_triggered = np.ndarray( (s_size,1), dtype=np.bool_)
        self.switch_mask = np.ndarray(  (s_size, 1), dtype=np.bool_)
        
        
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
                self.switch_mask[ind] = False
                self.diode_index.append(ind)
            else:
                self.switch_state[ind] =  None
                self.switch_triggered[ind] = False
                self.switch_mask[ind] = True
                self.external_switch_index.append(ind)
                
        self.swap_col_and_update("")
        self.M_size = self.M0.rank()
        
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
                        self.switch_state[ind] = 1 if value else 0
                        self.switch_triggered[ind] = 0
                       
                else:
                    for key, value in message.switch_states_map.items():
                        ind = self.switch_label_index_map[key]
                        if value != self.switch_state[ind]:
                            self.switch_triggered[ind] = 1
                        else:
                            self.switch_triggered[ind] = 0
                        self.switch_state[ind] = 1 if value else 0
                        
       
            else:
                raise ValueError("Unexpected case occurred")
            
    def publish(self):
        can_process = self.cur_system_time == 0 or is_rise_edge(self.iteration_frequency, self.cur_system_time)
        if can_process:
            self.iteration()
            

    
    # def update_state_with_dependent_variables(self):

    #     x_ind = Matrix(  len(self.independent_state_cols), 1, [0]*len(self.independent_state_cols) )
       
    #     x_state_imp = self.x_cur.copy()
        
    #     for i in range(len (self.independent_state_cols) ):
    #         col = self.independent_state_cols[i]
    #         x_ind[i] = x_state_imp[col]
            
        
    #     x_dep = -self.Add_inv*(self.Adi*x_ind+self.Bd*self.u)
    #     x_dep.subs(self.network_matrix.symbolic_to_value_map)
         
    #     for i in range(len(self.dependent_state_cols )):
    #         col = self.dependent_state_cols[i]
    #         x_state_imp[col] = x_dep[i]
    #     return x_state_imp

    def calc_impulse_response(self,  switch_triggere_labels:list[str]):
        
        # forced_triggered_diodes, self.Add_inv, self.Adi, self.Bd, self.independent_state_labels, self.independent_state_cols, self.dependent_state_labels, self.dependent_state_cols = determine_dependent_state_vars(self.M0, self.A, self.B,self.network_matrix,sw_volt_lab)
        
        
        # if len(forced_triggered_diodes) > 0:
        #     for lab in forced_triggered_diodes:
        #         ind = self.switch_label_index_map[lab]
        #         self.switch_state[ind] = ~self.switch_state[ind]
        #         self.swap_col_and_update(lab)
        #     return
        
        # x_ind = Matrix(  len(ind_state_cols), 1, [0]*len(ind_state_cols) )
       
        # x_state_imp = self.x_cur.copy()
        
        # for i in range(len (ind_state_cols) ):
        #     col = ind_state_cols[i]
        #     x_ind[i] = x_state_imp[col]
            
        
        # x_dep = -Add_inv*(Adi*x_ind+Bd*self.u)
        # x_dep.subs(self.network_matrix.symbolic_to_value_map)
         
        # for i in range(len(dep_state_cols )):
        #     col = dep_state_cols[i]
        #     x_state_imp[col] = x_dep[i]

        # x_state_imp = self.update_state_with_dependent_variables()
        
        
       
        if len(self.forced_switch_mapping) > 0 and len(switch_triggere_labels) > 0:
            for label in switch_triggere_labels:
                switch_ele = self.network_matrix.m_column_labels_to_obj_map[label]
                list_of_diodes = self.forced_switch_mapping[switch_ele]
                
                for diode in list_of_diodes:
                    diode_index = self.switch_label_index_map[diode.element_current_name]
                    self.switch_state[diode_index] = not self.switch_state[diode_index]
                    self.swap_col_and_update(diode.element_voltage_name)
        else:
        
            x_state_imp =   self.update_dependent_in_xcur()
            #impulse = self.S_dxdt*(x_state_imp - self.x_cur)
            # impulse = self._S_dxdt*(x_state_imp - self.x_cur)
            # check to see any diode's has a impulse
            difference = x_state_imp- self.x_cur
            difference = difference.astype(np.float32)
            impulse = np.matmul( self._S_dxdt, difference, dtype=np.float32   ) 
            for i in self.diode_index:
                volt_lab, I_lab = self.switch_index_label_map[i]
                #imp = impulse[i,0].subs(self.network_matrix.symbolic_to_value_map)
                imp = impulse[i,0]
                if imp > 0: 
                    # assert  self.switch_state[i] == False
                    self.switch_state[i] = True
                    self.swap_col_and_update(volt_lab)
                elif imp < 0:
                    # assert self.switch_state[i] == True
                    self.switch_state[i] = False
                    self.swap_col_and_update(volt_lab)
                else:
                    pass
                    
        
        
    def calc_nonimpulse_response(self):
        
        diode_switched = False
        non_impulse   =  np.matmul( self._Sx, self.x_cur )   +  np.matmul(self._Su, self.u)  
        # z_derivative = np.matmul( self._C_SW, self.x_cur )   +  np.matmul(self._D_SW, self.u) 
        # z_hat = non_impulse + 1/self.iteration_frequency * z_derivative 
        
        # is_consistent = False
        # for i in self.diode_index:
        #     if non_impulse[i,0] < 0 and z_hat[i,0] > 0:
        #         is_consistent = False
        #     elif non_impulse[i,0] > 0 and z_hat[i,0] > 0:
        #         is_consistent = False
        #     else:
        #         is_consistent = True
        
        #non_impulse.subs(self.network_matrix.symbolic_to_value_map)
        for i in self.diode_index:
            non_imp = non_impulse[i,0]
            volt_lab, I_lab = self.switch_index_label_map[i]
            diode_state = self.switch_state[i]
            
            # if not is_consistent:
            #     return
            # if debug_swap1 or debug_swap2 or debug_swap3 or debug_swap4:
            #     self.switch_state[0] = not self.switch_state[1]
            #     self.switch_state[1] = not self.switch_state[1]
            #     self.swap_col_and_update("V_D1")
            #     self.swap_col_and_update("V_D2")
            if diode_state == False and non_imp>0 :
                self.switch_state[i] = True
                self.swap_col_and_update(volt_lab)
                
                diode_switched = True
            elif diode_state == True and non_imp < 0 :
                self.switch_state[i] = False
                self.swap_col_and_update(volt_lab)
                
                diode_switched = True
            else:
                pass
        
        return diode_switched
            
    def plot_switch_graph(self):
        time_np_array = np.array(self.time_t)
        switch_state_np_array = np.array(self.switch_state_output)
        switch_triggered_np_array = np.array(self.switch_triggered_output)
        fig, _ = plt.subplots(self.fig_count)
        self.fig_count+=1

        # Create subplots for triggered signals and state signals
        ax1 = fig.add_subplot(211)  # Signal indicating switch triggered
        ax2 = fig.add_subplot(212)  # Signal of each switch state

        # Line maps for triggered and state signals
        line_map_triggered = {}
        line_map_state = {}

        for i in range(self.network_matrix.s_labels_size):  # Assuming `s_labels_size` is correct
            lab = self.network_matrix.s_labels[i]
            ele = self.network_matrix.m_column_labels_to_obj_map[lab]
            if isinstance(ele, ExternalSwitch):
                # Plot triggered signals
                line_triggered, = ax1.plot(
                    time_np_array, switch_triggered_np_array[:, i],
                    label=f"{ele.name} Triggered"
                )
                line_map_triggered[line_triggered] = (time_np_array, switch_triggered_np_array[:, i])

                # Plot state signals
                line_state, = ax2.plot(
                    time_np_array, switch_state_np_array[:, i],
                    label=f"{ele.name} State"
                )
                line_map_state[line_state] = (time_np_array, switch_state_np_array[:, i])

        # Add grids and legends
        ax1.grid()
        ax2.grid()
        ax1.legend()
        ax2.legend()

        # Connect pick events to handle clicks on lines
        fig.canvas.mpl_connect('pick_event', lambda event: on_pick(event, [line_map_triggered, line_map_state], fig))

        # Enable picking on all lines
        for line in line_map_triggered:
            line.set_picker(True)
        for line in line_map_state:
            line.set_picker(True)

        # Add interactive checkboxes for triggered signals
        labels_triggered = [line.get_label() for line in line_map_triggered.keys()]
        visibility_triggered = [line.get_visible() for line in line_map_triggered.keys()]
        check_ax_triggered = fig.add_axes([0.9, 0.6, 0.15, 0.3])  # Position for checkboxes
        check_triggered = CheckButtons(check_ax_triggered, labels_triggered, visibility_triggered)

        check_triggered.on_clicked(lambda label: toggle_visibility(label, [line_map_triggered], fig))

        # Add interactive checkboxes for state signals
        labels_state = [line.get_label() for line in line_map_state.keys()]
        visibility_state = [line.get_visible() for line in line_map_state.keys()]
        check_ax_state = fig.add_axes([0.9, 0.2, 0.15, 0.3])  # Position for checkboxes
        check_state = CheckButtons(check_ax_state, labels_state, visibility_state)

        check_state.on_clicked(lambda label: toggle_visibility(label, [line_map_state], fig))

        plt.show()
        # return fig

    def plot_output_graph(self, ax1_y_ticks=None, ax2_y_ticks=None):
        time_np_array = np.array(self.time_t)
        y_output_np_array = np.array(self.y_output, dtype=np.float64).squeeze()

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
            else:
                y_data = y_output_np_array if len(y_output_np_array.shape) == 1 else y_output_np_array[:, i]
                fig.add_trace(
                    go.Scatter(x=time_np_array, y=y_data, 
                            mode='lines', name=f"Current: {ele.name}"),
                    row=2, col=1
                )

        # Update layout for grids and legends
        fig.update_layout(
            title="Output Graph",
    
            showlegend=True,  # Enables the legend for toggling lines
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
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
            
    # def plot_output_graph(self, ax1_y_ticks=None, ax2_y_ticks=None):
    #     time_np_array = np.array(self.time_t)
    #     y_output_np_array = np.array(self.y_output).squeeze()
    #     fig, _ = plt.subplots(self.fig_count)
    #     self.fig_count+=1


    #     # Create subplots for current and voltage
    #     ax1 = fig.add_subplot(211)
    #     ax2 = fig.add_subplot(212)

    #     # Line map for all signals
    #     line_map = {}

    #     for i in range(self.network_matrix.y_label_size):
    #         lab = self.network_matrix.y_labels[i]
    #         ele = self.network_matrix.m_column_labels_to_obj_map[lab]
    #         if isinstance(ele, Voltmeter):
    #             if len(y_output_np_array.shape) == 1:
    #                 line, = ax1.plot(time_np_array, y_output_np_array, label=f"{ele.name}")
    #             else:
    #                 line, = ax1.plot(time_np_array, y_output_np_array[:, i], label=f"{ele.name}")
    #         else:
    #             line, = ax2.plot(time_np_array, y_output_np_array[:, i], label=f"{ele.name}")
    #         if len(y_output_np_array.shape) == 1:
    #             line_map[line] = (time_np_array, y_output_np_array)
    #         else:
    #             line_map[line] = (time_np_array, y_output_np_array[:, i])

    #     # Add grids and legends
    #     ax1.grid()
    #     ax2.grid()
    #     ax1.legend()
    #     ax2.legend()

    #     # Set custom y-axis ticks if provided
    #     if ax1_y_ticks is not None:
    #         ax1.yaxis.set_major_locator(plt.MultipleLocator(ax1_y_ticks))
    #     if ax2_y_ticks is not None:
    #         ax2.yaxis.set_major_locator(plt.MultipleLocator(ax2_y_ticks))

    #     # Connect pick events to handle clicks on lines
    #     fig.canvas.mpl_connect('pick_event', lambda event: on_pick(event, [line_map], fig))

    #     # Enable picking on all lines
    #     for line in line_map:
    #         line.set_picker(True)

    #     # Add interactive checkboxes
    #     labels = [line.get_label() for line in line_map.keys()]
    #     visibility = [line.get_visible() for line in line_map.keys()]
    #     check_ax = fig.add_axes([0.9, 0.4, 0.15, 0.4])  # Position for checkboxes
    #     check = CheckButtons(check_ax, labels, visibility)

    #     check.on_clicked(lambda label: toggle_visibility(label, [line_map], fig))

    #     plt.show()
        # return fig

    
    def update_y_cur(self, x):
        #TODO: correcT?
        
        # x_temp =self.update_dependent_in_xcur()
        self.y_cur = np.matmul( self._C_iteration ,x) +  np.matmul( self._D_iteration ,self.u)

        
    def update_x_cur(self):
        
        copy = self.x_cur.copy()
        #self.x_cur = radauIntegration( self.x_cur, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency )
        # if self.integration_strategy ==  "p_0_q_2":
        #     self.x_cur = p_0_q_2_integration( self.x_cur, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency ).copy()
        # el
        # if self.integration_strategy == "stiff":
        #     self.x_cur = stiffSolver( self.x_cur, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency ).copy()
        if self.integration_strategy == "Trapezoidal":
            self.x_cur = trapezoidalIntegration( self.x_cur, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency ).copy()
        else:
            self.x_cur = backwardEulerIntegration(self.x_cur, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency).copy()

        #TODO: update with dependent?
        # self.x_cur = self.update_dependent_in_xcur()
        # if self.M0.rank() < self.network_matrix.x_hat_label_size :
        #     #forced_triggered_diodes, self.Add_inv, self.Adi, self.Bd, self.independent_state_labels, self.independent_state_cols, self.dependent_state_labels, self.dependent_state_cols = determine_dependent_state_vars(self.M0, self.A, self.B,self.network_matrix,"")
        
        #     res = self.update_state_with_dependent_variables()
        #     self.x_cur = res.copy()
        if np.isnan(self.x_cur).any() or np.isinf(self.x_cur).any():
            p = 200
        p = 200
    def iteration(self):
        # the iteration process

        x_for_update =self.x_cur.copy()
        
        if self.cur_system_time == 0:
            # turn all diode to off state
            for lab, index  in self.switch_label_index_map.items():
                # ele = self.network_matrix.net[lab]
                if  index in  self.diode_index and  self.switch_state[index] == True:
                    
                    self.switch_state[index] = False
                    self.swap_col_and_update(lab)

        # if self.cur_system_time == 0:
            

        # #     p = 200
        # #     # all false
        #     self.swap_col_and_update("V_D2")
        #     self.switch_state[1] = False
        #     self.swap_col_and_update("V_D1")
        #     self.switch_state[0] = False
        #     p = 200
        #     #  False  True 
        #     self.swap_col_and_update("V_D2")
        #     self.switch_state[1] = True
        #     p= 00  
        #     # true, true 
        #     self.swap_col_and_update("V_D1")
        #     self.switch_state[0] = True
        #     p = 200
        #     # true false
        #     self.swap_col_and_update("V_D2")
        #     self.switch_state[1] = False
            
        #     p = 200
        cur_switch_state = self.switch_state[self.switch_mask]
        cur_diode_state = self.switch_state[~self.switch_mask]
        cur_switch_trigger = self.switch_triggered[self.switch_mask]
        # # record u and switch labe
        # # self.update_x_cur()

        trig = False
        # # for now, assume only one switch change in one time period
        switch_triggere_labels = []
        for i in range(len(self.switch_triggered)):
            if self.switch_triggered[i] :
                # assert trig  == False
                # print(self.cur_system_time)
                # means this switch istriggered
                sw_volt_lab, sw_I_lab = self.switch_index_label_map[i]
                self.swap_col_and_update(sw_volt_lab)
                switch_triggere_labels.append(sw_volt_lab)
                trig = True
     
        if self.M0.rank() < self.M_size or len(self.forced_switch_mapping) > 0 :
            self.calc_impulse_response( switch_triggere_labels= switch_triggere_labels)
            trig = True
            # The nonimpulse part
        diode_switched = self.calc_nonimpulse_response()      


        self.M_size = self.M0.rank()
        self.update_x_cur()
        
        # if trig or diode_switched:
        #     self.update_y_cur()
        #     self.update_x_cur()
        #     # self.update_y_cur()
        # else:
            
        #     self.update_x_cur()
        #     self.update_y_cur()
        if  diode_switched or trig:
            self.update_y_cur(self.x_cur)
        else:
            self.update_y_cur(x_for_update)
        # self.update_x_cur()
        #TODO: update x dependent for output?

        self.time_t.append(self.cur_system_time)
        
        self.u_output.append(  self.u.tolist())
        self.switch_state_output.append (  cur_switch_state.tolist()  )
        self.switch_triggered_output.append( cur_switch_trigger.tolist())
        
        self.y_output.append(self.y_cur[:,0].tolist())
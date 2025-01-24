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
                  print_matrix_for_matlab_format,
                  backwardEulerIntegration, trapezoidalIntegration, 
                  detemrminte_matrix_for_dependent_state_vars,
                  update_system_matrix_to_reflect_dependency
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
        self.__x_cur_ind = np.ndarray((self.number_of_state_variable,1), dtype=np.float64, )
        self.__x_cur_ind[:,:] = 0
        
        self.__x_cur_dep = np.ndarray((self.number_of_state_variable,1), dtype=np.float64, )
        self.__x_cur_dep[:,:] = 0
        
        #sp.Matrix( self.number_of_state_variable, 1,  [0 for k in range(self.number_of_state_variable)])  # assume initial value of zero in the beginning
        
        self.number_of_output = len(self.network_matrix.y_labels)
        self.y_cur = np.ndarray(  (self.number_of_output, 1), dtype=np.float64)
        self.y_cur[:, 0] = 0
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
    
    

    def update_dependent_in_xcur(self, x_cur_for_update):
        
        
        part_1  =  np.matmul(self.A_x_independent_filter, x_cur_for_update) # -1 on dependent variables
        res =   part_1    +   np.matmul( self._A_dependent, x_cur_for_update) +  np.matmul( self._B_dependent ,  self.u)
        
        # add back with original self.x_cir
        res +=x_cur_for_update
        #TODO: remove later
        
        for lab in self.dependent_state_var_labels:
            ind = self.network_matrix.x_hat_labels.index(lab)
            assert part_1[ind,0] == -x_cur_for_update[ind, 0]
        for lab in self.independent_state_var_labels:
            ind = self.network_matrix.x_hat_labels.index(lab)
            assert res[ind,0] == x_cur_for_update[ind,0]
            
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
        # #     # means stiff system encounter
        # #     # ration equation: https://en.wikipedia.org/wiki/Stiff_equation
        # #     # stiffness ratio is negotiable to change
        # #     self.integration_strategy = "stiff"
        #     print("System is very stiff")
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
            self.S_dxdt, self.Sx, self.Su, self.C1, self.C, self.D, self.M0, self.A, self.B, self.C_SW, self.D_SW, self.network_inconsistent_labels,M_offset_info = retrieveSystemMatrix(
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
            
            # # at here, determine any force-triggered events, dependent variables, and so forth before turn into numpy array
            # M0_new, A_new, B_new, A_x_ind_filter, A_dep, B_dep, ind_lab, dep_lab = detemrminte_matrix_for_dependent_state_vars(self.M0, self.A, self.B, self.network_matrix.x_hat_labels)
            # self.M0 = M0_new.copy()
            # self.B = B_new.copy()
            # self.A = A_new.copy()
            # self.A_x_independent_filter = A_x_ind_filter.copy()
            # self.A_dependent = A_dep.copy()
            # self.B_dependent = B_dep.copy()
            # self.independent_state_var_labels = ind_lab.copy()
            # self.dependent_state_var_labels = dep_lab.copy()
            
            
            # M0_value = sp.matrix2numpy(self.network_matrix.inductance_capacitance_M0.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            
            # M0_value_inverse = np.linalg.inv(M0_value)
            # self.A = M0_value_inverse@A_new
            # self.B = M0_value_inverse@B_new
            
            # _, piv = self.M0.rref()
            
            
            # filter out inconsistent labels from y _labels
            y_labels_filter = [x for x in self.network_matrix.y_labels if x not in self.network_inconsistent_labels]
            M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final = update_system_matrix_to_reflect_dependency(
                M0=self.M0.copy(),
                C1 = self.C1.copy(),
                A=self.A.copy(), B=self.B.copy(), C=self.C.copy(), D=self.D.copy(),
                m_pivots=self.network_matrix.M_pivots,
                u_labels=self.network_matrix.u_labels,
                y_labels=y_labels_filter,
                x_hat_labels=self.network_matrix.x_hat_labels,
                x_hat_col_offset_in_m_pivots=M_offset_info["x_hat_col_offset"],
                x_hat_label_to_obj_map=self.network_matrix.m_column_labels_to_obj_map,
                symbol_to_value_map=self.network_matrix.symbolic_to_value_map,
                element_name_to_obj_map=self.network_matrix.element_name_obj_map
            )
            self.M0= M0_final[:,:]
            self.A = A_final[:,:]
            self.B = B_final[:,:]
            self.C = C_final[:,:]
            self.D = D_final[:,:]
            self.A_dependent = A_dependent_final[:,:]
            self.B_dependent = B_dependent_final[:,:]
            # for col in range(self.M0.shape[0]):
            #     if col not in piv:
            #         self.A[col,:] = 0
            #         self.B[col, :] = 0
            # self.A = self.M0* self.A
            # self.B = self.M0 * self.B
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

            self.forced_switch_mapping = cache_Data[26].copy()
            self.independent_state_var_labels = cache_Data[27].copy()
            self.dependent_state_var_labels = cache_Data[28].copy()

            

        
        
        
        
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
            

    


    def calc_impulse_response(self,  switch_triggere_labels:list[str], x_cur_before_t0:np.ndarray):
           
        if len(self.forced_switch_mapping) > 0 and len(switch_triggere_labels) > 0:
            for label in switch_triggere_labels:
                switch_ele = self.network_matrix.m_column_labels_to_obj_map[label]
                list_of_diodes = self.forced_switch_mapping[switch_ele]
                
                for diode in list_of_diodes:
                    diode_index = self.switch_label_index_map[diode.element_current_name]
                    self.switch_state[diode_index] = not self.switch_state[diode_index]
                    self.swap_col_and_update(diode.element_voltage_name)
            

            # x_hat = np.matmul(self.A, x_cur_for_y) + np.matmul(self.B, self.u)
            # self.update_y_cur(x_hat_term=x_hat, x_cur_for_y=x_cur_for_y)
            
        else:

            difference = self.get_x_cur_with_dep()- x_cur_before_t0

            impulse = difference.astype(np.float32)
            
            impulse_output = self.C1@impulse
            # impulse = np.matmul( self._S_dxdt, difference, dtype=np.float32   ) 
            for i in self.diode_index:
                volt_lab, I_lab = self.switch_index_label_map[i]

                diode_ele = self.network_matrix.m_column_labels_to_obj_map[volt_lab]
                
                assert isinstance(diode_ele, Diode)
                vm_name = diode_ele.diode_voltmeter_name
                am_name = diode_ele.diode_ammeter_name
                vm_element = self.network_matrix.element_name_obj_map[vm_name]
                vm_index =  self.network_matrix.y_labels.index(vm_element.element_voltage_name)
                
                am_element = self.network_matrix.element_name_obj_map[am_name]
                am_index = self.network_matrix.y_labels.index(am_element.element_current_name)
                
                volt = impulse_output[vm_index]
                current = impulse_output[am_index]

                if volt > 0 and self.switch_state[i] == False: 
                    # assert  self.switch_state[i] == False
                    self.switch_state[i] = True
                    self.swap_col_and_update(volt_lab)
                elif current < 0 and self.switch_state[i] == True:
                    # assert self.switch_state[i] == True
                    self.switch_state[i] = False
                    self.swap_col_and_update(volt_lab)
                else:
                    pass
            
            
            
            # x_hat = np.matmul(self.A, x_cur_for_y) + np.matmul(self.B, self.u)  #TODO: use impulse in output?
            # self.update_y_cur(x_hat_term=x_hat, x_cur_for_y=x_cur_for_y)
            # replace 
            
        
        
    def calc_nonimpulse_response(self):
        
        diode_switched = False


        
        
        for i in self.diode_index:

            volt_lab, I_lab = self.switch_index_label_map[i]
            diode_state = self.switch_state[i]
            diode_ele = self.network_matrix.m_column_labels_to_obj_map[volt_lab]
            
            assert isinstance(diode_ele, Diode)
            vm_name = diode_ele.diode_voltmeter_name
            am_name = diode_ele.diode_ammeter_name
            vm_element = self.network_matrix.element_name_obj_map[vm_name]
            vm_index =  self.network_matrix.y_labels.index(vm_element.element_voltage_name)
            
            am_element = self.network_matrix.element_name_obj_map[am_name]
            am_index = self.network_matrix.y_labels.index(am_element.element_current_name)
            
            volt = self.y_cur[vm_index]
            current = self.y_cur[am_index]
        
            # get the vm, am from y_cur
            
            if diode_state == False and volt>0 :
                self.switch_state[i] = True
                self.swap_col_and_update(volt_lab)
                diode_switched = True
            elif diode_state == True and current < 0 :
                self.switch_state[i] = False
                self.swap_col_and_update(volt_lab)
                diode_switched = True
            else:
                pass
        
        
        # x_hat = np.matmul(self.A, x_cur_for_y) + np.matmul(self.B, self.u)  #TODO: use impulse in output?
        # self.update_y_cur(x_hat_term=x_hat, x_cur_for_y=x_cur_for_y)
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
            # legend=dict(
            #     yanchor="top",
            #     y=0.99,
            #     xanchor="right",
            #     x=-0.0001
            # )
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


    
    def update_internal_switch_response(self, switch_trigger_labels:list[str], x_cur_before_t0:np.ndarray):
        
        
        if len(self.forced_switch_mapping) > 0 and len(switch_trigger_labels) > 0:
            for label in switch_trigger_labels:
                switch_ele = self.network_matrix.m_column_labels_to_obj_map[label]
                list_of_diodes = self.forced_switch_mapping[switch_ele]
                
                for diode in list_of_diodes:
                    diode_index = self.switch_label_index_map[diode.element_current_name]
                    self.switch_state[diode_index] = not self.switch_state[diode_index]
                    self.swap_col_and_update(diode.element_voltage_name)

        
        # now, check for any impulse switch or soft switch
        
        impulse_output = self.C1@ (self.get_x_cur_with_dep() - x_cur_before_t0)
        

        self.update_y_cur(self.get_x_cur_with_dep() )
        non_impulse = self.y_cur.copy()

        for i in self.diode_index:
            volt_lab, I_lab = self.switch_index_label_map[i]
            diode_state = self.switch_state[i]
            diode_ele = self.network_matrix.m_column_labels_to_obj_map[volt_lab]
            
            assert isinstance(diode_ele, Diode)
            vm_name = diode_ele.diode_voltmeter_name
            am_name = diode_ele.diode_ammeter_name
            vm_element = self.network_matrix.element_name_obj_map[vm_name]
            vm_index =  self.network_matrix.y_labels.index(vm_element.element_voltage_name)
            
            am_element = self.network_matrix.element_name_obj_map[am_name]
            am_index = self.network_matrix.y_labels.index(am_element.element_current_name)
            
            volt_impulse = impulse_output[vm_index]
            current_impulse = impulse_output[am_index]

            volt_nonimpulse = non_impulse[vm_index]
            current_nonimpulse = non_impulse[am_index]
            
            if volt_impulse > 0 or ( diode_state==False and volt_nonimpulse>0 ):
                self.switch_state[i] = True
                self.swap_col_and_update(volt_lab)
            elif current_impulse <0 or (diode_state == True and current_nonimpulse < 0):
                self.switch_state[i] = False
                self.swap_col_and_update(volt_lab)
            else:
                pass
        
    
        # self.update_y_cur(self.get_x_cur_with_dep())
            
    def update_y_cur(self, x_cur_for_y ):
        
        self.y_cur =  np.matmul( self._C_iteration ,x_cur_for_y) +  np.matmul( self._D_iteration ,self.u)
    
    def get_x_hat(self,):
        return  np.matmul(self.A, self.get_x_cur_no_dep()) +np.matmul(self.B, self.u)
    def get_x_cur_no_dep(self):
        return self.__x_cur_ind
    

    def get_x_cur_with_dep(self):
        return (self._A_dependent@ self.get_x_cur_no_dep() + self._B_dependent@self.u)



    def update_x_cur(self):
        # no need to get x_cur_with_dep
        # because the corresponding row of A of the depent x is all 0
        if self.integration_strategy == "Trapezoidal":
            x_t = trapezoidalIntegration( self.get_x_cur_no_dep(), self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency ).copy()
        else:
            x_t = backwardEulerIntegration(self.get_x_cur_no_dep(), self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency).copy()

        
        self.__x_cur_ind =x_t

    def iteration(self):
        
        
        
        # #for debug
        # if self.cur_system_time == 0:
        #     # # came in as  TFTT
        #     tftt=200
            
        #     # swap to tfff
        #     self.switch_state[3] = False
        #     self.swap_col_and_update("V_D2")
        #     self.switch_state[2] = False
        #     self.swap_col_and_update("V_D1")
        #     tfff=200
            
        #     # swap to TFTF
        #     self.switch_state[2] = True
        #     self.swap_col_and_update("V_D1")
        #     tftf = 200
            
        #     # swap to TFFT
        #     self.switch_state[2] = False
        #     self.swap_col_and_update("V_D1")
        #     self.switch_state[3] = True
        #     self.swap_col_and_update("V_D2")
        #     tfft = 200

        #     # swap to FTFT
        #     self.switch_state[0] = False
        #     self.swap_col_and_update("V_S1")
        #     self.switch_state[1] = True
        #     self.swap_col_and_update("V_S2")
        #     ftft = 200
            
        #     # swap to ftff
        #     self.switch_state[3] = False
        #     self.swap_col_and_update("V_D2")
        #     ftff = 200
            
        #     # swap to fttf
        #     self.switch_state[2] = True
        #     self.swap_col_and_update("V_D1")
        #     fttf = 200
            
        #     # swap to fttt
        #     self.switch_state[3] = True
        #     self.swap_col_and_update("V_D2")
        #     fttt = 200
            
        #     # swap to fttf
        #     self.switch_state[3] = False
        #     self.swap_col_and_update("V_D2")
        #     fttf = 200
            
        #     # swap to tftf
        #     self.switch_state[0] = True
        #     self.swap_col_and_update("V_S1")
        #     self.switch_state[1] = False
        #     self.swap_col_and_update("V_S2")
        #     p = 200
        # # turn all diode to off 
        # if self.cur_system_time == 0:
        #     for i in self.diode_index:
        #         volt_lab, I_lab = self.switch_index_label_map[i]
        #         if self.switch_state[i] == True:
        #             self.switch_state[i] = False
        #             self.swap_col_and_update(volt_lab)
        # the iteration process
        x_before_t0 = self.get_x_cur_no_dep().copy()
        


        self.update_x_cur()
        # self.update_y_cur( self.get_x_cur_no_dep())



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
     
        # y_cur_before_update = self.y_cur.copy()
        self.update_internal_switch_response(switch_trigger_labels=switch_triggere_labels, x_cur_before_t0=x_before_t0)

        # if self.M0.rank() < self.network_matrix.x_hat_label_size or len(self.forced_switch_mapping) > 0 :
        #     self.calc_impulse_response( switch_triggere_labels= switch_triggere_labels, x_cur_before_t0=x_before_t0)
        #     trig = True
        # else:
        #     diode_switched = self.calc_nonimpulse_response()      


        self.M_size = self.M0.rank()

        
        self.time_t.append(self.cur_system_time)
        
        self.u_output.append(  self.u.tolist())
        self.switch_state_output.append (  cur_switch_state.tolist()  )
        self.switch_triggered_output.append( cur_switch_trigger.tolist())
        
        self.y_output.append(self.y_cur[:,0].tolist())
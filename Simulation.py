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
from util import (print_matrix,is_rise_edge, retrieveSystemMatrix,
                  backwardEulerIntegration, trapezoidalIntegration, 
                  update_system_matrix_to_reflect_dependency,retrieve_Zsw_hat,tustin_integration_step, radau_integration_step,
                  pade_0_3_integration,
                  pade_0_2_integration
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
    def __init__(self, switch: ExternalSwitch, switch_message: SwitchMessage):
        super().__init__()
        self.switch: ExternalSwitch = switch

        assert self.switch.duty_cycle <= 1.0
        self.cur_switch_status = switch.initial_switch_state
        self.switch_message = switch_message
        self.message_level_dependent = 1
        
    # def pwm_at_time_t(self, time_t) -> bool:
    #     period = 1 / self.switch.switch_frequency  # Period of the PWM signal
    #     time_in_period =  math.fmod( time_t , period)  # Time within the current PWM period
    #     high_duration = (
    #         self.switch.duty_cycle * period
    #     )  # Duration of the "high" state in one period

    #     val =  time_in_period < high_duration
    #     if self.switch.pwm_value_at_each_new_cycle:
    #         return val
    #     else:
    #         return not val
    # def pwm_at_time_t(self, time_t, delay: float = 0.0) -> bool:
    #     """
    #     Calculate the PWM signal state at a given time, with an optional delay.

    #     :param time_t: The time at which to evaluate the PWM signal.
    #     :param delay: The delay to apply to the PWM signal (default is 0.0).
    #     :return: True if the PWM signal is high at time_t, False otherwise.
    #     """
    #     period = 1 / self.switch.switch_frequency  # Period of the PWM signal
    #     time_with_delay = time_t - delay  # Apply the delay to the input time

    #     # Handle negative time_with_delay by wrapping it into the PWM period
    #     if time_with_delay < 0:
    #         time_with_delay = 0

    #     time_in_period = math.fmod(time_with_delay, period)  # Time within the current PWM period
    #     high_duration = (
    #         self.switch.duty_cycle * period
    #     )  # Duration of the "high" state in one period

    #     val = time_in_period < high_duration
    #     if self.switch.pwm_value_at_each_new_cycle:
    #         return val
    #     else:
    #         return not val
    def pwm_at_time_t(self, time_t, delay=0) -> bool:
        period = 1 / self.switch.switch_frequency  # Period of the PWM signal
        adjusted_time = time_t - delay  # Apply the delay
        time_in_period = math.fmod(adjusted_time, period)  # Time within the current PWM period
        high_duration = self.switch.duty_cycle * period  # Duration of the "high" state in one period

        val = time_in_period < high_duration
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
        self.u = np.ndarray( ( 1, self.u_size ), dtype=np.float64 )

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
        self.__x_cur_ind = np.ndarray((self.number_of_state_variable,1), dtype=np.float64, )
        self.__x_cur_ind[:,:] = 0

        self.y_cur = np.ndarray(  (self.network_matrix.u_label_size, 1), dtype=np.float64)
        self.y_cur[:, 0] = 0

        self.Q:Matrix = None
        self.C: Matrix =None
        self.C1:Matrix = None
        self.D :Matrix = None
        self.M0 :Matrix = None
        self.A :Matrix = None
        self.B :Matrix = None
        self.M_size = 0
        self.M_pivots: Tuple=None
        self.integration_strategy:str=""
        
        self._A_iteration:npt.NDArray = None
        self._B_iteration:npt.NDArray  =None
        self._C_iteration:npt.NDArray   = None
        self._D_iteration:npt.NDArray  = None
        self._A_dependent:npt.NDArray  = None
        self._B_dependent:npt.NDArray  = None
        
        
        self.C_impulse:npt.NDArray = None
        self.C_non_impulse:npt.NDArray= None
        self.D_impulse:npt.NDArray = None
        self.D_non_impulse:npt.NDArray = None
        self.A_dependent:Matrix = None
        self.B_dependent:Matrix =  None

        self.C_SW:npt.NDArray = None
        self.D_SW:npt.NDArray = None
        self.C_impulse_SW:npt.NDArray = None
        self.D_impulse_SW:npt.NDArray = None
        self.C_non_impulse_SW:npt.NDArray = None
        self.D_non_impulse_SW:npt.NDArray = None
        self.Z_hat_SW_A:npt.NDArray = None
        self.Z_hat_SW_B:npt.NDArray = None
        self.C1_SW:npt.NDArray = None

        self.y_dep_labels:list[str] = []
        self.forced_switch_mapping:dict[Element, list[Element]] = {}
        
        self.M_cache :dict[str, Matrix] = {}
        
        
        # ouput and debug record
        self.time_t:list[float] = []
        self.y_output:list[list[float]] = []
        self.x_output:list[list[float]] = []
        
        self.switch_state_output:list[list[int]] = []
        self.switch_triggered_output:list[list[int]] = []
        
        self.fig_count = 1
        self.initialize_data()
    
    


        
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
    

            
               
    def choose_intergation_strategy(self):
        # numerical oscillation (not system oscillation) will always occur for any real eigenvalue < 0
        
        # use trapezoidal  by default
        # use backward euler if real eigenvalue < -2 
        temp = self.A.subs(self.network_matrix.symbolic_to_value_map).copy()
        temp = temp* (1/self.iteration_frequency)

        
        # Step 2: Check stability (eigenvalues within [-1, 1])
        eigenvalues = np.linalg.eigvals(sp.matrix2numpy(temp, dtype=np.float64))
        stability = all(abs(eig) <= 1 for eig in eigenvalues)

        # Step 3: Check stiffness (large spread of eigenvalue magnitudes)
        min_eig = min(eigenvalues)
        max_eig = max(eigenvalues)
        min_eig_mag = min(np.abs(eigenvalues))
        max_eig_mag = max(np.abs(eigenvalues))
        stiffness = True if min_eig_mag==0 else  (max_eig_mag / min_eig_mag) > 10

        # Output results
        if all(abs(eig) <= 1 for eig in eigenvalues):
            print("Stable")
            self.integration_strategy= "Trapezoidal"
        else:
            print("Unstable")
            self.integration_strategy= "BackwardEuler"
        self.integration_strategy= "Trapezoidal"
        print("Eigenvalues:", eigenvalues)
        print("Stiffness:", stiffness)
        # if min( min_eig, max_eig  )  <= -2:
        # self.integration_strategy = "BackwardEuler"
        # else:
        #self.integration_strategy = "Trapezoidal"
            
        print(f"***********using {self.integration_strategy} *****************")
    # def choose_intergation_strategy(self):
    #     # numerical oscillation (not system oscillation) will always occur for any real eigenvalue < 0
        
    #     # use trapezoidal  by default
    #     # use backward euler if real eigenvalue < -2 
    #     temp = self.A.subs(self.network_matrix.symbolic_to_value_map)
    #     eigen_value_dict = temp.eigenvals()
        

    #     min_eig = min(  [  sp.re(x.subs(self.network_matrix.symbolic_to_value_map))  * (1/self.iteration_frequency) for x  in eigen_value_dict.keys()])
    #     max_eig =  max(  [  sp.re(x.subs(self.network_matrix.symbolic_to_value_map))  * (1/self.iteration_frequency) for x  in eigen_value_dict.keys()])
        
    #     max_abs = max([  abs(sp.re(x.subs(self.network_matrix.symbolic_to_value_map))  * (1/self.iteration_frequency)) for x  in eigen_value_dict.keys()])
    #     min_abs = min([  abs(sp.re(x.subs(self.network_matrix.symbolic_to_value_map))  * (1/self.iteration_frequency)) for x  in eigen_value_dict.keys()])
        
    #     if min_abs == 0 or  max_abs/min_abs > 1000:
    #     #     # means stiff system encounter
    #     #     # ration equation: https://en.wikipedia.org/wiki/Stiff_equation
    #     #     # stiffness ratio is negotiable to change
    #         print("System is very stiff")
    #     print(f"Max  eig, min eig {max_eig} {min_eig}")
    #     if min_eig <= -2:
    #         self.integration_strategy = "BackwardEuler"
    #     else:
    #         self.integration_strategy = "Trapezoidal"
            
    #     print(f"***********using {self.integration_strategy} *****************")
        
        
    def swap_col_and_update(self, label_to_Swap:str):
        if label_to_Swap != "":
            self.network_matrix.swap_M_matrix_columns(label_to_Swap)
        # do a cache
        

        
        key  = "".join(self.network_matrix.m_column_labels)
        if key not in self.M_cache.keys():
        
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
            # y_labels_filter = [x for x in self.network_matrix.y_labels if x not in self.network_inconsistent_labels]
            M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final, \
                self.C_impulse, self.C_non_impulse, self.D_impulse, self.D_non_impulse= update_system_matrix_to_reflect_dependency(
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
            self.M0= M0_final[:,:]
            self.A = A_final[:,:]
            self.B = B_final[:,:]
            self.C = C_final[:,:]
            self.D = D_final[:,:]
            self.A_dependent = A_dependent_final[:,:]
            self.B_dependent = B_dependent_final[:,:]

            self._A_iteration = sp.matrix2numpy(self.A.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._B_iteration = sp.matrix2numpy(self.B.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._C_iteration = sp.matrix2numpy(self.C.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._D_iteration = sp.matrix2numpy(self.D.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)

            self._A_dependent = sp.matrix2numpy(self.A_dependent.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self._B_dependent = sp.matrix2numpy(self.B_dependent.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            
            
            
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
            
            self.C_SW = sp.matrix2numpy(self.C_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self.D_SW = sp.matrix2numpy(self.D_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self.C_impulse_SW = sp.matrix2numpy(self.C_impulse_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self.D_impulse_SW = sp.matrix2numpy(self.D_impulse_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self.C_non_impulse_SW = sp.matrix2numpy(self.C_non_impulse_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self.D_non_impulse_SW= sp.matrix2numpy(self.D_non_impulse_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self.Z_hat_SW_A = sp.matrix2numpy(self.Z_hat_SW_A.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self.Z_hat_SW_B = sp.matrix2numpy(self.Z_hat_SW_B.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            self.C1_SW = sp.matrix2numpy(self.C1_SW.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float64)
            
            cache_Data = [
                            self.network_matrix.M[:,:], 
                            self.C1[:,:], self.C[:,:], self.D[:,:],
                            self.M0[:,:], self.A[:,:], self.B[:,:],
                            self._A_iteration[:,:],
                            self._B_iteration[:,:],
                            self._C_iteration[:,:],
                            self._D_iteration[:,:],
                            self.y_dep_labels.copy(),
                            self.A_dependent[:,:],
                            self.B_dependent[:,:],
                            self._A_dependent[:,:],
                            self._B_dependent[:,:],
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
                            self.Q.copy()
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
            self._A_iteration = cache_Data[7][:,:]
            self._B_iteration = cache_Data[8][:,:]
            self._C_iteration = cache_Data[9][:,:]
            self._D_iteration = cache_Data[10][:,:]
            self.y_dep_labels = cache_Data[11].copy()
            self.A_dependent = cache_Data[12][:,:]
            self.B_dependent = cache_Data[13][:,:]
            self._A_dependent = cache_Data[14][:,:]
            self._B_dependent = cache_Data[15][:,:]
            self.forced_switch_mapping = cache_Data[16].copy()
            self.C_impulse = cache_Data[17].copy()
            self.C_non_impulse = cache_Data[18].copy()
            self.D_impulse = cache_Data[19].copy()
            self.D_non_impulse = cache_Data[20].copy()

            
            self.C_SW=cache_Data[21].copy()
            self.D_SW=cache_Data[22].copy()
            self.C_impulse_SW=cache_Data[23].copy()
            self.D_impulse_SW=cache_Data[24].copy()
            self.C_non_impulse_SW=cache_Data[25].copy()
            self.D_non_impulse_SW=cache_Data[26].copy()
            self.Z_hat_SW_A=cache_Data[27].copy()
            self.Z_hat_SW_B=cache_Data[28].copy()
            self.C1_SW = cache_Data[29].copy()
            self.Q = cache_Data[30].copy()
        
        
        
        
    def initialize_data(self):
        
        # the diode state
        
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
                self.switch_state[ind] =  None
                self.switch_triggered[ind] = False
  
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
                        self.switch_state[ind] = True if value else False
                        self.switch_triggered[ind] = False
                       
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

    def plot_output_graph(self, ax1_y_ticks=None, ax2_y_ticks=None, outputfile_name="output.csv"):
        time_np_array = np.array(self.time_t)
        y_output_np_array = np.array(self.y_output, dtype=np.float64).squeeze()

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


    def update_internal_switch_response(self, switch_trigger_labels:list[str], x_cur_before_t0:np.ndarray):
        
        
        # if len(self.forced_switch_mapping) > 0 and len(switch_trigger_labels) > 0:
        #     for label in switch_trigger_labels:
        #         switch_ele = self.network_matrix.m_column_labels_to_obj_map[label]
        #         list_of_diodes = self.forced_switch_mapping[switch_ele]
                
        #         for diode in list_of_diodes:
        #             diode_index = self.switch_label_index_map[diode.element_current_name]
        #             self.switch_state[diode_index] = not self.switch_state[diode_index]
        #             self.swap_col_and_update(diode.element_voltage_name)

        
        # now, check for any impulse switch or soft switch
        
        # impulse_output = np.matmul(self.C1, (self.get_x_cur_with_dep() - x_cur_before_t0)) 
        impulse_val = np.matmul(self.C1_SW, (self.get_x_cur_with_dep() - x_cur_before_t0))

        # non_impulse  = np.matmul( self._C_iteration ,self.get_x_cur_with_dep()) +  np.matmul( self._D_iteration ,self.u)

        non_impulse_val = np.matmul( self.C_SW ,self.get_x_cur_with_dep()) +  np.matmul( self.D_SW ,self.u)
        
        swapped_flag = False
    
    
        diode_count = 0
        for i in self.diode_index:
            volt_lab, I_lab = self.switch_index_label_map[i]
            diode_state = self.switch_state[i]
            volt_nonimpulse = current_nonimpulse = non_impulse_val[diode_count]
            volt_impulse = current_impulse = impulse_val[diode_count]
  
            
            if volt_impulse > 0 or ( diode_state==False and volt_nonimpulse>0 ):
                self.switch_state[i] = True
                self.swap_col_and_update(volt_lab)
                swapped_flag = True
            elif current_impulse <0 or (diode_state == True and current_nonimpulse < 0):
                self.switch_state[i] = False
                self.swap_col_and_update(volt_lab)
                swapped_flag = True

            else:
                pass
                
            diode_count +=1
        

        impulse_occur =  (len(switch_trigger_labels) > 0) or (not swapped_flag)
        self.M_size =  self.M0.rank()

        self.update_y_cur(  impulse_occur)

    def update_y_cur(self, use_impulse= False ):
        
        if  use_impulse:
            self.y_cur =  np.matmul( self._C_iteration ,self.get_x_cur_no_dep()) +  np.matmul( self._D_iteration ,self.u)
        else:
            self.y_cur =  np.matmul(self.C_non_impulse, self.get_x_cur_no_dep()) + np.matmul(self.D_non_impulse, self.u)

    def get_x_hat(self,):
        return  np.matmul(self.A, self.get_x_cur_no_dep()) +np.matmul(self.B, self.u)
    def get_x_cur_no_dep(self):
        return self.__x_cur_ind
    

    def get_x_cur_with_dep(self):
        return (self._A_dependent@ self.get_x_cur_no_dep() + self._B_dependent@self.u)



    def update_x_cur(self):
        # no need to get x_cur_with_dep
        # because the corresponding row of A of the depent x is all 0
        
        x_before = self.get_x_cur_no_dep().copy()
        # if self.integration_strategy == "Trapezoidal":
        #x_t = trapezoidalIntegration( x_before, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency ).copy()
        # else:
        #     x_t = backwardEulerIntegration(x_before, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency).copy()
        # 
        #x_t = pade_0_3_integration( x_before, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency ).copy()
        
        x_t = pade_0_2_integration( x_before, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency ).copy()
        #x_t = tustin_integration_step(x_before, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency).copy()
        #x_t = radau_integration_step( x_before, self._A_iteration, self._B_iteration, self.u,   time_t=self.cur_system_time,dt=1/self.iteration_frequency ).copy()
        self.__x_cur_ind =x_t

    def iteration(self):

        x_before_t0 = self.get_x_cur_with_dep().copy()
 
        
        self.update_x_cur()

        # # for now, assume only one switch change in one time period
        switch_triggere_labels = []
        for i in range(len(self.switch_triggered)):


            if self.switch_triggered[i] :
                # assert self.switch_triggered[0] is True
                # assert self.switch_triggered[1] is True
                sw_volt_lab, sw_I_lab = self.switch_index_label_map[i]
                if self.switch_state[i]:
                    self.swap_col_and_update(sw_volt_lab)
                    
                    # debug
                    new_ind = self.network_matrix.m_column_labels.index(sw_I_lab)
                    assert new_ind <= self.network_matrix.redundant_size + self.network_matrix.s_labels_size
                    
                else:
                    self.swap_col_and_update(sw_I_lab)
                    new_ind = self.network_matrix.m_column_labels.index(sw_volt_lab)
                    assert new_ind <= self.network_matrix.redundant_size + self.network_matrix.s_labels_size
                switch_triggere_labels.append(sw_volt_lab)

        self.update_internal_switch_response(switch_trigger_labels=switch_triggere_labels, x_cur_before_t0=x_before_t0)

        
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
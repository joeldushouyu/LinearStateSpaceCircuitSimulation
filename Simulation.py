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
from util import is_rise_edge, retrieveSystemMatrix, swapTwoColumn,determine_dependent_state_vars, backwardEulerIntegration, trapezoidalIntegration
from typing import Tuple
import numpy as np
import numpy.typing as npt
from functools import total_ordering
import matplotlib.pyplot as plt
import matplotlib.ticker as plt_ticker
from matplotlib.widgets import CheckButtons
from visualize import on_pick
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

        return time_in_period < high_duration


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
                    self.switch_states_receive[index] = [message.is_switch_on()]
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
        self.u = np.ndarray( ( 1, self.u_size ), dtype=np.float32 )
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
        self.x_cur = np.ndarray((self.number_of_state_variable,1), dtype=np.float32, )
        self.x_cur[:,:] = 0
        
        #sp.Matrix( self.number_of_state_variable, 1,  [0 for k in range(self.number_of_state_variable)])  # assume initial value of zero in the beginning
        
        self.number_of_output = len(self.network_matrix.y_labels)
        self.y_cur = np.ndarray(  (self.number_of_output, 1), dtype=np.float32)
        #self.y_cur = sp.Matrix(self.number_of_output, 1, [0 for k in range(self.number_of_output)]) 
    
        self.C: None|Matrix =None
        self.D :None|Matrix = None
        self.M0 :None|Matrix = None
        self.A :None|Matrix = None
        self.B :None|Matrix = None
        self.S_dxdt:None|Matrix = None
        self.Sx:None|Matrix = None
        self.Su:None|Matrix = None
        self.M_size = 0
        self.M_pivots:None| Tuple=None
        self.integration_strategy:str=""
        
        self._A_iteration:None|np.array = None
        self._B_iteration:None|np.array=None
        self._C_iteration:None|np.array = None
        self._D_iteration:None|np.array = None
        self._S_dxdt:None|np.array = None
        self._Sx:None|np.array = None
        self._Su:None|np.array = None
        self.initialize_data()
    
        
        
        # ouput and debug record
        
        self.time_t:list[float] = []
        self.y_output:list[list[float]] = []
        self.x_output:list[list[float]] = []
        
        self.switch_state_output:list[list[int]] = []
        self.switch_triggered_output:list[list[int]] = []
        self.u_output:list[list[float]] = []
        
        
   
    def choose_intergation_strategy(self):
        # numerical oscillation (not system oscillation) will always occur for any real eigenvalue < 0
        
        # use trapezoidal  by default
        # use backward euler if real eigenvalue < -2 
        temp = self.A * (1/self.iteration_frequency)
        eigen_value_dict = temp.eigenvals()
        
        
        min_eig = min(  [  sp.re(x.subs(self.network_matrix.symbolic_to_value_map)) for x  in eigen_value_dict.keys()])
        
        if min_eig <= -2:
            self.integration_strategy = "BackwardEuler"
        else:
            self.integration_strategy = "Trapezoidal"
        
        
    def swap_col_and_update(self, label_to_Swap:str):
        if label_to_Swap != "":
            swapTwoColumn(self.network_matrix.M, self.network_matrix.m_column_labels,
                        self.network_matrix.m_column_labels_to_obj_map, label_to_Swap)
            
        self.network_matrix.M, self.M_pivots = self.network_matrix.M.rref()
        self.S_dxdt, self.Sx, self.Su, pivots, self.C, self.D, self.M0, self.A, self.B = retrieveSystemMatrix(
            
            
            M=self.network_matrix.M,
            s_labels_size=self.network_matrix.s_labels_size,
            y_labels_size=self.network_matrix.y_label_size,
            x_hat_labels_size=self.network_matrix.x_hat_label_size,
            x_labels_size=self.network_matrix.x_label_size,
            y_zero_labels_size=self.network_matrix.y_zero_label_size,
            s_zero_labels_size=self.network_matrix.s_zero_label_size
         )
        
        
        self._A_iteration = sp.matrix2numpy(self.A.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
        self._B_iteration = sp.matrix2numpy(self.B.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
        self._C_iteration = sp.matrix2numpy(self.C.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
        self._D_iteration = sp.matrix2numpy(self.D.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
        self._S_dxdt = sp.matrix2numpy(self.S_dxdt.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
        self._Sx = sp.matrix2numpy(self.Sx.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)
        self._Su = sp.matrix2numpy(self.Su.subs(self.network_matrix.symbolic_to_value_map), dtype=np.float32)

    
        
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
            


    def calc_impulse_response(self, sw_volt_lab:str):
        
        forced_triggered_diodes, Add_inv, Adi, Bd, ind_state_lab, ind_state_cols, dep_state_lab, dep_state_cols = determine_dependent_state_vars(self.M0, self.A, self.B,self.network_matrix,sw_volt_lab)
        
        
        if len(forced_triggered_diodes) > 0:
            for lab in forced_triggered_diodes:
                ind = self.switch_label_index_map[lab]
                self.switch_state[ind] = ~self.switch_state[ind]
                self.swap_col_and_update(lab)
            return
        
        x_ind = Matrix(  len(ind_state_cols), 1, [0]*len(ind_state_cols) )
       
        x_state_imp = self.x_cur.copy()
        
        for i in range(len (ind_state_cols) ):
            col = ind_state_cols[i]
            x_ind[i] = x_state_imp[col]
            
        
        x_dep = -Add_inv*(Adi*x_ind+Bd*self.u)
        x_dep.subs(self.network_matrix.symbolic_to_value_map)
         
        for i in range(len(dep_state_cols )):
            col = dep_state_cols[i]
            x_state_imp[col] = x_dep[i]


        #impulse = self.S_dxdt*(x_state_imp - self.x_cur)
        impulse = np.matmul( self._S_dxdt, (x_state_imp - self.x_cur), dtype=np.float32   )
        # check to see any diode's has a impulse
        
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
        
        
        non_impulse   =  np.matmul( self._Sx, self.x_cur )   +  np.matmul(self._Su, self.u)  
        #non_impulse.subs(self.network_matrix.symbolic_to_value_map)
        for i in self.diode_index:
            non_imp = non_impulse[i,0]
            volt_lab, I_lab = self.switch_index_label_map[i]
            diode_state = self.switch_state[i]
            
            if diode_state == False and non_imp>0:
                self.switch_state[i] = True
                self.swap_col_and_update(volt_lab)
            elif diode_state == True and non_imp < 0:
                self.switch_state[i] = False
                self.swap_col_and_update(volt_lab)
            else:
                pass



    def plot_output_graph(self, ax1_y_ticks=None, ax2_y_ticks=None):
        time_np_array = np.array(self.time_t)
        y_output_np_array = np.array(self.y_output).squeeze()
        fig = plt.figure()
        
        # Create subplots for current and voltage
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        line_map = {}  # To store line objects and their data
        
        for i in range(self.network_matrix.y_label_size):
            lab = self.network_matrix.y_labels[i]
            ele = self.network_matrix.m_column_labels_to_obj_map[lab]
            if isinstance(ele, Voltmeter):
                line, = ax1.plot(time_np_array, y_output_np_array[:, i], label=f"{ele.name}")
            else:
                line, = ax2.plot(time_np_array, y_output_np_array[:, i], label=f"{ele.name}")
            line_map[line] = (time_np_array, y_output_np_array[:, i])
        
        ax1.grid()
        ax2.grid()
        ax1.legend()
        ax2.legend()
        
        if ax1_y_ticks is not None:
            ax1.yaxis.set_major_locator(plt_ticker.MultipleLocator(ax1_y_ticks))
        if ax2_y_ticks is not None:
            ax2.yaxis.set_major_locator(plt_ticker.MultipleLocator(ax2_y_ticks))
        
        # Event handler for mouse clicks
        def on_pick(event):
            line = event.artist
            xdata, ydata = line_map[line]
            ind = event.ind[0]  # Get the index of the selected point
            x, y = xdata[ind], ydata[ind]
            print(f"Selected point: x={x}, y={y}")
            # Optionally, add a marker or annotation at the clicked point
            ax = line.axes
            ax.annotate(f'({x:.2f}, {y:.2f})', xy=(x, y), xytext=(10, 10),
                        textcoords='offset points', arrowprops=dict(arrowstyle='->'))
            fig.canvas.draw_idle()

        # Connect the event to the plot
        fig.canvas.mpl_connect('pick_event', on_pick)

        # Enable picking on all lines
        for line in line_map:
            line.set_picker(True)

        # Add interactive checkboxes
        labels = [line.get_label() for line in line_map.keys()]
        visibility = [line.get_visible() for line in line_map.keys()]
        check_ax = fig.add_axes([0.8, 0.4, 0.15, 0.4])  # Position for checkboxes
        check = CheckButtons(check_ax, labels, visibility)

        def toggle_visibility(label):
            for line in line_map:
                if line.get_label() == label:
                    line.set_visible(not line.get_visible())
            fig.canvas.draw_idle()
        
        check.on_clicked(toggle_visibility)

        plt.show()

    def iteration(self):
        # the iteration process
        

        cur_switch_state = self.switch_state[self.switch_mask]
        cur_diode_state = self.switch_state[~self.switch_mask]
        cur_switch_trigger = self.switch_triggered[self.switch_mask]
        # record u and switch labe
        

        trig = False
        # for now, assume only one switch change in one time period
        for i in range(len(self.switch_triggered)):
            if self.switch_triggered[i] :
                assert trig  == False
                # print(self.cur_system_time)
                # means this switch istriggered
                sw_volt_lab, sw_I_lab = self.switch_index_label_map[i]
                self.swap_col_and_update(sw_volt_lab)
            
            
        if self.M0.rank() < self.M_size:
            self.calc_impulse_response(sw_volt_lab=sw_volt_lab)

            # The nonimpulse part
        self.calc_nonimpulse_response()      
        self.M_size = self.M0.rank()

        

        if self.integration_strategy == "Trapezoidal":
            self.x_cur = trapezoidalIntegration( self.x_cur, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency )
        else:
            self.x_cur = backwardEulerIntegration(self.x_cur, self._A_iteration, self._B_iteration, self.u, time_t=1/self.iteration_frequency)
        
        # the outpyt
        # self.y_cur = self.C * self.x_cur + self.D * self.u
        # self.y_cur = self.y_cur.subs(self.network_matrix.symbolic_to_value_map)
        
        self.y_cur = np.matmul( self._C_iteration , self.x_cur) +  np.matmul( self._D_iteration ,self.u)
        self.time_t.append(self.cur_system_time)
        
        self.u_output.append(  self.u.tolist())
        self.switch_state_output.append (  cur_switch_state  )
        self.switch_triggered_output.append( cur_switch_trigger)
        
        self.y_output.append(self.y_cur.tolist())
        
        
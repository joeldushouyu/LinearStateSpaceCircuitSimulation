
from sympy import  Symbol
class Node:
    def __init__(self, name:str):
        self.name = name
        
        self.node_a_element:list[Element] = []  # node a of element
        self.node_b_element:list[Element] = [] # node b of element
        
        # self.row_index_in_A_matrix = 0
class GroundNode(Node):
    def __init__(self, name):
        super().__init__(name)
        
        
        
class Element:
    
    # convention, current flow from port a to port b
    def __init__(self, name:str, port_a:Node, port_b: Node):
        self.name = name
        self.port_a = port_a
        self.port_b = port_b

        self.element_voltage_name = f"V_{name}"
        self.element_current_name = f"I_{name}"
        self.is_port_element = None
        
        # self.col_index_in_A_matrix = 0
        
        
class PortElement(Element):
    
    def __init__(self, name, port_a, port_b):
        super().__init__(name, port_a, port_b)
        self.is_port_elemen = True
class VoltageCurrentSource(PortElement):
    #TODO: introduct variation in simulation 
    def __init__(self, name:str, port_a: Node, port_b: Node, amplitude:float, frequency:float, is_voltage_source:bool):
        super().__init__(name, port_a, port_b)   
        

        self.amplitude = amplitude
        self.frequency = frequency
        self.is_voltage_source = is_voltage_source

class Ammeter(PortElement):
    
    def __init__(self, name, port_a, port_b):
        super().__init__(name, port_a, port_b)
        
class Voltmeter(PortElement):
    def __init__(self, name, port_a, port_b):
        super().__init__(name, port_a, port_b)

class ExternalSwitch(PortElement):
    def __init__(self, name, port_a, port_b, pwm_value_at_each_new_cycle:bool, switch_frequency:float, duty_cycle:float):
        super().__init__(name, port_a, port_b)
        self.pwm_value_at_each_new_cycle = pwm_value_at_each_new_cycle  # true if pwm wave from hight to low for each cycle, false other wise
        self.initial_switch_state = self.pwm_value_at_each_new_cycle # assume at start of switch cycle at t = 0
        self.switch_frequency = switch_frequency
        self.duty_cycle = duty_cycle
class Diode(PortElement):
    def __init__(self, name, port_a, port_b, initial_switch_state:bool):
        super().__init__(name, port_a, port_b)
        self.initial_switch_state = initial_switch_state

class Inductor(PortElement):
    def __init__(self, name, port_a, port_b, inductance:float, inductor_symbol:Symbol, mutual_inductor_names:list[str]|None=None, K_factors:list[Symbol]|None = None):
        super().__init__(name, port_a, port_b)
        if mutual_inductor_names is not None:
            assert K_factors is not None
            assert len(mutual_inductor_names) == len(K_factors)
            self.mutual_inductor_names = mutual_inductor_names
            self.K_factors = K_factors 
        else:
            self.mutual_inductor_names = []
            self.K_factors   = []

        
        self.inductance = inductance
        self.inductor_symbol = inductor_symbol

class Capacitor(PortElement):
    def __init__(self, name, port_a, port_b, capacitance:float, capacitor_symbol:Symbol):
        super().__init__(name, port_a, port_b)
        self.capacitance = capacitance
        self.capacitor_symbol = capacitor_symbol

class NonPortElement(Element):
    def __init__(self, name:str, port_a: Node, port_b: Node):
        super().__init__(name, port_a, port_b)
        self.is_port_element = False
    def voltage_current_relationship(self,F_labels:list[str], element_name_obj_map:dict[str, Element]):
        pass
class Resistor(NonPortElement):
    
    def __init__(self, name:str, port_a: Node, port_b: Node, resistance:float, resistance_symbol:Symbol):
        super().__init__(name, port_a, port_b)
        self.resistance = resistance 
        self.resistance_symbol = resistance_symbol
    def voltage_current_relationship(self,F_labels:list[str], element_name_obj_map:dict[str, Element]):
        # find index of 
        v_ind = F_labels.index(self.element_voltage_name)
        current_ind = F_labels.index(self.element_current_name)

        zeros = [0]*len(F_labels)
        zeros[v_ind] = 1
        zeros[current_ind] = -self.resistance_symbol
        return zeros
    
# dependent label dependents on the either output of Voltmeter or Ammeter
# voltage depedent voltage source, current dependent voltage source
class DependentElement(NonPortElement):
    def __init__(self, name, port_a, port_b, meter_name:str, dependent_factor:float, dependent_symbol:Symbol, type_str:str):
        super().__init__(name, port_a, port_b)
        self.meter_name = meter_name
        self.dependent_factor = dependent_factor    
        self.dependent_symbol = dependent_symbol
        
        if type_str == "VCVS":
            self.type = 0
        elif type_str == "VCIS":
            self.type = 1
        elif type_str == "ICVS":
            self.type = 2
        elif type_str == "ICIS":
            self.type = 3
        else:
            raise ValueError("Unknown dependent type")
        
    def voltage_current_relationship(self,F_labels:list[str], element_name_obj_map:dict[str, Element]):
        
        # find index of dependent voltage and the dependent factor
        if self.type == 0:
            # voltage dependent voltage source
            input_ele = element_name_obj_map[self.meter_name]
            assert isinstance(input_ele, Voltmeter)
            independent_source_ind = F_labels.index( input_ele.element_voltage_name )
            
            module_output_ind = F_labels.index(self.element_voltage_name)
            

        elif self.type == 1:
            # voltage dependent current source
            input_ele = element_name_obj_map[self.meter_name]
            
            assert isinstance(input_ele, Voltmeter)
            independent_source_ind = F_labels.index( input_ele.element_voltage_name)
            module_output_ind = F_labels.index(self.element_current_name)
        elif self.type == 2:
            # current dependent voltage source
            input_ele = element_name_obj_map[self.meter_name]
            assert isinstance(input_ele, Ammeter)
            independent_source_ind = F_labels.index(input_ele.element_current_name)
            module_output_ind = F_labels.index(self.element_voltage_name)
        else:
            assert self.type == 3
            # current dependent current source
            input_ele = element_name_obj_map[self.meter_name]
            assert isinstance(input_ele, Ammeter)
            independent_source_ind = F_labels.index(input_ele.element_current_name)
            module_output_ind = F_labels.index(self.element_current_name)
            
        zeros = [0] * len(F_labels)
        zeros[module_output_ind] = 1
        zeros[independent_source_ind] = -self.dependent_symbol
        return zeros
            
            
    
    





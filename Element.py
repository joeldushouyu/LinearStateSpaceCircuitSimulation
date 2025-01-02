
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
    def __init__(self, name, port_a, port_b, initial_switch_state:bool, switch_frequency:float, duty_cycle:float):
        super().__init__(name, port_a, port_b)
        self.initial_switch_state = initial_switch_state
        self.switch_frequency = switch_frequency
        self.duty_cycle = duty_cycle
class Diode(PortElement):
    def __init__(self, name, port_a, port_b, initial_switch_state:bool):
        super().__init__(name, port_a, port_b)
        self.initial_switch_state = initial_switch_state

class Inductor(PortElement):
    def __init__(self, name, port_a, port_b, inductance:float, inductor_symbol:Symbol):
        super().__init__(name, port_a, port_b)
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
    def voltage_current_relationship(self,F_labels:list[str]):
        pass
class Resistor(NonPortElement):
    
    def __init__(self, name:str, port_a: Node, port_b: Node, resistance:float, resistance_symbol:Symbol):
        super().__init__(name, port_a, port_b)
        self.resistance = resistance 
        self.resistance_symbol = resistance_symbol
    def voltage_current_relationship(self,F_labels:list[str]):
        # find index of 
        v_ind = F_labels.index(self.element_voltage_name)
        current_ind = F_labels.index(self.element_current_name)

        zeros = [0]*len(F_labels)
        zeros[v_ind] = 1
        zeros[current_ind] = -self.resistance_symbol
        return zeros
# voltage depedent voltage source, current dependent voltage source
class DependentSource(NonPortElement):
    def __init__(self, name, port_a, port_b, dependent_source:str, dependent_factor:float, is_dependent_voltage_source:bool):
        super().__init__(name, port_a, port_b)
        self.dependent_source = dependent_source
        self.dependent_factor = dependent_factor    
        self.is_dependent_voltage_source = is_dependent_voltage_source
    def voltage_current_relationship(self,F_labels:list[str]):
        pass
    
    
    





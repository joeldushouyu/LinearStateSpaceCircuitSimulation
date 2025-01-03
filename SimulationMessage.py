
import math
from typing import Tuple
from sympy import Matrix
from Element import Element
from queue import PriorityQueue


# Message for simuation
from functools import total_ordering
@total_ordering
class Message:
    
    
    def __init__(self, message_manager):
        self._observers = []
        self.message_level = 0
        self.system_time = 0
        self.message_manager = message_manager
    def __eq__(self, other):
        return self.message_level == other.message_level
    
    def __lt__(self, other):
        return self.message_level < other.message_level
    def _notify(self): 
        # only can be invoked by manager
        for observer in self._observers:

            observer.update(self)
    
    def attach(self, observer):
  
        self._observers.append(observer)
  

    def detach(self, observer):

        self._observers.remove(observer)

    
class SystemTimeMessage(Message):
    
    def __init__(self, message_manager):
        super().__init__(message_manager)
        self.message_level = 1
        
    def set_time(self, new_time:float):
        self.system_time = new_time
        # this message is notified immediately
        self.message_manager.queue_message(self)
    
    def get_time(self):
        return self.system_time

class SwitchMessage(Message):
    def __init__(self, message_manager):
        super().__init__(message_manager)
        self.message_level = 2
        self.switch_on = False
        self.switch_voltage_label = ""

    def set_switch_status(self, switch_on:bool, switch_voltage_label:str, system_time:float):
        self.switch_on = switch_on
        self.switch_voltage_label  = switch_voltage_label
        self.system_time = system_time
        self.message_manager.queue_message(self)
        
    def is_switch_on(self)->bool:
        return self.switch_on

class VoltageCurrentMessage(Message):
    def __init__(self,manager):
        super().__init__(manager)
        self.message_level = 3
        self.value = 0.0
        self.source_column_label = None  # the nonzero column label


    def set_value(self,  new_value:float, source_label:str, system_time:float):
        self.value = new_value
        self.source_column_label = source_label
        self.system_time = system_time
        self.message_manager.queue_message(self)
    



class OversamplingMessage(Message):
    def __init__(self,message_manager):
        
        super().__init__(message_manager)
        self.message_level = 3

        
        self.switch_states_map:dict[str, bool] = {}
        
    def notify_result(self, switch_state_dict:dict[str, int], switch_states:list[bool], system_time):
   
        self.system_time = system_time
        
        self.switch_states_map = {}
        for key, val in switch_state_dict.items():
            self.switch_states_map[key] = switch_states[val]
        
        self.message_manager.queue_message(self)
        # clear out all result
        
# not multithread safe yet
class MessageManager:
    def __init__(self):
        self.message_queue = PriorityQueue()
        self.message_leve_size:dict[int, int] = {}
    def queue_message(self, message: Message):
        
        if message.message_level not in self.message_leve_size.keys():
            self.message_leve_size[message.message_level] = 1
        else:
            self.message_leve_size[message.message_level] +=1
        
        self.message_queue.put( (message.message_level,  message ))
    
    def publish_message(self, message_level:int):
        #TODO: need to have lock in multithread
        if message_level not in self.message_leve_size.keys():
            return 
        for i in range(self.message_leve_size[message_level]):
            message_level, message = self.message_queue.get()
            message._notify()
            self.message_leve_size[message_level] -=1
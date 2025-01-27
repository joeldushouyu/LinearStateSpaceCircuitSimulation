from FormNetworkMatrix import system_realization, NetworkMatrix, ExternalSwitch
from SimulationMessage import MessageManager, VoltageCurrentMessage, OversamplingMessage, SwitchMessage, SystemTimeMessage
from Simulation import VoltageCurrentSimulationModule, SystemClockSimulationModule, SwitchSimulationModule, SwitchOversampleModule, StateSpaceSimulationModule
import matplotlib.pyplot as plt
import numpy as np

import cProfile

netList = [
    "Vin, N1, 0, 12, 0",
    "L1, N1, N4, 150e-6",
    "AM1, N4, N2",
    "S1, N2, 0, ON",
    "D1, N2, N3, OFF",
    "C1, N3, 0, 33.33e-6",
    "R1, N3, 0, 6",
    "VM1, N3,0",
]

netList = [
    "Vin, N1, 0, 12, 0",
    "S1, N2, 0, ON, 50e3, 0.6",
    "L1, N1, N4, 150e-6",
    "D1, N2, N3, OFF",
    "C1, N3, 0, 33.33e-6",
    "R1, N3, 0, 6",
    "VM1, N3,0",
    "AM1, N4, N2",
]
supress = False
# boost network
end_sim_t = 0.002
switch_frequency = 50e3
netList = [
    "Vin, N1, 0, 6, 0",
    f"S1, N2, 0, ON, {switch_frequency}, 0.6",  
    "L1, N1, N4, 150e-6",
    "D1, N2, NAMD1, OFF, VMD1, AMD1",
    "AMD1, NAMD1, N3",
    "VMD1, N2, NAMD1",
    "C1, N3, 0, 33.33e-6",
    "R1, N3, 0, 6",
    "VM1-VR, N3,0",
    "AM1-IL, N4, N2",

]


# buck network
end_sim_t = 0.001
netList = [
    
    "Vin, N1, 0, 12, 0",
    f"S1, N1, N2-AM, ON, {switch_frequency}, 0.5", 
    "L1, N2, NA, 125e-06",
    "D1, 0, NAMD1, OFF, VMD1, AMD1",
    "VMD1, 0, NAMD1",
    "AMD1, NAMD1, N2",
    "C1, N3, 0, 4e-06",
    "R1, N3, N3-Resistor, 2.5",
    "VM1-VR, N3, 0",
    "AM1-IL, NA, N3",
    "VM2-Vin, N1, 0",
    "AM2-MOSFET, N2-AM, N2",
    "AM3-Resistor, N3-Resistor, 0",
]



# RC filter demo
# demonstrate if Resistor in cotree-nonport case
switch_frequency = 120
end_sim_t = 0.1
netList = [
    f"Vin, N1, 0, 10, {switch_frequency}",
    "R1, N1, N2, 10",
    "C1, N2, 0, 100e-6",
    "AM1, N2, N2-R",
    "R2, N2-R, 0, 1e3",
    "VM1, N2, 0",
    
]


# # # # # full-wave rectifier circuit
# # # switch_frequency = 1000
# # # end_sim_t = 0.005
# # # netList = [
    
# # #     "Vin, N1, N4, 100, 1000",
# # #     "L1, N1, N5, 125e-6",

# # #     "D1, N2, N3, ON",
# # #     "D2, 0, N4, ON",
# # #     "D3, 0, N2, OFF",
# # #     "R1, N3, 0, 1e3",
# # #     "VM1-R1, N3, 0",
# # #     "AM1-L, N5, N2",
# # #     "D4, N4, N3, OFF",
# # # ]

# # simplified half-bridge, capactiro,resistor parallel circuit
switch_frequency = 1000
end_sim_t = 0.005
netList = [
    
    "Vin, N1, 0, 20, 1000",
    "AM1-L, N1, Nt",
    "Rt, Nt, N2, 0.01",
    "D1, N2, NAMD1, ON, VMD1, AMD1",
    "VMD1, N2, NAMD1",
    "AMD1, NAMD1, N3",
    "D3, 0, NAMD3, OFF, VMD2, AMD2",
    "VMD2, 0, NAMD3",
    "AMD2, NAMD3, N2",
    "R1, N3, 0, 10e3",
    "C1, N3, 0, 10e-6",
    "VM1-C1, N3, 0",
    "VM2-Rt, Nt, N2",
]
supress=False



end_sim_t  = 0.1
switch_frequency = 60

# 3 winding transformer with simple resisto
netList = [
    
    f"Vin, N1, 0, 200, {switch_frequency}",
    "R1, N1, N2, 10",
    "LS0, N2, 0, 200e-6, [LS1, LS2], [0.99, 0.99]",
    "RS0, N2, 0, 100e3",
    "VM-p, N2, 0",


    "LS1, N3, 0, 400e-6, [LS0, LS2], [0.99, 0.99]",
    # "RS1, N3, 0, 1",
    "R2, N3, 0, 100e3",
    "VM-S1, N3, 0",
    
    "LS2, 0, N4, 400e-6, [LS0, LS1], [0.99, 0.99]",
    # "RS2, 0, N4, 1",
    "R3, N4, 0, 100e3",
    "VM-S2, N4, 0",

    # "RNA, NA, 0, 0.0001",

]



end_sim_t  = 0.2
switch_frequency = 60

# 2 winding transformer with RLC modeling
netList = [
    
    f"Vin, N1, 0, 200, {switch_frequency}",
    "R1, N1, N2, 1",
    "LS0, N2, 0, 200e-6, [LS1], [0.99]",

    "LS1, N3, 0, 400e-6, [LS0], [0.99]",

    "VMD1, N4, N5",
    "AMD1, N3, N4",
    "D1, N4, N5, ON, VMD1, AMD1",
    "CD1, N4, N5, 9e-9",
    "Ro, N5, N6, 10",
    "C0, N6, 0, 100e-6",
    
    "VMRC, N5, 0",
    "VMC, N6, 0",
    


]








end_sim_t  = 0.2
switch_frequency = 60

# 3 winding transformer with RLC modeling
netList = [
    
    f"Vin, N1, 0, 200, {switch_frequency}",
    "R1, N1, N2, 1",
    "LS0, N2, 0, 200e-6, [LS1, LS2], [0.99, 0.99]",
    "RS0, N2, 0, 100e3",
    "VM-p, N2, 0",


    "LS1, N3, 0, 400e-6, [LS0, LS2], [0.99, 0.99]",
    "AMD1, N3, N3AM",
    "VMD1, N3AM, N5",
    "D1, N3AM, N5, ON, VMD1, AMD1",
    "CD1, N3AM, N5, 9e-9",
    "VMLS1, N3, 0",
    


    
    "LS2, 0, N4, 400e-6, [LS0, LS1], [0.99, 0.99]",
    "AMD2, N4, N4AM",
    "VMD2, N4AM, N5",
    "D2, N4AM, N5, ON, VMD2, AMD2",
    "CD2, N4AM, N5, 9e-9",
    "VMLS2, N4, 0",
    
    "Rinternal, N5, N6, 0.001",
    "Cout, N6, 0, 100e-6",
    "Rout, N6, 0, 10e3",
    
    "VMout, N6, 0",



]




# end_sim_t  = 2e-3
# switch_frequency = 100e3
# duty_cycle = 0.5
# # HALF-bridge lswitch only
# netList = [
#     f"Vin, NSource, 0, 400, 0",
#     # "RInternal, N1, NSource, 0",
#     f"S1, NSource, NSW, ON, {switch_frequency}, {duty_cycle}",
#     f"S2, NSW, 0, OFF, {switch_frequency}, {1-duty_cycle}",
#     "Rin1, NSW, NR, 0.01",
#     "AMRIN, NR, NRIN",
#     "Cr, NRIN, NC, 24e-9",
#     "Lr, NC, 0, 60e-6",
#     "VMC, NRIN, 0",
#     "VML, NC, 0",


# ]

# supress=False
# end_sim_t  = 20e-6
# switch_frequency = 100e3
# duty_cycle = 0.5
# supress = True
# # HALF-bridge lswitch only
# netList = [
#     f"Vin, NSource, 0, 400, 0",
#     f"S1, NSource, NSW, ON, {switch_frequency}, {duty_cycle}",
#     f"S2, NSW, 0, OFF, {switch_frequency}, {1-duty_cycle}",
#     "Rin1, NSW, NR, 0.01",
    
#     "AM4, NR, NAMLR",
#     "VM5, NR, NLR",
#     "L1, NAMLR, NLR, 60e-6",

    
    
#     "AM5, NLR, NAMC",
#     "VM6, NLR, NC",
#     "C1, NAMC, NC, 24e-9",
    
#     "AM6, NAMSO, 0",
#     "LS0, NC, NAMSO, 280e-6, [LS1, LS2], [0.99, 0.99]",
#     "VM7, NC, 0",
    
#     "LS1, N3, 0, 968e-9, [LS0, LS2], [0.99, 0.99]",
#     "AM2, N3, N3AM",
#     "VM2, N3AM, N5",
#     "D1, N3AM, N5, ON, VM2, AM2",
#     # "VMLs1, N3, 0",

    
#     "LS2, 0, N4, 968e-9, [LS0, LS1], [0.99, 0.99]",
#     "AM3, N4, N4AM",
#     "VM3, N4AM, N5",
#     "D2, N4AM, N5, ON, VM3, AM3",
#     # "VMLS2, N4, 0",

#     "Rinternal, N5, N6, 0.001",
#     "C2, N6, 0, 1000e-6",
#     "Rout, N6, 0, 0.48",
#     "VM4, N6, 0",
# ]


supress=False
end_sim_t  =2e-3
switch_frequency = 100e3
duty_cycle = 0.5
supress = True
# HALF-bridge lswitch only
netList = [
    f"Vin, NSource, 0, 400, 0",
    f"S1, NSource, NSW, ON, {switch_frequency}, {duty_cycle}",
    f"S2, NSW, 0, OFF, {switch_frequency}, {1-duty_cycle}",
    "Rin1, NSW, NR, 0.01",
    
   
    "L1, NR, NLR, 60e-6",

    
    "VMC1, NLR, NC",
    "C1, NLR, NC, 24e-9",
    
    "LS0, NC, 0, 280e-6, [LS1, LS2], [0.99, 0.99]",
    "VMp, NC, 0",
    
    "LS1, N3, 0, 968e-9, [LS0, LS2], [0.99, 0.99]",
    "AMD1, N3, N3AM",
    "VMD1, N3AM, N5",
    "D1, N3AM, N5, ON, VMD1, AMD1",
    "VMS1, N3, 0",

    
    "LS2, 0, N4, 968e-9, [LS0, LS1], [0.99, 0.99]",
    "AMD2, N4, N4AM",
    "VMD2, N4AM, N5",
    "D2, N4AM, N5, ON, VMD2, AMD2",
    "VMS2, N4, 0",

    "Rinternal, N5, N6, 0.001",
    "C2, N6, 0, 1000e-6",
    "Rout, N6, 0, 0.48",
    "VMout, N6, 0",
]



network_matrix = system_realization(netList,supress)












message_manager = MessageManager()


# system_time_messages
system_time_messages = SystemTimeMessage(message_manager=message_manager)

# each switch has its own switch_message
external_switch_messages =[  SwitchMessage(message_manager=message_manager) for _ in range(len(network_matrix.external_switch_labels)) ]

# each voltage/current source has its own message
voltage_current_message_list  =[ VoltageCurrentMessage(manager=message_manager) for _ in range(len(network_matrix.u_labels))]

# one oversampling message
switch_oversample_message = OversamplingMessage(message_manager=message_manager)






# okay, now create each individual simulation modules

iteration_frequency =  max(1e6, switch_frequency*50)
state_space_module = StateSpaceSimulationModule(network_matrix=network_matrix, iteration_frequency= iteration_frequency) #TODO: change later
oversample_module =SwitchOversampleModule( network_matrix=network_matrix, sample_frequency=iteration_frequency, oversample_message=switch_oversample_message)

voltage_current_modules:list[VoltageCurrentSimulationModule] = [  ]

for i in range(len(network_matrix.u_labels)):
    u_lab = network_matrix.u_labels[i]    
    ele = network_matrix.m_column_labels_to_obj_map[u_lab]
    
    source_message = voltage_current_message_list[i]
    mod = VoltageCurrentSimulationModule(ele, source_message )
    voltage_current_modules.append(mod)

    
    


external_switch_modules:list[SwitchSimulationModule] = []
for i in range(len(network_matrix.external_switch_labels)):
    s_lab = network_matrix.external_switch_labels[i]
    ele = network_matrix.m_column_labels_to_obj_map[s_lab]
    
    switch_message = external_switch_messages[i]
    if isinstance(ele, ExternalSwitch):
        external_switch_modules.append( SwitchSimulationModule(ele, switch_message) )


system_clock = iteration_frequency*1
system_clock_module = SystemClockSimulationModule(system_clock, system_time_messages)


# now all all observers to the correspodning message
system_time_messages.attach(oversample_module)
system_time_messages.attach(state_space_module)
[   system_time_messages.attach(mod) for mod in voltage_current_modules ]
[ system_time_messages.attach(mod) for mod in external_switch_modules ]

[   mod.switch_message.attach(oversample_module)  for mod in external_switch_modules ]


[   mod.voltage_current_source_message.attach(state_space_module) for mod in voltage_current_modules ]
oversample_module.oversample_message.attach(state_space_module)


system_clock_module.update_list_of_node_module(   [state_space_module, oversample_module]  + voltage_current_modules + external_switch_modules)

system_clock_module.start_simuation(end_sim_t)




# state_space_module.plot_switch_graph()
state_space_module.plot_output_graph( )


from FormNetworkMatrix import system_realization, NetworkMatrix, ExternalSwitch
from SimulationMessage import MessageManager, VoltageCurrentMessage, OversamplingMessage, SwitchMessage, SystemTimeMessage
from Simulation import VoltageCurrentSimulationModule, SystemClockSimulationModule, SwitchSimulationModule, SwitchOversampleModule, StateSpaceSimulationModule
from util import swapTwoColumn, retrieveSystemMatrix, determine_dependent_state_vars,parameter_for_two_wind_transformer,parameter_for_two_wind_from_book
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

# boost network
end_sim_t = 0.005
switch_frequency = 50e3
netList = [
    "Vin, N1, 0, 6, 0",
    f"S1, N2, 0, ON, {switch_frequency}, 0.6",  #note, the switch frequency is 10 hz only
    "L1, N1, N4, 150e-6",
    "D1, N2, N3, OFF",
    "C1, N3, 0, 33.33e-6",
    "R1, N3, 0, 6",
    "VM1-VR, N3,0",
    "AM1-IR, N4, N2",
]


# buck network
end_sim_t = 0.001
netList = [
    
    "Vin, N1, 0, 12, 0",
    f"S1, N1, N2-AM, ON, {switch_frequency}, 0.5",  #note, the switch frequency is 10 hz only
    "L1, N2, NA, 125e-06",
    "D1, 0, N2, OFF",
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

netList = [
    f"Vin, N1, 0, 10, {switch_frequency}",
    "R1, N1, N2, 10",
    "C1, N2, 0, 100e-6",
    "AM1, N2, N2-R",
    "R2, N2-R, 0, 1e3",
    "VM1, N2, 0",
    
]


# # full-wave rectifier circuit
switch_frequency = 1000
end_sim_t = 0.005
netList = [
    
    "Vin, N1, N4, 100, 1000",
    "L1, N1, N5, 125e-6",

    "D1, N2, N3, ON",
    "D2, 0, N4, ON",
    "D3, 0, N2, OFF",
    "R1, N3, 0, 1e3",
    "VM1-R1, N3, 0",
    "AM1-L, N5, N2",
    "D4, N4, N3, OFF",
]
switch_frequency = 1000
end_sim_t = 0.005
# simplified half-bridge, capactiro,resistor parallel circuit
netList = [
    
    "Vin, N1, 0, 20, 1000",
    "AM1-L, N1, Nt",
    "Rt, Nt, N2, 0.01",
    "D1, N2, N3, ON",
    "D3, 0, N2, OFF",
    "R1, N3, 0, 10e3",
    "C1, N3, 0, 10e-6",
    "VM1-R1, N3, 0",
    "VM2-R1, Nt, N2",
]




# basic transformer
switch_frequency = 60
end_sim_t = 0.1
netList = [
    
    f"Vin, N1, 0, 40, {switch_frequency}",
    "R1, N1, N2, 10",
    "Lp, N2, 0, 400e-6, [Ls], [0.99]",
    "Ls, N3, 0, 800e-6, [Lp], [0.99]",  # note the current direction of LS
    "AMs, N3, N4",
    "Ro, N4, 0, 1e3",
    "VMout, N4, 0",
]







network_matrix = system_realization(netList)
# swapTwoColumn(network_matrix.M, network_matrix.m_column_labels, network_matrix.m_column_labels_to_obj_map, network_matrix.s_labels[0])
# swapTwoColumn(network_matrix.M, network_matrix.m_column_labels, network_matrix.m_column_labels_to_obj_map, network_matrix.s_labels[1])
# swapTwoColumn(network_matrix.M, network_matrix.m_column_labels, network_matrix.m_column_labels_to_obj_map, network_matrix.s_labels[0])
# network_matrix.M, pivots = network_matrix.M.rref()

# S_dxdt, Sx, Su, C1, C, D, M0, A, B = retrieveSystemMatrix(network_matrix.M, network_matrix.s_labels,
#                                                           network_matrix.y_labels, network_matrix.x_hat_labels,
#                                                           network_matrix.x_labels, network_matrix.y_zero_labels,
#                                                           network_matrix.s_zero_labels)


# Add_inv, Adi, Bd = determine_dependent_state_vars(M0=M0,  A=A, B=B,x_hat_labels=network_matrix.x_hat_labels)










# now, do some testing with 






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

iteration_frequency =  switch_frequency*25 
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

# fig1.show()

# plt.show()



# cProfile.run('system_clock_module.start_simuation(0.002)'  )

# time_t_np_array = np.array(state_space_module.time_t)
# u_output_np_array = np.array(state_space_module.u_output)[:,:,0]
# switch_output_np_array = np.array(state_space_module.switch_state_output)
# switch_trigger_np_array = np.array(state_space_module.switch_triggered_output)

# y_output_np_array = np.array(state_space_module.y_output).squeeze()


# plt.figure(1)
# plt.subplot(211)
# plt.plot(time_t_np_array, u_output_np_array)
# plt.subplot(212)
# plt.plot(time_t_np_array, switch_output_np_array)
# plt.plot(time_t_np_array, switch_trigger_np_array)
# plt.grid()
# plt.show()

# plt.figure(2)
# for col in range(y_output_np_array.shape[1]):  # Plot each column
#     plt.plot(time_t_np_array, y_output_np_array[:, col], label=f"Output {col}")
# plt.grid()
# plt.show()


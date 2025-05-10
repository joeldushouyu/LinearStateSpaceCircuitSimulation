from FormNetworkMatrix import system_realization, NetworkMatrix, ExternalSwitch
from SimulationMessage import MessageManager, VoltageCurrentMessage, OversamplingMessage, SwitchMessage, SystemTimeMessage
from Simulation import VoltageCurrentSimulationModule, SystemClockSimulationModule, SwitchSimulationModule, SwitchOversampleModule, StateSpaceSimulationModule
import matplotlib.pyplot as plt
import numpy as np
from visualize_data import plot_csv_ncolumns
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
    f"S1, N2, 0, ON, {switch_frequency}, 0.6, 0.0",  
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
    "Rin, N1, N1r, 0.001", # constraint of no C-E loop or I-J cutset 
    f"S1, N1r, N2-AM, ON, {switch_frequency}, 0.8, 0.0", 
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



# # simplified half-bridge, capactiro,resistor parallel circuit
switch_frequency = 1000
end_sim_t = 0.01
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
supress = True
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







supress = True
end_sim_t  = 0.5
switch_frequency = 60
# use backward euler for unstable system
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




end_sim_t  = 2e-3
switch_frequency = 100e3
duty_cycle = 0.5
# HALF-bridge lswitch only
netList = [
    f"Vin, NSource, 0, 400, 0",
    f"S1, NSource, NSW, ON, {switch_frequency}, {duty_cycle}, 0.0",
    "VMS1, NSource, NSW",
    f"S2, NSW, 0, OFF, {switch_frequency}, {1-duty_cycle}, 0.0",
    "VMS2, NSW, 0",
    "Rin1, NSW, NR, 0.01",
    "AMRIN, NR, NRIN",
    "Cr, NRIN, NC, 24e-9",
    "Lr, NC, 0, 60e-6",
    "VMC, NRIN, 0",
    "VML, NC, 0",


]




# # # full-wave rectifier circuit
# switch_frequency = 1000
# end_sim_t = 0.005
# # unstable system, so use backward euler 
# netList = [
    
#     "Vin, N1, N1_neg, 20, 1000",
#     "AM1-source, N1, Nt",
#     "Rt, Nt, N2, 0.01",
#     "D1, N2, NAMD1, ON, VMD1, AMD1",
#     "VMD1, N2, NAMD1",
#     "AMD1, NAMD1, N3",
    
#     "D4, N1_neg, NAMD4, OFF, VMD4, AMD4",
#     "AMD4, NAMD4, N3",
#     "VMD4, N1_neg, NAMD4 ",
    
#     "D3, 0, NAMD3, OFF, VMD3, AMD3",
#     "VMD3, 0, NAMD3",
#     "AMD3, NAMD3, N2",
    
#     "D2, 0, NAMD2, ON, VMD2, AMD2",
#     "AMD2, NAMD2, N1_neg",
#     "VMD2, 0, NAMD2 ",
    
#     "R1, N3, 0, 100",
#     "C1, N3, 0, 10e-6",
#     "VM1-C1, N3, 0",
#     # "VM2-Rt, Nt, N2",
# ]






def simulation_main(netList:list[str], end_sim_t:float,  data_output_filename:str,   switch_frequency:float,  iteration_frequency=None, cache_file=None):

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
    if iteration_frequency is None:
        iteration_frequency =  max(10e3, switch_frequency*20)
    state_space_module = StateSpaceSimulationModule(network_matrix=network_matrix, iteration_frequency= iteration_frequency) #TODO: change later
    oversample_module =SwitchOversampleModule( network_matrix=network_matrix, sample_frequency=iteration_frequency, oversample_message=switch_oversample_message)

    voltage_current_modules:list[VoltageCurrentSimulationModule] = [  ]

    for i in range(len(network_matrix.u_labels)):
        u_lab = network_matrix.u_labels[i]    
        ele = network_matrix.m_column_labels_to_obj_map[u_lab]
        
        source_message = voltage_current_message_list[i]
        mod = VoltageCurrentSimulationModule(ele, source_message )
        voltage_current_modules.append(mod)

        
        
    system_clock = iteration_frequency*1

    external_switch_modules:list[SwitchSimulationModule] = []
    for i in range(len(network_matrix.external_switch_labels)):
        s_lab = network_matrix.external_switch_labels[i]
        ele = network_matrix.m_column_labels_to_obj_map[s_lab]
        
        switch_message = external_switch_messages[i]
        if isinstance(ele, ExternalSwitch):
            external_switch_modules.append( SwitchSimulationModule(ele, switch_message, system_clock_frequency=system_clock) )



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
    state_space_module.cache_file = cache_file
    step_size = system_clock_module.start_simuation(end_sim_t)

    state_space_module.plot_output_graph(outputfile_name= data_output_filename )
    state_space_module.save_iterative_matrix_to_file("Metadata.h5", end_simulation_time=end_sim_t, iteration_step_number=step_size)



# simulation_main(netList, end_sim_t, "csv_data/Half-bridge-llc.csv", switch_frequency, switch_frequency*20 )

# state_space_module.plot_switch_graph()

# state_space_module.plot_output_graph(outputfile_name= "full-bridge-llc.csv" )
# state_space_module.plot_output_graph(outputfile_name= "csv_data/full-bridge-llc-x30.csv" )
# state_space_module.save_diode_debug_info_to_csv("csv_data/diode_switch_at_x30.csv")
# state_space_module.plot_output_graph(outputfile_name= "csv_data/Half-bridge-llc.csv" )
# state_space_module.plot_output_graph(outputfile_name= "Half-bridge-llc-x30-parallel.csv" )
# state_space_module.plot_output_graph(outputfile_name= "Half-bridge-llc-x70.csv" )
# state_space_module.plot_output_graph(outputfile_name= "Half-bridge-llc-x100.csv" )


def boost():
    
    # boost network
    end_sim_t = 0.002
    switch_frequency = 50e3
    netList = [
        "Vin, N1, 0, 6, 0",
        f"S1, N2, 0, ON, {switch_frequency}, 0.6, 0.0",  
        "L1, N1, N4, 150e-6",
        "D1, N2, NAMD1, OFF, VMD1, AMD1",
        "AMD1, NAMD1, N3",
        "VMD1, N2, NAMD1",
        "C1, N3, 0, 33.33e-6",
        "R1, N3, 0, 6",
        "VM1-VR, N3,0",
        "AM1-IL, N4, N2",

    ]
    sim_20 = "csv_data/boost20.csv"
    simulation_main(netList, end_sim_t, sim_20, switch_frequency, switch_frequency*20 )
    
    
def buck():
    # buck network
    end_sim_t = 0.001
    switch_frequency = 50e3
    netList = [
        
        "Vin, N1, 0, 12, 0",
        "Rin, N1, N1r, 0.001", # constraint of no C-E loop or I-J cutset 
        f"S1, N1r, N2-AM, ON, {switch_frequency}, 0.8, 0.0", 
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
    sim_20 = "csv_data/buck20.csv"
    simulation_main(netList, end_sim_t, sim_20, switch_frequency, switch_frequency*20 )
def half_brodge_llc():
    supress=False
    end_sim_t  =4e-3
    switch_frequency = 100e3
    duty_cycle = 0.5
    supress = True
    # HALF-bridge lswitch only
    netList = [
        f"Vin, NSource, 0, 1000, 0",
        f"S1, NSource, NSW, ON, {switch_frequency}, {duty_cycle}, 0.0",
        "VMSw1, NSource, NSW",
        f"S2, NSW, 0, OFF, {switch_frequency}, {duty_cycle}, 0.0",
        "VMSw2, NSW, 0",
        "AML1, NSW, NR",
        
        "L1, NR, NLR, 60e-6",
        "VML1, NR, NLR",
        
        "VMC1, NLR, NC",
        "C1, NLR, NC, 24e-9",
        
        "LS0, NC, 0, 280e-6, [LS1, LS2], [0.99, 0.99]",
        "VMp, NC, 0",
        
        "LS1, N3, 0, 968e-9, [LS0, LS2], [0.99, 0.99]",
        "AMD1, N3, N3AM",
        "VMD1, N3AM, N5",
        "D1, N3AM, N5, OFF, VMD1, AMD1",
        # "CD1, N3AM, N5, 9e-9",
        "VMS1, N3, 0",

        
        "LS2, 0, N4, 968e-9, [LS0, LS1], [0.99, 0.99]",
        "AMD2, N4, N4AM",
        "VMD2, N4AM, N5",
        "D2, N4AM, N5, OFF, VMD2, AMD2",
        # "CD2, N4AM, N5, 9e-9",
        "VMS2, N4, 0",

        "AMIout, N5, N6",
        "C2, N6, 0, 1000e-6",
        "Rout, N6, 0, 0.48",
        "VMout, N6, 0",
    ]
    sim_20 = "csv_data/Half-bridge-llcx20.csv"
    
    plec_x20 = "csv_data/half-bridge-llc-plec-x20.csv"
    plec_x30 = "csv_data/half-bridge-llc-plec-x30.csv"
    
    plec_hil_x20 = "csv_data/half-bridge-llc-plec-hilx20.csv"
    plec_hil_x30 = "csv_data/half-bridge-llc-plec-hilx30.csv"
    simulation_main(netList, end_sim_t, sim_20, switch_frequency, switch_frequency*20 )

    
    # define the mappings for it
    x_cols  = [0,0,0]
    
    y_labels:dict[str, list[int]]= {
    "Vmout": [14, 1, 2],
    "Vp": [9, 2, 7],
    "Vs1": [11, 3, 8],
    "Vs2": [13, 4, 9],
    "VD1": [10, 5, 10],
    "VD2": [12, 6, 11],
    "AM_D1": [2, 7, 12],
    "AM_D2": [3, 8, 13],
    "AML1": [1, 10, 14],
    "VC1": [8, 9, 6],
    "VL1": [7, 14, 5],
    "Vsw1": [5, 12, 3],
    "Vsw2": [6, 13, 4],
    "AMI0": [4, 11, 1]
    }

    for lab, index_list in y_labels.items():
        
        plot_csv_ncolumns( csv_files=[sim_20,plec_x20, plec_hil_x20],
                        x_cols= [0,0,0],
                        y_cols= index_list,
                        labels= ["python", "plec", "plec_hil"],
                        y_label= lab
                        )


def full_bridge_llc():
    
    
    
    # # the system modelin is unstable, require x250 iteration. Thus do some simplification
    # end_sim_t  = 1e-3
    # switch_frequency = 100e3
    # duty_cycle = 0.5
    # # Full bridge LLc circuit
    # netList = [
    #     f"Vin, NSource, 0, 600, 0",
    #     f"S1, NSource, NA, ON, {switch_frequency}, {duty_cycle}, 0.0",
    #     f"S2, NSource, NB, OFF, {switch_frequency}, {1-duty_cycle}, 0.0",
    #     f"S3, NA, 0, OFF, {switch_frequency}, {1-duty_cycle}, 0.0",
    #     f"S4, NB, 0, ON, {switch_frequency}, {duty_cycle}, 0.0",

    #     "Rr, NA, Nrr, 0.01",
    #     "Lr, Nrr, Nlr, 2e-6",
    #     # "Rlr, Nrr, Nlr, 1e-6",
    #     "Cr, Nlr, Ncr, 60e-9",
    #     "Lm, Ncr, NB, 100e-6",

    #     # "VMout, Ncr, 0"

    #     "Lp, Ncr, NB, 400e-6, [Ls], [0.99]",
    #     "RLP, Ncr, NB, 1e7",
        
        
    #     "Ls, NSA, NSB, 1e-6, [Lp], [0.99]",

    #     "D1, ND1AM, ND1D2, OFF, VMD1, AMD1",
    #     "AMD1, NSA, ND1AM",
    #     "VMD1, ND1AM, ND1D2",


        
    #     "D2, ND2AM, ND1D2, OFF, VMD2, AMD2",
    #     "AMD2, NSB, ND2AM",
    #     "VMD2, ND2AM, ND1D2",

        
    #     "D3, ND3AM, NSA, OFF, VMD3, AMD3",
    #     "AMD3, 0, ND3AM",
    #     "VMD3, ND3AM, NSA",


        
    #     "D4, ND4AM, NSB, OFF, VMD4, AMD4",
    #     "AMD4, 0, ND4AM",
    #     "VMD4, ND4AM, NSB",

    
    #     # "RINternal, ND1D2, nf, 0.0001",
    #     "C1, ND1D2, 0, 1e-3",
    #     "R1, ND1D2, 0, 0.25",
    #     "VMout, ND1D2, 0"

    # ]




    # another simplification here


    end_sim_t  = 1e-3
    switch_frequency = 100e3
    duty_cycle = 0.5
    # Full bridge LLc circuit
    netList = [
        f"Vin, NVIN, 0, 600, 0",
        "LVin, NVIN, 0, 1e-9",
        
        # for idea transformer of turning ration 1:1:1
        "VMLp, NVIN, 0",
        "ICIS-1, 0, NVIN, -1, AMS1",  # note, negative because of how we measure the current
        "ICIS-2, 0, NVIN, 1, AMS2",
        
        
        "VCVS-1, NA-AM, 0, 1, VMLp",
        "LVCVCS-1, NA-AM, 0, 1e-9",
        "AMS1, NA-AM, NSource",
        f"S1, NSource, NA, ON, {switch_frequency}, {duty_cycle}, 0.0",


        "VCVS-2, 0, NA-BM, 1, VMLp",
        "LVCVS-2, 0, NA-BM, 1e-9",
        "AMS2, NA-BM, NBSource",
        f"S3, NBSource, NA, OFF, {switch_frequency}, {duty_cycle}, 0.0",


        "Rr, NA, Nrr, 0.01",
        "Lr, Nrr, Nlr, 2e-6",
        "AMLr, Nlr, NlrAM",
        "Cr, NlrAM, Ncr, 60e-9",
        "VMCr, NlrAM, Ncr",
        "Lm, 0, Ncr, 100e-6",

        
        "LS0, Ncr, 0, 400e-6, [LS1, LS2], [0.99, 0.99]",
        
        "LS1, N3, 0, 1e-6, [LS0, LS2], [0.99, 0.99]",
        "AMD1, N3, N3AM",
        "VMD1, N3AM, ND1D2",
        "D1, N3AM, ND1D2, OFF, VMD1, AMD1",
        #CD1, N3AM, ND1D2, 1e-9",  #TODO: add capacitor for better numerical stability?
        # "RCD1, N3AM, ND1D2, 100e3",
        # # "VMS1, N3, 0",

        
        "LS2, 0, N4, 1e-6, [LS0, LS1], [0.99, 0.99]",
        "AMD2, N4, N4AM",
        "VMD2, N4AM, ND1D2",
        "D2, N4AM, ND1D2, OFF, VMD2, AMD2",
        "CD2, N4AM, ND1D2, 1e-9",
        # "RCD2, N4AM, ND1D2, 100e3",
        # # "VMS2, N4, 0",
    
        # "RINternal, ND1D2, nf, 0.0001",

        "C1, ND1D2, 0, 1e-3",
        "AMOut, ND1D2, Nout",
        "R1, Nout, 0, 0.25",
        "VMout, Nout, 0"

    ]
    # sim_20  = "csv_data/Full-bridge-simplfied-llcx20.csv" # apply simplfiy technique from DSPACE 
    # plec_20 = "csv_data/full-bridge-llc-plecx20.csv"
    # plec_hil_20="csv_data/full-bridge-llc-plec-hilx20.csv"
    # simulation_main(netList, end_sim_t, sim_20, switch_frequency, switch_frequency*20 )
    
    # y_labels:dict[str, list[int]]= {

    #     "Vmout": [11, 1, 7],
    #     "AMLr": [3, 11, 2],
    #     "AMIo": [6, 12, 12],
    #     "Vc": [8, 10, 1]
    # }
    
    # for lab, index_list in y_labels.items():
        
    #     plot_csv_ncolumns( csv_files=[sim_20,plec_20, plec_hil_20],
    #                     x_cols= [0,0,0],
    #                     y_cols= index_list,
    #                     labels= ["python", "plec", "plec_hil"],
    #                     y_label= lab
    #                     )

    sim_40  = "csv_data/Full-bridge-simplfied-llcx40.csv" # apply simplfiy technique from DSPACE 
    plec_30 = "csv_data/full-bridge-llc-plecx30.csv"
    plec_hil_30="csv_data/full-bridge-llc-plec-hilx30.csv"
    simulation_main(netList, end_sim_t, sim_40, switch_frequency, switch_frequency*40 )
    
    y_labels:dict[str, list[int]]= {

        "Vmout": [11, 1, 7],
        "AMLr": [3, 11, 2],
        "AMIo": [6, 12, 12],
        "Vc": [8, 10, 1]
    }
    
    for lab, index_list in y_labels.items():
        
        plot_csv_ncolumns( csv_files=[sim_40,plec_30, plec_hil_30],
                        x_cols= [0,0,0],
                        y_cols= index_list,
                        labels= ["python", "plec", "plec_hil"],
                        y_label= lab
                        )



def boost_pfc_half_bridge_llc():
    switch_frequency = 50e3
    duty_cycle = 0.5
    end_sim_t = 0.3
    netList = [
        "VAC, Nsource, 0, 156, 50",
        "Rvac, Nsource, Nrs_lf, 100",
        "Lf, Nrs_lf, Nlf_cf, 330e-6",
        "Cf, Nlf_cf, 0, 3e-6",
        "VMCF, Nlf_cf, 0",
        # diode A
        "AMDpa, Nlf_cf, NDpa_a",
        "VMDpa, NDpa_a, ND_lp",
        # "CDpa, NDpa_a, ND_lp, 9e-12",
        "Dpa, NDpa_a, ND_lp, OFF, VMDpa, AMDpa",
        
        #diode B
        "AMDpb, NDd_b, NDpb_a",
        "VMDpb, NDpb_a, 0",
        # "CDpb, NDpb_a, 0, 9e-12",        
        "Dpb, NDpb_a, 0, OFF, VMDpb, AMDpb",
        
        #Diode C
        "AMDpc, 0, NDpc_a",
        "VMDpc, NDpc_a, ND_lp",
        # "CDpc, NDpc_a, ND_lp, 9e-12",          
        "Dpc, NDpc_a, ND_lp, OFF, VMDpc, AMDpc",
        
        #Diode D
        "AMDpd, NDd_b, NDpd_a",
        "VMDpd, NDpd_a, Nlf_cf",
        # "CDpd, NDpd_a, Nlf_cf, 9e-12",        
        "Dpd, NDpd_a, Nlf_cf, OFF, VMDpd, AMDpd",
        
        "Lp1, ND_lp, NDP1_a, 90e-6",
        "Lp2, ND_lp, NDP2_a, 90e-6",
        
        # S1 and S2
        f"S1, NDP1_a, NDd_b, ON, {switch_frequency}, {duty_cycle}, 0.0",
        # "CS1, NDP1_a, NDd_b, 1e-6",
        f"S2, NDP2_a, NDd_b, OFF, {switch_frequency}, {duty_cycle}, 0.0",
        # "CS2, NDP2_a, NDd_b, 1e-6",
        #Dp1
        "AMDP1, NDP1_a, NDP1_n",
        "VMDP1, NDP1_n, NCP1",
        "DP1, NDP1_n, NCP1, OFF, VMDP1, AMDP1",
        # "CDP1, NDP1_n, NCP1, 9e-12",  #TODO: do it for all>
        #Dp2
        "AMDP2, NDP2_a, NDP2_n",
        "VMDP2, NDP2_n, NCP1",
        "DP2, NDP2_n, NCP1, OFF, VMDP2, AMDP2",
        # "CDP2, NDP2_n, NCP1, 9e-12",
        
        "CP1, NCP1, NDd_b, 880e-6",
        # "RCp1, NCP1, NDd_b, 100",
        "VMCP1, NCP1, NDd_b",

        f"S3, NCP1, NS3_S4,  ON, {switch_frequency}, {duty_cycle}, 0.0",
        # "CS3, NCP1, NS3_S4, 1e-6",
        f"S4, NS3_S4, NDd_b, OFF, {switch_frequency}, {duty_cycle}, 0.0",
        # "CS4, NS3_S4, NDd_b, 1e-6",
        "Lr, NS3_S4, Nlr_cr, 74e-6",
        "Cr, Nlr_cr, Nlmr1, 169e-9",
        "Lmr1, Nlmr1, NDd_b, 400e-6, [Lmr2, Lmr3], [0.99, 0.99]",

        "Lmr2, NLmr2, 0, 200e-6, [Lmr1, Lmr3], [0.99, 0.99]",
        "AMDsa, NLmr2, NDSA_N",
        "VMDsa, NDSA_N, NDSA_SB",
        "DSa, NDSA_N, NDSA_SB, OFF, VMDsa, AMDsa",
        "CDSA, NDSA_N, NDSA_SB, 12e-9",  # Add for numerical stability of final result
        
        "Lmr3, 0, NLmr3, 200e-6, [Lmr1, Lmr2], [0.99, 0.99]",
        "AMDsb, NLmr3, NDSB_N",
        "VMDsb, NDSB_N, NDSA_SB",
        "DSb, NDSB_N, NDSA_SB, OFF, VMDsb, AMDsb",
        "CDSV, NDSB_N, NDSA_SB, 12e-9",  # Add for numerical stability of final result
        
        "Routput, NDSA_SB, NCs1, 1",
        "Cs1, NCs1, 0, 40e-6",
        "Rcs1, NCs1, 0, 10",
        "VMout, NCs1, 0",
        

        # f"S3, NCP1, NSW, ON, {switch_frequency}, {duty_cycle}, 0.0",
        # f"S4, NSW, NDd_b, OFF, {switch_frequency}, {duty_cycle}, 0.0",

        # "AML1, NSW, NR",
        
        # "Lr, NR, NLR, 74e-6",
        # "Cr, NLR, NC, 169e-9",
        
        # "LS0, NC, NDd_b, 400e-6, [LS1, LS2], [0.99, 0.99]",
        # "VMp, NC, NDd_b",
        
        # "LS1, N3, 0, 200e-6, [LS0, LS2], [0.99, 0.99]",
        # "AMDsa, N3, N3AM",
        # "VMDsa, N3AM, N5",
        # "DSa, N3AM, N5, OFF, VMDsa, AMDsa",
        # "CD1, N3AM, N5, 9e-9",
        # "VMS1, N3, 0",

        
        # "LS2, 0, N4, 200e-6, [LS0, LS1], [0.99, 0.99]",
        # "AMDsb, N4, N4AM",
        # "VMDsb, N4AM, N5",
        # "DSb, N4AM, N5, OFF, VMDsb, AMDsb",
        # "CD2, N4AM, N5, 9e-9",
        # "VMS2, N4, 0",


        # "Routput, N5, N6, 1",
        # "C2, N6, 0, 40e-6",
        # "Rout, N6, 0, 10",
        # "VMout, N6, 0",
        
            
    ]    
    
    sim_20 = "csv_data/Boost_Half_Bridge_LLC.csv"
    # cache_file = "./LinearStateSpaceCircuitSimulation/Metadata.h5_cache"
    cache_file = "Metadata_boost_pfc_with_diode_02.h5"
    # cache_file = None
    simulation_main(netList, end_sim_t, sim_20, switch_frequency, switch_frequency*20, cache_file )
    
boost_pfc_half_bridge_llc()
# buck()    
# boost()
#half_brodge_llc()
# full_bridge_llc()
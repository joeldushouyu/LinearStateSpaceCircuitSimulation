from FormNetworkMatrix import system_realization, NetworkMatrix, ExternalSwitch
from SimulationMessage import MessageManager, VoltageCurrentMessage, OversamplingMessage, SwitchMessage, SystemTimeMessage
from Simulation import VoltageCurrentSimulationModule, SystemClockSimulationModule, SwitchSimulationModule, SwitchOversampleModule, StateSpaceSimulationModule
from util import swapTwoColumn, retrieveSystemMatrix, determine_dependent_state_vars,parameter_for_three_wind_transformer
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
end_sim_t = 0.002
switch_frequency = 50e3
netList = [
    "Vin, N1, 0, 6, 0",
    f"S1, N2, 0, ON, {switch_frequency}, 0.6",  #note, the switch frequency is 10 hz only
    "L1, N1, N4, 150e-6",
    "D1, N2, N3, OFF",
    "C1, N3, 0, 33.33e-6",
    "R1, N3, R1-A, 6",
    "VM1-VR, N3,0",
    "AM1-IL, N4, N2",
    "AM-IR, R1-A, 0",
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
    "VM1-C1, N3, 0",
    "VM2-Rt, Nt, N2",
]




# # basic transformer
# switch_frequency = 60
# end_sim_t = 0.1
# netList = [
    
#     f"Vin, N1, 0, 200, {switch_frequency}",
#     "R1, N1, N2, 10",
#     "Lp, N2, 0, 200e-6, [Ls], [0.99]",
#     "VMp, N2, 0",
#     "Ls, N3, 0, 400e-6, [Lp], [0.99]",  # note the current direction of LS
#     "AMs, N3, N4",
#     "Ro, N4, 0, 1e3",
#     "VMout, N4, 0",
    

# ]

# # basic transformer, model with dependent source



# basic transformer
switch_frequency = 60
end_sim_t = 0.1
netList = [
    
    f"Vin, N1, 0, 240, {switch_frequency}",
    "R1, N1, N2, 10",
    "L2, N2, 0, 400e-6",
    "ICIS-1, 0, N2, 1, AM-1",
    "VM-1, N2, 0",
    
    "VCVS-1, N3, 0, 1, VM-1",
    "L1, N3, Nam, 8.12e-6",
    "AM-1, N4, Nam",
    "R2, N4, 0, 1e3",
    "VMout, N4, 0",

]
# 3 winding transformer of with simple resistor
switch_frequency = 60
end_sim_t = 0.1
netList = [
    
    f"Vin, N1, 0, 200, {switch_frequency}",
    "R1, N1, NAM-LP, 10",
    "AM-R1, NAM-LP, N2",
    "VM-LP, N2, 0",
    "LP, N2, 0, 200e-6",
    "ICIS-1, 0, N2, -1.4, AM-L2",  # note, negative because of how we measure the current
    "ICIS-2, 0, N2, -1.4, AM-L3",
    
    
    "L2, N3, NAM-L2, 5.99e-6",
    "AM-L2, NAM-L2, N4",
    "VM-L2, N3, 0",
    "R2, N4, 0, 100e3",
    "VCVS-L1-L2, N3, NV3p, 0.7035, VM-LP",
    "VCVS-L3-L2, NV3p, 0, 0.49747,  VM-L3",
    
    "L3, N5, NAM-L3, 5.99e-6",
    "VM-L3, N5, N6",
    "AM-L3, NAM-L3, 0",
    "VCVS-L1-L3, N5, NV4p, 0.7035, VM-LP",
    "VCVS-L2-L3, NV4p, N6, 0.49747, VM-L2",
    "R3, N6, 0, 100e3",
    
    "VM-R3, N6, 0",
        

 
    
]
# 3 winding transformer of with diode modeling
switch_frequency = 60
end_sim_t = 0.2
# current_factor, VT2_factor, VT3_factor, LO_value = parameter_for_three_wind_transformer(280e-6, 968e-9, 968e-9, 0.99,0.99,0.99)
current_factor, VT2_factor, VT3_factor,LO_value = parameter_for_three_wind_transformer(200e-6, 400e-6, 400e-6, 0.99,0.99,0.99)
print(current_factor)
print(VT2_factor)
print(VT3_factor)
netList = [
    
    f"Vin, N1, 0, 200, {switch_frequency}",
    "R1, N1, NAM-LP, 1",
    "AM-R1, NAM-LP, N2",
    "VM-LP, N2, 0",
    "LP, N2, 0, 200e-6",
    f"ICIS-1, 0, N2, {str(-current_factor[0])}, AM-L2",  # note, negative because of how we measure the current
    f"ICIS-2, 0, N2, {str(-current_factor[1])}, AM-L3",
    
    
    "L2, N3, NAM-L2, 5.99e-6",
    "AM-L2, NAM-L2, N4",
    "VM-L2, N3, 0",
    f"VCVS-L1-L2, N3, NV3p, {str(VT2_factor[0])}, VM-LP",
    f"VCVS-L3-L2, NV3p, 0, {str(VT2_factor[1])},  VM-L3",
    "D1, N4, N7, ON",
    "VM-D1, N4, N7",
    
    "L3, N5, NAM-L3, 5.99e-6",
    "VM-L3, N5, N6",
    "AM-L3, NAM-L3, 0",
    f"VCVS-L1-L3, N5, NV4p, {str(VT3_factor[0])}, VM-LP",
    f"VCVS-L2-L3, NV4p, N6, {str(VT3_factor[1])}, VM-L2",
    "VM-R3, N6, 0",
    "D2, N6, N7, ON",
    "VM-D2, N6, N7",
    
    "Rinternal, N7, N8, 0.001",
    
    "C1, N8, 0, 100e-6",
    "Ro, N8, 0, 10e3",
    "VMC, N8, 0",
]





# end_sim_t = 1e-3
# pwm_ratio = 0.5
# switch_frequency = 100e3
# netList = [
#     "Vin, NSource, 0, 400, 0",
    
#     f"S1, NSource, NSA1, ON, {switch_frequency}, {pwm_ratio}",
    
#     "AMs1, NSA1, NSW",
#     f"S2, NSW, NSA2, OFF, {switch_frequency}, {pwm_ratio}", 
#     "AMS2, NSA2, 0",  

#     "R1, NSW, NR, 0.01", 
#     "AMR, NR, NC",
#     "C1, NC, NL, 24e-6",
#     "LR, NL, 0, 60e-6",
#     "VMR, NSW, 0",
#     "VMC, NC, 0",
#     "VML, NL, 0",
# ]











# # 3 winding transformer of with diode modeling
# switch_frequency = 60
# end_sim_t = 0.1
# # current_factor, VT2_factor, VT3_factor, LO_value = parameter_for_three_wind_transformer(280e-6, 968e-9, 968e-9, 0.99,0.99,0.99)
# current_factor, VT2_factor, VT3_factor,LO_value = parameter_for_three_wind_transformer(280e-6, 968e-9, 968e-9, 0.99,0.99,0.99)
# print(current_factor)
# print(VT2_factor)
# print(VT3_factor)
# netList = [
    
#     f"Vin, N1, 0, 400, {switch_frequency}",
#     "R1, N1, NAM-LP, 1",
#     "AM-R1, NAM-LP, N2",
#     "VM-LP, N2, 0",
#     "LP, N2, 0, 280e-6",
#     f"ICIS-1, 0, N2, -0.058, AM-L2",  # note, negative because of how we measure the current
#     f"ICIS-2, 0, N2, -0.058, AM-L3",
    
    
#     "L2, N3, NAM-L2, 14.495e-9",
#     "AM-L2, NAM-L2, N4",
#     "VM-L2, N3, 0",
#     f"VCVS-L1-L2, N3, NV3p, 0.029, VM-LP",
#     f"VCVS-L3-L2, NV3p, 0, 0.49747,  VM-L3",
#     "D1, N4, N7, ON",
#     "VM-D1, N4, N7",
    
#     "L3, N5, NAM-L3, 14.495e-9",
#     "VM-L3, N5, N6",
#     "AM-L3, NAM-L3, 0",
#     f"VCVS-L1-L3, N5, NV4p, 0.029, VM-LP",
#     f"VCVS-L2-L3, NV4p, N6,  0.49747, VM-L2",
#     "VM-R3, N6, 0",
#     "D2, N6, N7, ON",
#     "VM-D2, N6, N7",
    
#     "Rinternal, N7, N8, 0.001",
    
#     "C1, N8, 0, 1000e-6",
#     "Ro, N8, 0, 0.48",
#     "VMC, N8, 0",
# ]










# # llc modeling


end_sim_t = 2e-3
pwm_ratio = 0.5
switch_frequency = 100e3
# current_factor, VT2_factor, VT3_factor, LO_value = parameter_for_three_wind_transformer(280e-6, 968e-9, 968e-9, 0.99,0.99,0.99)
current_factor, VT2_factor, VT3_factor,LO_value = parameter_for_three_wind_transformer(280e-6, 968e-9, 968e-9, 0.99,0.99,0.99)
print(current_factor)
print(VT2_factor)
print(VT3_factor)
netList = [
    

    "Vin, NSource, 0, 400, 0",
    # "Rvin, NSource, NVin, 0.0001",
    f"S1, NSource, NSW, ON, {switch_frequency}, 0.5",
    # "VM-S1, NVin, NSW",
    f"S2, NSW, 0, OFF, {switch_frequency}, 0.5", 
    # "RS2, NRS2, 0, 0.0001",
    # "VM-S2, NSW, 0",
    "R1, NSW, NC, 0.001", 

    "Cr, NC, NL, 24e-9",
    "LR, NL, N2, 60e-6",
    # "R-LR, NL, N2, 1000e6",
    # "RLRR, NLRLR, N2, 0.001",

    "VM-LP, N2, 0",
    "LP, N2, 0, 280e-6",
    

    f"ICIS-1, 0, N2, -0.058, AM-L2",  # note, negative because of how we measure the current
    f"ICIS-2, 0, N2, -0.058, AM-L3",
    "R-ICIS, 0, N2, 2000e6",
    # "VM-ICSI, 0, N2",
        
    "L2, N3, NAM-L2, 14.495e-9",
    "AM-L2, NAM-L2, N4",
    "VM-L2, N3, 0",
    f"VCVS-L1-L2, N3, NV3p, 0.029, VM-LP",
    f"VCVS-L3-L2, NV3p, 0, 0.49747,  VM-L3",
    "D1, N4, N7, ON",
    "VM-D1, N4, 0",
    
    "L3, N5, NAM-L3, 14.495e-9",
    "VM-L3, N5, N6",
    "AM-L3, NAM-L3, 0",
    f"VCVS-L1-L3, N5, NV4p, 0.029, VM-LP",
    f"VCVS-L2-L3, NV4p, N6,  0.49747, VM-L2",
    "D2, N6, N7, ON",
    "VM-D2, N6, 0",
    
    "Rinternal, N7, N8, 0.001",
    
    "C1, N8, 0, 1000e-6",
    "Ro, N8, 0, 0.48",
    "VMC, N8, 0",
]





# # 3 winding transformer with simple resistor, but model secondary with ICVS
# netList = [
    
#     f"Vin, N1, 0, 200, {switch_frequency}",
#     "R1, N1, N2, 10",
#     "Lp, N2, NG, 200e-6, [LS1, LS2], [0.99, 0.99]",
#     "VM-p, N2, 0",
    
#     "LS1, N3, NG, 400e-6, [Lp, LS2], [0.99, 0.99]",
#     "RS1, N3, NLS1-AM, 1000e6",
#     "AM-S1, NLS1-AM, NG",
#     "VM-S1, N3, NG",
    
#     "LS2, NG, N4, 400e-6, [Lp, LS1], [0.99, 0.99]",
#     "RS2, N4, NLS2-AM, 1000e6",
#     "AM-S2, NLS2-AM, 0",
#     "VM-S2, N4, NG",
    
#     "ICVS-S1, N5, NG, 1000e6, AM-S1",  # ratio should be equal wi
#     "R2, N5, NG, 100e3",
#     "VM-S1-ideal, N5, NG",

    
#     "ICVS-S2, N6, NG, 1000e6, AM-S2",
#     "R3, N6, NG, 100e3",
#     "VM-S2-ideal, N6, NG",
#     "AMG, NG, 0",
    
#     "VM1-Out, N5, 0",
# ]


# # 3 winding diode-switch work with dependent source modeling.
# end_sim_t = 0.2
# netList = [
    
#     f"Vin, N1, 0, 200, {switch_frequency}",
#     "R1, N1, N2, 1",
#     "Lp, N2, NP-A, 200e-6, [LS1, LS2], [0.99, 0.99]",
#     "AMP, NP-A, NG",
#     "VM-p, N2, NG",
    
#     "LS1, N3, 0, 400e-6, [Lp, LS2], [0.99, 0.99]",
#     "RS1, N3, NLS1-AM, 1000e6",
#     "AM-S1, NLS1-AM, NG",
#     # "VM-S1, N3, 0",
    
#     "LS2, NG, N4, 400e-6, [Lp, LS1], [0.99, 0.99]",
#     "RS2, N4, NLS2-AM, 1000e6",
#     "AM-S2, NLS2-AM, NG",
#     # "VM-S2, N4, 0",
    
#     "ICVS-S1, N5, NG, 1000e6, AM-S1",  # ratio should be equal with the resistor of LS1
#     "VM-D1, N5, NG",
#     "AM-D1, N5, D1-AM",
#     "D1, D1-AM, N7, ON",
    
#     "ICVS-S2, N6, NG, 1000e6, AM-S2",
#     "VM-D2, N6, NG",
#     "AM-D2, N6, D2-AM",
#     "D2,  D2-AM, N7, OFF",
    
#     "Ro-o, N7, N8, 0.001",
#     "C1, N8, NG, 100e-6",
#     "Ro, N8, NG, 10e3",

#     "AMG, NG, 0",
    
#     "VM1-Out, N8, NG",
# ]


# # 3 winding transformer with simple resistor, but with ideal transformer modeling
# netList = [
    
#     f"Vin, N1, 0, 200, {switch_frequency}",
#     "R1, N1, N2, 10",
#     "Lp, N2, NG, 200e-6, [LS1, LS2], [0.99, 0.99]",
#     "VM-p, N2, 0",
    
#     "LS1, N3, NG, 400e-6, [Lp, LS2], [0.99, 0.99]",
#     "VCVS-1, N3, NLS1-AM, 1, VM-S1-ideal",
#     "AM-S1, NLS1-AM, NG",
#     "VM-S1, N3, NG",
    
#     "LS2, NG, N4, 400e-6, [Lp, LS1], [0.99, 0.99]",
#     "VCVS-2, N4, NLS2-AM, 1, VM-S2-ideal",
#     "AM-S2, NLS2-AM, 0",
#     "VM-S2, N4, NG",
    
#     "ICVS-S1, N5, NG, 1, AM-S1",  # ratio should be equal wi
#     "R2, N5, NG, 100e3",
#     "VM-S1-ideal, N5, NG",

    
#     "ICVS-S2, N6, NG, 2, AM-S2",
#     "R3, N6, NG, 100e3",
#     "VM-S2-ideal, N6, NG",
#     "AMG, NG, 0",
    
#     "VM1-Out, N5, 0",
# ]


# end_sim_t = 0.02
# netList = [
    
#     f"Vin, N1, 0, 200, {switch_frequency}",
#     "R1, N1, N2, 1",
#     "Lp, N2, NP-A, 200e-6, [Ls1, Ls2], [0.99, 0.99]",
#     "AMP, NP-A, NG",
#     "VM-p, N2, NG",
    
#     "Ls1, N5, NG, 400e-6, [Lp, Ls2], [0.99, 0.99]",
#     # "VM-L1, N5, NG",

    
#     "Ls2, NG, N6, 400e-6, [Lp, Ls1], [0.99, 0.99]",
#     # "VM-L2, N6, NG",
    
#     # "ICVS-S1, N5, NG, 2, AM-S1",  # ratio should be equal with the resistor of LS1
#     "VM-D1, N5, NG",
#     "AM-D1, N5, D1-AM",
#     "D1, D1-AM, N7, ON",
    
#     # "ICVS-S2, N6, NG, 2, AM-S2",
#     "VM-D2, N6, NG",
#     "AM-D2, N6, D2-AM",
#     "D2,  D2-AM, N7, ON",
    
#     "Ro-o, N7, N8, 0.001",
#     "C1, N8, NG, 100e-6",
#     "Ro, N8, NG, 10e3",
#     "AMG, NG, 0",
    
#     "VM1-Out, N8, NG",
# ]



# # break point

# # 3 winding diode-switch work with ideal transformer modeling
# end_sim_t = 0.0008
# netList = [
    
#     f"Vin, N1, 0, 200, {switch_frequency}",
#     "VM-vin, N1, 0",
#     "R1, N1, N2, 1",
#     "Lp, N2, NP-A, 200e-6, [LS1, LS2], [0.99, 0.99]",
#     "AMP, NP-A, NG",
#     "VM-p, N2, NG",
    
#     "LS1, N3, 0, 400e-6, [Lp, LS2], [0.99, 0.99]",
#     "RS1, N3, NLS1-AM, 200e6",
#     "AM-S1, NLS1-AM, NG",
#     # "VM-S1, N3, 0",
    
#     "LS2, NG, N4, 400e-6, [Lp, LS1], [0.99, 0.99]",
#     "RS2, N4, NLS2-AM, 200e6",
#     "AM-S2, NLS2-AM, NG",
#     # "VM-S2, N4, 0",
    
#     "ICVS-S1, N5, NG, 200e6, AM-S1",  # ratio should be equal with the resistor of LS1
#     "VM-D1, N5, NG",
#     "AM-D1, N5, D1-AM",
#     "D1, D1-AM, N7, OFF",
    
#     "ICVS-S2, N6, NG, 200e6, AM-S2",
#     "VM-D2, N6, NG",
#     "AM-D2, N6, D2-AM",
#     "D2,  D2-AM, N7, OFF",
    
#     "Ro-o, N7, N8, 0.001",
#     "C1, N8, NG, 10e-6",
#     "Ro, N8, NG, 1e3",

#     "AMG, NG, 0",

#     "VM1-Out, N8, NG",
# ]





# # end_sim_t = 0.1
# # netList = [
    
# #     f"Vin, N1, 0, 200, {60}",
# #     "R1, N1, N2, 1",
# #     "Lp, N2, NG, 200e-6, [LS1, LS2], [0.99, 0.99]",
# #     # "AMP, NP-A, 0",
# #     "VM-p, N2, 0",
    
# #     "LS1, N3, NG, 400e-6, [Lp, LS2], [0.99, 0.99]",
# #     # "RS1, N3, NLS1-AM, 0.1",
# #     # "AM-S1, NLS1-AM, 0",
# #     # "VM-S1, N3, 0",
    
# #     "LS2, NG, N4, 400e-6, [Lp, LS1], [0.99, 0.99]",
# #     # "RS2, N4, NLS2-AM, 0.1",
# #     # "AM-S2, NLS2-AM, 0",
# #     # "VM-S2, N4, 0",
    
# #     # "ICVS-S1, N5, 0, 2, AM-S1",  # ratio should be equal with the resistor of LS1
# #     # "VM-D1, N5, 0",
# #     # "AM-D1, N5, D1-AM",
# #     "D1, N3, N7, ON",
    
# #     # "ICVS-S2, N6, 0, 2, AM-S2",
# #     # "VM-D2, N6, 0",
# #     # "AM-D2, N6, D2-AM",
# #     "D2, N4, N7, ON",
    
# #     "Ro-o, N7, N8, 0.001",
# #     "C1, N8, NG, 100e-6",
# #     "Ro, N8, NG, 10e3",

# #     "RGround, NG, 0, 0.00001",
    
# #     "VM1-Out, N8, 0",
# # ]







# # 3 winding diode-switch work with  Voltagedependent source modeling But no "NG" node
# end_sim_t = 0.1
# netList = [
    
#     f"Vin, N1, 0, 200, {switch_frequency}",
#     "R1, N1, N2, 1",
#     "Lp, N2, NP-A, 200e-6, [LS1, LS2], [0.99, 0.99]",
#     "AMP, NP-A, 0",
#     "VM-p, N2, 0",
    
#     "LS1, N3, 0, 400e-6, [Lp, LS2], [0.99, 0.99]",
#     "RS1, N3, NLS1-AM, 2",
#     "AM-S1, NLS1-AM, 0",
#     "VM-S1, N3, 0",
    
#     "LS2, 0, N4, 400e-6, [Lp, LS1], [0.99, 0.99]",
#     "RS2, N4, NLS2-AM, 2",
#     "AM-S2, NLS2-AM, 0",
#     "VM-S2, N4, 0",
    
#     "VCVS-S1, N5, 0, 1, VM-S1",  # ratio should be equal with the resistor of LS1
#     "VM-D1, N5, 0",
#     "AM-D1, N5, D1-AM",
#     "D1, D1-AM, N7, ON",
    
#     "VCVS-S2, N6, 0, 1, VM-S2",
#     "VM-D2, N6, 0",
#     "AM-D2, N6, D2-AM"z
#     "D2,  D2-AM, N7, OFF",
    
#     "Ro-o, N7, N8, 0.001",
#     "C1, N8, 0, 100e-6",
#     "Ro, N8, 0, 10e3",

#     # "RGround, NG, 0, 0.00001",
    
#     "VM1-Out, N8, 0",
# ]


# # # 3 winding diode-switch work with dependent source modeling But no "NG" node
# # end_sim_t = 2e-3
# # switch_frequency = 100e3
# # netList = [
    
# #     f"Vin, N1, 0, 400, {switch_frequency}",
# #     "R1, N1, N2, 0.0001",
# #     "Lp, N2, NP-A, 280e-6, [LS1, LS2], [0.99, 0.99]",
# #     "AMP, NP-A, 0",
# #     # "VM-p, N2, 0",
    
# #     "LS1, N3, 0, 968e-9, [Lp, LS2], [0.99, 0.99]",[200e-6 2.800142853e-4 2.800142853e-4; 2.800142853e-4 400e-6 3.9600e-4; 2.800142853e-4 3.9600e-4 400e-6]
# #     "RS1, N3, NLS1-AM, 2",
# #     "AM-S1, NLS1-AM, 0",
# #     # "VM-S1, N3, 0",
    
# #     "LS2, 0, N4, 968e-9, [Lp, LS1], [0.99, 0.99]",
# #     "RS2, N4, NLS2-AM, 2",
# #     "AM-S2, NLS2-AM, 0",
# #     # "VM-S2, N4, 0",
    
# #     "ICVS-S1, N5, 0, 2, AM-S1",  # ratio should be equal with the resistor of LS1
# #     "VM-D1, N5, 0",
# #     "AM-D1, N5, D1-AM",
# #     "D1, D1-AM, N7, ON",
    
# #     "ICVS-S2, N6, 0, 2, AM-S2",        self.update_x_cur()



# # end_sim_t = 2e-3
# # pwm_ratio = 0.5
# # switch_frequency = 100e3








# end_sim_t = 2e-3
# pwm_ratio = 0.5
# switch_frequency = 100e3

# netList = [
#     "Vin, NSource, 0, 400, 0",
    
#     f"S1, NSource, NSA1, ON, {switch_frequency}, {pwm_ratio}",
    
#     "AMs1, NSA1, NSW",
#     f"S2, NSW, NSA2, OFF, {switch_frequency}, {1-pwm_ratio}", 
#     "AMS2, NSA2, 0",  

#     # "R1, NSW, NR, 0.1", 
#     "AMR, NSW, NC",
#     "Cr, NC, NL, 24e-9",
#     "LR, NL, N2, 60e-6",
#     "RLR, NL, N2, 1000e3",

#     "Lp, N2, 0, 280e-6, [LS1, LS2], [0.99, 0.99]",
#     # "AMP, NP-A, 0",
#     # "VM-p, N2, 0",
    
#     "LS1, N3, 0, 968e-9, [Lp, LS2], [0.99, 0.99]",
#     "RS1, N3, NLS1-AM, 2",
#     "AM-S1, NLS1-AM, 0",
#     # "VM-S1, N3, 0",
    
#     "LS2, 0, N4, 968e-9, [Lp, LS1], [0.99, 0.99]",
#     "RS2, N4, NLS2-AM, 2",
#     "AM-S2, NLS2-AM, 0",
#     # "VM-S2, N4, 0",
    
#     "ICVS-S1, N5, 0, 2, AM-S1",  # ratio should be equal with the resistor of LS1
#     "VM-D1, N5, 0",
#     "AM-D1, N5, D1-AM",
#     "D1, D1-AM, N7, ON",
#     "VM-D1-Across, D1-AM, N7",
    
#     "ICVS-S2, N6, 0, 2, AM-S2",
#     "VM-D2, N6, 0",
#     "AM-D2, N6, D2-AM",
#     "D2, D2-AM, N7, OFF",
#     "VM-D2-Across, D2-AM, N7",
    
#     "Ro-o, N7, N8, 0.001",
#     "C1, N8, 0, 100e-6",
#     "Ro, N8, 0, 0.58",

#     # "RGround, NG, 0, 0.00001",
    
#     "VM1-Out, N8, 0",
# ]

# end_sim_t = 1e-3
# pwm_ratio = 0.5
# switch_frequency = 100e3
# netList = [
#     "Vin, NSource, 0, 400, 0",
    
#     f"S1, NSource, NSA1, ON, {switch_frequency}, {pwm_ratio}",
    
#     "AMs1, NSA1, NSW",
#     f"S2, NSW, NSA2, OFF, {switch_frequency}, {pwm_ratio}", 
#     "AMS2, NSA2, 0",  

#     "R1, NSW, NR, 0.01", 
#     "AMR, NR, NC",
#     "C1, NC, NL, 24e-9",
#     "LR, NL, 0, 60e-6",
#     "VMR, NSW, 0",
#     "VMC, NC, 0",
#     "VML, NL, 0",
# ]














#cut point




# end_sim_t = 2e-3
# pwm_ratio = 0.5
# switch_frequency = 100e3

# netList = [
#     "Vin, NSource, 0, 400, 0",
    
#     f"S1, NSource, NSA1, ON, {switch_frequency}, {pwm_ratio}",
    
#     "AMs1, NSA1, NSW",
#     f"S2, NSW, NSA2, OFF, {switch_frequency}, {1-pwm_ratio}", 
#     "AMS2, NSA2, 0",  

#     # "R1, NSW, NR, 0.1", 
#     "AMR, NSW, NC",
#     "Cr, NC, NL, 24e-9",
#     "LR, NL, N2, 60e-6",
#     "RLR, NL, N2, 1000e3",

#     "Lp, N2, NP-A, 200e-6, [LS1, LS2], [0.99, 0.99]",
#     "AMP, NP-A, 0",
#     # "VM-p, N2, 0",
    
#     "LS1, N3, 0, 400e-6, [Lp, LS2], [0.99, 0.99]",
#     "RS1, N3, NLS1-AM, 2",
#     "AM-S1, NLS1-AM, 0",
#     "VM-S1, N3, 0",
    
#     "LS2, 0, N4, 400e-6, [Lp, LS1], [0.99, 0.99]",
#     "RS2, N4, NLS2-AM, 2",
#     "AM-S2, NLS2-AM, 0",
#     "VM-S2, N4, 0",
    
#     "VCVS-S1, N5, 0, 1, VM-S1",  # ratio should be equal with the resistor of LS1
#     "VM-D1, N5, 0",
#     "AM-D1, N5, D1-AM",
#     "D1, D1-AM, N7, OFF",
    
#     "VCVS-S2, N6, 0, 1, VM-S2",
#     "VM-D2, N6, 0",
#     "AM-D2, N6, D2-AM"
#     "D2,  D2-AM, N7, OFF",
    
#     "Ro-o, N7, N8, 0.001",
#     "C1, N8, 0, 1000e-6",
#     "Ro, N8, 0, 0.48",

#     # "RGround, NG, 0, 0.00001",
    
#     "VM1-Out, N8, 0",
# ]








switch_frequency=60
end_sim_t = 0.1

# 3 winding transformer with simple resistor, but model secondary with ICVS
netList = [
    
    f"Vin, N1, 0, 200, {switch_frequency}",
    "R1, N1, N2, 10",
    "LS0, N2, 0, 200e-6, [LS1, LS2], [0.99, 0.99]",
    "VM-p, N2, 0",

    "LS1, N3, 0, 400e-6, [LS0, LS2], [0.99, 0.99]",
    "RS1, N3, NLS1-AM, 100e3",
    "AM-S1, NLS1-AM, 0",
    "VM-S1, N3, 0",
    
    "LS2, 0, N4, 400e-6, [LS0, LS1], [0.99, 0.99]",
    "RS2, N4, NLS2-AM, 100e3",
    "AM-S2, NLS2-AM, 0",
    "VM-S2, N4, 0",
    

]


switch_frequency=60
end_sim_t = 1e-3

# 3 winding transformer with simple resistor, but model secondary with ICVS
netList = [
    
    f"Vin, N1, 0, 200, {switch_frequency}",
    "R1, N1, N2, 1",
    "LS0, N2, 0, 200e-6, [LS1, LS2], [0.99, 0.99]",
    "VM-p, N2, 0",

    "LS1, N3, 0, 400e-6, [LS0, LS2], [0.99, 0.99]",
    "D1, N3, NLS1-AM, ON",
    "VM-D1, N3, NLS1-AM",
    "AM-S1, NLS1-AM, N5",
    "VM-S1, N3, 0",
    
    "LS2, 0, N4, 400e-6, [LS0, LS1], [0.99, 0.99]",
    "D2, N4, NLS2-AM, ON",
    "VM-D2, N4, NLS2-AM",
    "AM-S2, NLS2-AM, N5",
    "VM-S2, N4, 0",
    
    "Rinternal, N5, N6, 0.001",
    "Rout, N6, 0, 10e3",
    "Cout, N6, 0, 100e-6",
    "VMcout, N6, 0",
    

    

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

iteration_frequency =  max(10e3, switch_frequency*25)
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


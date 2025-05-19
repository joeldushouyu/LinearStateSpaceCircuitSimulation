import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import argparse
import os
from typing import NamedTuple, Tuple
import math

from visualize_data import plot_csv_ncolumns




def half_brdige_llc_visualize():
    y_labels:dict[str, list[int]]= {
    "Vmout": [14, 1, 2,14,14],
    "Vp": [9, 2, 7,9,9],
    "Vs1": [11, 3, 8,11,11],
    "Vs2": [13, 4, 9,13,13],
    "VD1": [10, 5, 10,10,10],
    "VD2": [12, 6, 11,12,12],
    "AM_D1": [2, 7, 12,2,2],
    "AM_D2": [3, 8, 13,3,3],
    "AML1": [1, 10, 14,1,1],
    "VC1": [8, 9, 6,8,8],
    "VL1": [7, 14, 5,7,7],
    "Vsw1": [5, 12, 3,5,5],
    "Vsw2": [6, 13, 4,6,6],
    "AMI0": [4, 11, 1,4,4]
    }
    sim_20 = "../csv_data/Half-bridge-llcx20.csv"
    host_sim = "hostSim.csv"
    npu_sim = "npuSim.csv"
    host_naive = "hostSim_naive.csv"
    plec_x20 = "../csv_data/half-bridge-llc-plec-x20.csv"
    plec_x30 = "csv_data/half-bridge-llc-plec-x30.csv"

    plec_hil_x20 = "../csv_data/half-bridge-llc-plec-hilx20.csv"
    for lab, index_list in y_labels.items():
        
        plot_csv_ncolumns( csv_files=[sim_20,plec_x20, plec_hil_x20,host_sim,npu_sim],
                        x_cols= [0,0,0,0,0],
                        y_cols= index_list,
                        labels= ["python", "plec", "plec_hil", "c++",  "NPU_sim"],
                        y_label= lab
                        )
        
def boost_pfc_half_llc_visualize():
    
    y_labels: dict[str: list[int]] = {
  "vmcf":   [10,  1,  9, 9],
  "vmout":  [20, 11, 19, 19],  
  "amdpa":  [ 1, 18,  1, 1],
  "vmcp":   [17, 10, 16, 16],  
  "amdpb":  [ 2, 17,  2, 2],
  "amdpc":  [ 3, 16,  3, 3],
  "amdpd":  [ 4, 15,  4, 4],
  "amdp1":  [ 5, 20,  5, 5],
  "amdp2":  [ 6, 19,  6, 6],
  "amdsa":  [ 7, 14,  7, 7],
  "amdsb":  [ 8, 13,  8, 8],
  "vmdpa":  [11,  5, 10, 10],
  "vmdpb":  [12,  4, 11, 11],
  "vmdpc":  [13,  3, 12, 12],
  "vmdpd":  [14,  2, 13, 13],
  "vmdp1":  [15,  7, 14, 14],
  "vmdp2":  [16,  6, 15, 15],
  "vmdsa":  [18,  8, 17, 17],
  "vmdsb":  [19,  9, 18, 18],
}

    sim_20 = "../csv_data/Boost_Half_Bridge_LLC.csv"
    plec_x20 = "../csv_data/boost-pfc-half-llc-plecx20.csv"
    plec_hil_x20 = "../csv_data/boost-pfc-half-llc-plec-hilx20.csv"
    host_sim = "hostSim.csv"
    for lab, index_list in y_labels.items():
        
        plot_csv_ncolumns( csv_files=[plec_hil_x20,plec_x20, sim_20,host_sim],
                        x_cols= [0,0,0, 0],
                        y_cols= index_list,
                        labels= ["plec_hil", "plec", "python",  "c++-sim"],
                        y_label= lab
                        )    
        
        
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Process circuit simulation configuration.")
#     parser.add_argument("mode", help="which circuit to plot ")
#     args = parser.parse_args()
#     if args.mode == "0":
#         boost_pfc_half_llc_visualize()
#     else:
#         half_brdige_llc_visualize()

#TODO: cleanup in future

boost_pfc_half_llc_visualize()
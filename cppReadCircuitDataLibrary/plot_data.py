import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from visualize_data import plot_csv_ncolumns
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

host_naive = "hostSim_naive.csv"
plec_x20 = "../csv_data/half-bridge-llc-plec-x20.csv"
plec_x30 = "csv_data/half-bridge-llc-plec-x30.csv"

plec_hil_x20 = "../csv_data/half-bridge-llc-plec-hilx20.csv"
for lab, index_list in y_labels.items():
    
    plot_csv_ncolumns( csv_files=[sim_20,plec_x20, plec_hil_x20,host_sim,host_naive],
                    x_cols= [0,0,0,0,0],
                    y_cols= index_list,
                    labels= ["python", "plec", "plec_hil", "c++", "c++naive"],
                    y_label= lab
                    )
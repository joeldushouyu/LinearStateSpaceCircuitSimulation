

from  util import retrieveSystemMatrix, update_system_matrix_to_reflect_dependency, retrieve_Zsw_hat,assert_matrix_equal,determine_dependent_independent_state_mapping
from sympy import Matrix, symbols
import sympy as sp
from FormNetworkMatrix import Inductor, Capacitor, Element, Voltmeter, VoltageCurrentSource, Ammeter, Diode, ExternalSwitch
import numpy as np

import math





def test_retrieveSystemMatrix():

    # from the buck circut, switch on diode off
    #  Whenre there is no dependent state variable and output variable
    R1,L1,C1 = symbols("R1,L1,C1")
    m_columns = ['I_S1', 'V_D1', 'V_VM1-VR', 'V_VM2-Vin', 'I_AM1-IL', 'I_AM2-MOSFET', 'I_AM3-Resistor', 'V_L1', 'I_C1', 'I_L1', 'V_C1', 'V_S1', 'I_D1', 'I_VM1-VR', 'I_VM2-Vin', 'V_AM1-IL', 'V_AM2-MOSFET', 'V_AM3-Resistor', 'V_Vin']
    m = Matrix([
    [1, 0, 0, 0, 0, 0, 0, 0, 0,    -1,         0,    0, 1,    0, 0,    0,    0,          0,     0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0,     0,         0,   -1, 0,    0, 0,    0,   -1,          0,     1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0,     0,        -1,    0, 0,    0, 0,    0,    0,          0,     0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0,     0,         0,    0, 0,    0, 0,    0,    0,          0,    -1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0,    -1,         0,    0, 0,    0, 0,    0,    0,          0,     0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0,    -1,         0,    0, 1,    0, 0,    0,    0,          0,     0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0,     0,     -1/R1,    0, 0,    0, 0,    0,    0,       1/R1,     0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0,     0,      1/L1, 1/L1, 0,    0, 0, 1/L1, 1/L1,          0, -1/L1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, -1/C1, 1/(C1*R1),    0, 0, 1/C1, 0,    0,    0, -1/(C1*R1),     0]])

    Q_expect = sp.eye(5,5)
    M0_expect = Matrix([[1,0 ],
                        [0,1]])

    
    C1_expect = -1* Matrix([[0,0],
                        [0,0],
                        [0,0],
                        [0,0],
                        [0,0]])
    C_expect = -1*Matrix([
                [0,        -1],
                [0,         0],
                [-1,         0],
                [-1,         0],
                [0,     -1/R1]])
    D_expect = -1*Matrix([
            [0],
            [-1],
            [0],
            [0],
            [0],
    ])
    A_expect =-1* Matrix([
        [0,      1/L1],
       [-1/C1, 1/(C1*R1)]
    ])
    
    B_expect = -1*Matrix([
        [-1/L1],
        [0]
        
    ])
    m, pivots = m.rref()

    s_labels_size = 2
    s_zero_label_size = 2
    u_label_size = 1
    x_hat_label_size = 2
    x_label_size = 2
    y_label_size = 5
    y_zero_label_size = 5
    capacitor_size = 1
    inductor_size = 1

    Q, C1_m, C, D, M0, A, B,  inconsistent_labels,M_offset_info  = (
        retrieveSystemMatrix(
            M=m,
            m_pivots =  pivots,
            m_labels = m_columns,
            s_labels_size = s_labels_size,
            y_labels_size = y_label_size,
            x_hat_labels_size = x_hat_label_size,
            x_labels_size = x_label_size,
            y_zero_labels_size = y_zero_label_size,
            s_zero_labels_size = s_zero_label_size,
            capacitor_size=capacitor_size,
            inductor_size=inductor_size,
            voltage_source_size = 1,
            current_source_size= 0,
            redundant_offset=0
        )
    )

    assert C1_m.equals(C1_expect)
    assert C.equals(C_expect)
    assert D.equals(D_expect)
    assert M0.equals(M0_expect)
    assert A.equals(A_expect)
    assert B.equals(B_expect)
    assert inconsistent_labels == []
    assert_matrix_equal(Q_expect, Q)

    #TODO: check C_sw, D_sw
    m_columns = [
        "I_S1",
        "I_D1",
        "V_VM1-VR",
        "V_VM2-Vin",
        "I_AM1-IL",
        "I_AM2-MOSFET",
        "I_AM3-Resistor",
        "V_L1",
        "I_C1",
        "I_L1",
        "V_C1",
        "V_S1",
        "V_D1",
        "I_VM1-VR",
        "I_VM2-Vin",
        "V_AM1-IL",
        "V_AM2-MOSFET",
        "V_AM3-Resistor",
        "V_Vin",
    ]
    m = Matrix([
    [1, 0, 0, 0, 0, -1, 0, 0, 0,     0,         0, 0,    0,    0, 0,    0, 0,          0,  0],
    [0, 1, 0, 0, 0,  1, 0, 0, 0,    -1,         0, 0,    0,    0, 0,    0, 0,          0,  0],
    [0, 0, 1, 0, 0,  0, 0, 0, 0,     0,        -1, 0,    0,    0, 0,    0, 0,          0,  0],
    [0, 0, 0, 1, 0,  0, 0, 0, 0,     0,         0, 0,    0,    0, 0,    0, 0,          0, -1],
    [0, 0, 0, 0, 1,  0, 0, 0, 0,    -1,         0, 0,    0,    0, 0,    0, 0,          0,  0],
    [0, 0, 0, 0, 0,  0, 1, 0, 0,     0,     -1/R1, 0,    0,    0, 0,    0, 0,       1/R1,  0],
    [0, 0, 0, 0, 0,  0, 0, 1, 0,     0,      1/L1, 0, 1/L1,    0, 0, 1/L1, 0,          0,  0],
    [0, 0, 0, 0, 0,  0, 0, 0, 1, -1/C1, 1/(C1*R1), 0,    0, 1/C1, 0,    0, 0, -1/(C1*R1),  0],
    [0, 0, 0, 0, 0,  0, 0, 0, 0,     0,         0, 1,   -1,    0, 0,    0, 1,          0, -1]])
    Q_expect = Matrix([
        [1,0,0,0,0],
        [0,1,0,0,0],
        [0,0,1,0,0],
        [0,0,0,0,1]
    ])
    M0_expect = Matrix([[1,0],
                        [0,1]])

    C1_expect = -Matrix([[0,0],
                        [0,0],
                        [0,0],
                        [0,0]])
    C_expect = -Matrix([
            [0,        -1],
            [0,         0],
            [-1,         0],
            [0,     -1/R1]
        
    ])
    D_expect = -Matrix([
        [0],
        [-1],
        [0],
        [0]
    ])    
    
    A_expect = -Matrix([
        [    0,      1/L1],
        [-1/C1, 1/(C1*R1)]
    ])
    B_expect = -Matrix([
        [0],
        [0]
    ])
    m, pivots = m.rref()
    # When there is dependent y output variable, but no dependent x variable
    Q, C1_m, C, D, M0, A, B, inconsistent_labels,M_offset_info  = (
        retrieveSystemMatrix(
            M=m,
            m_pivots =  pivots,
            m_labels = m_columns,
            s_labels_size = s_labels_size,
            y_labels_size = y_label_size,
            x_hat_labels_size = x_hat_label_size,
            x_labels_size = x_label_size,
            y_zero_labels_size = y_zero_label_size,
            s_zero_labels_size = s_zero_label_size,
            capacitor_size=capacitor_size,
            inductor_size=inductor_size,
            voltage_source_size = 1,
            current_source_size= 0,
            redundant_offset=0
        )
    )
    assert C1_m.equals(C1_expect)
    assert C.equals(C_expect)
    assert D.equals(D_expect)
    assert M0.equals(M0_expect)
    assert A.equals(A_expect)
    assert B.equals(B_expect)
    assert inconsistent_labels == ["I_AM2-MOSFET"]
    assert_matrix_equal(Q_expect, Q)




def test_determine_dependent_independent_state_mapping():
    # Test to see if the problem can correclty identify the dependent/indepndent state variables
    
    
    # In the given M0, A, it exist ambiguit of which row does "D4" variable belong to.
    # Although "D4" column is nonzero in both row 3 and 5, but it should be in row 3.
    
    
    
    M0 = Matrix([
        [1,0,1,0,0,0,0,0,0,0],
        [0,1,1,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,-1,-1,0],
        [0,0,0,0,0,1,0,-1,0,0],
        [0,0,0,0,0,0,1,0,-1,0],
        [0,0,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],        
    ])
    A_raw = Matrix([
        [0,0,-0.01,0,0,0,0,0,0,-1],
        [0,0,-0.01,0,0,0,0,0,0,-1],
        [0,0,0,0,0,0,0,-1,1,0],
        [0,0,0,0,0,0,4,0,4,0],
        [0,0,0,-1,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0,0],
        [-1,-1,1,0,0,0,0,0,0,0],
        [0,0,0,0,-1,0,-1,0,-1,0],
        [0,0,0,0,0,-1,1,-1,1,0],
    ])
    
    m_pivots = [0,1,3,4,5,6,9,10,14,15]
    u_label = ["Vin"]
    y_labels = ["VM1"]
    x_hat_labels = ["V_Lm","V_Lp","V_Lr", "V_Ls", "I_C1", "I_CD1","I_CD2", "I_CD3", "I_CD4", "I_Cr"]
    x_hat_col_offset_in_m_pivots = 0
    
    
    independent_state_row_col_map,dependent_state_row_col_map,  \
            sys_A_row_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map, final_sys_A_row_idx_map, final_sys_A_col_idx_map,\
                sys_B_row_idx_map,sys_B_col_idx_map,ind_dep_B_row_idx_map,ind_dep_B_col_idx_map, final_sys_B_row_idx_map, final_sys_B_col_idx_map,\
                    sys_C_row_idx_map,sys_C_col_idx_map,ind_dep_C_row_idx_map,ind_dep_C_col_idx_map, final_sys_C_row_idx_map, final_sys_C_col_idx_map =  determine_dependent_independent_state_mapping(
                        M0_I=M0,
                        A_raw=A_raw,
                        m_pivots=m_pivots,
                        u_labels=u_label,
                        y_labels=y_labels,
                        x_hat_labels=x_hat_labels,
                        x_hat_col_offset_in_m_pivots=x_hat_col_offset_in_m_pivots
                    )

    
    independent_state_row_col_expect = {"V_Ls":[2,3], "I_Cr":[6,9],"V_Lr":[0,2], "V_Lp":[1,1], "I_CD4":[3,8], "I_CD3":[4,7], "I_CD2":[5,6]}
    dependent_state_row_col_expect = {"V_Lm":[7,0], "I_C1":[8,4], "I_CD1":[9,5]}
    
    assert independent_state_row_col_map == independent_state_row_col_expect
    assert dependent_state_row_col_expect == dependent_state_row_col_map
    


def test_retrieve_Zsw_hat_simple_case():
    #TODO: better test case of different number of capacitor/inductor current/voltage source
    # simple testcase of system with 1 inductor, 1 capacitor, 1 diode, 1 external switch, 1 Voltage source, 1 current source
    diode_am = Ammeter("AMD1", None, None)
    diode_vm = Voltmeter("VMD1", None, None)
    switch_vm = Voltmeter("VMSW", None, None)
    voltage_source = VoltageCurrentSource("Vcc", None, None, 5, 0, True)
    current_source = VoltageCurrentSource("I_in", None, None, 10, 0, False)
    inductor = Inductor("L1",None, None, 10, None)
    capacitor = Capacitor("C1", None, None, 10, None)
    # sw = ExternalSwitch("S1", None, None,True,100,0.1)
    diode = Diode("D1", None, None, False, diode_vm.name, diode_am.name)
    
    
    element_name_obj_map = { diode_am.name:diode_am, diode_vm.name:diode_vm  }
    x_hat_labels = [inductor.element_current_name, capacitor.element_voltage_name]
    u_labels = [current_source.element_current_name, voltage_source.element_voltage_name]
    y_labels = [diode_vm.element_voltage_name, diode_am.element_current_name, switch_vm.element_voltage_name]#y can be out of order
    
    # have the diode on, which need to look at the current measurement
    diode_column_label= [diode.element_current_name]
    m_column_labels_to_obj_map = {inductor.element_current_name: inductor, capacitor.element_voltage_name:capacitor,
                                  current_source.element_current_name: current_source, voltage_source.element_voltage_name:voltage_source,
                                  diode_vm.element_voltage_name:diode_vm, diode_am.element_current_name:diode_am, switch_vm.element_voltage_name:switch_vm,
                                  diode.element_current_name:diode, diode.element_voltage_name:diode
                                  
                                  }
    C1 = Matrix([
            [1,1],
            [2,2],
            [3,3]
    ])
    A = Matrix([
        [1,2],
        [3,4]
        
    ])
    
    B= Matrix([
        [2,3],
        [4,5]
    ])
    
    C= Matrix([
        [3,4],
        [5,6],
        [7,8]
    ])
    D= Matrix([
        [1,2],
        [3,4],
        [5,6]
        
    ])
    
    C_impulse = Matrix(
        [
            [2,2],
            [3,3],
            [4,4]
        ]
    )
    D_impulse = Matrix(
        [
            [2,3],
            [4,5],
            [6,7]
        ]
    )
    C_nonimpulse = Matrix([
        [3,4],
        [5,6],
        [7,8]
    ])
    D_nonimpulse = Matrix([
        [4,5],
        [6,7],
        [8,9]
    ])
        
    C1_SW, C_SW, D_SW, C_impulse_SW, D_impulse_SW, C_nonimpulse_SW, D_nonimpulse_SW,  Z_Sw_A, Z_SW_B = retrieve_Zsw_hat(  A=A, B=B, C=C, D=D,
                                                            C1=C1,
                                                            C_impulse_matrix=C_impulse, C_nonimpulse_matrix=C_nonimpulse,
                                                            D_impulse_matrix= D_impulse, D_nonimpulse_matrix= D_nonimpulse,                                           
                                                            x_hat_labels=x_hat_labels, u_labels=u_labels,
                                                          diode_column_labels=diode_column_label, y_labels=y_labels,
                                                          number_of_inductor=1, number_of_current_source=1,
                                                          element_name_obj_map=element_name_obj_map,
                                                          m_column_labels_to_obj_map=m_column_labels_to_obj_map
                                                          )
    
    ALL = Matrix([ [1]])
    ALC = Matrix([[2]])
    ACL = Matrix([[3]])
    ACC = Matrix([[4]])
    
    BLis = Matrix([[2]])
    BLvs = Matrix([[3]])
    BCis = Matrix([[4]])
    BCvs = Matrix([[5]])
    
    C_SW_raw_exp =  C[1,:]
    D_SW_raw_exp = D[1,:]
    
    C_impulse_SW_exp = C_impulse[1,:]
    D_impulse_SW_exp = D_impulse[1,:]
    
    C_nonimpulse_SW_exp = C_nonimpulse[1,:]
    D_nonimpulse_SW_exp = D_nonimpulse[1,:]
    
    C1_SW_exp = C1[1,:]
    
    C_SW_il = C_SW_raw_exp[:, :1]
    C_SW_vc = C_SW_raw_exp[:, 1:]
    

    
    C_dsw_il = C_SW_il@ALL + C_SW_vc@ACL
    C_dsw_vc = C_SW_il@ALC + C_SW_vc@ACC
    
    D_dsw_is = C_SW_il@BLis + C_SW_vc@BCis
    D_dsw_vs = C_SW_il@BLvs + C_SW_vc@BCvs
    

    
    Z_Sw_A_exp = sp.BlockMatrix([ [C_dsw_il ,C_dsw_vc] ])
    Z_SW_B_exp = sp.BlockMatrix([ [D_dsw_is , D_dsw_vs]])
    
    assert_matrix_equal(C_SW_raw_exp, C_SW)
    assert_matrix_equal(D_SW_raw_exp, D_SW)
    assert_matrix_equal( Z_Sw_A, Z_Sw_A_exp)
    assert_matrix_equal(Z_SW_B_exp, Z_SW_B)
    assert_matrix_equal(C_impulse_SW, C_impulse_SW_exp)
    assert_matrix_equal(C_nonimpulse_SW, C_nonimpulse_SW_exp)
    assert_matrix_equal(D_impulse_SW, D_impulse_SW_exp)
    assert_matrix_equal(D_nonimpulse_SW_exp, D_nonimpulse_SW)
    assert_matrix_equal(C1_SW, C1_SW_exp)
    
    




def test_retrieve_Zsw_hat_complex():

    #Two diode, 3 inductor, 1 capacitor, 2 voltage source, 1 current source
    
    
    diode1_am = Ammeter("AMD1", None, None)
    diode1_vm = Voltmeter("VMD1", None, None)
    diode2_am = Ammeter("AMD2", None, None)
    diode2_vm = Voltmeter("VMD2", None, None)
    switch_vm = Voltmeter("VMSW", None, None)
    
    
    voltage_source1 = VoltageCurrentSource("Vcc1", None, None, 5, 0, True)
    voltage_source2 = VoltageCurrentSource("Vcc2", None, None, 20, 0, True)
    current_source = VoltageCurrentSource("I_in", None, None, 10, 0, False)
    inductor1 = Inductor("L1",None, None, 10, None)
    inductor2 = Inductor("L2", None, None, 10e-6, None)
    inductor3 = Inductor("L3", None, None, 1, None)
    capacitor = Capacitor("C1", None, None, 10, None)
    
    diode1 = Diode("D1", None, None, False, diode1_vm.name, diode1_am.name)
    diode2 = Diode("D2", None, None, True, diode2_vm.name, diode2_am.name)
    
    element_name_obj_map = { diode1_am.name:diode1_am, diode1_vm.name:diode1_vm, 
                            diode2_am.name:diode2_am, diode2_vm.name:diode2_vm     }
    x_hat_labels = [inductor1.element_current_name,
                    inductor2.element_current_name, inductor3.element_current_name,
                    capacitor.element_voltage_name]
    u_labels = [current_source.element_current_name, voltage_source1.element_voltage_name, voltage_source2.element_voltage_name]
    y_labels = [diode1_vm.element_voltage_name, diode1_am.element_current_name, switch_vm.element_voltage_name, 
                diode2_vm.element_voltage_name, diode2_am.element_current_name ]#y can be out of order
    
    # diode 1 is on, diode2 is off
    diode_column_label= [diode1.element_current_name, diode2.element_voltage_name]
    m_column_labels_to_obj_map = {inductor1.element_current_name: inductor1,
                                  inductor2.element_current_name: inductor2, inductor3.element_current_name: inductor3,
                                  capacitor.element_voltage_name:capacitor,
                                  current_source.element_current_name: current_source, voltage_source1.element_voltage_name:voltage_source1, voltage_source2.element_voltage_name:voltage_source2,
                                  diode1_vm.element_voltage_name:diode1_vm, diode1_am.element_current_name:diode1_am, 
                                  diode2_vm.element_voltage_name:diode2_vm, diode2_am.element_current_name:diode2_am,
                                  switch_vm.element_voltage_name:switch_vm,
                                  diode1.element_current_name:diode1, diode1.element_voltage_name:diode1,
                                  diode2.element_current_name:diode2, diode2.element_voltage_name:diode2
                                  
                                  }
    
    A = Matrix([
        [1,2,3,4],
        [5,6,7,8],
        [9,10,11,12],
        [13,14,15,16]
        
    ])
    
    B= Matrix([
        [2,3,4],
        [5,6,7],
        [8,9,10],
        [11,12,13]
    ])
    
    C= Matrix([
        [3,4,5,6],
        [7,8,9,10],
        [11,12,13,14],
        [15,16,17,18],
        [19,20,21,22]
    ])
    D= Matrix([
        [1,2,3],
        [4,5,6],
        [7,8,9],
        [10,11,12],
        [13,14,15]

    ])
    C1 = C - sp.ones( C.shape[0],C.shape[1])
    C_impulse= C+sp.ones( C.shape[0],C.shape[1])
    C_nonimpulse = C+sp.ones( C.shape[0],C.shape[1])+sp.ones( C.shape[0],C.shape[1])
    
    D_impulse = D+sp.ones(D.shape[0], D.shape[1])
    D_nonimpulse = D+sp.ones(D.shape[0], D.shape[1]) + sp.ones(D.shape[0], D.shape[1])
    
    C1_SW, C_SW, D_SW, C_impulse_SW, D_impulse_SW, C_nonimpulse_SW, D_nonimpulse_SW,  Z_Sw_A, Z_SW_B = retrieve_Zsw_hat(  
                                                            A=A, B=B, C=C, D=D, C1=C1,
                                                        C_impulse_matrix=C_impulse, C_nonimpulse_matrix=C_nonimpulse,
                                                        D_impulse_matrix=D_impulse, D_nonimpulse_matrix=D_nonimpulse,
                                                        x_hat_labels=x_hat_labels, u_labels=u_labels,
                                                          diode_column_labels=diode_column_label, y_labels=y_labels,
                                                          number_of_inductor=3, number_of_current_source=1,
                                                          element_name_obj_map=element_name_obj_map,
                                                          m_column_labels_to_obj_map=m_column_labels_to_obj_map
                                                          )
    
    ALL = Matrix([         
        [1,2,3],
        [5,6,7],
        [9,10,11],])
    ALC = Matrix([
        [4],
        [8],
        [12],
    ])
    ACL = Matrix([
    [13,14,15]
    ])
    ACC = Matrix([[16]])
    
    BLis = Matrix([
        [2],
        [5],
        [8]
        
    ])
    BLvs = Matrix([
        
        [3,4],
        [6,7],
        [9,10]
        
    ])
    BCis = Matrix([[11]])
    BCvs = Matrix([[12,13]])
    
    C_SW_raw_exp =Matrix([
        [7,8,9,10],  
        [15,16,17,18],
    ])
    D_SW_raw_exp = Matrix([
        [4,5,6],
        [10,11,12],
    ])
    
    C_SW_impulse_exp = C_SW_raw_exp+ sp.ones(C_SW_raw_exp.shape[0], C_SW_raw_exp.shape[1] )
    C_SW_nonimpulse_exp =  C_SW_raw_exp+ sp.ones(C_SW_raw_exp.shape[0], C_SW_raw_exp.shape[1] )+ sp.ones(C_SW_raw_exp.shape[0], C_SW_raw_exp.shape[1] )
    
    D_SW_impulse_exp = D_SW_raw_exp+ sp.ones(D_SW_raw_exp.shape[0], D_SW_raw_exp.shape[1])
    D_SW_nonimpulse_exp = D_SW_raw_exp +sp.ones(D_SW_raw_exp.shape[0], D_SW_raw_exp.shape[1]) + sp.ones(D_SW_raw_exp.shape[0], D_SW_raw_exp.shape[1])
    C1_exp =  C_SW_raw_exp - sp.ones(C_SW_raw_exp.shape[0], C_SW_raw_exp.shape[1] )
    C_SW_il = Matrix(
        [
        [7,8,9],  
        [15,16,17],
        ]
    )
    C_SW_vc = Matrix([
        [10],  
        [18],
    ])
    
    # D_sw_is = D_SW_raw[:, :number_of_current_source]
    # D_sw_vs = D_SW_raw[:, number_of_current_source:]
    
    C_dsw_il = C_SW_il@ALL + C_SW_vc@ACL
    C_dsw_vc = C_SW_il@ALC + C_SW_vc@ACC
    
    D_dsw_is = C_SW_il@BLis + C_SW_vc@BCis
    D_dsw_vs = C_SW_il@BLvs + C_SW_vc@BCvs
    

    
    Z_Sw_A_exp = sp.BlockMatrix([ [C_dsw_il ,C_dsw_vc] ])
    Z_SW_B_exp = sp.BlockMatrix([ [D_dsw_is ,D_dsw_vs]])
    
    assert_matrix_equal(C_SW_raw_exp, C_SW)
    assert_matrix_equal(D_SW_raw_exp, D_SW)
    assert_matrix_equal( Z_Sw_A, Z_Sw_A_exp)
    assert_matrix_equal(Z_SW_B_exp, Z_SW_B)
    assert_matrix_equal(C_SW_impulse_exp, C_impulse_SW)
    assert_matrix_equal(D_SW_impulse_exp, D_impulse_SW)
    assert_matrix_equal(C_SW_nonimpulse_exp, C_nonimpulse_SW)
    assert_matrix_equal(D_SW_nonimpulse_exp, D_nonimpulse_SW)
    assert_matrix_equal(C1_SW, C1_exp)
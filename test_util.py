

from  util import retrieveSystemMatrix, update_system_matrix_to_reflect_dependency
from sympy import Matrix, symbols
import sympy as sp
from FormNetworkMatrix import Inductor, Capacitor, Element
import numpy as np

import math

# def test_determine_matrx_for_dependent_state_vars():
#     M0 = Matrix([[1,0],
#                  [0,0]])
#     A = Matrix([[1,2],
#                 [4,2]])
    
#     B = Matrix([[10],
#                 [20]])
    
#     x_hat_labels = ["IL","Vc"]
    
#     M0_expect = Matrix([
#         [1,0],
#         [0,0]
#     ])
#     A_expect = Matrix([
#         [1,2],
#         [0,0]
#     ])
#     B_expect = Matrix([
#         [10],
#         [0]
#     ])
    
#     A_x_ind_expect = Matrix([
#         [0,0],
#         [0,-1]
#     ])
    
#     A_dependent_expect = Matrix([
#         [0, 0],
#         [-2,0]
#     ])
#     B_dependent_expect = Matrix([
#         [0],
#         [-10]
        
#     ])  
    
#     M0_new, A_new, B_new, A_x_ind, A_dependent, B_dependent, ind_labs, dep_labs = detemrminte_matrix_for_dependent_state_vars(M0=M0, A=A, B=B, x_hat_labels=x_hat_labels )
    
#     assert M0_expect.equals(M0_new)
#     assert A_expect.equals(A_new)
#     assert B_expect.equals(B_new)
#     assert A_x_ind_expect.equals(A_x_ind)
#     assert A_dependent_expect.equals(A_dependent)
#     assert B_dependent_expect.equals(B_dependent)
#     assert len(ind_labs) == 1 and ind_labs[0] == "IL"
#     assert len(dep_labs) == 1 and dep_labs[0] == "Vc"
    
    
    
#     M0 = Matrix([[0,1],
#                  [0,0]])
#     A = Matrix([[2,4],
#                 [3,4]])
    
#     B = Matrix([[10],
#                 [20]])
    
#     x_hat_labels = ["IL","Vc"]
    
#     M0_expect = Matrix([
#         [0,0],
#         [0,1]
#     ])
#     A_expect = Matrix([
#         [0,0],
#         [2,4]
#     ])
#     B_expect = Matrix([
#         [0],
#         [10]
#     ])
    
#     A_x_ind_expect = Matrix([
#         [-1,0],
#         [0,-0]
#     ])
    
#     A_dependent_expect = Matrix([
#         [0, -4/3],
#         [0,0]
#     ])
#     B_dependent_expect = Matrix([
#         [-20/3],
#         [0]
        
#     ])  
    
#     M0_new, A_new, B_new, A_x_ind, A_dependent, B_dependent, ind_labs, dep_labs  = detemrminte_matrix_for_dependent_state_vars(M0=M0, A=A, B=B, x_hat_labels=x_hat_labels )
    
#     assert M0_expect.equals(M0_new)
#     assert A_expect.equals(A_new)
#     assert B_expect.equals(B_new)
#     assert A_x_ind_expect.equals(A_x_ind)
#     assert A_dependent_expect.equals(A_dependent)
#     assert B_dependent_expect.equals(B_dependent)
    
#     assert len(ind_labs) == 1 and dep_labs[0] == "IL"
#     assert len(dep_labs) == 1 and ind_labs[0] == "Vc"
    
    
def assert_matrix_equal(matrix1: Matrix, matrix2: Matrix, tolerance: float = 1e-5) -> None:
    """
    Asserts that two sympy matrices are equal within a specified tolerance.

    Args:
        matrix1 (sp.Matrix): The first matrix to compare.
        matrix2 (sp.Matrix): The second matrix to compare.
        tolerance (float): The maximum allowed difference between corresponding elements. Default is 1e-5.

    Raises:
        AssertionError: If the matrices differ by more than the specified tolerance.
    """
    # Check if the matrices have the same dimensions
    assert matrix1.shape == matrix2.shape, f"Matrices have different shapes: {matrix1.shape} != {matrix2.shape}"

    # Compare each element
    for i in range(matrix1.rows):
        for j in range(matrix1.cols):
            assert abs(matrix1[i, j] - matrix2[i, j]) < tolerance, \
                f"Matrices differ at position ({i}, {j}): {matrix1[i, j]} != {matrix2[i, j]}"


def test_retrieveSystemMatrix():
    # when no clicts
    # from the buck circut, switch on diode off
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

    
    M0_expect = Matrix([[1,0 ],
                        [0,1]])
    s_dxdt_expect = -1*Matrix([[0,0],
                            [0,0]])
    sx_expect = -1*Matrix([[-1,0],
                        [0,0]])
    su_expect = -1*Matrix([[0],
                        [1]])
    
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

    s_dxdt, Sx, Su, C1_m, C, D, M0, A, B, C_sw, D_sw, inconsistent_labels = (
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
    assert s_dxdt.equals(s_dxdt_expect)
    assert Sx.equals(sx_expect)
    assert Su.equals(su_expect)
    assert C1_m.equals(C1_expect)
    assert C.equals(C_expect)
    assert D.equals(D_expect)
    assert M0.equals(M0_expect)
    assert A.equals(A_expect)
    assert B.equals(B_expect)
    assert inconsistent_labels == []
    

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
    
    M0_expect = Matrix([[1,0],
                        [0,1]])
    s_dxdt_expect = -Matrix([[0,0],
                            [0,0]])
    sx_expect = -Matrix([[0,0],
                         [-1,0]])
    su_expect = -Matrix([[0],
                         [0]])
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
    # When there is conflict, switch off, diode off
    s_dxdt, Sx, Su, C1_m, C, D, M0, A, B, C_sw, D_sw, inconsistent_labels = (
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
    assert s_dxdt.equals(s_dxdt_expect)
    assert Sx.equals(sx_expect)
    assert Su.equals(su_expect)
    assert C1_m.equals(C1_expect)
    assert C.equals(C_expect)
    assert D.equals(D_expect)
    assert M0.equals(M0_expect)
    assert A.equals(A_expect)
    assert B.equals(B_expect)
    assert inconsistent_labels == ["I_AM2-MOSFET"]
    



def system_one():
    M0 = Matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])
    A = Matrix([
    [  1,2,3,4],
    [  5,6,7,8],
    [  9,10,11,12],
    [ 13,14,15,16]])
    B = Matrix([
    [1],
    [2],
    [3],
    [4]])
    
    
    C = Matrix([
    [2,3,4,5],
    [6,7,8,9],
    [10,11,12,13],
    [14,15,16,17]])
    
    D = Matrix([
    [1],
    [2],
    [3],
    [4]])
    m_pivots = (0, 1, 2, 3, 4)
    x_hat_labels = ['V_LS0', 'V_LS1', 'V_LS2', 'I_Cout']
    u_labels = ["Vin"]
    y_labels = ['V_VMD1', 'V_VMD2', 'I_AMD1', 'I_AMD2']
    x_hat_col_offset_in_m_pivots = 1
    
    
    K12 = symbols("K12")
    K23 = symbols("K23")
    K13 = symbols("K13")

    symbol_to_value_map = { K12:0.99, K23:0.99, K13:0.99 }
    L0 =Inductor("LS0",None,None,
                 200e-6,None, ["LS1", "LS2"], [K12, K13] )
    L1 =Inductor("LS1",None,None,
                 300e-6,None, ["LS0", "LS2"], [K12, K23] )
    L2 =Inductor("LS2",None,None,
                 400e-6,None, ["LS0", "LS1"], [K13, K23] )
    C0 = Capacitor("C1",None,None, 100e-6, None)
    element_name_to_obj_map = { "LS0":L0, "LS1":L1, "LS2":L2, "C1":C0 }
    x_hat_label_to_obj_map = { 'V_LS0':L0,   'V_LS1':L1, 'V_LS2':L2, 'I_Cout':C0 }
    
    C1 = Matrix([
        [4,3,2,1],
        [8,7,6,5],
        [12,11,10,9],
        [16,15,14,13]
    ])
    return M0, A, B, C, D,C1,  m_pivots, x_hat_labels, x_hat_col_offset_in_m_pivots, u_labels, y_labels,  x_hat_label_to_obj_map,symbol_to_value_map ,element_name_to_obj_map
    
def system_two():
    M0=Matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0]])
    A = Matrix([
    [  1,2,0,4],
    [  5,6,0,8],
    [  9,10,0,12],
    [ 13,14,1,16]])
    B = Matrix([
    [1],
    [2],
    [3],
    [4]])
    
    
    C = Matrix([
    [2,3,4,5],
    [6,7,8,9],
    [10,11,12,13],
    [14,15,16,17]])
    
    D = Matrix([
    [1],
    [2],
    [3],
    [4]])
    m_pivots = (0, 1, 2, 4, 7)
    x_hat_labels = ['V_LS0', 'V_LS1', 'V_LS2', 'I_Cout']
    u_labels = ["Vin"]
    y_labels = ['V_VMD1', 'V_VMD2', 'I_AMD1', 'I_AMD2']
    x_hat_col_offset_in_m_pivots = 1
    K12 = symbols("K12")
    K23 = symbols("K23")
    K13 = symbols("K13")
    
    symbol_to_value_map = { K12:0.99, K23:0.99, K13:0.99 }
    L0 =Inductor("LS0",None,None,
                 200e-6,None, ["LS1", "LS2"], [K12, K13] )
    L1 =Inductor("LS1",None,None,
                 300e-6,None, ["LS0", "LS2"], [K12, K23] )
    L2 =Inductor("LS2",None,None,
                 400e-6,None, ["LS0", "LS1"], [K13, K23] )
    C0 = Capacitor("C1",None,None, 100e-6, None)
    x_hat_label_to_obj_map = { 'V_LS0':L0,   'V_LS1':L1, 'V_LS2':L2, 'I_Cout':C0 }
    element_name_to_obj_map = { "LS0":L0, "LS1":L1, "LS2":L2, "C1":C0 }

    
    C1 = Matrix([
        [4,3,2,1],
        [8,7,6,5],
        [12,11,10,9],
        [16,15,14,13]
    ])
    return M0, A, B, C, D,C1,  m_pivots, x_hat_labels, x_hat_col_offset_in_m_pivots, u_labels, y_labels,  x_hat_label_to_obj_map,symbol_to_value_map ,element_name_to_obj_map
    
def system_three():
    M0=Matrix([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]])
    A = Matrix([
    [  1,0,0,4],
    [  5,0,0,8],
    [  9,1,0,12],
    [ 13,14,1,16]])
    B = Matrix([
    [1],
    [2],
    [3],
    [4]])
    
    
    C = Matrix([
    [2,3,4,5],
    [6,7,8,9],
    [10,11,12,13],
    [14,15,16,17]])
    
    D = Matrix([
    [1],
    [2],
    [3],
    [4]])
    m_pivots = (0, 1, 4, 6, 7)
    x_hat_labels = ['V_LS0', 'V_LS1', 'V_LS2', 'I_Cout']
    u_labels = ["Vin"]
    y_labels = ['V_VMD1', 'V_VMD2', 'I_AMD1', 'I_AMD2']
    x_hat_col_offset_in_m_pivots = 1
    K12 = symbols("K12")
    K23 = symbols("K23")
    K13 = symbols("K13")
    symbol_to_value_map = { K12:0.99, K23:0.99, K13:0.99 }
    L0 =Inductor("LS0",None,None,
                 200e-6,None, ["LS1", "LS2"], [K12, K13] )
    L1 =Inductor("LS1",None,None,
                 300e-6,None, ["LS0", "LS2"], [K12, K23] )
    L2 =Inductor("LS2",None,None,
                 400e-6,None, ["LS0", "LS1"], [K13, K23] )
    C1 = Capacitor("C1",None,None, 100e-6, None)
    x_hat_label_to_obj_map = { 'V_LS0':L0,   'V_LS1':L1, 'V_LS2':L2, 'I_Cout':C1 }
    
    element_name_to_obj_map = { "LS0":L0, "LS1":L1, "LS2":L2, "C1":C1 }
    
    C1 = Matrix([
        [4,3,2,1],
        [8,7,6,5],
        [12,11,10,9],
        [16,15,14,13]
    ])
    return M0, A, B, C, D,C1,  m_pivots, x_hat_labels, x_hat_col_offset_in_m_pivots, u_labels, y_labels,  x_hat_label_to_obj_map,symbol_to_value_map ,element_name_to_obj_map

    
    
def system_four():
    # when a inductor(LR) and a transformer(model as inductor LS0) is in series
    M0=Matrix([
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])
    A = Matrix([
    [  0,7,5,4],
    [  0,2,4,8],
    [  0,1,3,12],
    [ 1,14,1,16]])
    B = Matrix([
    [1],
    [2],
    [3],
    [4]])
    
    
    C = Matrix([
    [2,3,4,5],
    [6,7,8,9],
    [10,11,12,13],
    [14,15,16,17]
    ])
    
    D = Matrix([
    [1],
    [2],
    [3],
    [4]])
    m_pivots = (0, 1, 3, 4, 5)
    x_hat_labels = ["V_LR", 'V_LS0', 'V_LS1', 'V_LS2']
    u_labels = ["Vin"]
    y_labels = ['V_VMD1', 'V_VMD2', 'I_AMD1', 'I_AMD2']
    x_hat_col_offset_in_m_pivots = 1
    K12 = symbols("K12")
    K23 = symbols("K23")
    K13 = symbols("K13")
    symbol_to_value_map = { K12:0.99, K23:0.99, K13:0.99 }
    L0 =Inductor("LS0",None,None,
                 200e-6,None, ["LS1", "LS2"], [K12, K13] )
    L1 =Inductor("LS1",None,None,
                 300e-6,None, ["LS0", "LS2"], [K12, K23] )
    L2 =Inductor("LS2",None,None,
                 400e-6,None, ["LS0", "LS1"], [K13, K23] )
    LR = Inductor("LR",None,None, 50e-6, None)
    x_hat_label_to_obj_map = { 'V_LR':LR , 'V_LS0':L0,   'V_LS1':L1, 'V_LS2':L2}
    
    element_name_to_obj_map = {"LR":LR ,  "LS0":L0, "LS1":L1, "LS2":L2}
    
    C1 = Matrix([
        [4,3,2,1],
        [8,7,6,5],
        [12,11,10,9],
        [16,15,14,13]
    ])
    return M0, A, B, C, D,C1,  m_pivots, x_hat_labels, x_hat_col_offset_in_m_pivots, u_labels, y_labels,  x_hat_label_to_obj_map,symbol_to_value_map ,element_name_to_obj_map
       
    
def test_update_system_matrix_to_reflect_dependency_system_1():
    # test 1
    M0, A, B, C, D,C1,  m_pivots, x_hat_labels, x_hat_col_offset_in_m_pivots, \
    u_labels, y_labels,  x_hat_label_to_obj_map,symbol_to_value_map ,\
        element_name_to_obj_map= system_one()
    M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final = update_system_matrix_to_reflect_dependency(
        
        M0=M0,
        C1=C1,
        A=A,B=B,C=C,D=D,m_pivots=m_pivots,x_hat_labels=x_hat_labels,
        x_hat_col_offset_in_m_pivots=x_hat_col_offset_in_m_pivots,x_hat_label_to_obj_map=x_hat_label_to_obj_map,
        symbol_to_value_map=symbol_to_value_map,
        element_name_to_obj_map = element_name_to_obj_map,
        u_labels=u_labels,
        y_labels=y_labels
    )
    
    
    M0_final_exp = Matrix([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])
    
    E = np.array([
        [200e-6, 0.99 * math.sqrt(200e-6 * 300e-6), 0.99 * math.sqrt(200e-6 * 400e-6), 0],
        [0.99 * math.sqrt(300e-6 * 200e-6), 300e-6, 0.99 * math.sqrt(300e-6 * 400e-6), 0],
        [0.99 * math.sqrt(200e-6 * 400e-6), 0.99 * math.sqrt(300e-6 * 400e-6), 400e-6, 0],
        [0, 0, 0, 100e-6]
    ])
        
    A_final_exp =  Matrix( np.linalg.inv(E)  @sp.matrix2numpy(A, dtype=np.float64))
    B_fina_exp =  Matrix(np.linalg.inv(E) @ sp.matrix2numpy(B, dtype=np.float64))
    
    C_final_exp =   Matrix([
    [2,3,4,5],
    [6,7,8,9],
    [10,11,12,13],
    [14,15,16,17]])  + C1@E@A_final_exp
    
    D_final_exp = Matrix([
    [1],
    [2],
    [3],
    [4]])+ C1@E@B_fina_exp
    
    A_dependent_final_expect = sp.eye(4,4)
    B_dependent_final_expect = sp.zeros(4,1)
    
    
    assert_matrix_equal(M0_final, M0_final_exp)
    assert_matrix_equal(A_final, A_final_exp)
    assert_matrix_equal(B_fina_exp, B_final)
    assert_matrix_equal(C_final, C_final_exp)
    assert_matrix_equal(D_final, D_final_exp)
    assert_matrix_equal(A_dependent_final, A_dependent_final_expect)
    assert_matrix_equal(B_dependent_final, B_dependent_final_expect)

def test_update_system_matrix_to_reflect_dependency_system_2():
    M0, A, B, C, D,C1_m,  m_pivots, x_hat_labels, x_hat_col_offset_in_m_pivots, \
    u_labels, y_labels,  x_hat_label_to_obj_map,symbol_to_value_map ,\
        element_name_to_obj_map= system_two()

    E_origin = np.array([
        [200e-6, 0.99 * math.sqrt(200e-6 * 300e-6), 0.99 * math.sqrt(200e-6 * 400e-6), 0],
        [0.99 * math.sqrt(300e-6 * 200e-6), 300e-6, 0.99 * math.sqrt(300e-6 * 400e-6), 0],
        [0.99 * math.sqrt(200e-6 * 400e-6), 0.99 * math.sqrt(300e-6 * 400e-6), 400e-6, 0],
        [0, 0, 0, 100e-6]
    ])
    M0_final_expect = Matrix([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,0,0],
        [0,0,0,1]  
    ])
    E = np.array([
        [200e-6,                        0.99 * math.sqrt(200e-6 * 300e-6),  0],
        [0.99 * math.sqrt(300e-6 * 200e-6), 300e-6,                          0],
        [0,                               0,                            100e-6]
    ], dtype=np.float64)
    A11 = np.array([
        [1,2,4],
        [5,6,8],
        [9,10,12]        
    ], dtype=np.float64)
    A12 = np.array([
        [0],
        [0],
        [0]
    ], dtype=np.float64)
    A21 = np.array([ 
        [13,14,16]
    ], dtype=np.float64)
    
    A22 = np.array(
        [[1]], dtype=np.float64
    )
    
    B1 = np.array([
        [1],
        [2],
        [3]], dtype=np.float64)
    B2 = np.array([[4]], dtype=np.float64)
    
    C1 = np.array([
        [2,3,5],
        [6,7,9],
        [10,11,13],
        [14,15,17]
    ], dtype=np.float64)
    C2 = np.array(
        [
            [4],
            [8],
            [12],
            [16]
        ], dtype=np.float64
    )
    
    E_inv = np.linalg.inv(E)
    A22_inv = np.linalg.inv(A22)    
    
    
    A11_new = E_inv @(A11 - A12@A22_inv@A21)
    B1_new = E_inv @(B1 - A12@A22_inv@B2)
    
    A_final_expect = sp.zeros(4,4)
    A_final_expect[0:2, 0:2] = A11_new[0:2, 0:2]
    A_final_expect[0:2, 3] = A11_new[0:2, 2]
    A_final_expect[3,0] = A11_new[2, 0]
    A_final_expect[3,1] = A11_new[2, 1]
    A_final_expect[3,3] = A11_new[2, 2]
    
    
    B_final_expect = sp.zeros(4,1)
    B_final_expect[0:2, :] = B1_new[0:2, :]
    B_final_expect[3, :] = B1_new[2, :]
    
    D_final_exp = D-C2@A22_inv@B2
    
    C_new = C1-C2@A22_inv@A21
    
    C_final_exp = sp.zeros(4,4)
    C_final_exp[:, 0:2] = C_new[:, 0:2]
    C_final_exp[:, 3] = C_new[:, 2]
    
    # add the affect from C1
    C_final_exp = C_final_exp  + C1_m @E_origin  @ A_final_expect
    D_final_exp = D_final_exp + C1_m @ E_origin @B_final_expect
    
    A_x2  = -1*A22_inv@A21
    B_x2 = -1*A22_inv@B2
    
    A_dependent_final_expect = sp.eye(4,4)
    A_dependent_final_expect[2,2] = 0
    A_dependent_final_expect[2, 0:2] = A_x2[:,0:2]
    A_dependent_final_expect[2, 3] = A_x2[:, 2]
    B_dependent_final_expect = sp.zeros(4,1)
    B_dependent_final_expect[2, :] = B_x2[:,:]

    
    M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final = update_system_matrix_to_reflect_dependency(
        
        M0=M0,
        C1=C1_m,
        A=A,B=B,C=C,D=D,m_pivots=m_pivots,x_hat_labels=x_hat_labels,
        x_hat_col_offset_in_m_pivots=x_hat_col_offset_in_m_pivots,x_hat_label_to_obj_map=x_hat_label_to_obj_map,
        element_name_to_obj_map=element_name_to_obj_map,
        symbol_to_value_map=symbol_to_value_map,
        u_labels=u_labels,
        y_labels=y_labels
    )
    
    
    assert_matrix_equal(M0_final, M0_final_expect)
    assert_matrix_equal(A_final, A_final_expect)
    assert_matrix_equal(B_final_expect, B_final)
    assert_matrix_equal(C_final, C_final_exp)
    assert_matrix_equal(D_final, D_final_exp)
    assert_matrix_equal(A_dependent_final, A_dependent_final_expect)
    assert_matrix_equal(B_dependent_final, B_dependent_final_expect)


def test_update_system_matrix_to_reflect_dependency_system_3(): 
    M0, A, B, C, D,C1_m,  m_pivots, x_hat_labels, x_hat_col_offset_in_m_pivots, \
    u_labels, y_labels,  x_hat_label_to_obj_map,symbol_to_value_map ,\
        element_name_to_obj_map= system_three()
    E_origin = np.array([
        [200e-6, 0.99 * math.sqrt(200e-6 * 300e-6), 0.99 * math.sqrt(200e-6 * 400e-6), 0],
        [0.99 * math.sqrt(300e-6 * 200e-6), 300e-6, 0.99 * math.sqrt(300e-6 * 400e-6), 0],
        [0.99 * math.sqrt(200e-6 * 400e-6), 0.99 * math.sqrt(300e-6 * 400e-6), 400e-6, 0],
        [0, 0, 0, 100e-6]
    ])
    M0_final_expect = Matrix([
        [1,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,1]
    ])
    E = np.array([
        [200e-6,             0],
        [0,               100e-6]
    ], dtype=np.float64)
    
    A11 =np.array([
        [1,4],
        [5,8],     
    ], dtype=np.float64)
    A12 =np.array([
        [0,0],
        [0,0],     
    ], dtype=np.float64)
    A21 =np.array([
        [9,12],
        [13,16],     
    ], dtype=np.float64)
    A22 =np.array([
        [1,0],
        [14,1],     
    ], dtype=np.float64)
    
    B1 = np.array(
        [[1],
         [2]], dtype=np.float64
    )
    B2 = np.array(
        [
            [3],
            [4]
        ], dtype=np.float64
    )
    
    C1 = np.array(
        [
            [2,5],
            [6,9],
            [10,13],
            [14,17]
        ], dtype=np.float64
    )
    C2 = np.array(
        [
            [3,4],
            [7,8],
            [11,12],
            [15,16]
        ], dtype=np.float64
    )
    
    D  =np.array([
        [1],
        [2],
        [3],
        [4]       
    ], dtype=np.float64)
    
    E_inv = np.linalg.inv(E)
    A22_inv = np.linalg.inv(A22)
    
    
    A11_new = E_inv @(A11 - A12@A22_inv@A21)
    B1_new = E_inv @(B1 - A12@A22_inv@B2)
    
    A_final_expect = sp.zeros(4,4)
    A_final_expect[0,0] = A11_new[0,0]
    A_final_expect[0,3] = A11_new[0,1]
    A_final_expect[3,0] = A11_new[1,0]
    A_final_expect[3,3] = A11_new[1,1]
    
    B_final_expect = sp.zeros(4,1)
    B_final_expect[0,0] = B1_new[0,0]
    B_final_expect[3,0] = B1_new[1,0]
    
    D_final_exp = Matrix( D-C2@A22_inv@B2)
    
    C_new = C1-C2@A22_inv@A21
    C_final_exp = sp.zeros(4,4)
    C_final_exp[:,0] =  C_new[:,0]
    # C_final_exp[0,3] = C_new[0,1]
    # C_final_exp[3,0] = C_new[1,0]
    C_final_exp[:,3] = C_new[:,1]
    
    
    # apply the affect of C1 on C, D matrix
    
    C_final_exp += C1_m @ E_origin@A_final_expect
    D_final_exp += C1_m @ E_origin @ B_final_expect
    
    A_x2  = -1*A22_inv@A21
    B_x2 = -1*A22_inv@B2
    
    A_dependent_final_expect = sp.eye(4,4)
    A_dependent_final_expect[1,1] = 0
    A_dependent_final_expect[2,2] = 0
    
    A_dependent_final_expect[1,0] = A_x2[0,0]
    A_dependent_final_expect[1,3] = A_x2[0,1]
    A_dependent_final_expect[2,0] = A_x2[1,0]
    A_dependent_final_expect[2,3] = A_x2[1,1]
    
    B_dependent_final_expect = sp.zeros(4,1)
    B_dependent_final_expect[1, :] = B_x2[0, :]
    B_dependent_final_expect[2, :] = B_x2[1, :]
    
    M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final = update_system_matrix_to_reflect_dependency(
        
        M0=M0,
        C1=C1_m,
        A=A,B=B,C=C,D=D,m_pivots=m_pivots,x_hat_labels=x_hat_labels,
        x_hat_col_offset_in_m_pivots=x_hat_col_offset_in_m_pivots,x_hat_label_to_obj_map=x_hat_label_to_obj_map,
        symbol_to_value_map=symbol_to_value_map,
        element_name_to_obj_map=element_name_to_obj_map,
        u_labels=u_labels,
        y_labels=y_labels
    )
    
    
    assert_matrix_equal(M0_final, M0_final_expect)
    assert_matrix_equal(A_final, A_final_expect)
    assert_matrix_equal(B_final_expect, B_final)
    assert_matrix_equal(C_final, C_final_exp)
    assert_matrix_equal(D_final, D_final_exp)
    assert_matrix_equal(A_dependent_final, A_dependent_final_expect)
    assert_matrix_equal(B_dependent_final, B_dependent_final_expect)




def test_update_system_matrix_to_reflect_dependency_system_4(): 
    M0, A, B, C, D,C1_m,  m_pivots, x_hat_labels, x_hat_col_offset_in_m_pivots, \
    u_labels, y_labels,  x_hat_label_to_obj_map,symbol_to_value_map ,\
        element_name_to_obj_map= system_four()
    E_origin = np.array([
        [50e-6, 0,                                      0,                              0],
        [0,     200e-6,                             0.99 * math.sqrt(200e-6 * 300e-6),  0.99 * math.sqrt(200e-6 * 400e-6)],
        [0,     0.99 * math.sqrt(300e-6 * 200e-6), 300e-6,                              0.99 * math.sqrt(300e-6 * 400e-6)],
        [0,     0.99 * math.sqrt(200e-6 * 400e-6), 0.99 * math.sqrt(300e-6 * 400e-6),   400e-6],
        
    ])
   


    M0_final_expect = Matrix([
        [0,1,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])
    E = np.array([
        [200e-6+50e-6,                             0.99 * math.sqrt(200e-6 * 300e-6),  0.99 * math.sqrt(200e-6 * 400e-6)], # plus the 50e-6 inductor that is dependent
        [0.99 * math.sqrt(300e-6 * 200e-6), 300e-6,                              0.99 * math.sqrt(300e-6 * 400e-6)],
        [0.99 * math.sqrt(200e-6 * 400e-6), 0.99 * math.sqrt(300e-6 * 400e-6),   400e-6],
    ], dtype=np.float64)
    
    A11 =np.array([
    [  7,5,4],
    [  2,4,8],
    [  1,3,12],
    ], dtype=np.float64)
    A12 =np.array([
        [0],
        [0],
        [0]

    ], dtype=np.float64)
    A21 =np.array([
        [14,1,16],
    ], dtype=np.float64)
    A22 =np.array([
        [1],
    ], dtype=np.float64)
    
    B1 = np.array(
        [
        [1],
        [2],
        [3]
         ], dtype=np.float64
    )
    B2 = np.array(
        [
        [4],
        ], dtype=np.float64
    )
    
    C1 = np.array(
        [
        [3,4,5],
        [7,8,9],
        [11,12,13],
        [15,16,17]
        ], dtype=np.float64
    )
    C2 = np.array(
        [
        [2],
        [6],
        [10],
        [14]
        ], dtype=np.float64
    )


    
    D  =np.array([
        [1],
        [2],
        [3],
        [4]       
    ], dtype=np.float64)
    
    E_inv = np.linalg.inv(E)
    A22_inv =  np.linalg.inv(A22)
    
    
    A11_new = E_inv @(A11 - A12@A22_inv@A21)
    B1_new = E_inv @(B1 - A12@A22_inv@B2)
    
    A_final_expect = sp.zeros(4,4)
    A_final_expect[1:4, 1:4] = A11_new
    
    B_final_expect = sp.zeros(4,1)
    B_final_expect[1:, :] = B1_new[:,:]

    
    # because LR is in series with Ls0 => Lr is dependent. Thus, LR's row in A, B should be the same as LS0's row
    A_final_expect[0,:] = A_final_expect[1,:]
    B_final_expect[0,:] = B_final_expect[1,:]
    
    D_final_exp = Matrix( D-C2@A22_inv@B2)
    
    C_new = C1-C2@A22_inv@A21
    C_final_exp = sp.zeros(4,4)
    C_final_exp[:,1:4] =  C_new[:,:]

    
    # apply the affect of C1 on C, D matrix
    
    C_final_exp += C1_m @ E_origin@A_final_expect
    D_final_exp += C1_m @ E_origin @ B_final_expect
    
    A_x2  = -1*A22_inv@A21
    B_x2 = -1*A22_inv@B2
    
    A_dependent_final_expect = sp.eye(4,4)
    A_dependent_final_expect[0,0] = 0

    
    A_dependent_final_expect[0, 1:] = A_x2[:, :]
    
    B_dependent_final_expect = sp.zeros(4,1)
    B_dependent_final_expect[0, :] = B_x2[0, :]

    
    M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final = update_system_matrix_to_reflect_dependency(
        
        M0=M0,
        C1=C1_m,
        A=A,B=B,C=C,D=D,m_pivots=m_pivots,x_hat_labels=x_hat_labels,
        x_hat_col_offset_in_m_pivots=x_hat_col_offset_in_m_pivots,x_hat_label_to_obj_map=x_hat_label_to_obj_map,
        symbol_to_value_map=symbol_to_value_map,
        element_name_to_obj_map=element_name_to_obj_map,
        u_labels=u_labels,
        y_labels=y_labels
    )
    
    
    assert_matrix_equal(M0_final, M0_final_expect)
    assert_matrix_equal(A_final, A_final_expect)
    assert_matrix_equal(B_final_expect, B_final)
    assert_matrix_equal(C_final, C_final_exp)
    assert_matrix_equal(D_final, D_final_exp)
    assert_matrix_equal(A_dependent_final, A_dependent_final_expect)
    assert_matrix_equal(B_dependent_final, B_dependent_final_expect)

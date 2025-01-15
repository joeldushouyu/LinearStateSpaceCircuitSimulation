

from  util import retrieveSystemMatrix, detemrminte_matrix_for_dependent_state_vars
from sympy import Matrix, symbols





def test_determine_matrx_for_dependent_state_vars():
    M0 = Matrix([[1,0],
                 [0,0]])
    A = Matrix([[1,2],
                [4,2]])
    
    B = Matrix([[10],
                [20]])
    
    x_hat_labels = ["IL","Vc"]
    
    M0_expect = Matrix([
        [1,0],
        [0,0]
    ])
    A_expect = Matrix([
        [1,2],
        [0,0]
    ])
    B_expect = Matrix([
        [10],
        [0]
    ])
    
    A_x_ind_expect = Matrix([
        [0,0],
        [0,-1]
    ])
    
    A_dependent_expect = Matrix([
        [0, 0],
        [-2,0]
    ])
    B_dependent_expect = Matrix([
        [0],
        [-10]
        
    ])  
    
    M0_new, A_new, B_new, A_x_ind, A_dependent, B_dependent, ind_labs, dep_labs = detemrminte_matrix_for_dependent_state_vars(M0=M0, A=A, B=B, x_hat_labels=x_hat_labels )
    
    assert M0_expect.equals(M0_new)
    assert A_expect.equals(A_new)
    assert B_expect.equals(B_new)
    assert A_x_ind_expect.equals(A_x_ind)
    assert A_dependent_expect.equals(A_dependent)
    assert B_dependent_expect.equals(B_dependent)
    assert len(ind_labs) == 1 and ind_labs[0] == "IL"
    assert len(dep_labs) == 1 and dep_labs[0] == "Vc"
    
    
    
    M0 = Matrix([[0,1],
                 [0,0]])
    A = Matrix([[2,4],
                [3,4]])
    
    B = Matrix([[10],
                [20]])
    
    x_hat_labels = ["IL","Vc"]
    
    M0_expect = Matrix([
        [0,0],
        [0,1]
    ])
    A_expect = Matrix([
        [0,0],
        [2,4]
    ])
    B_expect = Matrix([
        [0],
        [10]
    ])
    
    A_x_ind_expect = Matrix([
        [-1,0],
        [0,-0]
    ])
    
    A_dependent_expect = Matrix([
        [0, -4/3],
        [0,0]
    ])
    B_dependent_expect = Matrix([
        [-20/3],
        [0]
        
    ])  
    
    M0_new, A_new, B_new, A_x_ind, A_dependent, B_dependent, ind_labs, dep_labs  = detemrminte_matrix_for_dependent_state_vars(M0=M0, A=A, B=B, x_hat_labels=x_hat_labels )
    
    assert M0_expect.equals(M0_new)
    assert A_expect.equals(A_new)
    assert B_expect.equals(B_new)
    assert A_x_ind_expect.equals(A_x_ind)
    assert A_dependent_expect.equals(A_dependent)
    assert B_dependent_expect.equals(B_dependent)
    
    assert len(ind_labs) == 1 and ind_labs[0] == "IL"
    assert len(dep_labs) == 1 and dep_labs[0] == "Vc"
    
    

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
            current_source_size= 0
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
            current_source_size= 0
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
    
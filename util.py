from Element import (
    Element, ExternalSwitch, Diode
)
from typing import Tuple
import sympy as sp
from sympy import Matrix, pi, pprint, Symbol, eye, zeros, simplify
from numba import njit, prange
import numpy as np
import numpy.typing as npt
import math
def is_rise_edge(frequency, time_t) -> bool:
    
    # assume time_t is higher resolution than frequency
    """
    Determines if a rising edge of a square wave occurs at the given time.

    Parameters:
    - frequency (float): Frequency of the square wave in Hz.
    - time_t (float): Time in seconds to evaluate.

    Returns:
    - bool: True if the time corresponds to a rising edge, False otherwise.
    """
    if frequency <= 0:
        raise ValueError("frequency must be a positive number.")
    
    period = 1 / frequency  # Period of the square wave
    # Calculate the exact time within the period
    time_in_period = time_t % period
    epsilon = 1e-9  # Tolerance for numerical precision issues
    # Rising edge occurs at the start of each period (time_in_period close to 0)
    if time_t == 0.0:
        return True
    else:
        return abs(time_in_period) < epsilon or abs(time_in_period - period) < epsilon

def print_matrix(A_matrix, column_names: list[str], row_names: list[str]):
    # Determine column widths
    col_widths = [
        max(len(str(val)) for val in col)
        for col in zip(*A_matrix.tolist(), column_names)
    ]
    row_label_width = max(len(row_label) for row_label in row_names)

    # Determine column widths
    col_widths = [
        max(len(str(val)) for val in col)
        for col in zip(*A_matrix.tolist(), column_names)
    ]
    row_label_width = max(len(row_label) for row_label in row_names)

    # Print column headers
    header = " " * (row_label_width + 1) + " ".join(
        f"{col:<{col_widths[i]}}" for i, col in enumerate(column_names)
    )
    print(header)

    # Print rows with row labels
    for row_label, row in zip(row_names, A_matrix.tolist()):
        row_str = " ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row))
        print(f"{row_label:<{row_label_width}} {row_str}")


def swapTwoColumn(
    matrix: Matrix,
    cur_col_name: list[str],
    label_obj_map: dict[str, Element],
    col_label: str,
):
    # find the element of the col_label

    ele = label_obj_map[col_label]

    if col_label == ele.element_current_name:
        voltage_ind = cur_col_name.index(ele.element_voltage_name)
        current_ind = cur_col_name.index(col_label)

    else:
        current_ind = cur_col_name.index(ele.element_current_name)
        voltage_ind = cur_col_name.index(col_label)
    cur_col_name[voltage_ind], cur_col_name[current_ind] = (
        cur_col_name[current_ind],
        cur_col_name[voltage_ind],
    )

    temp = matrix[:, current_ind]
    matrix[:, current_ind] = matrix[:, voltage_ind]
    matrix[:, voltage_ind] = temp





def calculate_dependent_state_vars(M0: Matrix, x_hat_labels:list[str]):
    
    
    independent_state_vars = []
    dependent_state_vars = []

    cols = M0.cols
    _, M0_pivots = M0.rref()
    j = 0
    for i in range(len(cols)):
        is_independent =  j < len(M0_pivots) and M0_pivots[j] == i
        if is_independent:
            independent_state_vars.append(  x_hat_labels[i]  )
            j += 1
        else:
            dependent_state_vars.append(x_hat_labels[i]) 



def retrieveSystemMatrix(
    M: Matrix,
    s_labels_size:int,
    y_labels_size:int,
    x_hat_labels_size:int,
    x_labels_size:int,
    y_zero_labels_size: int,
    s_zero_labels_size: int,
    capacitor_size:int,
    inductor_size:int,
    voltage_source_size:int,
    current_source_size:int,
) -> Tuple[Matrix]:
    assert capacitor_size + inductor_size == x_hat_labels_size == x_labels_size
    y_col_offset = s_labels_size
    x_hat_col_offset = y_labels_size + y_col_offset
    x_col_offset = x_hat_col_offset + x_hat_labels_size
    zero_offset = x_col_offset + x_labels_size
    u_col_offset = zero_offset + y_zero_labels_size + s_zero_labels_size

    s_row_offset = 0
    y_row_offset = s_labels_size
    x_row_offset = y_row_offset + y_labels_size
    s_dxdt = -M[s_row_offset:y_row_offset, x_hat_col_offset:x_col_offset]
    Sx = -M[s_row_offset:y_row_offset, x_col_offset:zero_offset]
    Su = -M[s_row_offset:y_row_offset, u_col_offset:]

    C1 = -M[y_row_offset:x_row_offset, x_hat_col_offset:x_col_offset]
    C = -M[y_row_offset:x_row_offset, x_col_offset:zero_offset]
    D = -M[y_row_offset:x_row_offset, u_col_offset:]

    M0 = M[x_row_offset:, x_hat_col_offset:x_col_offset]
    A = -M[x_row_offset:, x_col_offset:zero_offset]
    B = -M[x_row_offset:, u_col_offset:]
    
    #TODO: order changed
    
    ALL = A[0:inductor_size, 0:inductor_size]
    ALC = A[0:inductor_size, inductor_size:]
    ACL = A[inductor_size:, 0:inductor_size]
    ACC = A[inductor_size:, inductor_size:]
    
    
    
    BLis = B[0:inductor_size, 0:current_source_size]
    BLvs = B[0:inductor_size, current_source_size:]
    BCis = B[inductor_size:, 0:current_source_size]
    BCvs = B[inductor_size:, current_source_size:]
    

    Csw_il = Sx[:, 0:inductor_size]
    Csw_vc = Sx[:, inductor_size:]
    
    Dsw_is = Su[:, 0:current_source_size]
    Dsw_vs = Su[:, current_source_size:]
    
    
    Cdsw_iL = Csw_il *ALL + Csw_vc*ACL
    Cdsw_vC = Csw_il * ALC + Csw_vc*ACC
    
    

    Ddsw_is = Csw_il*BLis +Csw_vc*BCis
    
    if current_source_size == 0:
         Ddsw_vs = Csw_vc*BCvs
    else:
        Ddsw_vs = Csw_il*BLis + Csw_vc*BCvs
    
    
    # if current_source_size >0 and voltage_source_size >0:
    t1 = [ Cdsw_iL , Cdsw_vC]
    t2  = [  Ddsw_is , Ddsw_vs]
    
    t1_useful = [x for x in t1 if len(x) > 0]
    t2_useful = [x for x in t2 if len(x) > 0]
    
    C_sw = Matrix(t1_useful)
    D_sw = Matrix(t2_useful)
    
    if len(C_sw) == 0:
        C_sw =  zeros(  C.shape[0], C.shape[1])
    if len(D_sw) == 0:
        D_sw = zeros(D.shape[0], D.shape[1])
    return s_dxdt, Sx, Su, C1, C, D, M0, A, B,C_sw,D_sw




def determine_dependent_state_vars(M0: Matrix, A:Matrix, B:Matrix, network_matrix, sw_lab:str):
    # sw_lab is volt/current label of the external switch that cause it
    indenepdent_state_vars_labels = []
    dependent_state_vars_labels = []
    
    independent_state_vars_cols = []
    dependent_state_vars_cols = []
    
    cols = M0.cols
    _, pivots = M0.rref()
    j = 0
    for i in range(cols):
        is_independent = j  < len(pivots)  and pivots[j] == i
        if is_independent:
            indenepdent_state_vars_labels.append( network_matrix.x_hat_labels[i] )  
            independent_state_vars_cols.append(i)
            j += 1
        else:
            dependent_state_vars_labels.append(network_matrix.x_hat_labels[i])
            dependent_state_vars_cols.append(i)
    
    
    zero_rows = []
    
    for i in range(M0.rows):
        if M0[i,:].is_zero_matrix:
            zero_rows.append(i)
    zero_count = len(zero_rows)
    independent_count= len(indenepdent_state_vars_labels)
    dependent_count = len(dependent_state_vars_labels)
    
    Adi = Matrix(zero_count, independent_count, [0]*( zero_count*independent_count ))
    Add_inv = Matrix(zero_count, dependent_count, [0] *(zero_count * dependent_count) )
    Bd = Matrix( zero_count, B.cols, [0]*(zero_count *B.cols) )  # B.cols is the number of input variable
    
    
    forced_diode_switches = []
    for i in range(zero_count):
        
        row = zero_rows[i]
        
        # see if the rows of A is empty but B is not empty
        if A[row,:].is_zero_matrix and not B[row,:].is_zero_matrix:
            
            # network_matrix.print_M_matrix()
           
            # find nonzero labels of this row in the network.M matrix
            row_num_in_m = row + network_matrix.s_labels_size+ network_matrix.y_label_size
            
            row_in_m = network_matrix.M[row_num_in_m, :]
            offset = network_matrix.s_labels_size + network_matrix.y_label_size + network_matrix.x_hat_label_size
        
        
            for i in range( offset,   row_in_m.cols):
                if row_in_m[i] != 0:
                    lab = network_matrix.m_column_labels[i]
                    ele = network_matrix.m_column_labels_to_obj_map[lab]
                    if isinstance(ele, Diode):
                        forced_diode_switches.append(lab)
                    elif isinstance(ele, ExternalSwitch):
                        assert ele.element_current_name == sw_lab or ele.element_voltage_name == sw_lab
                    else:
                        pass
            
                        
        else:
            for j in range(dependent_count):
                col = dependent_state_vars_cols[j]
                Add_inv[i, j]  = A[row, col]
            for j in range(independent_count):
                col = independent_state_vars_cols[j]
                Adi[i,j] = A[row, col]
            
            for j in range(B.cols):
                Bd[i,j] = B[row, j]
        

            Add_inv = Add_inv.inv()
    
    return  forced_diode_switches, Add_inv, Adi, Bd, indenepdent_state_vars_labels, independent_state_vars_cols, dependent_state_vars_labels, dependent_state_vars_cols




def transfer_func_and_poles(A: Matrix, B: Matrix, C:Matrix, D:Matrix, symbolic_value_map):
    
    S = sp.symbols("s")
    I = Matrix(np.eye(A.shape[0]))
    transfer_func = simplify(  C*(S*I-A).inv() *B + D )
    
    poles = sp.factor(  sp.det(S*I-A))
    # Find poles (roots of the characteristic equation)
    poles_roots = sp.solve(poles.subs(symbolic_value_map), S)  # Alternatively, use roots(poles, s) for more detailed output

    return transfer_func, poles,poles_roots


# def backwardEulerIntegration(x_cur: np.ndarray, A: np.ndarray, B: np.ndarray, u: np.ndarray, time_t: float):
#     """
#     Implements Backward Euler integration for stiff systems
#     Using Padé approximation with p=0, q=1
    
#     Args:
#         x_cur: Current state vector
#         A: State matrix
#         B: Input matrix
#         u: Input vector
#         time_t: Time step
#     """
#     # Padé coefficients for p=0, q=1
#     eye = np.eye(A.shape[0], dtype=np.float32)
    
#     # Compute (I - dt*A)^(-1)
#     solver_matrix = np.linalg.inv(eye - time_t * A)
    
#     # State transition: x(t+dt) = (I - dt*A)^(-1) * x(t)
#     state_transition = solver_matrix @ x_cur
    
#     # Input integration: dt * (I - dt*A)^(-1) * B * u
#     input_effect = time_t * solver_matrix @ B @ u
    
#     return state_transition + input_effect

# @njit(parallel=True)
def backwardEulerIntegration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):
    # p = 0
    # q = 1
    # a = np.float32(0)
    #b = np.float32(-1/2)
    # time_t = np.float32(time_t)
    eye_a =  np.eye(A.shape[0], dtype=np.float32)
    
    # e_at_part =    (  eye_a+  A*time_t*a )@    np.linalg.inv( eye_a +A*time_t*b  )    
    
    # # e_at_part = (  eye_a+  A*time_t*a ) * (  eye_a +A*time_t*b )**-1
    
    # # integ_part = time_t*(1*a-1*b) * ( eye_a + A*time_t*b ) **-1
    
    # integ_part = time_t*  ( a-b ) * np.linalg.inv( eye_a + A*time_t*b )
    
    
    
    # https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Moler03.pdf
    # assume start from 0 - > result in coefficient
    # but still keep same integration method
    # but simplify alot, major issue with previous is did not use the inverse library of np
    p =0
    q = 1
    a1 = np.float32(0)  # because does not exist
    b1 = np.float32(-1)  #NOTE: new factor from the website
    e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 )
    integ_part = time_t * e_at_part
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 

    # # https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Moler03.pdf
    # # assume start from 0 - > result in coefficient
    # # also change to actual integration methods
    # p =0
    # q = 1
    # a1 = np.float32(0)  # because does not exist
    # b1 = np.float32(-1)
    # e_at_part = (  eye_a  + A*time_t*a1  ) * (  eye_a +A*time_t*b1 )**-1
    # integ_part = time_t*e_at_part
    # p1 = e_at_part @ x_cur 
    # p2 =  integ_part@ B @ u 
    # res = p1+p2
    # return  res 
# @njit(parallel=True)
def trapezoidalIntegration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):
    
    # p = 0
    # q = 1
    # a = np.float32(1/2)
    # b = np.float32(-1/2)
    # time_t = np.float32(time_t)
    eye_a =  np.eye(A.shape[0], dtype=np.float32)
    
    # e_at_part =    (  eye_a+  A*time_t*a )@    np.linalg.inv( eye_a +A*time_t*b  )    
    
    # # e_at_part = (  eye_a+  A*time_t*a ) * (  eye_a +A*time_t*b )**-1
    
    # # integ_part = time_t*(1*a-1*b) * ( eye_a + A*time_t*b ) **-1
    
    # integ_part = time_t*  ( a-b ) * np.linalg.inv( eye_a + A*time_t*b )
    
    
    # p1 = e_at_part @ x_cur 
    # p2 =  integ_part@ B @ u 
    # res = p1+p2
    # return  res 
   # https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Moler03.pdf
    # assume start from 0 - > result in coefficient
    # but still keep same integration method
    # but simplify a lot, by using the inverse library of np
    p =1
    q = 1
    a1 = np.float32(1/2)
    b1 = np.float32(-1/2)
    
    solver_part = np.linalg.inv(  eye_a +A*time_t*b1 )

    e_at_part = (  eye_a  + A*time_t*a1  ) @ solver_part
    integ_part = time_t*(a1-b1) * solver_part
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 
def parameter_for_two_wind_transformer(L1:float, L2:float, K: float):
    
    ne =  math.sqrt(L2/L1) # turn ratio
    M = K*math.sqrt(L1*L2)
    
    La =   (1-K)*L1
    Lu =   K*L1
    Lb =   (1-K)*L2
    print(Lb)
    print(ne**2*La)

    return La, Lu, Lb, (ne)

def parameter_for_two_wind_from_book(L1, L2, K):
    
    
    # try another version from the paper
    n = math.sqrt(L2 / L1)
    La = L1
    Lu = -(L1*(K**2 - 1))/K**2
    
    return La, Lu, n
    
    # n = K* math.sqrt(L2/L1)
    # M = K*math.sqrt(L1*L2)
    # La = (1-K**2)*L1
    # Lu = K**2*L1
    # return La, Lu, n #TODO?
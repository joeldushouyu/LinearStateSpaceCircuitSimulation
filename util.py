import scipy.integrate
import scipy.linalg
from Element import (
    Element, ExternalSwitch, Diode
)
from typing import Tuple
import sympy as sp
from sympy import Matrix, pi, pprint, Symbol, eye, zeros, simplify, BlockMatrix
from numba import njit, prange
import numpy as np
import numpy.typing as npt
import math
import sys
from scipy.integrate import solve_ivp


import scipy.linalg  
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

def print_matrix(A_matrix, column_names: list[str], row_names: list[str], file=sys.stdout):
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
    print(header,file=file)

    # Print rows with row labels
    for row_label, row in zip(row_names, A_matrix.tolist()):
        row_str = " ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row))
        print(f"{row_label:<{row_label_width}} {row_str}", file=file)


def print_matrix_for_matlab_format(matrix: Matrix, f=sys.stdout):

    print(f"\n [",file=f)
    arr = np.array(matrix).astype(float)
    rows = []
    for row in arr:
        row_str = ", ".join(f"{x:.8f}" for x in row)
        rows.append(row_str + ";")
    print("\n".join(rows),file=f)
    print("];")

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

    temp = matrix[:, current_ind].copy()
    matrix[:, current_ind] = matrix[:, voltage_ind].copy()
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
    m_pivots: list[int],
    m_labels:list[str],
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
    
    redundant_offset:int
) -> Tuple[Matrix]:
    assert capacitor_size + inductor_size == x_hat_labels_size == x_labels_size
    

    s_row_col_offset = redundant_offset

    y_row_col_offset = s_labels_size +s_row_col_offset 
    
    # s_row_col_offset = 0
    # y_row_col_offset = s_labels_size 
    x_hat_row_col_offset = y_labels_size + y_row_col_offset
    
    
        
    y_col_offset = s_labels_size +s_row_col_offset 
    # y_col_offset = s_labels_size
    x_hat_col_offset = y_labels_size + y_col_offset
    x_col_offset = x_hat_row_col_offset + x_hat_labels_size
    zero_offset = x_col_offset + x_labels_size
    u_col_offset = zero_offset + y_zero_labels_size + s_zero_labels_size

    # s_row_offset = 0
    # y_row_offset = s_labels_size
    # x_row_offset = y_row_offset + y_labels_size
    
    
    
    # those offset are ideal when network is consistent
    # but when network is no longer consistent, ie the pivots are not in sequential order
    


    inconsistent_labels:list[str] = []
    
    i = 0
    s_row_inconsistent_count = 0
    y_row_inconsistent_count = 0
    
    pivot_ind= 0
    for i in range(len(m_labels)):
        if m_pivots[pivot_ind] != i:
            lab = m_labels[i]
            if  i < y_row_col_offset:
                # inconsistent in switch row, which is unexpected?
                inconsistent_labels.append(lab)
                s_row_inconsistent_count += 1
            elif i < x_hat_row_col_offset:
                y_row_inconsistent_count += 1   #indicate dependency exist in the state variables
                inconsistent_labels.append(lab)
       
            else:
                pivot_ind += 1
                # dependency in x  raise ValueError("Unexpected case")        
                pass
        else:
            pass # all good
            pivot_ind +=1

        if pivot_ind == len(m_pivots):
            break # 
    
    # update
    
    y_row_col_offset -= s_row_inconsistent_count
    x_hat_row_col_offset -= ( s_row_inconsistent_count + y_row_inconsistent_count)
    

    s_dxdt = -M[s_row_col_offset:y_row_col_offset, x_hat_col_offset:x_col_offset]
    Sx = -M[s_row_col_offset:y_row_col_offset, x_col_offset:zero_offset]
    Su = -M[s_row_col_offset:y_row_col_offset, u_col_offset:u_col_offset+voltage_source_size+current_source_size ]

    C1 = -M[y_row_col_offset:x_hat_row_col_offset, x_hat_col_offset:x_col_offset]
    C = -M[y_row_col_offset:x_hat_row_col_offset, x_col_offset:zero_offset]
    D = -M[y_row_col_offset:x_hat_row_col_offset, u_col_offset: u_col_offset+voltage_source_size+current_source_size]

    M0 = M[x_hat_row_col_offset:x_hat_row_col_offset+ x_hat_labels_size , x_hat_col_offset:x_col_offset]
    A = -M[x_hat_row_col_offset:x_hat_row_col_offset+x_hat_labels_size, x_col_offset:zero_offset]
    B = -M[x_hat_row_col_offset:x_hat_row_col_offset+x_hat_labels_size, u_col_offset: u_col_offset+voltage_source_size+current_source_size]
    
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
    Ddsw_vs = Csw_il * BLvs + Csw_vc * BCvs
    # if current_source_size == 0:
    #      Ddsw_vs = Csw_vc*BCvs
    # else:
    #     Ddsw_vs = Csw_il*BLis + Csw_vc*BCvs
    
    
    # if current_source_size >0 and voltage_source_size >0:
    t1 = [ Cdsw_iL , Cdsw_vC]
    t2  = [  Ddsw_is , Ddsw_vs]
    
    t1_useful = [x for x in t1 if len(x) > 0]
    t2_useful = [x for x in t2 if len(x) > 0]
    
    # C_sw = Matrix(BlockMatrix(t1_useful))
    # D_sw = Matrix(BlockMatrix(t2_useful))
    
    if len(t1_useful) == 0:
        C_sw =  zeros(  C.shape[0], C.shape[1])
    else:
        C_sw = Matrix(BlockMatrix(t1_useful))
    if len(t2_useful) == 0:
        D_sw = zeros(D.shape[0], D.shape[1])
    else:
        D_sw = Matrix(BlockMatrix(t2_useful))
    return s_dxdt, Sx, Su, C1, C, D, M0, A, B,C_sw,D_sw, inconsistent_labels


def detemrminte_matrix_for_dependent_state_vars(M0: Matrix, A: Matrix, B: Matrix, x_hat_labels:list[str]):
    


    M0, pivots = M0.rref()
    
    independent_state_row_col_map:dict[str, list[int]] = {}
    dependent_state_row_col_map:dict[str, list[int]] = {}
    
        
    # first, process the independent, ie the pivots
    for i  in range(len(pivots)):
        pivot_col = pivots[i]
        pivot_row = i   # by def, pivots are the first nonzero in each row: if pivots-> also 

        label = x_hat_labels[pivot_col]
        
        independent_state_row_col_map[label] = [pivot_row, pivot_col]
        
    dependent_row_start = len(pivots)
    for i in range(M0.cols):
        if i not in pivots:
            label = x_hat_labels[i]
            dependent_state_row_col_map[label] = [dependent_row_start, i]
            dependent_row_start += 1
    

    A_x_independent_filter = Matrix(A.rows, A.cols, [0]*(A.rows *A.cols ))  
    A_dependent =  Matrix(A.rows, A.cols, [0]*(A.rows *A.cols ))   
    B_dependent = Matrix(B.rows, B.cols, [0]*(B.rows *B.cols ) )   

    zero_M0 = Matrix( 1, M0.cols, [0]*M0.cols )
    zero_A = Matrix(1, A.cols, [0]*A.cols)
    zero_B = Matrix(1, B.cols, [0]*B.cols)

    A_temp = A[:,:]
    B_temp = B[:,:]
    M0_temp = M0[:,:]
    
    assert len(x_hat_labels) == M0.cols == M0.rows
    for var_ind in range(len(x_hat_labels)):
        var_label = x_hat_labels[var_ind]
        
        if var_label in independent_state_row_col_map:
            independent_row = independent_state_row_col_map[var_label][0]
            independent_col = independent_state_row_col_map[var_label][1]
            assert independent_col == var_ind
            
            M0[var_ind, :] = M0_temp[independent_row, :  ].copy()
            A[var_ind, :] = A_temp[independent_row, :].copy()
            B[var_ind, :] = B_temp[independent_row, :].copy()
        else:
            dependent_row = dependent_state_row_col_map[var_label][0]
            dependent_col = dependent_state_row_col_map[var_label][1]
            assert dependent_col == var_ind
            
            M0[var_ind, :] = zero_M0[:, :]
            
            ajk =  A_temp[dependent_row, dependent_col] # 8-58

            if ajk == 0:
                factor =0
            else:
                factor = -(1/ajk)
                
            A_temp[dependent_row, dependent_col] = 0
            
            A_dependent[var_ind , :] = factor *  A_temp[dependent_row, :].copy()
            B_dependent[var_ind, :] =  factor *  B_temp[dependent_row, :].copy()
            A[var_ind, :] = zero_A[:,:].copy()
            B[var_ind, :]  = zero_B[:,:].copy()
            
            A_x_independent_filter[var_ind, var_ind] = -1
    
    
    return M0, A, B, A_x_independent_filter,A_dependent,B_dependent, [x for x in independent_state_row_col_map.keys()], [x for x in dependent_state_row_col_map.keys()]
            
            
        
                

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
    
    
    
    # check if any inconsistent actually occurs
    
    
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
#     eye = np.eye(A.shape[0], dtype=np.float64)
    
#     # Compute (I - dt*A)^(-1)
#     solver_matrix = np.linalg.inv(eye - time_t * A)
    
#     # State transition: x(t+dt) = (I - dt*A)^(-1) * x(t)
#     state_transition = solver_matrix @ x_cur
    
#     # Input integration: dt * (I - dt*A)^(-1) * B * u
#     input_effect = time_t * solver_matrix @ B @ u
    
#     return state_transition + input_effect

# @njit(parallel=True)

def radauIntegration(x_cur: np.ndarray, A: np.ndarray, B: np.ndarray, u: np.ndarray, time_t: float):
    """
    Implements 3rd order Radau IIA integration for stiff systems.
    This method is L-stable and particularly suitable for stiff problems.
    
    Args:
        x_cur: Current state vector
        A: State matrix
        B: Input matrix
        u: Input vector
        time_t: Time step
    """
    # A = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]])  # Example 4x4 matrix
    # B = np.array([[0], [1], [0], [0]])  # Example 4x1 matrix (input matrix)
    #u = np.array([1])  # Constant input (scalar)
    t_span = [0, time_t]  # Time span for one step

    # Define the derivative function
    # Define the derivative function
    def lti_system(t, x):
        # Ensure that both A @ x and B @ u are 1D arrays (of shape (n,))
        return np.squeeze(A @ x + B @ u)

    # Ensure x_cur is 1D (flatten if necessary)
    x_cur = x_cur.flatten()
    u = u.flatten()
    # Solve the system
    solution = solve_ivp(
        lti_system,
        t_span=t_span,
        y0=x_cur,  # y0 must be 1-dimensional
        method='Radau'
    )

    # Return the state at the end of the integration
    return np.reshape(solution.y[:, -1], (-1, 1))



def backwardEulerIntegration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):
    # p = 0
    # q = 1
    # a = np.float64(0)
    #b = np.float64(-1/2)
    # time_t = np.float64(time_t)
    eye_a =  np.eye(A.shape[0], dtype=np.float64)
    
    # e_at_part =    (  eye_a+  A*time_t*a )@    np.linalg.inv( eye_a +A*time_t*b  )    
    
    # # e_at_part = (  eye_a+  A*time_t*a ) * (  eye_a +A*time_t*b )**-1
    
    # # integ_part = time_t*(1*a-1*b) * ( eye_a + A*time_t*b ) **-1
    
    # integ_part = time_t*  ( a-b ) * np.linalg.inv( eye_a + A*time_t*b )
    
    
    
    # #https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Moler03.pdf
    # # assume start from 0 - > result in coefficient
    # # but still keep same integration method
    # # but simplify alot, major issue with previous is did not use the inverse library of np
    p =0
    q = 1
    a1 = np.float64(0)  # because does not exist
    b1 = np.float64(-1)  #NOTE: new factor from the website
    e_at_part = e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 ) #np.linalg.solve(eye_a + A*time_t*b1, eye_a) #e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 )
    

    integ_part = time_t * e_at_part
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 
    # eye_a = np.eye(A.shape[0], dtype=np.float64)
    # solver_matrix = np.linalg.inv(eye_a - time_t * A)
    # return solver_matrix @ (x_cur + time_t * B @ u)

    # # for now, implement expm use np
    # eye_a = np.eye(A.shape[0], dtype=np.float64)
    # solver_matrix = np.linalg.inv(eye_a - time_t * A)
    # return solver_matrix @ (x_cur + time_t * B @ u)
    # https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Moler03.pdf
    # assume start from 0 - > result in coefficient
    # also change to actual integration methods
    # p =0
    # q = 1
    # a1 = np.float64(0)  # because does not exist
    # b1 = np.float64(-1)
    # e_at_part = (  eye_a  + A*time_t*a1  ) * (  eye_a +A*time_t*b1 )**-1
    # integ_part = time_t*e_at_part
    # p1 = e_at_part @ x_cur 
    # p2 =  integ_part@ B @ u 
    # res = p1+p2
    # return  res 

# def trapezoidalIntegration(x_cur: np.ndarray, A: np.ndarray, B: np.ndarray, u: np.ndarray, time_t: float):
#     """
#     Performs trapezoidal integration for solving a linear, time-invariant system.

#     Parameters:
#     x_cur : np.ndarray
#         Current state vector of the system (x_k).
#     A : np.ndarray
#         State matrix of the LTI system.
#     B : np.ndarray
#         Input matrix of the LTI system.
#     u : np.ndarray
#         Input vector applied to the system (u_k).
#     time_t : float
#         Time step size (\Delta t).

#     Returns:
#     np.ndarray
#         Updated state vector (x_{k+1}).
#     """
#     eye_a =  np.eye(A.shape[0], dtype=np.float64)
    
#     # state_trans = scipy.linalg.expm(A *time_t)
#     # zero_input_response = state_trans @x_cur
    
#     # zero_value_response =   time_t/2 *( eye_a +  state_trans ) @B @u
    
#     # return zero_input_response + zero_value_response
    

    
#     # Rearranging the equation:
#     # (I - (h/2)A)x(t+h) = (I + (h/2)A)x(t) + (h/2)B(u(t) + u(t+h))
#     # Assuming u(t+h) ≈ u(t) for simplicity
    
#     solver_matrix = np.linalg.inv(eye_a - (time_t/2) * A)
#     x_next = solver_matrix @ ((eye_a + (time_t/2) * A) @ x_cur + time_t * B @ u)
    
#     return x_next


# @njit(parallel=True)
def trapezoidalIntegration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):
    
    # p = 0
    # q = 1
    # a = np.float64(1/2)
    # b = np.float64(-1/2)
    # time_t = np.float64(time_t)
    eye_a =  np.eye(A.shape[0], dtype=np.float64)
    
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
    a1 = np.float64(1/2)
    b1 = np.float64(-1/2)
    
    solver_part =solver_part = np.linalg.inv(  eye_a +A*time_t*b1 ) # np.linalg.solve(eye_a + A*time_t*b1, eye_a) #solver_part = np.linalg.inv(  eye_a +A*time_t*b1 )

    e_at_part = (  eye_a  + A*time_t*a1  ) @ solver_part
    integ_part = time_t*(a1-b1) * solver_part
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 
    
    # I = np.eye(A.shape[0])  # Identity matrix of size n x n
    
    # # Compute the matrix to invert
    # inv_matrix = np.linalg.inv(I - (time_t / 2) * A)
    
    # # Compute intermediate terms
    # term1 = (I + (time_t / 2) * A) @ x_cur  # (I + h/2 * A) * x_k
    # term2 = (time_t / 2) * B @ ( 2*u)  # h/2 * B * (u_k + u_k+1) # assume u is the same
    
    # # Compute the next state
    # x_next = inv_matrix @ (term1 + term2)
    # return x_next
    
    # 
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
    


def parameter_for_three_wind_transformer(Lp, L1, L2, K12, K13, K23):
    decimal_precision = 3
    # https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=703254
    M12= K12*math.sqrt(Lp *L1)
    M13 = K13*math.sqrt(Lp*L2)
    M23 = K23*math.sqrt(L1*L2)
    L = Matrix([[Lp, M12, M13 ], 
                    [M12, L1, M23], 
                    [M13, M23, L2]])
    B = L.inv()
    
    n1 = 1
    n2 = L[0,1]/L[0,0]
    n3 = L[0,2]/L[0,0]
    
    l12 = -1/(n1*n2*B[0,1])
    l13 = -1/(n1*n3*B[0,2])
    l23 = -1/(n2*n3*B[1,2])
    
    L02 = (n2**2) * 1/( (1/l12) +(1/l23) )
    L03 = (n3**2) * 1/( (1/l13) + (1/l23) )
    
    
    
    VT2_factor =[   round(L02/(n2*l12),decimal_precision), round( L02/(n2*n3*l23),decimal_precision) ]
    VT3_factor = [ round(L03/(n3*l13),decimal_precision) , round(L03/(n2*n3*l23),decimal_precision)]
    
    return [round(n2,decimal_precision), round(n3,decimal_precision)], VT2_factor, VT3_factor, [Lp , L02, L03]
    
    
    
# output
# Helper function to convert matrix to string representation
def matrix_to_string(matrix, col_labels, row_labels):
    output = []
    # Add column headers
    output.append("\t" + "\t".join(str(label) for label in col_labels))
    
    # Add rows with labels
    for i, row in enumerate(matrix):
        row_str = f"{row_labels[i]}\t" + "\t".join(f"{val:8.3f}" if isinstance(val, (int, float)) else str(val) for val in row)
        output.append(row_str)
    
    return "\n".join(output)

def write_matrix_info(net, filename="matrix_output.txt"):

    s_dxdt, Sx, Su, C1, C, D, M0, A, B, C_SW, D_SW = retrieveSystemMatrix(
        M=net.M,
        s_labels_size=net.s_labels_size,
        y_labels_size=net.y_label_size,
        x_hat_labels_size=net.x_hat_label_size,
        x_labels_size=net.x_label_size,
        y_zero_labels_size=net.y_zero_label_size,
        s_zero_labels_size=net.s_zero_label_size,
        capacitor_size= net.capacitor_size,
        inductor_size=net.inductor_size,
        voltage_source_size=net.voltage_source_size,
        current_source_size=net.current_source_Size
        
    )
    with open(filename, 'w') as f:
        # Helper function to write both to console and file
        def dual_print(text):
            print(text)
            f.write(str(text) + '\n')

        # Print matrix M with labels
        print_matrix(net.M, net.m_column_labels, ["" for x in range(net.M.shape[0])])
        f.write("\nMatrix M with labels:\n")
        f.write(matrix_to_string(net.M, net.m_column_labels, ["" for x in range(net.M.shape[0])]) + '\n')

        # Print all other matrices
        matrices = {
            "s_dxdt": s_dxdt,
            "sx": Sx,
            "su": Su,
            "C1": C1,
            "C": C,
            "D": D,
            "M0": M0,
            "A": A,
            "B": B,
            "C_SW": C_SW,
            "D_SW": D_SW
        }

        for name, matrix in matrices.items():
            dual_print(f"\n{name}")
            dual_print(matrix)
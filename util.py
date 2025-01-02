from Element import (
    Element,
)
from typing import Tuple

from sympy import Matrix, pi, pprint, Symbol, eye, zeros
from numba import njit, prange
import numpy as np
import numpy.typing as npt
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
    s_labels: list[str],
    y_labels: list[str],
    x_hat_labels: list[str],
    x_labels: list[str],
    y_zero_labels: list[str],
    s_zero_labels: list[str],
) -> Tuple[Matrix]:
    y_col_offset = len(s_labels)
    x_hat_col_offset = len(s_labels) + y_col_offset
    x_col_offset = x_hat_col_offset + len(x_hat_labels)
    zero_offset = x_col_offset + len(x_labels)
    u_col_offset = zero_offset + len(y_zero_labels) + len(s_zero_labels)

    s_row_offset = 0
    y_row_offset = len(s_labels)
    x_row_offset = y_row_offset + len(y_labels)
    s_dxdt = -M[s_row_offset:y_row_offset, x_hat_col_offset:x_col_offset]
    Sx = -M[s_row_offset:y_row_offset, x_col_offset:zero_offset]
    Su = -M[s_row_offset:y_row_offset, u_col_offset:]

    C1 = -M[y_row_offset:x_row_offset, x_hat_col_offset:x_col_offset]
    C = -M[y_row_offset:x_row_offset, x_col_offset:zero_offset]
    D = -M[y_row_offset:x_row_offset, u_col_offset:]

    M0 = M[x_row_offset:, x_hat_col_offset:x_col_offset]
    A = -M[x_row_offset:, x_col_offset:zero_offset]
    B = -M[x_row_offset:, u_col_offset:]

    return s_dxdt, Sx, Su, C1, C, D, M0, A, B




def determine_dependent_state_vars(M0: Matrix, A:Matrix, B:Matrix, x_hat_labels:list[str]):
    
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
            indenepdent_state_vars_labels.append( x_hat_labels[i] )  
            independent_state_vars_cols.append(i)
            j += 1
        else:
            dependent_state_vars_labels.append(x_hat_labels[i])
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
    
    
    
    for i in range(zero_count):
        
        row = zero_rows[i]
        
        # see if the rows of A is empty but B is not empty
        if A[row,:].is_zero_matrix and not B[row,:].is_zero_matrix:
            pass  # TODO: network inconsistent
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
    
    return Add_inv, Adi, Bd, indenepdent_state_vars_labels, independent_state_vars_cols, dependent_state_vars_labels, dependent_state_vars_cols



# @njit(parallel=True)
def backwardEulerIntegration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):
    # pade approximation of y=0    
    p = 1
    q= 1
    a = np.float32( 0)
    b = np.float32(-1/2)
    time_t = np.float32(time_t)
    # e_at_part = (  eye(A.shape[0]) + A*time_t*a ) *  (  eye(A.shape[0])  + A*time_t*b )**-1
    # integ_part = time_t*(1*a-1*b)* (   eye(A.shape[0])  + A*time_t*b )**-1 
    eye_a =  np.eye(A.shape[0], dtype=np.float32)
      
    
    e_at_part =    (  eye_a+  A*time_t*a )@    np.linalg.inv( eye_a +A*time_t*b  )    
    
    # e_at_part = (  eye_a+  A*time_t*a ) * (  eye_a +A*time_t*b )**-1
    
    # integ_part = time_t*(1*a-1*b) * ( eye_a + A*time_t*b ) **-1
    
    integ_part = time_t*  ( a-b ) * np.linalg.inv( eye_a + A*time_t*b )
    
    
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 



# @njit(parallel=True)
def trapezoidalIntegration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):
    
    p = 0
    q = 1
    a = np.float32(1/2)
    b = np.float32(-1/2)
    time_t = np.float32(time_t)
    eye_a =  np.eye(A.shape[0], dtype=np.float32)
    
    e_at_part =    (  eye_a+  A*time_t*a )@    np.linalg.inv( eye_a +A*time_t*b  )    
    
    # e_at_part = (  eye_a+  A*time_t*a ) * (  eye_a +A*time_t*b )**-1
    
    # integ_part = time_t*(1*a-1*b) * ( eye_a + A*time_t*b ) **-1
    
    integ_part = time_t*  ( a-b ) * np.linalg.inv( eye_a + A*time_t*b )
    
    
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 
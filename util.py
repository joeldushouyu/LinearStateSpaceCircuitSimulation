import scipy.integrate
import scipy.linalg
from Element import (
    Element, ExternalSwitch, Diode, Capacitor, Inductor,VoltageCurrentSource
)
from typing import Tuple
import sympy as sp
from sympy import Matrix, pi, pprint, Symbol, eye, zeros, simplify, BlockMatrix
from numba import njit, prange
import numpy as np
import numpy.typing as npt
import sys
from scipy.integrate import ode,solve_ivp
import math


    
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







def reogranize_matrix_by_row_col_mapping(matrix: Matrix, old_lab_row_idx_mapping:dict[str, int], old_lab_col_idx_mapping:dict[str, int],
                                         new_lab_row_idx_mapping:dict[str, int], new_lab_col_idx_mapping:dict[str, int]
                                         ):
    
    num_rows = len(new_lab_row_idx_mapping)
    num_cols = len(new_lab_col_idx_mapping)

# Create a new zero matrix with the desired dimensions
    new_matrix = sp.zeros(num_rows, num_cols)

    # Populate the new matrix
    for new_row_label, new_row_idx in new_lab_row_idx_mapping.items():
        for new_col_label, new_col_idx in new_lab_col_idx_mapping.items():
            # Get the original row and column indices
            original_row_idx = old_lab_row_idx_mapping[new_row_label]
            original_col_idx = old_lab_col_idx_mapping[new_col_label]
            
            # Assign the value from the original matrix to the new matrix
            new_matrix[new_row_idx, new_col_idx] = matrix[original_row_idx, original_col_idx]
    return new_matrix


def apply_inductance_capactiance_to_state_matrix(cap_parallel_ind_series_ind_dep_mapping:dict[str,list[str]],
                                                M0_I: Matrix, A: Matrix, B: Matrix, C: Matrix, D: Matrix, x_hat_label_to_obj_map:dict[list, Element],
                                                independent_state_number:int, dependent_state_number:int,
                                                symbol_to_value_map:dict[Symbol, ],
                                                ind_dep_A_row_idx_map:dict[str, list[int]], 
                                                ind_dep_A_col_idx_map:dict[str, list[int]]
                                                 ):
    


    # update M0 based on any natual independent/dependent in M0
    M0_I_res = sp.zeros( independent_state_number + dependent_state_number)
    M0_I_res[:independent_state_number, :independent_state_number] = sp.eye(independent_state_number)
    # Get M0_I to be in the same format as plexim
    for ind_label, col in ind_dep_A_col_idx_map.items():
        if ind_label in cap_parallel_ind_series_ind_dep_mapping:
            for dep_lab in cap_parallel_ind_series_ind_dep_mapping[ind_label]:
                dep_row  = ind_dep_A_row_idx_map[ dep_lab ]
                
                M0_I_res[dep_row, col] = 1  

    E = Matrix(independent_state_number, independent_state_number, [0]*independent_state_number *independent_state_number)
    
    for row_lab, row_idx in ind_dep_A_row_idx_map.items():
        for col_lab, col_idx in ind_dep_A_col_idx_map.items():
            
            if row_idx >= independent_state_number or col_idx >= independent_state_number:
                continue
            
            
            if  row_lab  == col_lab:
                ele = x_hat_label_to_obj_map[row_lab]
                if isinstance(ele, Capacitor):
                    E[row_idx, col_idx] =ele.capacitance
                    # apply the affect of parallel capacitor
                    if row_lab in cap_parallel_ind_series_ind_dep_mapping:
                        parallel_capacitor_labels:list[str] = cap_parallel_ind_series_ind_dep_mapping[row_lab]
                        for parallel_lab in parallel_capacitor_labels:
                            parallel_element = x_hat_label_to_obj_map[parallel_lab]
                            assert isinstance(parallel_element, Capacitor)
                            E[row_idx, col_idx ] += parallel_element.capacitance
                else:
                    assert isinstance(ele, Inductor)
                    E[row_idx, col_idx] = ele.inductance
                    
                    # apply the affect of inductor in series
                    if row_lab in cap_parallel_ind_series_ind_dep_mapping:
                        series_inductor_labels:list[str] = cap_parallel_ind_series_ind_dep_mapping[row_lab]
                        for ser_lab in series_inductor_labels:
                            series_element = x_hat_label_to_obj_map[ser_lab]
                            assert isinstance(series_element, Inductor)
                            E[row_idx, col_idx] += series_element.inductance
                
            else:
                # check for possible mutual inductance affect
                row_ele = x_hat_label_to_obj_map[row_lab]
                col_ele = x_hat_label_to_obj_map[col_lab]
                
                if isinstance(row_ele, Inductor)  and isinstance(col_ele, Inductor) and row_ele.name in col_ele.mutual_inductor_names:
                    K_factor_ind = col_ele.mutual_inductor_names.index(row_ele.name)
                    E[row_idx, col_idx] = col_ele.K_factors[K_factor_ind] * sp.sqrt(col_ele.inductance*row_ele.inductance)
                    
    
    A11 = sp.matrix2numpy( A[:independent_state_number, :independent_state_number], dtype=np.float64)
    A12 = sp.matrix2numpy(A[:independent_state_number, independent_state_number:], dtype=np.float64)
    A21 = sp.matrix2numpy(A[independent_state_number:, :independent_state_number], dtype=np.float64)
    A22 = sp.matrix2numpy(A[independent_state_number:, independent_state_number:], dtype=np.float64)
    
    B1 = sp.matrix2numpy( B[:independent_state_number, :], dtype=np.float64)
    B2 = sp.matrix2numpy(B[independent_state_number:, :], dtype=np.float64)
    C1 = sp.matrix2numpy(C[:, :independent_state_number], dtype=np.float64)
    C2 = sp.matrix2numpy(C[:, independent_state_number:], dtype=np.float64)
    
    
    E = E.subs(symbol_to_value_map)
    E_np = sp.matrix2numpy(E, dtype=np.float64)
    E_inverse = np.linalg.inv(E_np)
    A22_inverse = np.linalg.inv(A22)
    A11_new = E_inverse@( A11 - A12@A22_inverse@A21)
    A12_new = sp.zeros(A12.shape[0], A12.shape[1])
    A21_new = sp.zeros(A21.shape[0], A21.shape[1])
    A22_new = sp.zeros( A22.shape[0], A22.shape[1] )
    B1_new = E_inverse @(B1 - A12@A22_inverse@B2)
    B2_new = sp.zeros(B2.shape[0], B2.shape[1])
    
    
    C1_new = C1-C2@A22_inverse@A21
    C2_new = sp.zeros(C2.shape[0], C2.shape[1])
    
    D_new = D-C2@A22_inverse@B2
    
    
    A11_dependent_matrix = sp.eye(independent_state_number) # simplify a copye of A11 matrix
    A21_dependent_matrix = -1*A22_inverse@A21
    B2_dependent_matrix = -1*A22_inverse@B2
    B1_dependent_matrix = sp.zeros(B1.shape[0], B1.shape[1])
    A12_dependent_matrix = sp.zeros( independent_state_number, dependent_state_number)
    A22_dependent_matrix = sp.zeros(dependent_state_number, dependent_state_number)
        


    
    A_res = sp.BlockMatrix( [ [ Matrix(A11_new),  Matrix(A12_new)],
                             [Matrix(A21_new), Matrix(A22_new)]]   )
    B_res = sp.BlockMatrix([ [Matrix(B1_new)], 
                            [Matrix(B2_new)] ])
    C_res = sp.BlockMatrix(  [ [Matrix(C1_new), 
                                Matrix(C2_new)]] )
    D_res =  sp.Matrix(D_new)
    
    A_dependent_res = sp.BlockMatrix( [  [Matrix(A11_dependent_matrix),  Matrix(A12_dependent_matrix)],
                                        [Matrix(A21_dependent_matrix), Matrix(A22_dependent_matrix)]]  )
    B_dependent_res = sp.BlockMatrix( [  [Matrix(B1_dependent_matrix)],
                                       [ Matrix(B2_dependent_matrix)]] )
    
    return M0_I_res, A_res, B_res, C_res, D_res, A_dependent_res, B_dependent_res                 
            
    
def determine_dependent_independent_state_mapping(M0_I: Matrix, A_raw:Matrix,  m_pivots:list[int], u_labels:list[str], y_labels:list[str], x_hat_labels: list[str], x_hat_col_offset_in_m_pivots:int  ):
    
    
    # could have two possible scenario when there exist dependency
    
    #TODO: add more doc in the future
    
    independent_state_row_col_map:dict[str, list[int]] = {}
    dependent_state_row_col_map:dict[str, list[int]] = {}
    # determine the the dependent/independent state variabls with their row/column
    _,M0_pivots = M0_I.rref() 
    
    
    
    #NOTE: remember by def of pivot, pivot row is the first nonzero value in that pivot column
    
    # start by looking from dependency state first
    
    # dependency state happen when pivots exist in the correspong "x" label column, not "x_hat" label column
    dependent_col_offset = x_hat_col_offset_in_m_pivots+len(x_hat_labels)
    dependent_pivot_col = [col for col in m_pivots if col >=dependent_col_offset]
    
    for col in dependent_pivot_col:
        col_in_A = col-dependent_col_offset
        if col_in_A  >=len(x_hat_labels):
            # means is a force trigger related
            continue
        label = x_hat_labels[col_in_A]
        A_col = A_raw[:, col_in_A]
        pivot_row = None
        for row in range(A_col.rows):
            if A_col[row] != 0:
                pivot_row = row
                break
        assert pivot_row is not None
        
        dependent_state_row_col_map[label] = [pivot_row, col_in_A]
    
    # state dependency
    # for marking elements that are naturally dependent on another element
    # this happen in capacitors in parallel or inductor in series
    
    cap_parallel_ind_series_ind_dep_mapping:dict[str, list[str]] = {}
    
    
    
    for index in range(len(M0_pivots)):
        # assert M0_pivots[index] == m_pivots[ index + x_hat_col_offset_in_m_pivots ]
        pivot_col = M0_pivots[index]
        label = x_hat_labels[pivot_col]
        pivot_row = index # by def, pivots are the first nonzero in each row
        if label in dependent_state_row_col_map:
            # scenario where on state are idential to another state
            # for example, two inductor in series or two capacitor in parallel. I_L / V_C is the same for both element
            # there should be another 1's column in the same row
            
            M0_I_row = M0_I[pivot_row, :]
            assert math.isclose(M0_I_row[pivot_col] , 1)
            new_pivot_col = None
            for new_col in range(pivot_col+1,  M0_I_row.cols):
                if math.isclose( M0_I_row[new_col], 1):
                    new_pivot_col = new_col
            assert new_pivot_col is not None
            # update new pivot col, 
            pivot_col = new_pivot_col  

            if x_hat_labels[pivot_col]  not in cap_parallel_ind_series_ind_dep_mapping:
                cap_parallel_ind_series_ind_dep_mapping[ x_hat_labels[pivot_col] ] = [label]
            else:
                cap_parallel_ind_series_ind_dep_mapping[ x_hat_labels[pivot_col] ].append(label)

            label = x_hat_labels[pivot_col]
        else:
            pass
        independent_state_row_col_map[label] = [pivot_row, pivot_col]

    
    
    sys_A_row_idx_map:dict[str, int]  = {}
    sys_A_col_idx_map:dict[str, int] = {}
    
    sys_B_row_idx_map:dict[str, int ] = {}
    sys_B_col_idx_map:dict[str, int] = {}
    
    sys_C_row_idx_map:dict[str,int] = {}
    sys_C_col_idx_map:dict[str,int] = {}

    final_sys_A_row_idx_map:dict[str, int]  = {}
    final_sys_A_col_idx_map:dict[str, int] = {}
    
    final_sys_B_row_idx_map:dict[str, int ] = {}
    final_sys_B_col_idx_map:dict[str, int] = {}

    final_sys_C_row_idx_map:dict[str,int] = {}
    final_sys_C_col_idx_map:dict[str,int] = {}


    ind_dep_A_row_idx_map:dict[str, int] = {}
    ind_dep_A_col_idx_map:dict[str, int] = {}
    
    ind_dep_B_row_idx_map:dict[str, int] = {}
    ind_dep_B_col_idx_map:dict[str, int] = {}
    
    ind_dep_C_row_idx_map:dict[str, int] = {}
    ind_dep_C_col_idx_map:dict[str, int] = {}
    

    

    # the final index should be in the order define in x_hat_labe, y_label, and u_label
    for index, y_lab in enumerate(y_labels):
        final_sys_C_row_idx_map[y_lab] = index

    for index, u_lab in enumerate(u_labels):
        final_sys_B_col_idx_map[u_lab] = index
    for index, x_hat_lab in enumerate(x_hat_labels):
        final_sys_A_col_idx_map[x_hat_lab] = index
        final_sys_A_row_idx_map[x_hat_lab] = index
        final_sys_C_col_idx_map[x_hat_lab] = index
        final_sys_B_row_idx_map[x_hat_lab] = index

    for index, y_lab in enumerate(y_labels):
        sys_C_row_idx_map[y_lab] = index
        ind_dep_C_row_idx_map[y_lab] = index
    
    for index, u_lab in enumerate(u_labels):
        sys_B_col_idx_map[u_lab] = index
        ind_dep_B_col_idx_map[u_lab] = index

    index = 0
    for lab, system_row_col in independent_state_row_col_map.items():
        ind_dep_A_row_idx_map[lab] = index
        ind_dep_A_col_idx_map[lab] = index
        
        sys_A_row_idx_map[lab] = system_row_col[0]
        sys_A_col_idx_map[lab] = system_row_col[1]

        sys_B_row_idx_map[lab] = system_row_col[0]
        ind_dep_B_row_idx_map[lab] = index
        
        sys_C_col_idx_map[lab] = system_row_col[1]
        ind_dep_C_col_idx_map[lab] = index
        
        index +=1
    for lab, system_row_col in dependent_state_row_col_map.items():
        ind_dep_A_row_idx_map[lab] = index
        ind_dep_A_col_idx_map[lab] = index
        
        sys_A_row_idx_map[lab] = system_row_col[0]
        sys_A_col_idx_map[lab] = system_row_col[1]

        sys_B_row_idx_map[lab] = system_row_col[0]
        ind_dep_B_row_idx_map[lab] = index
        
        sys_C_col_idx_map[lab] = system_row_col[1]
        ind_dep_C_col_idx_map[lab] = index
        index +=1

    
    
    
    
    
    
    return cap_parallel_ind_series_ind_dep_mapping,  independent_state_row_col_map,dependent_state_row_col_map,  \
        sys_A_row_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map, final_sys_A_row_idx_map, final_sys_A_col_idx_map,\
            sys_B_row_idx_map,sys_B_col_idx_map,ind_dep_B_row_idx_map,ind_dep_B_col_idx_map, final_sys_B_row_idx_map, final_sys_B_col_idx_map,\
                sys_C_row_idx_map,sys_C_col_idx_map,ind_dep_C_row_idx_map,ind_dep_C_col_idx_map, final_sys_C_row_idx_map, final_sys_C_col_idx_map


def update_system_matrix_to_reflect_dependency(M0: Matrix,
                                               Q:Matrix,
                                               C1:Matrix,
                                               A: Matrix, B: Matrix, C: Matrix, D: Matrix,
                                               m_pivots:list[int], 
                                               u_labels:list[str],
                                               y_labels:list[str],
                                               y_dependent_labels:list[str],
                                               x_hat_labels: list[str], x_hat_col_offset_in_m_pivots:int,
                                                x_hat_label_to_obj_map:dict[str, Element],
                                                element_name_to_obj_map:dict[str, Element],
                                                symbol_to_value_map:dict[Symbol, ],
                                               ):
    
    
    
    if len(y_dependent_labels):
        # means there is dependent in y output
        independent_y_labels= [x for x in y_labels if x not in y_dependent_labels]
    else:
        independent_y_labels = y_labels    
    
    cap_parallel_ind_series_ind_dep_mapping, independent_state_row_col_map,dependent_state_row_col_map,  \
        sys_A_row_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map, final_sys_A_row_idx_map, final_sys_A_col_idx_map,\
            sys_B_row_idx_map,sys_B_col_idx_map,ind_dep_B_row_idx_map,ind_dep_B_col_idx_map, final_sys_B_row_idx_map, final_sys_B_col_idx_map,\
                sys_C_row_idx_map,sys_C_col_idx_map,ind_dep_C_row_idx_map,ind_dep_C_col_idx_map, final_sys_C_row_idx_map, final_sys_C_col_idx_map= determine_dependent_independent_state_mapping(

        M0_I=M0, A_raw=A, m_pivots=m_pivots, x_hat_labels=x_hat_labels, x_hat_col_offset_in_m_pivots=x_hat_col_offset_in_m_pivots,
        u_labels=u_labels, y_labels=independent_y_labels
    )
    M0_temp= reogranize_matrix_by_row_col_mapping(M0, sys_A_row_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map)
    A_temp = reogranize_matrix_by_row_col_mapping(A, sys_A_row_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map )
    B_temp = reogranize_matrix_by_row_col_mapping(B,  sys_B_row_idx_map, sys_B_col_idx_map, ind_dep_B_row_idx_map, ind_dep_B_col_idx_map)
    C_temp = reogranize_matrix_by_row_col_mapping(C,  sys_C_row_idx_map, sys_C_col_idx_map, ind_dep_C_row_idx_map, ind_dep_C_col_idx_map)
    D_temp = D[:, :]

    M0_I_res, A_res, B_res, C_res, D_res, A_dependent_res, B_dependent_res   = apply_inductance_capactiance_to_state_matrix(
        cap_parallel_ind_series_ind_dep_mapping=cap_parallel_ind_series_ind_dep_mapping,
         M0_I=M0_temp, A=A_temp, B=B_temp, C=C_temp, D=D_temp,
         x_hat_label_to_obj_map=x_hat_label_to_obj_map, independent_state_number=len(independent_state_row_col_map), dependent_state_number=len(dependent_state_row_col_map),
         symbol_to_value_map=symbol_to_value_map,
         ind_dep_A_row_idx_map=ind_dep_A_row_idx_map,
         ind_dep_A_col_idx_map=ind_dep_A_col_idx_map
    )
    
    # now, reogranize matrix back to original form
    
    
    
    # update M0_mapping with 
    
    M0_final = reogranize_matrix_by_row_col_mapping(M0_I_res, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map, final_sys_A_row_idx_map, final_sys_A_col_idx_map)
    A_final = reogranize_matrix_by_row_col_mapping(A_res, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map, final_sys_A_row_idx_map, final_sys_A_col_idx_map)
    B_final = reogranize_matrix_by_row_col_mapping(B_res, ind_dep_B_row_idx_map, ind_dep_B_col_idx_map, final_sys_B_row_idx_map, final_sys_B_col_idx_map)
    C_final = reogranize_matrix_by_row_col_mapping(C_res, ind_dep_C_row_idx_map, ind_dep_C_col_idx_map, final_sys_C_row_idx_map, final_sys_C_col_idx_map )
    D_final = D_res[:,:]
    
    A_dependent_final = reogranize_matrix_by_row_col_mapping(A_dependent_res, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map, final_sys_A_row_idx_map, final_sys_A_col_idx_map )
    B_dependent_final = reogranize_matrix_by_row_col_mapping(B_dependent_res, ind_dep_B_row_idx_map, ind_dep_B_col_idx_map, final_sys_B_row_idx_map, final_sys_B_col_idx_map)
    
    
    # https://web.eecs.utk.edu/~dcostine/ECE692/Fall2024/tutorials.php?topic=PLECS
    # from the description of "State Order Reduction" here, it means the dependent source of capacitor in parallel or dependent source of inductor in series
    # should be identical to the counter independent part
    
    
    for ind_label, dependent_labels_list in cap_parallel_ind_series_ind_dep_mapping.items():
        indep_row = final_sys_A_row_idx_map[ind_label]
        
        for dep_lab in dependent_labels_list:
            dep_row = final_sys_A_row_idx_map[dep_lab]
            A_final[dep_row, :] = A_final[indep_row, :]
            B_final[dep_row, :] = B_final[indep_row, :]
    
    # apply the affect of c1 to C, D matrix
    # given y = C1*x_hat + Cx+DU
    # y =   ([C1*E^-1*A]+C)*x + ([C1*E*B]+D)*u
    E = sp.zeros( len(x_hat_labels), len(x_hat_labels) )
    
    for cur_index, label in enumerate(x_hat_labels):
        ele = x_hat_label_to_obj_map[label]

        if isinstance(ele, Capacitor):
            E[cur_index, cur_index] = ele.capacitance
        else:
            assert isinstance(ele, Inductor)
            E[cur_index, cur_index] = ele.inductance
            
            for name, factor in zip(ele.mutual_inductor_names, ele.K_factors):
                mutual_ele = element_name_to_obj_map[name]
                mutu_ind = x_hat_labels.index( mutual_ele.element_voltage_name)
                
                E[cur_index, mutu_ind] = factor * sp.sqrt( ele.inductance * mutual_ele.inductance )
    
    E= E.subs(symbol_to_value_map)
    
    
    D_non_impulse = D_final.copy()
    C_non_impulse = C_final.copy()
    # given E is a identity like matrix, E^-1 == E, so skipped the E^-1 step here
    D_final = D_final + C1 @E @B_final
    C_final = C_final + C1@E@A_final
    
    D_impulse = C1 @E @B_final
    C_impulse = C1@E@A_final
    
    
    
    # if there exist dependent y output. means Q is a fat matrix
    # this means it is underdetermined systems of equations
    # thus, used minimum nom solution in this case
    
    if len(y_dependent_labels) > 0:
        assert len(y_dependent_labels) + len(independent_y_labels) == len(y_labels)
        assert C.shape[0] == C1.shape[0] == len(independent_y_labels)
        Q_np_array = np.array(Q, dtype=np.float64)


        D_non_impulse = np.linalg.lstsq(Q_np_array, np.array(D_non_impulse, dtype=np.float64),rcond=None)[0]
        C_non_impulse = np.linalg.lstsq(Q_np_array, np.array(C_non_impulse, dtype=np.float64),rcond=None)[0]

        D_final = np.linalg.lstsq(Q_np_array,np.array(D_final, dtype=np.float64),rcond=None )[0]
        C_final = np.linalg.lstsq(Q_np_array, np.array(C_final, dtype=np.float64),rcond=None)[0]
        
        D_impulse = np.linalg.lstsq(Q_np_array, np.array(D_impulse, dtype=np.float64),rcond=None)[0]
        C_impulse = np.linalg.lstsq(Q_np_array, np.array(C_impulse, dtype=np.float64),rcond=None)[0]
    

        # convert back to sp.Matrix object
        D_non_impulse = sp.Matrix(D_non_impulse)
        C_non_impulse = sp.Matrix(C_non_impulse)
        D_final = sp.Matrix(D_final)
        C_final = sp.Matrix(C_final)
        C_impulse = sp.Matrix(C_impulse)
        D_impulse = sp.Matrix(D_impulse)
    
    return M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final, C_impulse, C_non_impulse, D_impulse, D_non_impulse


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
    x_hat_row_col_offset = y_labels_size + y_row_col_offset
    
    
        
    y_col_offset = s_labels_size +s_row_col_offset 
    x_hat_col_offset = y_labels_size + y_col_offset
    x_col_offset = x_hat_row_col_offset + x_hat_labels_size
    zero_offset = x_col_offset + x_labels_size
    u_col_offset = zero_offset + y_zero_labels_size + s_zero_labels_size


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
                # inconsistent_labels.append(lab)
                s_row_inconsistent_count += 1
                # raise ValueError("Inconsistent in switch row")
            elif i < x_hat_row_col_offset:
                y_row_inconsistent_count += 1  
                inconsistent_labels.append(lab) # means found inconsistent output variable
       
            else:
                pivot_ind += 1
                # dependency in x  raise ValueError("Unexpected case")        
                pass
        else:
            pivot_ind +=1

        if pivot_ind == len(m_pivots):
            break # 
    
    # update
    
    y_row_col_offset -= s_row_inconsistent_count
    x_hat_row_col_offset -= ( s_row_inconsistent_count + y_row_inconsistent_count)
    

    M_offset_info = {"s_row_col_offset":s_row_col_offset, "y_row_col_offset":y_row_col_offset, "x_hat_row_col_offset":x_hat_row_col_offset,
                     "y_col_offset":y_col_offset, "x_hat_col_offset":x_hat_col_offset, "x_col_offset":x_col_offset, "zero_offset":zero_offset,
                     "u_col_offset":u_col_offset
                     }

    Q = M[y_row_col_offset:x_hat_row_col_offset,  y_col_offset: x_hat_col_offset]
    C1 = -M[y_row_col_offset:x_hat_row_col_offset, x_hat_col_offset:x_col_offset]
    C = -M[y_row_col_offset:x_hat_row_col_offset, x_col_offset:zero_offset]
    D = -M[y_row_col_offset:x_hat_row_col_offset, u_col_offset: u_col_offset+voltage_source_size+current_source_size]

    M0 = M[x_hat_row_col_offset:x_hat_row_col_offset+ x_hat_labels_size , x_hat_col_offset:x_col_offset]
    A = -M[x_hat_row_col_offset:x_hat_row_col_offset+x_hat_labels_size, x_col_offset:zero_offset]
    B = -M[x_hat_row_col_offset:x_hat_row_col_offset+x_hat_labels_size, u_col_offset: u_col_offset+voltage_source_size+current_source_size]
      
      
    # sanity check
    if len(inconsistent_labels) == 0:
        assert_matrix_equal( Q, sp.eye(  y_labels_size, y_labels_size ))
    return Q, C1, C, D, M0, A, B,inconsistent_labels, M_offset_info


def transfer_func_and_poles(A: Matrix, B: Matrix, C:Matrix, D:Matrix, symbolic_value_map):
    
    S = sp.symbols("s")
    I = Matrix(np.eye(A.shape[0]))
    transfer_func = simplify(  C*(S*I-A).inv() *B + D )
    
    poles = sp.factor(  sp.det(S*I-A))
    # Find poles (roots of the characteristic equation)
    poles_roots = sp.solve(poles.subs(symbolic_value_map), S)  # Alternatively, use roots(poles, s) for more detailed output

    return transfer_func, poles,poles_roots


def backwardEulerIntegration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):

    eye_a =  np.eye(A.shape[0], dtype=np.float64)
    
    # #https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Moler03.pdf
    # # assume start from 0 - > result in coefficient
    # # but still keep same integration method
    # # but simplify alot, major issue with previous is did not use the inverse library of np
    p =0
    q = 1
    a1 = np.float64(0)  # because does not exist
    b1 = np.float64(-1)  #NOTE: new factor from the website
    e_at_part = e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 ) #np.linalg.solve(eye_a + A*time_t*b1, eye_a) #e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 )
    

    integ_part = time_t * e_at_part  # simplified out (a1-b1), since (0-(-1)) == 1
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 



def tustin_integration_step(x_cur: np.ndarray, A: np.ndarray, B: np.ndarray, u: np.ndarray, time_t: float) -> np.ndarray:
    # page 47 file:///home/shouyu/Downloads/PLECS_-_User_Manual.pdf
    
    # if assume un, un-1 is the same
    
    eye_A = sp.eye(A.shape[0], A.shape[1])
    A_d_p1 = sp.matrix2numpy( ( eye_A - (time_t/2) *A ), dtype=np.float64)
    
    A_d_p1_inv = np.linalg.inv(A_d_p1)
    
    A_d = A_d_p1_inv @ (eye_A + (time_t/2)*A )
    
    B_d = A_d_p1_inv @B*(time_t/2)
    
    return A_d*x_cur + 2*(B_d@u)  # TODO: assume un-1 and un is the same

def trapezoidalIntegration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):
    

    eye_a =  np.eye(A.shape[0], dtype=np.float64)

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

            

def retrieve_Zsw_hat(A: Matrix, B: Matrix, C: Matrix, D: Matrix,
                    C1: Matrix, 
                    C_impulse_matrix:Matrix, C_nonimpulse_matrix:Matrix, 
                    D_impulse_matrix:Matrix, D_nonimpulse_matrix:Matrix,
                    x_hat_labels:list[str], u_labels:list[str], diode_column_labels:list[str],
                    y_labels: list[str], number_of_inductor:int, number_of_current_source:int,
                    element_name_obj_map:dict[str, Element], m_column_labels_to_obj_map:dict[str, Element]):
    
    
    # assume A,B, C,D is already finalized
    # assume source is sorted in current, voltage order
    # assume state is sorted in inductor, capacitor order

    # sanity check 
    for ind, lab in enumerate(x_hat_labels):
        ele = m_column_labels_to_obj_map[lab]
        if ind < number_of_inductor:
            assert isinstance(ele, Inductor)
        else:
            assert isinstance(ele, Capacitor)
    for ind, lab in enumerate(u_labels):
        ele = m_column_labels_to_obj_map[lab]
        assert isinstance(ele, VoltageCurrentSource)
        if ind < number_of_current_source:
            assert ele.is_voltage_source is False
        else:
            assert ele.is_voltage_source

    
    ALL = A[:number_of_inductor, :number_of_inductor]
    ALC = A[:number_of_inductor, number_of_inductor:]
    ACL = A[number_of_inductor:, :number_of_inductor]
    ACC = A[number_of_inductor:, number_of_inductor:]
    

    BLis = B[:number_of_inductor, :number_of_current_source]
    BLvs= B[:number_of_inductor, number_of_current_source:]
    BCis=B[number_of_inductor:, :number_of_current_source]
    BCvs=B[number_of_inductor:, number_of_current_source:]
    
    # retrieve the rows of Z
    # if diode is on, look at the current of the diode
    # if diode is off, look at the voltage of the diode
    
    C_SW = sp.zeros( len(diode_column_labels), len(x_hat_labels) )
    D_SW = sp.zeros( len(diode_column_labels), len(u_labels) )
    C1_SW =  sp.zeros( len(diode_column_labels), len(x_hat_labels) )
    C_impulse_SW = sp.zeros(len(diode_column_labels), len(x_hat_labels) )
    D_impulse_SW = sp.zeros(len(diode_column_labels), len(u_labels))

    C_nonimpulse_SW = sp.zeros(len(diode_column_labels), len(x_hat_labels))
    D_nonimpulse_SW = sp.zeros(len(diode_column_labels), len(u_labels))
    for sw_index, sw in  enumerate(diode_column_labels):
        sw_ele =  m_column_labels_to_obj_map[sw]
        if isinstance(sw_ele, Diode):
            if sw == sw_ele.element_voltage_name:
                # means switch is off
                # need to find the y rows of the voltmere
                diode_voltmeter = element_name_obj_map[sw_ele.diode_voltmeter_name]
                voltmeter_index = y_labels.index(diode_voltmeter.element_voltage_name)
                C_SW[sw_index, :] = C[voltmeter_index, :]
                D_SW[sw_index, :] = D[voltmeter_index, :]
                C_impulse_SW[sw_index, :] = C_impulse_matrix[voltmeter_index, :]
                D_impulse_SW[sw_index, :] = D_impulse_matrix[voltmeter_index, :]
                C_nonimpulse_SW[sw_index, :] = C_nonimpulse_matrix[voltmeter_index, :]
                D_nonimpulse_SW[sw_index, :] = D_nonimpulse_matrix[voltmeter_index, :]
                C1_SW[sw_index, :]  = C1[voltmeter_index, :]
                
            else:
                # means swwitch is on
                diode_ammeter = element_name_obj_map[sw_ele.diode_ammeter_name]
                ammeter_index = y_labels.index(diode_ammeter.element_current_name)
                C_SW[sw_index, :] = C[ammeter_index, :]
                D_SW[sw_index, :] = D[ammeter_index, :]
                C_impulse_SW[sw_index, :] = C_impulse_matrix[ammeter_index, :]
                D_impulse_SW[sw_index, :] = D_impulse_matrix[ammeter_index, :]
                C_nonimpulse_SW[sw_index, :] = C_nonimpulse_matrix[ammeter_index, :]
                D_nonimpulse_SW[sw_index, :] = D_nonimpulse_matrix[ammeter_index, :]
                C1_SW[sw_index, :]  = C1[ammeter_index, :]
    C_SW_il = C_SW[:, :number_of_inductor]
    C_SW_vc = C_SW[:, number_of_inductor:]
    

    if number_of_current_source == 0:
        C_dsw_il = C_SW_il@ALL + C_SW_vc@ACL
        C_dsw_vc = C_SW_il@ALC + C_SW_vc@ACC
    else:
        C_dsw_il = C_SW_il@ALL + C_SW_vc@ACL
        C_dsw_vc = C_SW_il@ALC + C_SW_vc@ACC
    
    D_dsw_is = C_SW_il@BLis + C_SW_vc@BCis
    D_dsw_vs = C_SW_il@BLvs + C_SW_vc@BCvs
    

    
    Z_hat_Sw_A = sp.BlockMatrix([ [C_dsw_il, C_dsw_vc] ])
    Z_hat_SW_B = sp.BlockMatrix([ [D_dsw_is ,D_dsw_vs]])
    
    return C1_SW, C_SW, D_SW, C_impulse_SW, D_impulse_SW, C_nonimpulse_SW, D_nonimpulse_SW,  Z_hat_Sw_A, Z_hat_SW_B
    

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
from scipy.optimize import linear_sum_assignment



def int_to_binary_list(n, length):
    # Convert the integer to a binary string with the specified length
    binary_str = format(n, f'0{length}b')
    
    # Convert the binary string to a list of booleans
    bool_list = [bit == '1' for bit in binary_str]
    int_list = [  0 if (not state) else 1 for state in bool_list ]
    return bool_list, int_list

def create_cost_map(assignment_dict:dict[int:list[int]]):
    """Creates a cost matrix based on allowed assignments between people and items.

    This function generates a cost matrix where rows represent people and columns represent items.
    The cost matrix is initialized with `np.inf` (indicating prohibited assignments) and then
    updated to 0 for allowed assignments based on the input dictionary.

    Parameters
    ----------
    assignment_dict : dict[int, list[int]]
        A dictionary where keys represent people (as integers) and values are lists of items
        (as integers) that each person is allowed to be assigned to.

    Returns
    -------
    tuple[np.ndarray, list[int], list[int]]
        A tuple containing three elements:
        1. cost_matrix (np.ndarray): A 2D numpy array representing the cost matrix.
           - Rows correspond to people, and columns correspond to items.
           - `0` indicates an allowed assignment.
           - `np.inf` indicates a prohibited assignment.
        2. people (list[int]): A list of people (keys from `assignment_dict`) in the order they appear in the cost matrix.
        3. items (list[int]): A sorted list of unique items (values from `assignment_dict`) in the order they appear in the cost matrix.

    Example
    -------
    >>> assignment_dict = {
    ...     1: [101, 102],
    ...     2: [102, 103],
    ...     3: [101, 103]
    ... }
    >>> cost_matrix, people, items = create_cost_map(assignment_dict)
    >>> print(cost_matrix)
    [[  0.   0. inf]
     [inf   0.   0.]
     [  0. inf   0.]]
    >>> print(people)
    [1, 2, 3]
    >>> print(items)
    [101, 102, 103]
    """
    # Get the number of people (rows) and unique items (columns)
    people = list(assignment_dict.keys())
    items = sorted(set(item for sublist in assignment_dict.values() for item in sublist))
    
    # Initialize the cost matrix with np.inf (prohibited assignments)
    num_people = len(people)
    num_items = len(items)
    cost_matrix = np.full((num_people, num_items), np.inf)
    
    # Fill the cost matrix with 0 for allowed assignments
    for pep, allowed_items in assignment_dict.items():
        person_idx = people.index(pep)
        for item in allowed_items:
            item_idx = items.index(item)  # Find the column index for the item
            cost_matrix[person_idx, item_idx] = 0  # Allow the assignment
    
    return cost_matrix, people, items
    
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
    """Swaps two columns in a matrix and updates the corresponding column names.

    This function is used to swap the columns of a matrix based on the provided column label.
    It also updates the column names list (`cur_col_name`) to reflect the swap. The function
    identifies the columns to swap by looking up the associated element in the `label_obj_map`
    and determining the corresponding voltage and current column indices.

    Parameters
    ----------
    matrix : Matrix
        A 2D matrix (e.g., a numpy array or similar) where columns represent variables
        (e.g., voltage and current) and rows represent data points.
    cur_col_name : list[str]
        A list of strings representing the current column names in the matrix.
    label_obj_map : dict[str, Element]
        A dictionary mapping column labels to their corresponding `Element` objects.
        Each `Element` object should have the following attributes:
        - `element_current_name`: The name of the current column associated with the element.
        - `element_voltage_name`: The name of the voltage column associated with the element.
        - `element_current_name`: The current name of the element.
    col_label : str
        The label of the column to be swapped. This label should correspond to either
        a voltage or current column in the `label_obj_map`.

    Notes
    -----
    - The function modifies the input matrix and `cur_col_name` list in place.
    - The function assumes that the `Element` objects in `label_obj_map` have the necessary
      attributes (`element_current_name` and `element_voltage_name`) to determine the
      columns to swap.

    Example
    -------
    >>> import numpy as np
    >>> from dataclasses import dataclass

    >>> @dataclass
    ... class Element:
    ...     element_current_name: str
    ...     element_voltage_name: str
    ...     element_current_name: str

    >>> matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> cur_col_name = ["V1", "I1", "V2"]
    >>> label_obj_map = {
    ...     "I1": Element(element_current_name="I1", element_voltage_name="V1", element_current_name="I1"),
    ...     "V2": Element(element_current_name="I2", element_voltage_name="V2", element_current_name="V2"),
    ... }
    >>> col_label = "I1"
    >>> swapTwoColumn(matrix, cur_col_name, label_obj_map, col_label)
    >>> print(matrix)
    [[2 1 3]
     [5 4 6]
     [8 7 9]]
    >>> print(cur_col_name)
    ['I1', 'V1', 'V2']
    """
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


def apply_inductance_capactiance_to_state_matrix(
                                                M0_I: Matrix, E:Matrix, A: Matrix, B: Matrix, C: Matrix, D: Matrix,
                                                independent_state_number:int, dependent_state_number:int,
                                                symbol_to_value_map:dict[Symbol, ],
                                                 )-> Tuple[Matrix]:
    

    """
    This function redefine A,B,C,D matrix based on the relationship between dependent and independent state variable.
    
    For methodology and derivation, please refer to the technical paper.
    Returns
    -------
    Tuple[Matrix]
        1. Mo_I is stil the original M0_I matrix
        2. A_res, B_res, C_res, D_res is reogranized state space matrix
        3. A_dependent_res, B_dependent_res has describe how dependent variable relates to independent variables.
            x = A_depeendent_res*x + B_dependent_res*u retrive values of both independent and dependent state variables.
    """

    
    A11 = sp.matrix2numpy( A[:independent_state_number, :independent_state_number], dtype=np.float64)
    A12 = sp.matrix2numpy(A[:independent_state_number, independent_state_number:], dtype=np.float64)
    A21 = sp.matrix2numpy(A[independent_state_number:, :independent_state_number], dtype=np.float64)
    A22 = sp.matrix2numpy(A[independent_state_number:, independent_state_number:], dtype=np.float64)
    
    B1 = sp.matrix2numpy( B[:independent_state_number, :], dtype=np.float64)
    B2 = sp.matrix2numpy(B[independent_state_number:, :], dtype=np.float64)
    C1 = sp.matrix2numpy(C[:, :independent_state_number], dtype=np.float64)
    C2 = sp.matrix2numpy(C[:, independent_state_number:], dtype=np.float64)
    
    
    
    M_f = M0_I @ E
    M_f = M_f.subs(symbol_to_value_map)

    M11 = sp.matrix2numpy( M_f[:independent_state_number, :independent_state_number], dtype=np.float64  )
    M12 = sp.matrix2numpy( M_f[:independent_state_number, independent_state_number:], dtype=np.float64  )



    A22_inverse = np.linalg.inv(A22)
    M11_12_inv = np.linalg.inv(  M11- M12@A22_inverse@A21 )
    
    A11_new = (M11_12_inv)  @( A11 - A12@A22_inverse@A21)
    A12_new = sp.zeros(A12.shape[0], A12.shape[1])
    A21_new = -A22_inverse@A21@A11_new
    
    
    A22_new = sp.zeros( A22.shape[0], A22.shape[1] )
    B1_new = M11_12_inv @(B1 - A12@A22_inverse@B2)
    B2_new = -A22_inverse@A21@B1_new
    
    
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
    
    return M0_I, A_res, B_res, C_res, D_res, A_dependent_res, B_dependent_res                 
            
    
def determine_dependent_independent_state_mapping(M0_I: Matrix, A_raw:Matrix,  m_pivots:list[int], u_labels:list[str], y_labels:list[str], x_hat_labels: list[str], x_hat_col_offset_in_m_pivots:int  ):
    """Determines the mapping between dependent and independent state variables for a system.

    This function processes the given matrices and labels to identify dependent and independent
    state variables, their corresponding row and column indices, and maps them to system matrices
    (A, B, C). It uses the Reduced Row Echelon Form (RREF) of the `M0_I` matrix and the Hungarian
    algorithm to resolve ambiguities in pivot assignments.

    Parameters
    ----------
    M0_I : Matrix
        The M0 matrix as defined in Equation 11 of Antonio's "An efficient algorithm ...".
        It represents the initial state of the system.
    A_raw : Matrix
        The A_raw matrix as defined in Equation 11 of Antonio's "An efficient algorithm ...".
        It represents the raw state matrix of the system.
    m_pivots : list[int]
        A list of pivot columns in the `M0_I` matrix.
    u_labels : list[str]
        A list of input labels (control variables) for the system.
    y_labels : list[str]
        A list of output labels (measured variables) for the system.
    x_hat_labels : list[str]
        A list of state derivative labels (state variables) for the system.
    x_hat_col_offset_in_m_pivots : int
        The column offset in `m_pivots` where the state derivative labels begin.

    Returns
    -------
    tuple
        A tuple containing the following mappings:
        1. independent_state_row_col_map : dict[str, list[int]]
           - Maps independent state labels to their corresponding row and column indices.
        2. dependent_state_row_col_map : dict[str, list[int]]
           - Maps dependent state labels to their corresponding row and column indices.
        3. sys_A_row_idx_map : dict[str, int]
           - Maps state labels to their row indices in the system matrix A.
        4. sys_A_col_idx_map : dict[str, int]
           - Maps state labels to their column indices in the system matrix A.
        5. ind_dep_A_row_idx_map : dict[str, int]
           - Maps state labels to their row indices in the independent/dependent matrix A.
        6. ind_dep_A_col_idx_map : dict[str, int]
           - Maps state labels to their column indices in the independent/dependent matrix A.
        7. final_sys_A_row_idx_map : dict[str, int]
           - Maps state labels to their final row indices in the system matrix A.
        8. final_sys_A_col_idx_map : dict[str, int]
           - Maps state labels to their final column indices in the system matrix A.
        9. sys_B_row_idx_map : dict[str, int]
           - Maps state labels to their row indices in the system matrix B.
        10. sys_B_col_idx_map : dict[str, int]
            - Maps state labels to their column indices in the system matrix B.
        11. ind_dep_B_row_idx_map : dict[str, int]
            - Maps state labels to their row indices in the independent/dependent matrix B.
        12. ind_dep_B_col_idx_map : dict[str, int]
            - Maps state labels to their column indices in the independent/dependent matrix B.
        13. final_sys_B_row_idx_map : dict[str, int]
            - Maps state labels to their final row indices in the system matrix B.
        14. final_sys_B_col_idx_map : dict[str, int]
            - Maps state labels to their final column indices in the system matrix B.
        15. sys_C_row_idx_map : dict[str, int]
            - Maps state labels to their row indices in the system matrix C.
        16. sys_C_col_idx_map : dict[str, int]
            - Maps state labels to their column indices in the system matrix C.
        17. ind_dep_C_row_idx_map : dict[str, int]
            - Maps state labels to their row indices in the independent/dependent matrix C.
        18. ind_dep_C_col_idx_map : dict[str, int]
            - Maps state labels to their column indices in the independent/dependent matrix C.
        19. final_sys_C_row_idx_map : dict[str, int]
            - Maps state labels to their final row indices in the system matrix C.
        20. final_sys_C_col_idx_map : dict[str, int]
            - Maps state labels to their final column indices in the system matrix C.

    Raises
    ------
    ValueError
        If no valid assignment can be found for the Hungarian algorithm, indicating an invalid system configuration.

    Notes
    -----
    - The function assumes that the input matrices and labels are consistent with the system's structure.
    - The Hungarian algorithm is used to resolve ambiguities in pivot assignments for mixed dependent/independent states.
    - The function modifies the input matrices and labels in place to generate the mappings.
    """


    independent_state_row_col_map:dict[str, list[int]] = {}
    dependent_state_row_col_map:dict[str, list[int]] = {}
    # determine the the dependent/independent state variabls with their row/column
    _,M0_pivots = M0_I.rref() 
    
    
    #NOTE: remember by def of pivot, pivot row is the first nonzero value in that pivot column
    
    # start by looking from dependency state first
    
    # dependency state happen when pivots column exist in the correspong "x" label column, not "x_hat" label column
    dependent_col_offset = x_hat_col_offset_in_m_pivots+len(x_hat_labels)
    dependent_pivot_col = [col for col in m_pivots if col >=dependent_col_offset]
    
    for col in dependent_pivot_col:
        col_in_A = col-dependent_col_offset
        if col_in_A  >=len(x_hat_labels):
            # means y dependent variable, not x dependent variable.
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
    
    # second step, only process the independent pivor im Mo_I that is the only non_zero value in that row
    dep_inde_mixed_row ={}
    for index in range(len(M0_pivots)):
        pivot_col = M0_pivots[index]
        label = x_hat_labels[pivot_col]
        pivot_row = index # by def, pivots are the first nonzero in each row
        
        M0_I_row = M0_I[pivot_row, :]
        
        non_zero_val = len([x for x in M0_I_row if (not math.isclose(x, 0))])
        
        assert non_zero_val > 0
        if non_zero_val == 1:
            independent_state_row_col_map[label] = [pivot_row, pivot_col]
        else:
            dep_inde_mixed_row[label] = ( pivot_row, pivot_col)
            
    # now, last step of processing rows that have mixed pivot_row, pivot colr
    # this is a bipartite problem, with number of node on left == number of node on right
    # solve using the hungarian algorithm
    
    # first, build the hungarian matrix
    potential_pivot_row_pivot_col_mapping:dict[int, list[int]] ={}
    potential_pivot_col = []
    potential_pivot_row = []
    for label, info in dep_inde_mixed_row.items():

        pivot_row = info[0]
        pivot_col = info[1]
        M0_I_row = M0_I[pivot_row, :]
        for new_col in reversed(range(pivot_col, M0_I_row.cols)): # start to see from backward
            new_lab =  x_hat_labels[new_col]
            if (not math.isclose(M0_I_row[new_col], 0) and  (new_lab not in independent_state_row_col_map) and (new_lab not in dependent_state_row_col_map) ):
                if pivot_row not in potential_pivot_row_pivot_col_mapping:
                    potential_pivot_row_pivot_col_mapping[pivot_row] = [new_col]
                else:
                    potential_pivot_row_pivot_col_mapping[pivot_row].append(new_col)
                if new_col not in potential_pivot_col:
                    potential_pivot_col.append(new_col)
        potential_pivot_row.append(pivot_row)        
    
    assert len(potential_pivot_col) == len(potential_pivot_row_pivot_col_mapping) ==len(potential_pivot_row)
    
    cost_map, rows, cols = create_cost_map(potential_pivot_row_pivot_col_mapping)
    
    # solve the assignment problem
    
    row_ind, col_ind = linear_sum_assignment(cost_map)

    # Check if the assignment is valid
    total_cost = cost_map[row_ind, col_ind].sum()
    if total_cost < np.inf:
        pass
    else:
        raise ValueError("No valid assignment exists.")
    
    
    
    # now, update them in the independent label mapping
    for row_idx, col_idx in zip(row_ind, col_ind):
        pivot_row = rows[row_idx]
        pivot_col = cols[col_idx]
        label = x_hat_labels[pivot_col]
        
        independent_state_row_col_map[label] = [pivot_row, pivot_col]
    assert len(independent_state_row_col_map) + len(dependent_state_row_col_map) == len(x_hat_labels)
    
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

    
    
    
    
    assert len(sys_A_row_idx_map) == len(sys_A_row_idx_map) == len(ind_dep_A_row_idx_map) == len(ind_dep_A_col_idx_map) == len(final_sys_A_row_idx_map) ==len(final_sys_A_col_idx_map)
    
    return  independent_state_row_col_map,dependent_state_row_col_map,  \
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
                                                symbol_to_value_map:dict[Symbol, float ],
                                               )-> Tuple[Matrix]:
    """Given the raw state-space matrix, this function resolve the dependent state-variable and output variable
    and form a new set of A,B,C,D matrix.
    
    For more detail on the algorithm used here, please refer to the technical paper that derives the equation.

    Parameters
    ----------
    M0 : Matrix
        M0 as define in equatio(14)
    Q : Matrix
        _description_
    C1 : Matrix
        _description_
    A : Matrix
        _description_
    B : Matrix
        _description_
    C : Matrix
        _description_
    D : Matrix
        _description_
    m_pivots : list[int]
        _description_
    u_labels : list[str]
        _description_
    y_labels : list[str]
        _description_
    y_dependent_labels : list[str]
        _description_
    x_hat_labels : list[str]
        _description_
    x_hat_col_offset_in_m_pivots : int
        _description_
    x_hat_label_to_obj_map : dict[str, Element]
        _description_
    element_name_to_obj_map : dict[str, Element]
        _description_
    symbol_to_value_map : dict[Symbol, float ]
        _description_

    Returns
    -------
    Tuple[Matrix]
        1. M0_final, the M_0 matrix after reogranized 
        2. A_final, B_final, C_final, D_final state space matrix that fits into the standard state-space equation form
            of x_hat = A_final*x +B_final*u and y = C_final*x+D_Final*u
        3, A_dependent_final, B_dependent_final matrix describes how dependent state variable depend on independent state variable.
            x_value = A_dependent_final*x + B_dependent_final*u give both independent and dependent state value.
        4. C_impulse, C_non_impulse, D_impulse, D_non_impulse
            C_impulse, D_impulse are matrix result from simplification of C1 
            C_non_impulse and D_non_impulse are result from given C, D matrix.
            C_final = C_impulse + C_non_impulse
            D_final = D_impulse + D_non_impulse
    """
    # build E base on the order of X_hat_labels
    
    E = sp.zeros( len(x_hat_labels), len(x_hat_labels) )
    #E is the matrix that contians the inductance, mutual inductance, capacitance between each X variables.
    
    for cur_index, label in enumerate(x_hat_labels):
        ele = x_hat_label_to_obj_map[label]

        if isinstance(ele, Capacitor):
            E[cur_index, cur_index] = ele.capacitance
        else:
            assert isinstance(ele, Inductor)
            E[cur_index, cur_index] = ele.inductance
            # Below is adding the mutual inductance into E matrix
            for name, factor in zip(ele.mutual_inductor_names, ele.K_factors):
                mutual_ele = element_name_to_obj_map[name]
                mutu_ind = x_hat_labels.index( mutual_ele.element_voltage_name)
                
                E[cur_index, mutu_ind] = factor * sp.sqrt( ele.inductance * mutual_ele.inductance )
    
    E= E.subs(symbol_to_value_map)
    
    
    if len(y_dependent_labels):
        # means there is dependent in y output
        independent_y_labels= [x for x in y_labels if x not in y_dependent_labels]
    else:
        independent_y_labels = y_labels    
    
    # The function below generates a 3 set of mapping
    
    # set 1:sys_A_row_idx_map,sys_A_col_idx_map
    # This is the mapping of input 'A'. In this case, it is the state variable to row/column mapping of input 'A;
    # set 2: ind_dep_A_row_idx_map, ind_dep_A_col_idx_map
    # This is the mapping of state varibale of 'A' group by independent state variable, dependent state variable
    # set 3: final_sys_A_row_idx_map, final_sys_A_col_idx_map
    # This is the output mapping of 'A_final', which should align with the x_hat_labels order.
    
    # similar explantion for B,C,D,C1, ....
    independent_state_row_col_map,dependent_state_row_col_map,  \
        sys_A_row_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map, final_sys_A_row_idx_map, final_sys_A_col_idx_map,\
            sys_B_row_idx_map,sys_B_col_idx_map,ind_dep_B_row_idx_map,ind_dep_B_col_idx_map, final_sys_B_row_idx_map, final_sys_B_col_idx_map,\
                sys_C_row_idx_map,sys_C_col_idx_map,ind_dep_C_row_idx_map,ind_dep_C_col_idx_map, final_sys_C_row_idx_map, final_sys_C_col_idx_map= determine_dependent_independent_state_mapping(

        M0_I=M0, A_raw=A, m_pivots=m_pivots, x_hat_labels=x_hat_labels, x_hat_col_offset_in_m_pivots=x_hat_col_offset_in_m_pivots,
        u_labels=u_labels, y_labels=independent_y_labels
    )
                
    independent_state_labels_list = [  x for x in independent_state_row_col_map.keys()]
    dependent_state_labels_list = [x for x in dependent_state_row_col_map.keys()]                
    M0_temp= reogranize_matrix_by_row_col_mapping(M0, sys_A_row_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map)
    A_temp = reogranize_matrix_by_row_col_mapping(A, sys_A_row_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map )
    B_temp = reogranize_matrix_by_row_col_mapping(B,  sys_B_row_idx_map, sys_B_col_idx_map, ind_dep_B_row_idx_map, ind_dep_B_col_idx_map)
    C_temp = reogranize_matrix_by_row_col_mapping(C,  sys_C_row_idx_map, sys_C_col_idx_map, ind_dep_C_row_idx_map, ind_dep_C_col_idx_map)
    D_temp = D[:, :]
    E_temp = reogranize_matrix_by_row_col_mapping(E, sys_A_col_idx_map, sys_A_col_idx_map, ind_dep_A_row_idx_map, ind_dep_A_col_idx_map)

    M0_I_res, A_res, B_res, C_res, D_res, A_dependent_res, B_dependent_res   = apply_inductance_capactiance_to_state_matrix(
        M0_I=M0_temp, E=E_temp, A=A_temp, B=B_temp, C=C_temp, D=D_temp,
        independent_state_number=len(independent_state_row_col_map), 
        dependent_state_number=len(dependent_state_row_col_map),
        symbol_to_value_map=symbol_to_value_map,

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
    
    
    # apply the affect of c1 to C, D matrix
    # given y = C1*x_hat + Cx+DU
    # y =  C1 * E *x_hat + Cx+Du, because in paper, it assumed E already factored into C1

    D_non_impulse = D_final.copy()
    C_non_impulse = C_final.copy()


    D_impulse = C1 @E @B_final
    C_impulse = C1@E@A_final
    
    
    D_final = D_final + D_impulse
    C_final = C_final + C_impulse
     
    
    # step to simplify 
    # Qy = Cx+Du
    # if there exist dependent y output. means Q is a fat matrix
    # this means it is underdetermined systems of equations
    # thus, used minimum nom solution in this case
    # if no dependent y output, Q is an identity matrix, thus no further simplification is required.
    
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
    else:
        assert_matrix_equal(Q, sp.eye(len(y_labels))) # assert Q to be a identity matrix
    
    

    return M0_final, A_final, B_final, C_final, D_final, A_dependent_final, B_dependent_final, C_impulse, C_non_impulse, D_impulse, D_non_impulse,independent_state_labels_list, dependent_state_labels_list


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
) -> Tuple[Matrix|list[str]|dict[str,int]]:
    """Retrieve the block matrices from 'M' given 'M' is defined as Equation 11 in Antonio Massarini's "An Efficient Algorithm for the formulation ..."

    Parameters
    ----------
    M : Matrix
        Network topology matrix.
    m_pivots : list[int]
        List of pivot columns of 'M' matrix.
    m_labels : list[str]
        Labels for each column in 'M' matrix.
    s_labels_size : int
        _description_
    y_labels_size : int
        _description_
    x_hat_labels_size : int
        _description_
    x_labels_size : int
        _description_
    y_zero_labels_size : int
        _description_
    s_zero_labels_size : int
        _description_
    capacitor_size : int
        _description_
    inductor_size : int
        _description_
    voltage_source_size : int
        _description_
    current_source_size : int
        _description_
    redundant_offset : int
        If redundant offset = 0, means 'M' is in Equation(13), else imply 'M' is in Equation(11) of Antonio Massarin's "An efficient Algorithm for the formulation ..."

    Returns
    -------
    Tuple[Matrix|list[str]|dict[str,int]]
        Return Q, C1, C, D, M0, A,B, inconsistent_labels, offset_information
        Q,C1,C,D,M0,A,B are the blokc matrix as defined in Equation 11 of Antonio's "An efficient Algorithm...".
        inconsistent_labels are list of y_output(meters) that are dependent due to C-E-loop or I-J-cutset.
        offset_information gives information of the start row&column of each block matrix in 'M'.
    """
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

def pade_0_2_integration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):

    eye_a =  np.eye(A.shape[0], dtype=np.float64)
    
    # #https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Moler03.pdf
    # # assume start from 0 - > result in coefficient
    # # but still keep same integration method
    # # but simplify alot, major issue with previous is did not use the inverse library of np
    p =0
    q = 1
    a1 = np.float64(0)  # because does not exist
    b1 = np.float64(-1)  #NOTE: new factor from the website
    b2 = 1/2
    
    e_at_part = e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 + np.linalg.matrix_power(A*time_t,2)*b2 ) #np.linalg.solve(eye_a + A*time_t*b1, eye_a) #e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 )
    

    integ_part = time_t * -1 * ( eye_a*b1 + A*time_t*b2 ) @e_at_part  # simplified out (a1-b1), since (0-(-1)) == 1
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 
def pade_0_3_integration(x_cur: np.ndarray, A:  np.ndarray, B:  np.ndarray, u:  np.ndarray, time_t:float):

    eye_a =  np.eye(A.shape[0], dtype=np.float64)
    
    # #https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Moler03.pdf
    # # assume start from 0 - > result in coefficient
    # # but still keep same integration method
    # # but simplify alot, major issue with previous is did not use the inverse library of np
    p =0
    q = 1
    a1 = np.float64(0)  # because does not exist
    b1 = np.float64(-1)  #NOTE: new factor from the website
    b2 = 1/2
    b3= -1/3
    
    e_at_part = e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 + np.linalg.matrix_power(A*time_t,2)*b2 
                                           + np.linalg.matrix_power(A*time_t, 3)*b3
                                           ) #np.linalg.solve(eye_a + A*time_t*b1, eye_a) #e_at_part =  np.linalg.inv(  eye_a +A*time_t*b1 )
    

    integ_part = time_t * -1 * ( eye_a*b1 + A*time_t*b2 +np.linalg.matrix_power(A*time_t,2)*b3 ) @e_at_part  # simplified out (a1-b1), since (0-(-1)) == 1
    p1 = e_at_part @ x_cur 
    p2 =  integ_part@ B @ u 
    res = p1+p2
    return  res 


def tustin_integration_step(x_cur: np.ndarray, A: np.ndarray, B: np.ndarray, u: np.ndarray, time_t: float) -> np.ndarray:
    # page 47 PLECS_-_User_Manual.pdf
    
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
    


    C_dsw_il = C_SW_il@ALL + C_SW_vc@ACL
    C_dsw_vc = C_SW_il@ALC + C_SW_vc@ACC
    
    D_dsw_is = C_SW_il@BLis + C_SW_vc@BCis
    D_dsw_vs = C_SW_il@BLvs + C_SW_vc@BCvs
    

    
    Z_hat_Sw_A = sp.BlockMatrix([ [C_dsw_il, C_dsw_vc] ])
    Z_hat_SW_B = sp.BlockMatrix([ [D_dsw_is ,D_dsw_vs]])
    
    return C1_SW, C_SW, D_SW, C_impulse_SW, D_impulse_SW, C_nonimpulse_SW, D_nonimpulse_SW,  Z_hat_Sw_A, Z_hat_SW_B
    






def radau_integration_step(x_cur: np.ndarray, A: np.ndarray, B: np.ndarray, u: np.ndarray, time_t: float, dt: float) -> np.ndarray:
    """
    Perform one step of numerical integration using Radau's method.

    Args:
        x_cur (np.ndarray): Current state vector (shape: (6, 1)).
        A (np.ndarray): System matrix (shape: (6, 6)).
        B (np.ndarray): Input matrix (shape: (6, 1)).
        u (np.ndarray): Input vector (shape: (1, 1)).
        time_t (float): Current time.
        dt (float): Time step size.

    Returns:
        np.ndarray: Updated state vector after one integration step (shape: (6, 1)).
    """
    # Ensure x_cur is 1-dimensional
    x_cur_flat = x_cur.flatten()
    u_flat = u.flatten()
    # Define the system dynamics (dx/dt = A*x + B*u)
    def system_dynamics(t, x):
        return A @ x + B @ u_flat  # u is a scalar (shape (1, 1))

    # Define the time span for the current step
    t_span = (time_t, time_t + dt)

    # Use solve_ivp with Radau's method to integrate over the current step
    sol = solve_ivp(system_dynamics, t_span, x_cur_flat, method='BDF')

    # Return the updated state (last state from the solution) as a column vector
    return sol.y[:, -1].reshape(-1, 1)
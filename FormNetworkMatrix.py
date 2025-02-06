from Element import (
    Element,
    GroundNode,
    Node,
    Inductor,
    Capacitor,
    ExternalSwitch,
    Diode,
    Resistor,
    DependentElement,
    VoltageCurrentSource,
    Voltmeter,
    Ammeter,
    PortElement,
    NonPortElement,
)
from typing import Tuple
from functools import cached_property, cmp_to_key
# any example of boost
import numpy as np
import sympy as sp
from sympy import Matrix, pi, pprint, Symbol, eye, zeros

from util import print_matrix,  swapTwoColumn, retrieveSystemMatrix, transfer_func_and_poles, print_matrix_for_matlab_format
import ast
import re
class NetworkMatrix:
    def __init__(
        self,
        M_topology:Matrix,
        m_column_labels: list[str],
        m_colmn_labels_to_obj_map: dict[str, Element],
        element_name_obj_map:dict[str, Element],
        symbolic_to_value_map:dict[sp.Symbol, float],
        s_label_size:int,
        y_label_size:int,
        x_hat_label_size:int,
        x_label_size:int,
        s_zero_label_size:int,
        y_zero_label_size:int,
        u_label_size:int,
        capactior_size:int,
        inductor_size:int,
        voltage_source_size:int,
        current_source_size:int,
        redundant_size:int,
        simpilfied = True,
    ):
        """Object contain informations about the circuit network topology.

        Parameters
        ----------
        M_topology : Matrix
            Initial network topolgy matrix. Equation 11 in Antonio Massarini's "An efficient algorithm for ..."
        m_column_labels : list[str]
            Label for each column in M_topology matrix. The label are ordered as described in Equation 9 of Antonio Massarini's "An efficient algorithm for ..."
        m_colmn_labels_to_obj_map : dict[str, Element]
            Mapping of label to corresponding Element object.
        element_name_obj_map : dict[str, Element]
            Mapping of element name to Element object.
        symbolic_to_value_map : dict[sp.Symbol, float]
            Mapping of sp.Symbol to the actual value.
        s_label_size : int
            Number of switch/diode.
        y_label_size : int
            Number of Ammeter/Voltmeter.
        x_hat_label_size : int
            Number of state derivation variable.
        x_label_size : int
            Number of state variable.
        s_zero_label_size : int
            Number of zero valued switch variable, see Equation 10 in Antonio MAssarini's "An efficient algorithm for ..."
        y_zero_label_size : int
            Number of zero valued meterm variable, see Equation 10 in Antonio MAssarini's "An efficient algorithm for ..."
        u_label_size : int
            Number of inputs.
        capactior_size : int
            _description_
        inductor_size : int
            _description_
        voltage_source_size : int
            _description_
        current_source_size : int
            _description_
        redundant_size : int
            Redundant offset row&columns size in the M_topology matrix. If redundant_size == 0, means M_toplogy matrix is in the Equation (13) form.
            Otherwise, it means the M_topology matrix is in Equation (11) form of "Antonio Massarini's "An efficient algorithm for..."
        simpilfied : bool, optional
            If true, indicate M_toploy matrix is in Equation (13), else means M_toplogy is in equation (11) form of Antonio Massarini's "An efficient algorithm for ..."
        """
        
        if simpilfied:
            M_topology = M_topology[redundant_size:, redundant_size:]
            m_column_labels[redundant_size:]
            self.simplified = True
            self.redundant_size = 0
        else:
            self.redundant_size = redundant_size
            self.simplified = False
        
        assert capactior_size+inductor_size == x_hat_label_size == x_label_size
        assert voltage_source_size+current_source_size == u_label_size 
        self.capacitor_size = capactior_size
        self.inductor_size = inductor_size
        self.voltage_source_size = voltage_source_size
        self.current_source_Size = current_source_size
        
        
        
        # M_topology describe the topology relation between matrix
        # M is the matrix of M_toplolgy after doing rref() for the current toplogy
        self.M ,  self.M_toplolgy_pivots = M_topology.rref()
        self.M_topology = M_topology[:,:]
        self.M, self.M_pivots = self.M.rref()
        
  
        
        self.m_column_labels = m_column_labels
        self.m_column_labels_to_obj_map = m_colmn_labels_to_obj_map
        self.symbolic_to_value_map = symbolic_to_value_map
        self.element_name_obj_map = element_name_obj_map
        
        self.s_labels_size = s_label_size
        self.y_label_size = y_label_size
        self.x_hat_label_size = x_hat_label_size
        self.x_label_size = x_label_size
        self.s_zero_label_size = s_zero_label_size
        self.y_zero_label_size = y_zero_label_size
        self.u_label_size = u_label_size
        
    

    def rref_update(self):
        """Update the network matrix topology after column swapped.
        """
        self.M_topology, _ = self.M_topology.rref()
        self.M = self.M_topology.copy()
        
        self.M, self.M_pivots = self.M.rref()

        self.M = self.M.subs(self.symbolic_to_value_map)
    
        
    def swap_M_matrix_columns(self, labels_to_swap:str):
        """Swap the voltage/current column of element with its current/voltage column in self.M_topology matrix.

        Parameters
        ----------
        labels_to_swap : str
            Voltage/Current label of the element.
        """
        
        swapTwoColumn(self.M_topology, self.m_column_labels, self.m_column_labels_to_obj_map, labels_to_swap )


    def print_M_matrix(self ):
        print_matrix(self.M, self.m_column_labels, ["" for x in range(self.M.shape[0])])
        
    @property
    def external_switch_labels(self):
        return [     lab for lab in self.s_labels if isinstance(self.m_column_labels_to_obj_map[lab], ExternalSwitch)      ]
    @property
    def s_labels(self):
        

        return self.m_column_labels[ self.redundant_size : self.s_labels_size + self.redundant_size]

    @property
    def y_labels(self):
        offset = self.redundant_size + self.s_labels_size
        return self.m_column_labels[offset: offset+ self.y_label_size]

    @property
    def x_hat_labels(self):
        offset = self.redundant_size+ self.s_labels_size+ self.y_label_size
        return self.m_column_labels[offset: offset+ self.x_hat_label_size]
    @property
    def x_labels(self):
        offset = self.redundant_size+self.s_labels_size+ self.y_label_size + self.x_hat_label_size
        return self.m_column_labels[offset: offset + self.x_label_size]
    @property
    def s_zero_labels(self):
        offset = self.redundant_size + self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size
        return self.m_column_labels[offset: offset+  self.s_zero_label_size]
    @property
    def y_zero_labels(self):
        offset = self.redundant_size + self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size + self.s_zero_label_size
        
        return self.m_column_labels[offset: offset + self.y_zero_label_size]
    @property
    def u_labels(self):
        offset = self.redundant_size + self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size + self.s_zero_label_size + self.y_zero_label_size
        return self.m_column_labels[offset: ]
    
    
    
    
def update_column_labels(element_col_map: dict[str, int]) -> list[str]:
    """Return column labels(key of the 'element_col_map') sorted in ascending order

    Parameters
    ----------
    element_col_map : dict[str, int]
        _description_

    Returns
    -------
    list[str]
        Sorted column labels.
    """
    sorted_ele_col = [
        k for k, v in sorted(element_col_map.items(), key=lambda item: item[1])
    ]

    return sorted_ele_col


def update_row_labels(node_row_map: dict[str, int]) -> list[str]:
    return [k for k, v in sorted(node_row_map.items(), key=lambda item: item[1])]


def reorder_matrix_by_colum_label(
    matrix: Matrix, new_col_name: list[str], ele_name_col_map: dict[str, int]
) -> Matrix:
    """Reorders the columns of a matrix based on provided column names.

    This function rearranges the columns of the input matrix according to
    the specified order of column names. The mapping from element names
    to their new positions is maintained through the `ele_name_col_map`.

    Parameters
    ----------
    matrix : Matrix
        The input 2D array or DataFrame to be reordered.
    new_col_name : list[str]
        List of new column names in the desired order.
    ele_name_col_map : dict[str, int]
        Mapping from element names (keys) to their corresponding column indices.

    Returns
    -------
    Matrix
        The matrix with columns reordered according to `new_col_name`.

    Note
    ----
    This function creates a temporary copy of the input matrix and modifies it in place.
    """
    m_temp = matrix[:, :]
    for col in range(len(new_col_name)):
        new_ele_name = new_col_name[col]

        matrix[:, col] = m_temp[:, ele_name_col_map[new_ele_name]]

        ele_name_col_map[new_ele_name] = col


def read_netlis_description(
    netList: list[list[str]],
    node_name_obj_map: dict[str, Node],
    ele_name_obj_map: dict[str, Element],
    ele_name_col_map: dict[str, int],
    symbollic_to_value_map: dict[Symbol:float],
    switch_list: list[ExternalSwitch | Diode],
    source_list: list[VoltageCurrentSource],
    inductor_capacitor_list: list[Inductor | Capacitor],
    meter_list: list[Voltmeter | Ammeter],
):
    """Extract the circuit elements from list of description string.

    Parameters
    ----------
    netList : list[list[str]]
        List of circuit elements.
    node_name_obj_map : dict[str, Node]
        Mapping of node name to Node object.
    ele_name_obj_map : dict[str, Element]
        Mapping of element name to Element object. 
    ele_name_col_map : dict[str, int]
        Mapping of element name to column index of the incident matrix.
    symbollic_to_value_map : dict[Symbol:float]
        Mapping of sp.Symbol to value.
    switch_list : list[ExternalSwitch  |  Diode]
        List of all switch/diode.
    source_list : list[VoltageCurrentSource]
        List of voltage/current sources.
    inductor_capacitor_list : list[Inductor  |  Capacitor]
        List of inductors/capacitors.
    meter_list : list[Voltmeter  |  Ammeter]
        List of Voltmeter/Ammeter.

    Raises
    ------
    ValueError
        When unknown element is found in "netList"
    """
    for i in range(len(netList)):
        desc = netList[i]
        # labels = [s.strip() for s in desc.split(",")]
        # Regular expression to match elements
        pattern = r'\[.*?\]|[^,\s]+'

        # Use re.findall to extract elements
        labels = re.findall(pattern, desc)
        if labels[1] not in node_name_obj_map:
            node_name_obj_map[labels[1]] = Node(labels[1])
        node_a = node_name_obj_map[labels[1]]
        if labels[2] not in node_name_obj_map:
            node_name_obj_map[labels[2]] = Node(labels[2])
        node_b = node_name_obj_map[labels[2]]

        ele = None
        match labels[0][0]:
            case "V":
                if labels[0][1] == "M":
                    ele = Voltmeter(labels[0], node_a, node_b)
                    meter_list.append(ele)
                elif len(labels[0]) > 4 and labels[0][0:4] == "VCVS":
                    factor_val = float(labels[3])
                    factor_symbol = sp.symbols( labels[0] + "_factor" )
                    ele = DependentElement( labels[0], node_a, node_b,labels[4] ,factor_val, factor_symbol,"VCVS" )
                    
                    symbollic_to_value_map[factor_symbol] = factor_val
                elif len(labels[0]) > 4 and labels[0][0:4] == "VCIS":
                    factor_val = float(labels[3])
                    factor_symbol = sp.symbols(labels[0] + "_factor")
                    ele = DependentElement(labels[0], node_a, node_a, labels[4], factor_val, factor_symbol, "VCIS")
                    symbollic_to_value_map[factor_symbol]  = factor_val
                else:
                    ele = VoltageCurrentSource(
                        labels[0],
                        node_a,
                        node_b,
                        float(labels[3]),
                        float(labels[4]),
                        True,
                    )
                    source_list.append(ele)
            case "I":
                if len(labels[0]) > 4 and labels[0][0:4] == "ICVS":
                    factor_val = float(labels[3])
                    factor_symbol = sp.symbols( labels[0] + "_factor" )
                    ele = DependentElement(labels[0], node_a, node_b, labels[4], factor_val,factor_symbol, "ICVS")
                    symbollic_to_value_map[factor_symbol] = factor_val
                elif len(labels[0]) > 4 and labels[0][0:4] == "ICIS":
                    factor_val = float(labels[3])
                    factor_symbol = sp.symbols(labels[0] + "_factor")
                    ele = DependentElement(labels[0], node_a, node_b, labels[4], factor_val, factor_symbol, "ICIS")
                    symbollic_to_value_map[factor_symbol] = factor_val
                else:
                    raise ValueError("Unknown element")
            case "L":
                inductor_symbol = sp.symbols(labels[0])
                inductor_val = float(labels[3])
                
                
                mutual_inductor_symbols = None
                mutual_k = None
                if len(labels) > 4:
                    mutual_inductor_symbols =labels[4].strip("[]").replace(" ","").split(",")
                    mutual_k_str = [float(x) for x in labels[5].strip("[]").split(",")]
                    mutual_k = []
                    for ind in range(len(mutual_inductor_symbols)):
                        
                        
                        mutual_ind_sy = mutual_inductor_symbols[ind]
                        mutual_sym = f"K-{labels[0]}-{mutual_ind_sy}" if labels[0] <=mutual_ind_sy else f"K-{mutual_ind_sy}-{labels[0]}"
                        
                        K_sym = sp.symbols(mutual_sym )
                        if K_sym not in symbollic_to_value_map:
                            symbollic_to_value_map[K_sym] = float(mutual_k_str[ind])
                        else:
                            assert symbollic_to_value_map[K_sym] == float(mutual_k_str[ind])
                        mutual_k.append(K_sym)
                    
                    
                ele = Inductor(labels[0], node_a, node_b, inductor_val, inductor_symbol, mutual_inductor_names=mutual_inductor_symbols, K_factors=mutual_k)
                symbollic_to_value_map[inductor_symbol] = inductor_val
                inductor_capacitor_list.append(ele)
            case "C":
                capacitor_symbol = sp.symbols(labels[0])
                capacitor_val = float(labels[3])
                ele = Capacitor(
                    labels[0], node_a, node_b, capacitor_val, capacitor_symbol
                )
                symbollic_to_value_map[capacitor_symbol] = capacitor_val
                inductor_capacitor_list.append(ele)
            case "D":
                initial_state = True if labels[3] == "ON" else False
       
                ele = Diode(labels[0], node_a, node_b, initial_state, labels[4], labels[5])
                switch_list.append(ele)
            case "S":
                pwm_val_at_beginning_of_each_cycle = True if labels[3] == "ON" else False
                ele = ExternalSwitch(
                    labels[0],
                    node_a,
                    node_b,
                    pwm_val_at_beginning_of_each_cycle,
                    float(labels[4]),
                    float(labels[5]),
                    float(labels[6]), 
                )
                switch_list.append(ele)
            case "A":
                ele = Ammeter(labels[0], node_a, node_b)
                meter_list.append(ele)
            case "R":
                resistance_symbol = sp.symbols(labels[0])
                resistance_val = float(labels[3])
                ele = Resistor(
                    labels[0], node_a, node_b, resistance_val, resistance_symbol
                )
                symbollic_to_value_map[resistance_symbol] = resistance_val

        ele_name_col_map[labels[0]] = i
        ele_name_obj_map[labels[0]] = ele
        node_a.node_a_element.append(ele)
        node_b.node_b_element.append(ele)

    # sort
    inductor_capacitor_list = inductor_capacitor_list.sort(key=lambda x: x.name)


def gen_incident_matrix(
    node_name_obj_map: dict[str, Node],
    node_name_row_map: dict[str, int],
    ele_name_obj_map: dict[str, Element],
    ele_name_col_map: dict[str, int],
) -> Tuple[Matrix, list[str], list[str], list[str], list[str]]:
    """Retrive A(incident) matrix and rearrange element into either tree/cotree port/non-port
    
    For detail, refer to chapter 4 and 6-5-2 of "Computer-Aided Analysis of Electronic Circuits" by Leon-o-Chua and Pen-Min-Lin.

    Parameters
    ----------
    node_name_obj_map : dict[str, Node]
        Mapping of node element to Node object.
    node_name_row_map : dict[str, int]
        mapping of node element to row index in the A matrix.
    ele_name_obj_map : dict[str, Element]
        mapping of element name to Element object.
    ele_name_col_map : dict[str, int]
        mapping of element name to column index in the A matrix.

    Returns
    -------
    Tuple[Matrix, list[str], list[str], list[str], list[str]]
        Incident matrix, tree port elements, co-tree port element, tree non-port element, co-tree non-port element.
    """
    A_matrix = sp.Matrix(
        len(node_name_obj_map) - 1,
        len(ele_name_obj_map),
        [0 for k in range((len(node_name_obj_map) - 1) * len(ele_name_obj_map))],
    )
    cur_row_ind = 0
    for node_name, node in dict(
        sorted(node_name_obj_map.items(), key=lambda item: item[0])
    ).items():
        if isinstance(node, GroundNode):
            continue

        node_name_row_map[node.name] = cur_row_ind

        for ele in node.node_a_element:
            A_matrix[cur_row_ind, ele_name_col_map[ele.name]] = 1
        for ele in node.node_b_element:
            A_matrix[cur_row_ind, ele_name_col_map[ele.name]] = -1
        cur_row_ind += 1

    column_names = update_column_labels(ele_name_col_map)
    row_names = update_row_labels(node_name_row_map)
    print("Incident mateix before reogranize")
    print_matrix(A_matrix=A_matrix, column_names=column_names, row_names=row_names)

    # do rref to get the pivot columns of A
    _, pivots = A_matrix.rref()
    # print(pivots)
    assert len(pivots) == A_matrix.shape[0]

    # reorder the column of A according to the pivots

    for i in range(len(pivots)):
        piv = pivots[i]
        cur_element_name = column_names[i]
        cur_element_col = ele_name_col_map[cur_element_name]
        if piv != cur_element_col:
            # swap columns
            new_element_name = column_names[piv]
            new_element_col = ele_name_col_map[new_element_name]
            assert piv == new_element_col

            ele_name_col_map[cur_element_name] = new_element_col
            ele_name_col_map[new_element_name] = cur_element_col

            temp = A_matrix[:, cur_element_col]
            A_matrix[:, cur_element_col] = A_matrix[:, new_element_col]
            A_matrix[:, new_element_col] = temp

            column_names = update_column_labels(ele_name_col_map)
            row_names = update_row_labels(node_name_row_map)
    # print_matrix(A_matrix=A_matrix, column_names=column_names, row_names=row_names)
    # reorganize a matrix to a, z, y, b form
    # a is the port in tree, z is nonport in tree
    # b is port in co-tree, y is nonport in cotree

    # look at tree first
    tree_port = []
    cotree_port = []
    tree_nonport = []
    cotree_nonport = []

    for ele_name in column_names[0 : len(row_names)]:
        if isinstance(ele_name_obj_map[ele_name], PortElement):
            tree_port.append(ele_name)
        else:
            tree_nonport.append(ele_name)
    for ele_name in column_names[len(row_names) :]:
        if isinstance(ele_name_obj_map[ele_name], PortElement):
            cotree_port.append(ele_name)
        else:
            cotree_nonport.append(ele_name)

    
    reorder_matrix_by_colum_label(
        A_matrix,
        tree_port + tree_nonport + cotree_nonport + cotree_port,
        ele_name_col_map,
    )
    # update column_names
    column_names = update_column_labels(ele_name_col_map)
    
    assert all(x==y for x,y in zip(  column_names, tree_port+tree_nonport+cotree_nonport+cotree_port  ))
    
    print("Incident mateix after reogranize")
    print_matrix(A_matrix=A_matrix, column_names=column_names, row_names=row_names)
    return A_matrix, tree_port, cotree_port, tree_nonport, cotree_nonport


def system_realization(netList: list[list[str]], supress_inconsistenc=False)->NetworkMatrix:
    """Retrieve the circuit network toplolgy from netList variable

    Parameters
    ----------
    netList : list[list[str]]
        List of elements in the newtork
    supress_inconsistenc : bool, optional
        _description_, by default False

    Returns
    -------
    NetworkMatrix
        Circuit Network
    """
    
    #TODO: instead of the supress inconsistence parameter
    # check for cutset, loop, and connectivy of the graph
    
    # if everything is good but still did not get full rank M0 at the beginning, means inherent dependency between elements, like two inductor connect in series
    
    # process netlisth
    node_name_obj_map: dict[str, Node] = {"0": GroundNode("GND")}
    node_name_row_map: dict[str, int] = {}
    ele_name_obj_map: dict[str, Element] = {}
    ele_name_col_map: dict[str, int] = {}

    symbollic_to_value_map: dict[Symbol:float] = {}
    symbolic_str_to_var_map:dict[str, Symbol] = {}
    switch_list: list[ExternalSwitch | Diode] = []
    source_list: list[VoltageCurrentSource] = []
    inductor_capacitor_list: list[Inductor | Capacitor] = []
    meter_list: list[Voltmeter | Ammeter] = []

    # load from netlist
    read_netlis_description(
        netList=netList,
        node_name_obj_map=node_name_obj_map,
        ele_name_obj_map=ele_name_obj_map,
        ele_name_col_map=ele_name_col_map,
        symbollic_to_value_map=symbollic_to_value_map,
        switch_list=switch_list,
        source_list=source_list,
        inductor_capacitor_list=inductor_capacitor_list,
        meter_list=meter_list,
    )

    # now, build the Indcidence matrix A

    A_matrix, tree_port, cotree_port, tree_nonport, cotree_nonport = (
        gen_incident_matrix(
            node_name_obj_map=node_name_obj_map,
            node_name_row_map=node_name_row_map,
            ele_name_obj_map=ele_name_obj_map,
            ele_name_col_map=ele_name_col_map,
        )
    )
    column_names = update_column_labels(ele_name_col_map)
    row_names = update_row_labels(node_name_row_map)

    A_tree_inverse = A_matrix[0 : len(row_names), 0 : len(row_names)].inv()

    D_matrix = A_tree_inverse * A_matrix  #(3-30) equation in Leo-chua's book


    a = len(tree_port)
    z = len(tree_nonport)
    y = len(cotree_nonport)
    b = len(cotree_port)
    D_cotree: Matrix = D_matrix[0 : len(row_names), len(row_names) :]  # 6.55 of Chua
    D_ay: Matrix = D_cotree[0:a, 0:y]
    D_ab: Matrix = D_cotree[0:a, y:]
    D_zy: Matrix = D_cotree[a:, 0:y]
    D_zb: Matrix = D_cotree[a:, y:]

    # now, forming the F matrix in Leo-chua's book (6-66) 

    # add iz
    iz_labels = []
    vy_labels = []
    iy_labels = []
    vz_labels = []
    ia_labels = []
    vb_labels = []
    ib_labels = []
    va_labels = []

    for z_ele_name in tree_nonport:
        ele = ele_name_obj_map[z_ele_name]
        iz_labels.append(ele.element_current_name)
        vz_labels.append(ele.element_voltage_name)
    for y_ele_name in cotree_nonport:
        ele = ele_name_obj_map[y_ele_name]
        iy_labels.append(ele.element_current_name)
        vy_labels.append(ele.element_voltage_name)
    for a_ele_name in tree_port:
        ele = ele_name_obj_map[a_ele_name]
        ia_labels.append(ele.element_current_name)
        va_labels.append(ele.element_voltage_name)
    for b_ele_name in cotree_port:
        ele = ele_name_obj_map[b_ele_name]
        ib_labels.append(ele.element_current_name)
        vb_labels.append(ele.element_voltage_name)
    F_labels = (
        iz_labels
        + vy_labels
        + iy_labels
        + vz_labels
        + ia_labels
        + vb_labels
        + ib_labels
        + va_labels
    )

    row_in_F = []
    for z_ele_name in tree_nonport:
        ele: NonPortElement = ele_name_obj_map[z_ele_name]
        row_in_F.append(ele.voltage_current_relationship(F_labels,ele_name_obj_map))
    for y_ele_name in cotree_nonport:
        ele: NonPortElement = ele_name_obj_map[y_ele_name]
        row_in_F.append(ele.voltage_current_relationship(F_labels,ele_name_obj_map))

    F_lower_matrix = sp.Matrix(row_in_F)

    # pprint(F_lower_matrix)

    F_iz = F_lower_matrix[:, 0:z]

    start_ind = F_iz.cols
    F_vy = F_lower_matrix[:, start_ind : start_ind + y]

    start_ind += F_vy.cols
    F_iy = F_lower_matrix[:, start_ind : start_ind + y]

    start_ind += F_iy.cols
    F_vz = F_lower_matrix[:, start_ind : start_ind + z]

    start_ind += F_vz.cols
    F_ia = F_lower_matrix[:, start_ind : start_ind + a]

    start_ind += F_ia.cols
    F_vb = F_lower_matrix[:, start_ind : start_ind + b]

    start_ind += F_vb.cols
    F_ib = F_lower_matrix[:, start_ind : start_ind + b]

    start_ind += F_ib.cols
    F_va = F_lower_matrix[:, start_ind:]

    F_iy_hat = F_iy - F_iz * D_zy

    F_vz_hat = F_vz + F_vy * (D_zy.transpose())

    F_ib_hat = F_ib - F_iz * D_zb

    F_va_hat = F_va + F_vy * (D_ay.transpose())

    F_ia_hat = F_ia
    F_vb_hat = F_vb

    row1_size = D_ab.shape[0]
    row2_size = D_ab.transpose().shape[0]
    row3_size = F_va_hat.shape[0]

    col1_size = y
    col2_size = z
    col3_size = a
    col4_size = b
    col5_size = b
    col6_size = a

    if col1_size == 0 and col2_size == 0:
        m_ = [
            [
                eye(row1_size, col3_size),
                zeros(row1_size, col4_size),
                D_ab,
                zeros(row1_size, col6_size),
            ],
            [
                zeros(row2_size, col3_size),
                eye(row2_size, col4_size),
                zeros(row2_size, col5_size),
                -D_ab.transpose(),
            ],
            [F_ia_hat, F_vb_hat, F_ib_hat, F_va_hat],
        ]
        M = Matrix(m_)
        m_labels = ia_labels + vb_labels + ib_labels + va_labels
        m_labels_mapping = {m_labels[i]: i for i in range(len(m_labels))}
    elif col2_size == 0:
        m_ = [
            [
                D_ay,
                eye(row1_size, col3_size),
                zeros(row1_size, col4_size),
                D_ab,
                zeros(row1_size, col6_size),
            ],
            [
                zeros(row2_size, col1_size),
                zeros(row2_size, col3_size),
                eye(row2_size, col4_size),
                zeros(row2_size, col5_size),
                -D_ab.transpose(),
            ],
            [F_iy_hat, F_ia_hat, F_vb_hat, F_ib_hat, F_va_hat],
        ]
        M = Matrix(m_)
        m_labels = iy_labels + ia_labels + vb_labels + ib_labels + va_labels
        m_labels_mapping = {m_labels[i]: i for i in range(len(m_labels))}
    elif col1_size == 0:
        m_ = [
            [
                zeros(row1_size, col2_size),
                eye(row1_size, col3_size),
                zeros(row1_size, col4_size),
                D_ab,
                zeros(row1_size, col6_size),
            ],
            [
                -D_zb.transpose(),
                zeros(row2_size, col3_size),
                eye(row2_size, col4_size),
                zeros(row2_size, col5_size),
                -D_ab.transpose(),
            ],
            [F_vz_hat, F_ia_hat, F_vb_hat, F_ib_hat, F_va_hat],
        ]
        M = Matrix(m_)
        m_labels = vz_labels + ia_labels + vb_labels + ib_labels + va_labels
        m_labels_mapping = {m_labels[i]: i for i in range(len(m_labels))}
    else:
        m_ = [
            [
                D_ay,
                zeros(row1_size, col2_size),
                eye(row1_size, col3_size),
                zeros(row1_size, col4_size),
                D_ab,
                zeros(row1_size, col6_size),
            ],
            [
                zeros(row2_size, col1_size),
                -D_zb.transpose(),
                zeros(row2_size, col3_size),
                eye(row2_size, col4_size),
                zeros(row2_size, col5_size),
                -D_ab.transpose(),
            ],
            [F_iy_hat, F_vz_hat, F_ia_hat, F_vb_hat, F_ib_hat, F_va_hat],
        ]
        M = Matrix(m_)
        m_labels = iy_labels + vz_labels + ia_labels + vb_labels + ib_labels + va_labels
        m_labels_mapping = {m_labels[i]: i for i in range(len(m_labels))}

    
    # At this point, M matrix is define exactly as (6-67) in the book by Leon-o-chu and pen-lin, and a (8) in Antonio Massarini and Ugo Reeggiani "An efficient Algorithm for the formulation of state equations ..."
    # now reorder the m_label matrix

    # the order is w, u_tilt, s, y, x_hat, x, 0, u
    # w is all nonport element [iy, vz]
    w = iy_labels + vz_labels

    def sort_for_u(item1:VoltageCurrentSource, item2:VoltageCurrentSource): # current source first
        if item1.is_voltage_source == False and item2.is_voltage_source:
            return -1
        elif item1.is_voltage_source and item2.is_voltage_source == False:
            return 1
        else:
            return 0
    def sort_for_meter(item1:Element, item2:Element):  # voltmeter first
        if isinstance(item1,Voltmeter) and isinstance(item2, Ammeter):
            return 1
        elif isinstance(item1, Ammeter) and isinstance(item2, Voltmeter):
            return -1
        else:
            return 0
    def sort_for_switch(item1:Element, item2:Element):  # switch first, then diode
        if isinstance(item1, ExternalSwitch) and isinstance(item2, Diode):
            return -1
        elif isinstance(item1, Diode ) and isinstance(item2, ExternalSwitch):
            return 1
        else:
            return 0
    def sort_for_capacitor_inductor(item1:Element, item2:Element):
        if isinstance(item1, Inductor) and isinstance(item2, Capacitor):
            return -1
        elif isinstance(item1, Capacitor) and isinstance(item2, Inductor):
            return 1
        else:
            
            if isinstance(item1, Inductor) and isinstance(item2, Inductor):
                if len(item1.K_factors) > 0 and len(item2.K_factors) > 0 and item1.name in item2.mutual_inductor_names:
                    return 0
                else:
                    if item1.name < item2.name:
                        return -1
                    else:
                        return 1
            return 0

    u_tilt = []
    u = []
    y = []
    y_zero = []
    s = []
    s_zero = []
    x_hat = []
    x = []
    source_list.sort(key=cmp_to_key(sort_for_u))  # current sources first, than voltages source
    meter_list.sort(key = cmp_to_key(sort_for_meter)) # Ammeters, than voltmeters
    switch_list.sort(key=cmp_to_key(sort_for_switch)) # External Switches, then diodes
    inductor_capacitor_list.sort(key=cmp_to_key(sort_for_capacitor_inductor)) # indocutors, than capacitors

    
    for ele in source_list:
        if  not ele.is_voltage_source:  # current source
            u_tilt.append( ele.element_voltage_name)
            u.append(ele.element_current_name)
        else:  # voltage source
            u_tilt.append( ele.element_current_name)
            u.append(ele.element_voltage_name)
    
    for ele in meter_list:
        if isinstance(ele, Voltmeter):
            y.append(ele.element_voltage_name)
            y_zero.append( ele.element_current_name)
        else:  # Ammeter
            y.append(ele.element_current_name)
            y_zero.append(ele.element_voltage_name)
    
    for ele in switch_list:
        if ele.initial_switch_state:
            s.append(ele.element_current_name)
            s_zero.append(ele.element_voltage_name)
        else:
            s.append(ele.element_voltage_name)
            s_zero.append(ele.element_current_name)
    
    for ele in inductor_capacitor_list:
        if isinstance(ele, Inductor):
            x_hat.append(ele.element_voltage_name)
            x.append(ele.element_current_name)
        else:
            x_hat.append(ele.element_current_name)
            x.append(ele.element_voltage_name)
    

    # x_hat = ['I_C1', 'V_L1', 'V_LS0', 'V_LS1', 'V_LS2', 'I_C2']
    # x = ['V_C1', 'I_L1', 'I_LS0', 'I_LS1', 'I_LS2', 'V_C2']
    
    # x_hat = ['V_Lr','I_Cr','I_C1','V_Lm','V_Lp','V_Ls']
    # x =['I_Lr','V_Cr','V_C1','I_Lm','I_Lp','I_Ls']
    reordered_m_labels = w + u_tilt + s + y + x_hat + x + s_zero + y_zero + u
    reordered_m_lable_obj_mapping = {}
    capacitor_count = 0
    inductor_count = 0
    voltage_source_count = 0
    current_source_count = 0
    for key, value in ele_name_obj_map.items():
        reordered_m_lable_obj_mapping[value.element_voltage_name] = value
        reordered_m_lable_obj_mapping[value.element_current_name] = value
        
        if isinstance(value, Capacitor):
            capacitor_count += 1
        elif isinstance(value, Inductor):
            inductor_count += 1
        elif isinstance(value,VoltageCurrentSource):
            if value.is_voltage_source:
                voltage_source_count += 1
            else:
                current_source_count += 1
        
    reorder_matrix_by_colum_label(M, reordered_m_labels, m_labels_mapping)

    # M = M.subs(symbollic_to_value_map)

    
    # do any rref on M matrix
    M, pivots = M.rref()
    print(pivots)
    # ensure pivots are in consective order
    for i in range(len(pivots)):
        if i != pivots[i]:
            if supress_inconsistenc:
                print("Warning: inconsistency system detected!")
            else:
                raise ValueError("Network inconsistency detect for initial circuit topology")

    print_matrix(M, reordered_m_labels, ["" for x in range(M.shape[0])])

    
    net =  NetworkMatrix(
        M_topology=M[:,:],
        m_column_labels=reordered_m_labels,
        m_colmn_labels_to_obj_map=reordered_m_lable_obj_mapping,
        element_name_obj_map=ele_name_obj_map,
        symbolic_to_value_map=symbollic_to_value_map,
        s_label_size= len(s),
        y_label_size=len(y),
        x_hat_label_size=len(x_hat),
        x_label_size=len(x),
        s_zero_label_size=len(s_zero),
        y_zero_label_size=len(y_zero),
        u_label_size=len(u),
        capactior_size=capacitor_count,
        inductor_size=inductor_count,
        voltage_source_size=voltage_source_count,
        current_source_size=current_source_count,
        redundant_size= len(w+u_tilt),
        simpilfied=False

    )

    net.rref_update()  # do it for the first time


    return net    
    


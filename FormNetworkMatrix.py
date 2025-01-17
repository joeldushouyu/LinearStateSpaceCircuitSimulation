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

from util import print_matrix, write_matrix_info,  swapTwoColumn, retrieveSystemMatrix, transfer_func_and_poles, print_matrix_for_matlab_format
import ast
import re
class NetworkMatrix:
    def __init__(
        self,
        M_topology:Matrix,
        m_column_labels: list[str],
        m_colmn_labels_to_obj_map: dict[str, Element],
        element_name_obj_map:dict[str, Element],
        symbolic_to_value_map:dict[str, float],
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
        simpilfied = True
    ):
        
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
        # M is the matrix after apply mutual inductance effect between inductors
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
        
        # self.external_switch_labels = []
        
        # for i in range(len(self.s_labels)):
        #     lab = self.s_labels[i]
        #     ele = self.m_column_labels_to_obj_map[lab]
        #     if isinstance(ele, ExternalSwitch):
        #         self.external_switch_labels.append(lab)
    def apply_mutual_inductance_effect(self, sub_value=True):

        # x_hat_col_offset = self.s_labels_size+ self.y_label_size  + self.redundant_size
        
        # for x_hat_index,  x_hat_lab in enumerate( self.m_column_labels[x_hat_col_offset: x_hat_col_offset+self.x_hat_label_size]):
            
        #     if x_hat_index +x_hat_col_offset  not in self.M_toplolgy_pivots:
        #         continue # means is dependent matrix
        #     ele = self.m_column_labels_to_obj_map[x_hat_lab]
        #     if isinstance(ele, Inductor):
        #         for mutual_index, mutual_element_name in enumerate(ele.mutual_inductor_names):
        #             mutual_inductor_ele = self.element_name_obj_map[mutual_element_name]  
        #             k_value = ele.K_factors[mutual_index]
                    
        #             mutual_inductor_col = self.m_column_labels.index( mutual_inductor_ele.element_voltage_name)
        #             inductor_row =  self.M_toplolgy_pivots.index( x_hat_index +x_hat_col_offset) # by def, pivot's column is the first nonzero in the row
                    
        #             assert mutual_inductor_col < x_hat_col_offset + self.x_hat_label_size
        #             assert inductor_row < x_hat_col_offset + self.x_hat_label_size
                    
        #             # rescale by 1/ele.inductor_symbol, because ele.inductor_symbol is already in the M_topolgy matrix
        #             # after doing rref, the col of x_hat of inductor = 1, means the whole role is already scaled bye
        #             # 1/ele.inductance already
        #             if mutual_inductor_col in self.M_toplolgy_pivots :
        #                 self.M[inductor_row, mutual_inductor_col ] =  k_value * sp.sqrt(ele.inductor_symbol * mutual_inductor_ele.inductor_symbol)
                    
        #             inductor_col = self.m_column_labels.index( ele.element_voltage_name)
        #             self.M[inductor_row, inductor_col] = ele.inductor_symbol
        #     elif isinstance(ele, Capacitor):
        #         capacitor_col = self.m_column_labels.index( ele.element_current_name)
        #         capacitor_row =  self.M_toplolgy_pivots.index( x_hat_index +x_hat_col_offset) # by def, pivot's column is the first nonzero in the row
        #         self.M[capacitor_row, capacitor_col] = ele.capacitor_symbol
        if sub_value:
    
            self.M, self.M_pivots = self.M.rref()



            self.M = self.M.subs(self.symbolic_to_value_map)
    
    
    def rref_update(self):
        self.M_topology = self.M_topology.subs(self.symbolic_to_value_map)
        self.M, self.M_toplolgy_pivots = self.M_topology.rref(iszerofunc=lambda x:abs(x)<10**-10)
        self.M = self.M_topology[:,:].copy()
        self.apply_mutual_inductance_effect(True)
    def update_M_matrix(self, labels_to_swap:str, sub_value = True):
        
        
        swapTwoColumn(self.M_topology, self.m_column_labels, self.m_column_labels_to_obj_map, labels_to_swap )
        # self.M_topology = self.M_topology.subs(self.symbolic_to_value_map)
        # self.M, self.M_toplolgy_pivots = self.M_topology.rref(iszerofunc=lambda x:abs(x)<10**-10)
        # self.M = self.M_topology[:,:].copy()
        # self.apply_mutual_inductance_effect(sub_value)
        

    def print_M_matrix(self ):
        print_matrix(self.M, self.m_column_labels, ["" for x in range(self.M.shape[0])])
        
    @cached_property
    def external_switch_labels(self):
        return [     lab for lab in self.s_labels if isinstance(self.m_column_labels_to_obj_map[lab], ExternalSwitch)      ]
    @cached_property
    def s_labels(self):
        

        return self.m_column_labels[ self.redundant_size : self.s_labels_size + self.redundant_size]

    @cached_property
    def y_labels(self):
        offset = self.redundant_size + self.s_labels_size
        return self.m_column_labels[offset: offset+ self.y_label_size]

    @cached_property
    def x_hat_labels(self):
        offset = self.redundant_size+ self.s_labels_size+ self.y_label_size
        return self.m_column_labels[offset: offset+ self.x_hat_label_size]
    @cached_property
    def x_labels(self):
        offset = self.redundant_size+self.s_labels_size+ self.y_label_size + self.x_hat_label_size
        return self.m_column_labels[offset: offset + self.x_label_size]
    @cached_property
    def s_zero_labels(self):
        offset = self.redundant_size + self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size
        return self.m_column_labels[offset: offset+  self.s_zero_label_size]
    @cached_property
    def y_zero_labels(self):
        offset = self.redundant_size + self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size + self.s_zero_label_size
        
        return self.m_column_labels[offset: offset + self.y_zero_label_size]
    @cached_property
    def u_labels(self):
        offset = self.redundant_size + self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size + self.s_zero_label_size + self.y_zero_label_size
        return self.m_column_labels[offset: ]
def update_column_labels(element_col_map: dict[str, int]) -> list[str]:
    sorted_ele_col = [
        k for k, v in sorted(element_col_map.items(), key=lambda item: item[1])
    ]

    return sorted_ele_col


def update_row_labels(node_row_map: dict[str, int]) -> list[str]:
    return [k for k, v in sorted(node_row_map.items(), key=lambda item: item[1])]


def reorder_matrix_by_colum_label(
    matrix: Matrix, new_col_name: list[str], ele_name_col_map: dict[str, int]
) -> Matrix:
    m_temp = matrix[:, :]
    # assert len(new_col_name) == len(ele_name_col_map)


        
    for col in range(len(new_col_name)):
        if col == 4:
            p = 20
        new_ele_name = new_col_name[col]

        matrix[:, col] = m_temp[:, ele_name_col_map[new_ele_name]]

        ele_name_col_map[new_ele_name] = col


def read_netlis_description(
    netList: list[list[str]],
    node_name_obj_map: dict[str, Node],
    node_name_row_map: dict[str, int],
    ele_name_obj_map: dict[str, Element],
    ele_name_col_map: dict[str, int],
    symbollic_to_value_map: dict[Symbol:float],
    switch_list: list[ExternalSwitch | Diode],
    source_list: list[VoltageCurrentSource],
    inductor_capacitor_list: list[Inductor | Capacitor],
    meter_list: list[Voltmeter | Ammeter],
):
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
                ele = Diode(labels[0], node_a, node_b, initial_state)
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


def system_realization(netList: list[list[str]]):
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
        node_name_row_map=node_name_row_map,
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
    # # get D matrix
    # # D = At^-1 *A
    A_tree_inverse = A_matrix[0 : len(row_names), 0 : len(row_names)].inv()

    D_matrix = A_tree_inverse * A_matrix
    # pprint(D_matrix)

    a = len(tree_port)
    z = len(tree_nonport)
    y = len(cotree_nonport)
    b = len(cotree_port)
    D_cotree: Matrix = D_matrix[0 : len(row_names), len(row_names) :]  # 6.55 of Chua
    D_ay: Matrix = D_cotree[0:a, 0:y]
    D_ab: Matrix = D_cotree[0:a, y:]
    D_zy: Matrix = D_cotree[a:, 0:y]
    D_zb: Matrix = D_cotree[a:, y:]

    # now, forming the F matrix in 6-66 chua

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
            return -1
        elif isinstance(item1, Ammeter) and isinstance(item2, Voltmeter):
            return 1
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
    # generate util, u
    u_tilt = []
    u = []
    y = []
    y_zero = []
    s = []
    s_zero = []
    x_hat = []
    x = []
    source_list.sort(key=cmp_to_key(sort_for_u))
    meter_list.sort(key = cmp_to_key(sort_for_meter))
    switch_list.sort(key=cmp_to_key(sort_for_switch))
    inductor_capacitor_list.sort(key=cmp_to_key(sort_for_capacitor_inductor))
    #u: current source, then voltage source
    #x: inductor, then capacitor
    
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



    
    # do any rref on M matrix
    M, pivots = M.rref()
    print(pivots)
    # ensure pivots are in consective order
    for i in range(len(pivots)):
        assert i == pivots[i]


    # multiple L/C to result in correct x_hat. Since ic = C*dv/dt
    #page 349 of Chua, section 4
    offset = len(w + u_tilt + s + y)
    
    for i in range(offset, offset+len(x_hat)):
        label = x_hat[i-offset]
        ele = reordered_m_lable_obj_mapping[label]

        if isinstance(ele, Capacitor):
            #M[i,i] *= ele.capacitor_symbol
            M[i,i] = ele.capacitor_symbol
        else:
            assert isinstance(ele, Inductor)
            # #M[i,i] *= ele.inductor_symbol 
            M[i,i] = ele.inductor_symbol 
            
            for index, mutual_element_lab in enumerate(ele.mutual_inductor_names):
                mutual_inductor_ele = ele_name_obj_map[mutual_element_lab]
                
                col_index = offset  + x_hat.index(mutual_inductor_ele.element_voltage_name)
                
                k_value =  ele.K_factors[index]
                M[i, col_index] = k_value *  sp.sqrt( ele.inductor_symbol *  mutual_inductor_ele.inductor_symbol )

    
    #M = M.subs(symbollic_to_value_map)
    # # # debug
    # M, pivots = M.rref()
    # redundant_columns_size = len(w + u_tilt)
    # M = M[redundant_columns_size:, redundant_columns_size:]
    # reordered_m_labels = reordered_m_labels[redundant_columns_size:]
    # print_matrix(M, reordered_m_labels, ["" for x in range(M.shape[0])])

    # swapTwoColumn(M, reordered_m_labels, reordered_m_lable_obj_mapping, "V_D1")
    # # swapTwoColumn(M, reordered_m_labels, reordered_m_lable_obj_mapping, "V_D2")
    # # k = M.subs(symbollic_to_value_map)
    # # k[5,6] = 0
    # # # k[6,6] = 0
    # # k[6,5] = 0
    # # k[6,7] = 0
    # # k[7,6] = 0
    
    
    # M_t, p = M.rref()
    
    

    # M_t[:, 6] *=0.000280014285349873
    # M_t[:, 7] *=  0.000280014285349873
    # M_t, p = M_t.rref()
    k = 200
    # swapTwoColumn(M, reordered_m_labels, reordered_m_lable_obj_mapping, "V_D1")
    # M, _ = M.rref()

    
    # # # M = M.subs(symbollic_to_value_map)
    # M, pivot = M.rref()

    # assert M.rank() == M.shape[0]


    print_matrix(M, reordered_m_labels, ["" for x in range(M.shape[0])])
    
    # # print("M before reduced with real value")
    # print_matrix(M.subs(symbollic_to_value_map), reordered_m_labels, ["" for x in range(M.shape[0])])
    # now, remove the w, utilted columns from the matrix
    # redundant_columns_size = len(w + u_tilt)
    
    
    # M = M[redundant_columns_size:, redundant_columns_size:]
    # reordered_m_labels = reordered_m_labels[redundant_columns_size:]
    
    
    
    
    M, pivot = M.rref()
    
    
    M = M.subs(symbollic_to_value_map)
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
    # net.M_topology, _ = net.M_topology.rref()
    net.apply_mutual_inductance_effect()  # do it for the first time

    s_dxdt, Sx, Su, C1, C, D, M0, A, B, C_SW, D_SW, inconsistent_labels = retrieveSystemMatrix(
        M=net.M,
        m_labels=net.m_column_labels,
        m_pivots=net.M_pivots,
        s_labels_size=net.s_labels_size,
        y_labels_size=net.y_label_size,
        x_hat_labels_size=net.x_hat_label_size,
        x_labels_size=net.x_label_size,
        y_zero_labels_size=net.y_zero_label_size,
        s_zero_labels_size=net.s_zero_label_size,
        capacitor_size= net.capacitor_size,
        inductor_size=net.inductor_size,
        voltage_source_size=net.voltage_source_size,
        current_source_size=net.current_source_Size,
        redundant_offset=net.redundant_size
        
    )
    with open("test.txt","w") as f:
        print_matrix(net.M, net.m_column_labels, ["" for x in range(net.M.shape[0])], file=f)
    print("s_dxdt")
    pprint(s_dxdt)

    print("sx")
    pprint(Sx)

    print("su")
    pprint(Su)

    print("C1")
    pprint(C1)
    print("C")
    pprint(C)
    print("D")
    pprint(D)

    print("M0")
    pprint(M0)
    print("A")
    pprint(A)
    print("B")
    pprint(B)

    print("C_SW")
    pprint(C_SW)
    
    print("D_SW")
    pprint(D_SW)

    _, pivot = net.M.rref()
    
    for i in range(len(pivot)):
        if pivot[i] != i:
            raise ValueError("Error in the network matrix")
        
        
    # # check transfer func and stability
    A_iter= A.subs(symbollic_to_value_map)
    B_iter = B.subs(symbollic_to_value_map)
    C_iter = C.subs(symbollic_to_value_map)
    D_iter = D.subs(symbollic_to_value_map)
    
    # # Print matrices in MATLAB format
    # print("\nA = [")
    # print(np.array2string(np.array(A_iter).astype(float), separator=', ', precision=8).replace('[', '').replace(']', ''))
    # print("];")

    # print("\nB = [")
    # print(np.array2string(np.array(B_iter).astype(float), separator=', ', precision=8).replace('[', '').replace(']', ''))
    # print("];")

    # print("\nC = [")
    # print(np.array2string(np.array(C_iter).astype(float), separator=', ', precision=8).replace('[', '').replace(']', ''))
    # print("];")

    # print("\nD = [")
    # print(np.array2string(np.array(D_iter).astype(float), separator=', ', precision=8).replace('[', '').replace(']', ''))
    # print("];")
    
    
    
    
    print("A with subs")
    pprint(A)
    # transfer_func, poles, pole_roots = transfer_func_and_poles(A, B, C, D, symbolic_value_map=symbollic_to_value_map)
    # print("Transfer function :")
    # pprint(transfer_func)
    # print("DET SI-A  POLES")
    # pprint(sp.simplify(poles))
    # print("Poles of system")
    # print(pole_roots)
    
    print("Eigen values of A")  # should be less than 1 for discrete system, or less than 0 for    
    pprint(A_iter.eigenvals())
    
    # check if any negative eigen values
    # Check if any eigenvalue has a positive real part
    for eigenval in A_iter.eigenvals():
        if eigenval.as_real_imag()[0] > 0:  # Check real part of eigenvalue
            warning_msg = "Warning: System is unstable! Found eigenvalue with positive real part."
            print(warning_msg)
            # raise ValueError(warning_msg)
    
    # print("value of eigen values of A")
    # tmp = A.subs(symbollic_to_value_map)
    # print(tmp.eigenvals())
    
    # write_matrix_info(net=net)
    
    
    
    # test of swap
    # false, true
    # net.update_M_matrix("V_D1")
    # net.update_M_matrix("V_D2")
    # s_dxdt, Sx, Su, C1, C, D, M0, A, B, C_SW, D_SW, inconsistent_labels = retrieveSystemMatrix(
    #     M=net.M,
    #     m_labels=net.m_column_labels,
    #     m_pivots=net.M_pivots,
    #     s_labels_size=net.s_labels_size,
    #     y_labels_size=net.y_label_size,
    #     x_hat_labels_size=net.x_hat_label_size,
    #     x_labels_size=net.x_label_size,
    #     y_zero_labels_size=net.y_zero_label_size,
    #     s_zero_labels_size=net.s_zero_label_size,
    #     capacitor_size= net.capacitor_size,
    #     inductor_size=net.inductor_size,
    #     voltage_source_size=net.voltage_source_size,
    #     current_source_size=net.current_source_Size,
    #     redundant_offset=net.redundant_size
        
    # )
    return net    
    

    # try to swap it
    # swapTwoColumn(M, reordered_m_labels, reordered_m_lable_obj_mapping, "I_S1")
    # swapTwoColumn(M, reordered_m_labels, reordered_m_lable_obj_mapping, "V_D1")
    # M, pivot = M.rref()
    # print("After swap")
    # print_matrix(M, reordered_m_labels, ["" for x in range(M.shape[0])])

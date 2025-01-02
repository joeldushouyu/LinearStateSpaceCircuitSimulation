from Element import (
    Element,
    GroundNode,
    Node,
    Inductor,
    Capacitor,
    ExternalSwitch,
    Diode,
    Resistor,
    DependentSource,
    VoltageCurrentSource,
    Voltmeter,
    Ammeter,
    PortElement,
    NonPortElement,
)
from typing import Tuple
from functools import cached_property
# any example of boost
import numpy as np
import sympy as sp
from sympy import Matrix, pi, pprint, Symbol, eye, zeros

from util import print_matrix, swapTwoColumn, retrieveSystemMatrix


class NetworkMatrix:
    def __init__(
        self,
        M: Matrix,
        m_column_labels: list[str],
        m_colmn_labels_to_obj_map: dict[str, Element],
        symbolic_to_value_map:dict[str, float],
        s_label_size:int,
        y_label_size:int,
        x_hat_label_size:int,
        x_label_size:int,
        s_zero_label_size:int,
        y_zero_label_size:int,
        u_label_size:int
    ):
        self.M = M
        self.m_column_labels = m_column_labels
        self.m_column_labels_to_obj_map = m_colmn_labels_to_obj_map
        self.symbolic_to_value_map = symbolic_to_value_map

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


    @cached_property
    def external_switch_labels(self):
        return [     lab for lab in self.s_labels if isinstance(self.m_column_labels_to_obj_map[lab], ExternalSwitch)      ]
    @cached_property
    def s_labels(self):
        return self.m_column_labels[: self.s_labels_size]

    @cached_property
    def y_labels(self):
        offset =  self.s_labels_size
        return self.m_column_labels[offset: offset+ self.y_label_size]

    @cached_property
    def x_hat_labels(self):
        offset = self.s_labels_size+ self.y_label_size
        return self.m_column_labels[offset: offset+ self.x_hat_label_size]
    @cached_property
    def x_labels(self):
        offset = self.s_labels_size+ self.y_label_size + self.x_hat_label_size
        return self.m_column_labels[offset: offset + self.x_label_size]
    @cached_property
    def s_zero_labels(self):
        offset = self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size
        return self.m_column_labels[offset: offset+  self.s_zero_label_size]
    @cached_property
    def y_zero_labels(self):
        offset = self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size + self.s_zero_label_size
        
        return self.m_column_labels[offset: offset + self.y_zero_label_size]
    @cached_property
    def u_labels(self):
        offset = self.s_labels_size+ self.y_label_size + self.x_hat_label_size + self.x_label_size + self.s_zero_label_size + self.y_zero_label_size
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
    assert len(new_col_name) == len(ele_name_col_map)

    for i in range(len(new_col_name)):
        new_ele_name = new_col_name[i]

        matrix[:, i] = m_temp[:, ele_name_col_map[new_ele_name]]

        ele_name_col_map[new_ele_name] = i


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
        labels = [s.strip() for s in desc.split(",")]

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
            case "L":
                inductor_symbol = sp.symbols(labels[0])
                inductor_val = float(labels[3])
                ele = Inductor(labels[0], node_a, node_b, inductor_val, inductor_symbol)
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
                initial_state = True if labels[3] == "ON" else False
                ele = ExternalSwitch(
                    labels[0],
                    node_a,
                    node_b,
                    initial_state,
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
    # print_matrix(A_matrix=A_matrix, column_names=column_names, row_names=row_names)

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

    # print_matrix(A_matrix=A_matrix, column_names=column_names, row_names=row_names)
    return A_matrix, tree_port, cotree_port, tree_nonport, cotree_nonport


def system_realization(netList: list[list[str]]):
    # process netlisth
    node_name_obj_map: dict[str, Node] = {"0": GroundNode("GND")}
    node_name_row_map: dict[str, int] = {}
    ele_name_obj_map: dict[str, Element] = {}
    ele_name_col_map: dict[str, int] = {}

    symbollic_to_value_map: dict[Symbol:float] = {}

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
        row_in_F.append(ele.voltage_current_relationship(F_labels))
    for y_ele_name in cotree_nonport:
        ele: NonPortElement = ele_name_obj_map[y_ele_name]
        row_in_F.append(ele.voltage_current_relationship(F_labels))

    F_lower_matrix = sp.Matrix(row_in_F)

    # pprint(F_lower_matrix)

    F_iz = F_lower_matrix[:, 0:z]

    start_ind = len(F_iz)
    F_vy = F_lower_matrix[:, start_ind : start_ind + y]

    start_ind += len(F_vy)
    F_iy = F_lower_matrix[:, start_ind : start_ind + y]

    start_ind += len(F_iy)
    F_vz = F_lower_matrix[:, start_ind : start_ind + z]

    start_ind += len(F_vz)
    F_ia = F_lower_matrix[:, start_ind : start_ind + a]

    start_ind += len(F_ia)
    F_vb = F_lower_matrix[:, start_ind : start_ind + b]

    start_ind += len(F_vb)
    F_ib = F_lower_matrix[:, start_ind : start_ind + b]

    start_ind += len(F_ib)
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
    u_tilt = [
        ele.element_current_name if ele.is_voltage_source else ele.element_voltage_name
        for ele in source_list
    ]
    s = [
        ele.element_current_name
        if ele.initial_switch_state
        else ele.element_voltage_name
        for ele in switch_list
    ]
    y = [
        ele.element_current_name
        if isinstance(ele, Ammeter)
        else ele.element_voltage_name
        for ele in meter_list
    ]
    x_hat = [
        ele.element_current_name
        if isinstance(ele, Capacitor)
        else ele.element_voltage_name
        for ele in inductor_capacitor_list
    ]
    x = [
        ele.element_voltage_name
        if isinstance(ele, Capacitor)
        else ele.element_current_name
        for ele in inductor_capacitor_list
    ]

    y_zero = [
        ele.element_current_name
        if isinstance(ele, Voltmeter)
        else ele.element_voltage_name
        for ele in meter_list
    ]
    s_zero = [
        ele.element_current_name
        if not ele.initial_switch_state
        else ele.element_voltage_name
        for ele in switch_list
    ]
    u = [
        ele.element_voltage_name if ele.is_voltage_source else ele.element_current_name
        for ele in source_list
    ]

    reordered_m_labels = w + u_tilt + s + y + x_hat + x + s_zero + y_zero + u
    reordered_m_lable_obj_mapping = {}
    for key, value in ele_name_obj_map.items():
        reordered_m_lable_obj_mapping[value.element_voltage_name] = value
        reordered_m_lable_obj_mapping[value.element_current_name] = value
    reorder_matrix_by_colum_label(M, reordered_m_labels, m_labels_mapping)

    # multiple L/C to result in correct x_hat. Since ic = C*dv/dt
    offset = len(w + u_tilt + s + y)
    for i in range(offset, offset + len(x_hat)):
        ele = inductor_capacitor_list[i - offset]

        if isinstance(ele, Capacitor):
            M[:, i] *= ele.capacitor_symbol
        else:
            M[:, i] *= ele.inductor_symbol
    M, pivot = M.rref()

    assert M.rank() == M.shape[0]

    # now, remove the w, utilted columns from the matrix
    redundant_columns_size = len(w + u_tilt)
    M = M[redundant_columns_size:, redundant_columns_size:]
    reordered_m_labels = reordered_m_labels[redundant_columns_size:]
    print_matrix(M, reordered_m_labels, ["" for x in range(M.shape[0])])

    s_dxdt, Sx, Su, C1, C, D, M0, A, B = retrieveSystemMatrix(
        M=M,
        s_labels=s,
        y_labels=y,
        x_hat_labels=x_hat,
        x_labels=x,
        y_zero_labels=y_zero,
        s_zero_labels=s_zero,
    )
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

    net =  NetworkMatrix(
        M=M,
        m_column_labels=reordered_m_labels,
        m_colmn_labels_to_obj_map=reordered_m_lable_obj_mapping,
        symbolic_to_value_map=symbollic_to_value_map,
        s_label_size= len(s),
        y_label_size=len(y),
        x_hat_label_size=len(x_hat),
        x_label_size=len(x),
        s_zero_label_size=len(s_zero),
        y_zero_label_size=len(y_zero),
        u_label_size=len(u)

    )
    
    
    return net    
    

    # try to swap it
    # swapTwoColumn(M, reordered_m_labels, reordered_m_lable_obj_mapping, "I_S1")
    # swapTwoColumn(M, reordered_m_labels, reordered_m_lable_obj_mapping, "V_D1")
    # M, pivot = M.rref()
    # print("After swap")
    # print_matrix(M, reordered_m_labels, ["" for x in range(M.shape[0])])

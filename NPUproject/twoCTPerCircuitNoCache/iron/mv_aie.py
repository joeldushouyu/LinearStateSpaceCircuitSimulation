import numpy as np
import sys

from aie.dialects.aie import *
from aie.dialects.aiex import *
from aie.extras.context import mlir_mod_ctx
from aie.helpers.dialects.ext.scf import _for as range_
import math

import numpy as np
import sys

from ml_dtypes import bfloat16
from aie.extras.context import mlir_mod_ctx
from aie.dialects.aie import *
from aie.dialects.aiex import *
from aie.helpers.dialects.ext.scf import _for as range_

import numpy as np
import sys

from aie.dialects.aie import *
from aie.dialects.aiex import *
from aie.extras.context import mlir_mod_ctx
from aie.helpers.dialects.ext.scf import _for as range_

from aie.dialects import memref

from aie.dialects._aie_ops_gen import buffer as buffer_raw
from aie.helpers.util import try_convert_np_type_to_mlir_type
import numpy as np
import sys
import aie.utils.trace as trace_utils
from aie.utils.trace import PortEvent
from aie.utils.trace_events_enum import CoreEvent, MemEvent, ShimTileEvent, MemTileEvent
from enum import IntEnum
from aie.extras.dialects.ext.arith import constant, index_cast

from aie.ir import *
from aie.ir import MemRefType, IndexType
from aie.dialects import arith, memref
from aie.dialects.memref import AllocaScopeOp

from aie.helpers.util import np_ndarray_type_to_memref_type
from aie.dialects.memref import alloc, store, alloca
from aie.extras import types as T


from aie.dialects.aiex import control_packet
import os
import json
import json


def custom_ceil(x, multiplier):
  return math.ceil(x / multiplier) * multiplier




def generate_packet_attribute(packet_type:int, packet_id:int):
    return Attribute.parse(f"#aie.packet_info<pkt_type = {packet_type}, pkt_id = {packet_id}>")

kernel_mat_v_size = 16
def single_mat_vect_mult():
    dev = AIEDevice.npu2
    


    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
    file_path = os.path.join(script_dir, "final_config.json")

    with open(file_path, "r") as f:
        extracted_data = json.load(f)

    trace_size = extracted_data.get("trace_size")
    state_size = extracted_data.get("state_size")
    u_size = extracted_data.get("u_size")
    y_size = extracted_data.get("y_size")
    diode_size = extracted_data.get("diode_size")
    switch_size = extracted_data.get("switch_size")
    C1_DSW_row_size = extracted_data.get("C1_DSW_row_size")
    C1_DSW_col_size = extracted_data.get("C1_DSW_col_size")
    C1_DSW_matrix_size = extracted_data.get("C1_DSW_matrix_size")
    C1_DSW_buffer_size = extracted_data.get("C1_DSW_buffer_size")
    A_B_C_D_row_size = extracted_data.get("A_B_C_D_row_size")
    A_B_C_D_col_size = extracted_data.get("A_B_C_D_col_size")
    A_B_C_D_matrix_size = extracted_data.get("A_B_C_D_matrix_size")
    A_B_C_D_buffer_size = extracted_data.get("A_B_C_D_buffer_size")
    AB_matrix_size = extracted_data.get("AB_mat_size")
    CD_nat_or_imp_matrix_size= extracted_data.get("CD_nat_or_imp_mat_size")
    input_switch_size = extracted_data.get("input_switch_size")
    input_size_per_iteration = extracted_data.get("input_size_per_iteration")
    output_size_per_iteration = extracted_data.get("output_size_per_iteration")
    iteration_step_per_ping_pong_buffer = extracted_data.get("iteration_step_per_ping_pong_buffer")
    buffer_size_of_in_ping_pong = extracted_data.get("buffer_size_of_in_ping_poing")
    buffer_size_of_out_ping_pong = extracted_data.get("buffer_size_of_out_ping_pong")
    ping_pong_buffer_iteration = extracted_data.get("ping_pong_buffer_iteration")
    buffer_size_of_cur_X_U = extracted_data.get("buffer_size_of_cur_X_U")
    buffer_size_of_C1_DSW_mat_res = extracted_data.get("buffer_size_of_C1_DSW_mat_res")
    buffer_size_of_A_B_C_D_mat_res = extracted_data.get("buffer_size_of_A_B_C_D_mat_res")
    stack_size_in_byte = extracted_data.get("stack_size")
    total_switch_diode_state = extracted_data.get("total_switch_diode_state")
    dtype_in = np.dtype[np.float32]
    dtype_out = np.dtype[np.float32]
    dtype_npuint32  = np.dtype[np.uint32]
    
    SHIMTILE_0_CONTROL_ID=8
    @device(AIEDevice.npu2)
    def device_body():


   
        # Tile declarations
        ShimTile_0 = tile(0,0)
        ShimTile_0.attributes["controlled_id"] = generate_packet_attribute(0,SHIMTILE_0_CONTROL_ID)
        ShimTile_1 = tile(1, 0)
        # ComputeTile_0_2 = tile(0,2)        
        # ComputeTile_0_2 = tile(0,2, allocation_scheme="bank-aware")        
        ComputeTile_0_2 = tile(0, 2,allocation_scheme="bank-aware") # round robin allocation bank allocation        
        ComputeTile_0_3 = tile(0,3, allocation_scheme="basic-sequential")


        
        #NOTE: mem_bank flag seem not working anymore after Tile() is configure to basic-sequential address mode
        offset = stack_size_in_byte
        assert stack_size_in_byte %64 == 0

        switch_diode_matrix_ty = np.ndarray[ (C1_DSW_buffer_size, ), dtype_in]
        switch_diode_buffer = [
            buffer_raw(tile=ComputeTile_0_3, buffer=try_convert_np_type_to_mlir_type(switch_diode_matrix_ty), sym_name=f"switch_diode_buffer", address=offset) 
        ]
        switch_diode_prod_lock =  lock(ComputeTile_0_3, lock_id=0, init=1, sym_name="switch_diode_prod_lock")
        switch_diode_con_lock = lock(ComputeTile_0_3, lock_id=1, init=0, sym_name="switch_diode_con_lock")
        offset+= C1_DSW_buffer_size*4
        assert offset %64 == 0
        

        A_B_C_D_ty = np.ndarray[(A_B_C_D_buffer_size,  ), dtype_in]
        A_B_C_D_buffer = [
            buffer_raw(tile=ComputeTile_0_3, buffer=try_convert_np_type_to_mlir_type(A_B_C_D_ty), sym_name="A_B_C_D_buffer", address=offset)
        ]
        A_B_C_D_prod_lock = lock(ComputeTile_0_3, lock_id=2, init=2, sym_name="A_B_C_D_prod_lock")
        A_B_C_D_con_lock = lock(ComputeTile_0_3, lock_id=3, init=0, sym_name="A_B_C_D_con_lock")
        offset += A_B_C_D_buffer_size*4
        assert offset %64 == 0
        
        control_packet_ty = np.ndarray[ (16,),dtype_npuint32  ]
        control_packet_CT_out = [
            buffer_raw(tile=ComputeTile_0_3, buffer = try_convert_np_type_to_mlir_type(control_packet_ty), 
                       sym_name="control_packet_CT_out", address=offset
                       )
            
        ]
        offset += 64
        assert offset%64 == 0
        control_packet_CT_out_prod_lock = lock(ComputeTile_0_3, lock_id=4, init=1, sym_name="control_packet_CT_out_prod_lock")
        control_packet_CT_out_con_lock = lock(ComputeTile_0_3, lock_id=5, init=0, sym_name="control_packet_CT_out_con_lock")

        control_packet_CT_in = [
            buffer_raw(tile=ComputeTile_0_3, buffer=try_convert_np_type_to_mlir_type(control_packet_ty),
                       sym_name="control_packet_CT_in", address=offset
                       )
        ]
        offset += 64        
        assert offset%64 == 0
        control_packet_CT_in_prod_lock = lock(ComputeTile_0_3, lock_id=6, init=1, sym_name="control_packet_CT_in_prod_lock")
        control_packet_CT_in_con_lock = lock(ComputeTile_0_3, lock_id=7, init=0, sym_name="control_packet_CT_in_con_lock")
        
        C1_DSW_matrix_ty = np.ndarray[ (C1_DSW_matrix_size,), dtype_in]
        AB_matrix_ty = np.ndarray[(AB_matrix_size,), dtype_in]
        CD_natural_impulse_matrix_ty = np.ndarray[(CD_nat_or_imp_matrix_size*2, ), dtype_in]
        
        C1_DSW_matrix_buffer= [
            buffer_raw(tile=ComputeTile_0_3, buffer=try_convert_np_type_to_mlir_type(C1_DSW_matrix_ty),
                       sym_name="C1_DSW_matrix_buffer", address=offset
                       )
        ]
        C1_DSW_matrix_prod_lock = lock(ComputeTile_0_3, lock_id=8, init=1, sym_name="C1_DSW_matrix_prod_lock")
        C1_DSW_matrix_con_lock = lock(ComputeTile_0_3, lock_id=9, init=0, sym_name="C1_DSW_matrix_con_lock")
        offset += 4*C1_DSW_matrix_size
        assert offset %64 == 0
        
        AB_matrix_buffer = [
            buffer_raw(tile=ComputeTile_0_3, buffer=try_convert_np_type_to_mlir_type(AB_matrix_ty),
                       sym_name="AB_matrix_buffer", address=offset
                       )
            
        ]
        AB_matrix_prod_lock = lock(ComputeTile_0_3, lock_id=10, init=1, sym_name="AB_matrix_prod_lock")
        AB_matrix_con_lock = lock(ComputeTile_0_3, lock_id=11, init=0, sym_name="AB_matrix_con_lock")
        offset += 4*AB_matrix_size
        assert offset%64 == 0
        
        CD_natural_impulse_matrix_buffer = [
            buffer_raw(tile=ComputeTile_0_3, buffer=try_convert_np_type_to_mlir_type(CD_natural_impulse_matrix_ty),
                       sym_name="CD_natural_impulse_matrix_buffer", address=offset
                       )
        ]
        CD_natural_impulse_matrix_prod_lock = lock(ComputeTile_0_3, lock_id=12, init=1, sym_name="CD_natural_impulse_matrix_prod_lock")
        CD_natural_impulse_matrix_con_lock = lock(ComputeTile_0_3, lock_id=13, init=0, sym_name="CD_natural_impulse_matrix_con_lock")
        
        offset += 4*(2*CD_nat_or_imp_matrix_size)
        assert offset%64 == 0        
        assert offset <= (64*1024)  # total of less than 64kB
        
        
    
        in_data_ty = np.ndarray[ (buffer_size_of_in_ping_pong, ), dtype_in]
        out_data_ty = np.ndarray[ (buffer_size_of_out_ping_pong, ), dtype_out]
        
        in_buffer = [
            buffer(tile=ComputeTile_0_2, datatype=in_data_ty, name=f"in_buffer_{0}"),
            buffer(tile=ComputeTile_0_2, datatype=in_data_ty, name=f"in_buffer_{1}"),
        ]
        in_buffer_prod_lock = lock(ComputeTile_0_2, lock_id=8, init=2, sym_name="in_buffer_p_lock")
        in_buffer_con_lock = lock(ComputeTile_0_2, lock_id=9, init=0, sym_name="in_buffer_c_lock")
  
  
        out_buffer = [
            buffer(tile=ComputeTile_0_2,datatype=out_data_ty, name=f"out_buffer_{0}" ), 
            buffer(tile=ComputeTile_0_2, datatype=out_data_ty, name=f"out_buffer_{1}" ), #             
        ]        
        out_buffer_prod_lock = lock(ComputeTile_0_2, lock_id=10, init=2)
        out_buffer_con_lock = lock(ComputeTile_0_2, lock_id=11, init=0)

        # first uint32 externalSwitchDiodeState
        # then external_switch_toggled(uint32 0==false, else is true)
        # then diode_change  (uint32 0== false, else is true)
        C_D_matrix_select_ty = np.ndarray[ (3, ), np.dtype[np.uint32]]
        # test_buf = [
        #     buffer(tile=ComputeTile_0_2, datatype=C_D_matrix_select_ty, name="test_buf")   
        # ]
        
        C_D_matrix_select_buffer = [
            buffer(tile=ComputeTile_0_2, datatype=C_D_matrix_select_ty, name="C_D_matrix_select_buffer")   
        ]
        
        
        # strategy to balance out the S2MM workload on two port of CT_0_2

         
        @mem(ComputeTile_0_2)
        def m(block):
            s0 = dma_start(DMAChannelDir.S2MM, 0, dest=block[1], chain=block[3])
            with block[1]:
                use_lock(in_buffer_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(in_buffer[0], offset=0, len=buffer_size_of_in_ping_pong)
                use_lock(in_buffer_con_lock, LockAction.Release, value=1)
                next_bd(block[2])
            with block[2]:
                use_lock(in_buffer_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(in_buffer[1], offset=0, len=buffer_size_of_in_ping_pong)
                use_lock(in_buffer_con_lock, LockAction.Release, value=1)
                next_bd(block[1])
            with block[3]:
                s1= dma_start(DMAChannelDir.MM2S, 0, dest=block[4], chain=block[6])
            with block[4]:
                use_lock(out_buffer_con_lock, action=LockAction.AcquireGreaterEqual, value=1)
                dma_bd(out_buffer[0],  offset=0, len=buffer_size_of_out_ping_pong, packet=(0,9))
                use_lock(out_buffer_prod_lock, LockAction.Release, value=1)
                next_bd(block[5])
            with block[5]:
                use_lock(out_buffer_con_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(out_buffer[1],   offset=0, len=buffer_size_of_out_ping_pong, packet=(0,9))                
                use_lock(out_buffer_prod_lock, LockAction.Release, value=1)
                next_bd(block[4])
            with block[6]:
                EndOp()
        @mem(ComputeTile_0_3)
        def m(block):
            # s0  = dma_start(DMAChannelDir.S2MM, 0, dest=block[1], chain=block[3])
            # with block[1]:
            #     use_lock(switch_diode_prod_lock, LockAction.AcquireGreaterEqual, value=1)
            #     dma_bd(switch_diode_buffer[0], offset=0, len=C1_DSW_buffer_size)
            #     use_lock(switch_diode_con_lock, LockAction.Release, value=1)
            #     next_bd(block[2])
            # with block[2]:
            #     use_lock(A_B_C_D_prod_lock, LockAction.AcquireGreaterEqual, value=1)
            #     dma_bd( A_B_C_D_buffer[0], offset=0, len=A_B_C_D_buffer_size)
            #     use_lock(A_B_C_D_con_lock, LockAction.Release, value=1)
            #     next_bd(block[7]) # finished 
            # with block[3]:
            #     s1 = dma_start(DMAChannelDir.MM2S, 0, dest=block[4], chain=block[5])
            # with block[4]:
            #     use_lock(control_packet_CT_out_con_lock, LockAction.AcquireGreaterEqual, value=1)
            #     dma_bd(control_packet_CT_out[0],offset=0, len=2, packet=(0, 8), bd_id=4 )# have CT to set the len of control packet message
            #     use_lock(control_packet_CT_out_prod_lock, LockAction.Release, value=1)
            #     next_bd(block[4])                
            # with block[5]:
            #     s2 = dma_start(DMAChannelDir.S2MM, 1, dest=block[6], chain=block[7] )
            # with block[6]:
            #     use_lock(control_packet_CT_in_prod_lock, LockAction.AcquireGreaterEqual, value=1)
            #     dma_bd(control_packet_CT_in[0], offset=0, len=1) # can also be change by CT
            #     use_lock(control_packet_CT_in_con_lock, LockAction.Release, value=1)
            #     next_bd(block[6])
            # with block[7]:
            #     EndOp()
            
            
            s0 =  dma_start(DMAChannelDir.MM2S, 0, dest=block[1], chain=block[2])
            with block[1]:
                use_lock(control_packet_CT_out_con_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(control_packet_CT_out[0],offset=0, len=2, packet=(0, 8), bd_id=4 )# have CT to set the len of control packet message
                use_lock(control_packet_CT_out_prod_lock, LockAction.Release, value=1)
                next_bd(block[1])                
            with block[2]:
                s1= dma_start(DMAChannelDir.S2MM, 1, dest=block[3], chain=block[4] )
            with block[3]:
                use_lock(control_packet_CT_in_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(control_packet_CT_in[0], offset=0, len=1) # can also be change by CT
                use_lock(control_packet_CT_in_con_lock, LockAction.Release, value=1)
                next_bd(block[3])
            with block[4]:
                s2  = dma_start(DMAChannelDir.S2MM, 0, dest=block[5], chain=block[11]) 
            with block[5]:
                use_lock(C1_DSW_matrix_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(C1_DSW_matrix_buffer[0], offset=0, len = kernel_mat_v_size) # first transfer 16
                use_lock(C1_DSW_matrix_con_lock, LockAction.Release, value=1)
                next_bd(block[6])
            with block[6]:
                use_lock(C1_DSW_matrix_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(C1_DSW_matrix_buffer[0], offset=kernel_mat_v_size, len =C1_DSW_matrix_size-kernel_mat_v_size )
                use_lock(C1_DSW_matrix_con_lock, LockAction.Release, value=1)
                next_bd(block[7])
            with block[7]:
                use_lock(AB_matrix_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(AB_matrix_buffer[0], offset=0, len=kernel_mat_v_size)
                use_lock(AB_matrix_con_lock, LockAction.Release, value=1)
                next_bd(block[8])
            with block[8]:
                use_lock(CD_natural_impulse_matrix_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(CD_natural_impulse_matrix_buffer[0], offset=0, len=kernel_mat_v_size)
                use_lock(CD_natural_impulse_matrix_con_lock, LockAction.Release, value=1)
                next_bd(block[9])
            with block[9]:
                use_lock(AB_matrix_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(AB_matrix_buffer[0], offset=kernel_mat_v_size, len = AB_matrix_size - kernel_mat_v_size)
                use_lock(AB_matrix_con_lock, LockAction.Release, value=1)
                next_bd(block[10])                
            with block[10]:
                use_lock(CD_natural_impulse_matrix_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(CD_natural_impulse_matrix_buffer[0], offset=kernel_mat_v_size, len= (2*CD_nat_or_imp_matrix_size)-kernel_mat_v_size)
                use_lock(CD_natural_impulse_matrix_con_lock, LockAction.Release, value=1)
                next_bd(block[5])
            with block[11]:
                EndOp()
                
        CT_0_3_main_func = external_func("CT_main", inputs=[
            in_data_ty, out_data_ty,
            in_data_ty, out_data_ty,            
            np.int32, np.int32,
            np.int32,
            switch_diode_matrix_ty, A_B_C_D_ty,
            C_D_matrix_select_ty,
            np.int32, np.int32,
            np.int32, np.int32,
            control_packet_ty,
            control_packet_ty,
            np.int32, np.int32,
            np.int32, np.int32,
            np.int32, np.int32,
            C1_DSW_matrix_ty,
            AB_matrix_ty,
            CD_natural_impulse_matrix_ty                                           
        ])

        @core(ComputeTile_0_3, "kernel1.o", stack_size=stack_size_in_byte)
        def core_body():
            # for _ in range_(sys.maxsize):
            CT_0_3_main_func(
                in_buffer[0], out_buffer[0],
                in_buffer[1], out_buffer[1],                
                constant(8),constant(9),
                constant(48 +3 ),
                switch_diode_buffer[0], A_B_C_D_buffer[0],
                C_D_matrix_select_buffer[0],
                constant(48+4), constant(48+5),
                constant(48+6), constant(48+7),
                control_packet_CT_out[0],
                control_packet_CT_in[0],
                constant(48+8), constant(48+9),
                constant(48+10), constant(48+11),
                constant(48+12), constant(48+13),
                C1_DSW_matrix_buffer[0],
                AB_matrix_buffer[0],
                CD_natural_impulse_matrix_buffer[0]
            )


        CT_0_2_main_func = external_func("CT_0_2_main", inputs=[
            out_data_ty, out_data_ty,
            A_B_C_D_ty,
            C_D_matrix_select_ty,
            np.int32, np.int32
        ] )
        @core(ComputeTile_0_2, "kernel2.o", stack_size=stack_size_in_byte)
        def core_body():
            CT_0_2_main_func(
                out_buffer[0],out_buffer[1],
                A_B_C_D_buffer[0],
                C_D_matrix_select_buffer[0],
                constant(10+48),constant(11+48),
            )
            
        matrix_size =C1_DSW_buffer_size+A_B_C_D_buffer_size
        data_flow_out_size = buffer_size_of_out_ping_pong *ping_pong_buffer_iteration   # lest do 4 multple o f ping-pong size
        data_flow_in_size =  buffer_size_of_in_ping_pong*ping_pong_buffer_iteration

        
        if(trace_size > 0):
            tiles_to_trace = [ComputeTile_0_2] #TODO: also shimtile?
            trace_utils.configure_packet_tracing_flow(tiles_to_trace, ShimTile_1)

        # leave first 6(0-5) packet id for tracing
        packetflow( 6, source=ShimTile_0, source_port=WireBundle.DMA, source_channel=0, 
                   dest = ComputeTile_0_3, dest_port=WireBundle.DMA, dest_channel=0
                   )
        # Shimtile TilControl -> Computile_0_3
        packetflow(pkt_id=7, source=ShimTile_0, source_port=WireBundle.TileControl, source_channel=0,
                   dest = ComputeTile_0_3, dest_port=WireBundle.DMA, dest_channel=1
                   )
        #CT_0_3 -> Shimtile Tilecontrol
        packetflow(pkt_id=8, source=ComputeTile_0_3, source_port=WireBundle.DMA, source_channel=0,
                   dest=ShimTile_0, dest_port=WireBundle.TileControl, dest_channel=0
                   )
        # output ping-pong form CT_0_2
        packetflow(pkt_id=9, source=ComputeTile_0_2, source_port=WireBundle.DMA, source_channel=0,
                    dest = ShimTile_0, dest_port= WireBundle.DMA, dest_channel=1
                   ) 
        # only one should be sufficient for now?TODO, since we are compute Bound anyway 
        packetflow( 10, source=ShimTile_0, source_port=WireBundle.DMA, source_channel=1, 
                   dest = ComputeTile_0_2, dest_port=WireBundle.DMA, dest_channel=0
                   )
        
        memref.global_("in_SHM_CT_0_3_0", T.memref( matrix_size, T.f32() ), sym_visibility="public")            
        memref.global_("in_SHM_CT_0_3_1", T.memref(data_flow_in_size, T.f32()), sym_visibility="public")

        memref.global_("out_CT_0_2_SHM", T.memref( data_flow_out_size, T.f32()), sym_visibility="public" ) # result out

     
        shim_dma_allocation("in_SHM_CT_0_3_0", DMAChannelDir.MM2S, 0, 0)        
        shim_dma_allocation("out_CT_0_2_SHM", DMAChannelDir.S2MM, 1,0)
        shim_dma_allocation("in_SHM_CT_0_3_1", DMAChannelDir.MM2S, 1, 0 )

        @runtime_sequence(np.ndarray[(matrix_size, ), dtype_in], np.ndarray[(matrix_size, ), dtype_out], np.ndarray[(data_flow_in_size,), dtype_in], np.ndarray[(data_flow_out_size,), dtype_out]  )
        def sequence(A,B, in_buf, out_buf):
            # work balance module
            if(trace_size > 0):
                trace_utils.configure_packet_tracing_aie2(
                    tiles_to_trace=tiles_to_trace,
                    ddr_id=4,   # last in/out parameter(not just need to pass in host, did not define in sequence)
                    shim =ShimTile_1,
                    trace_size=trace_size, # beacuse have 2 tile to,
                        coretile_events=[
                        CoreEvent.INSTR_EVENT_0,
                        CoreEvent.INSTR_EVENT_1,
                        CoreEvent.INSTR_VECTOR,
                        PortEvent(CoreEvent.PORT_RUNNING_0, 1, True),  # master(1)
                        PortEvent(CoreEvent.PORT_RUNNING_1, 1, False),  # slave(1)
                        PortEvent(CoreEvent.PORT_RUNNING_2, 7, False),  # slave(1)                        
                        # CoreEvent.INSTR_CASCADE_PUT,
                        # CoreEvent.INSTR_CASCADE_GET,
                        # CoreEvent.INSTR_STORE,
                        CoreEvent.LOCK_STALL,
                        CoreEvent.STREAM_STALL,
                    ],
                    coremem_events=[
                            MemEvent.CONFLICT_DM_BANK_0,
                            MemEvent.CONFLICT_DM_BANK_1,
                            MemEvent.CONFLICT_DM_BANK_2,
                            MemEvent.CONFLICT_DM_BANK_3,
                            MemEvent.CONFLICT_DM_BANK_4,
                            MemEvent.CONFLICT_DM_BANK_5,
                            MemEvent.CONFLICT_DM_BANK_6,
                            MemEvent.CONFLICT_DM_BANK_7,
                    ],         
                   shimtile_events=[
                        ShimTileEvent.DMA_MM2S_0_START_TASK,
                        ShimTileEvent.DMA_MM2S_0_FINISHED_BD,
                        ShimTileEvent.DMA_MM2S_0_MEMORY_STARVATION,
                        ShimTileEvent.DMA_MM2S_0_FINISHED_TASK,
                        ShimTileEvent.DMA_MM2S_ERROR,
                        ShimTileEvent.CONTROL_PKT_ERROR
   
                    ],                                      
                )
    


            # changes 
            # MM2S 0 sending input iteration data only
            
            # MM2S 1 sends C1_DSW, ABCD matrixes
            # version of DMA transmit data without doing data reordering(should be done by host already)
            
            # repalce npu_dam_memcpy_nd with manual setp
            #npu_write32(address=0x1d000, column=0, row=0, value= C1_DSW_buffer_size+A_B_C_D_buffer_size )
            npu_write32(address=0x1d004, column=0, row=0, value=0)
            npu_write32(address=0x1d008, column=0, row=0, value= (1<<30) | (6<<19) | (0<<16))
            npu_write32(address=0x1d00C, column=0, row=0, value=0)
            npu_write32(address=0x1d010, column=0, row=0, value= (2<<30))
            npu_write32(address=0x1d014, column=0, row=0, value=0)
            npu_write32(address=0x1d018, column=0, row=0, value=0)
            npu_write32(address=0x1d01C, column=0, row=0, value=0x2000000)
            
            npu_address_patch (addr = 0x1d004 , arg_idx = 0 , arg_plus = 0 ) # argidx=0, since is A, arg_puls=0 for zero offset
            npu_maskwrite32(address=0x1d210, column=0, row=0, mask=0xF00,  value=(SHIMTILE_0_CONTROL_ID<<8))
            #npu_write32(address=0x1D214, column=0, row=0, value=0x0) #trigger by CT_03 through control packet
            
            
            # now, push to MM2S-0
            # npu_dma_memcpy_nd(
            #     metadata="in_SHM_CT_0_3_0",
            #     bd_id=0,
            #     mem=A, offsets=[0,0,0,0], 
            #     sizes = [  1,1,1, C1_DSW_buffer_size+A_B_C_D_buffer_size],
            #     strides= [ 0,0,0,1 ],
            #     packet=(0,6)                  
            # )
            
            # enable core access to bus
            npu_maskwrite32(address=0x32038, column=0, row=2, value=0x1, mask=0x1) # NOTE: the place of it is crucial
            npu_maskwrite32(address=0x32038, column=0, row=3, value=0x1, mask=0x1)

            npu_dma_memcpy_nd(metadata="in_SHM_CT_0_3_1", bd_id=1, mem=in_buf, offsets=[0,0,0,0], 
                                     sizes=[1,1,1, data_flow_in_size ], strides=[0,0,0,1], packet=(0,10))
            
            npu_dma_memcpy_nd(metadata="out_CT_0_2_SHM", bd_id=3, mem=out_buf, offsets=[0,0,0,0], sizes=[1,1,1, data_flow_out_size], 
                                     strides=[0,0,0,1], issue_token=True)


            npu_dma_wait("out_CT_0_2_SHM")

with mlir_mod_ctx() as ctx:
    single_mat_vect_mult()
    res = ctx.module.operation.verify()
    if res == True:
        print(ctx.module)
    else:
        print(res)

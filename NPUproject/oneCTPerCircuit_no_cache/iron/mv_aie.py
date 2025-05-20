from struct import pack
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

# def round_to_nearest_multiple(n, multiple):
#   """Rounds an integer to the nearest multiple of a given number"""
#   if multiple == 0:
#       return n  # Avoid division by zero
#   return ((n + multiple - 1) // multiple) * multiple
import os
import json
import json
# npu_dma_memcpy_nd
def balance_matrix_transfer_case(switch_diode_matrix_size, buffer_A_B_C_D_size, A_B_C_D_row_size, A_B_C_D_col_size):
    mid_point = (switch_diode_matrix_size+ buffer_A_B_C_D_size)//2
    
    # Note: the matrix granduality is divided to 2 matrix
    # one matrix for switch_diode case, and repeats for total_sw_size
    
    # another matrix for A_B_C_D_ case, and repeats for total_sw_size
    
    
    
    mid_size = (mid_point-switch_diode_matrix_size)
    
    A_B_C_D_matrix_number_cutoff = mid_size//(  A_B_C_D_row_size *A_B_C_D_col_size )
    
    return   A_B_C_D_matrix_number_cutoff

    # if(mid_point > switch_diode_matrix_size and mid_point < (switch_diode_matrix_size+A_B_matrix_size)):
    #     return 1, mid_point-switch_diode_matrix_size  # midpoint in A_B_matrix
    # elif(mid_point   >  (switch_diode_matrix_size+A_B_matrix_size) and mid_point < (switch_diode_matrix_size+A_B_matrix_size+C_D_imp_matrix_size)):
    #     return 2, mid_point-switch_diode_matrix_size-A_B_matrix_size
    # else:
    #     raise ValueError("Unexpected scenario")
    

# def custom_floor(x, multiplier):
#   return math.floor(x / multiplier) * multiplier

def custom_ceil(x, multiplier):
  return math.ceil(x / multiplier) * multiplier




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

    A_B_C_D_row_size = extracted_data.get("A_B_C_D_row_size")
    A_B_C_D_col_size = extracted_data.get("A_B_C_D_col_size")
    A_B_C_D_matrix_size = extracted_data.get("A_B_C_D_matrix_size")

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
    
    matrixAllCached:int = extracted_data.get("matrixAllCached")
    cachMatrixNum:int = extracted_data.get("cachMatrixNum")
    
    assert matrixAllCached == 0
    
    dtype_in = np.dtype[np.float32]
    dtype_out = np.dtype[np.float32]
    dtype_control_packet = np.dtype[np.int32]
    
    @device(AIEDevice.npu2)
    def device_body():


   
        # Tile declarations
        ShimTile_0 = tile(0,0)
        ShimTile_1 = tile(1, 0)
        # ComputeTile_0_2 = tile(0,2)        
        # ComputeTile_0_2 = tile(0,2, allocation_scheme="bank-aware")        
        ComputeTile_0_2 = tile(0,2, allocation_scheme="basic-sequential")

        in_data_ty = np.ndarray[ (buffer_size_of_in_ping_pong*2, ), dtype_in]
        out_data_ty = np.ndarray[ (buffer_size_of_out_ping_pong*2, ), dtype_out]
        control_packet_command_out_ty = np.ndarray[ (3,), dtype_control_packet  ] 
            # for write: 1st:regular packet_header for routing, 2nd int32 for address to write, 3rd int32 follow the data value that write to 
            # for read: 1st: regular packet header for routing, 2nd int32 for address to read, 3rd int32 should be undefined( TODO: potentially need to manipulate register at runtime?)
        control_packet_command_res_ty = np.ndarray[ (1,), dtype_control_packet]
        #NOTE: mem_bank flag seem not working anymore after Tile() is configure to basic-sequential address mode
        offset = stack_size_in_byte
        assert stack_size_in_byte %64 == 0
        
        control_packet_command_out_prod_lock = lock(ComputeTile_0_2, lock_id=0, init=0, sym_name="control_packet_command_out_prod_lock")
        control_packet_command_out_con_lock = lock(ComputeTile_0_2, lock_id=1, init=0, sym_name="control_packet_command_out_con_lock")
        control_packet_command_out_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(control_packet_command_out_ty), sym_name=f"control_packet_command_out_buffer", address=offset)
        ]        
        control_packet_command_res_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(control_packet_command_res_ty), sym_name="control_packet_command_res_buffer", address=offset)
        ]
        offset += 64
        
        
        s2mm_prod_lock = lock(ComputeTile_0_2, lock_id=8, init=2, sym_name="s2mm_prod_lock") # init=2 for initial transfer of input ping-pong buffer
        s2mm_con_lock = lock(ComputeTile_0_2, lock_id=9, init=0, sym_name="s2mm_con_lock")
        in_buffer = [
          buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(in_data_ty), sym_name=f"in_buffer_{0}", address=offset),

        ]
        offset+= buffer_size_of_in_ping_pong*2*4
        
        offset = custom_ceil(offset, 64)
        assert offset %64 == 0
        
        """
        cur_x_u_ty = np.ndarray[ (buffer_size_of_cur_X_U,), dtype_in ]
        cur_x_u_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(cur_x_u_ty ), sym_name="cur_x_u_buffer", address=offset)
        ]
        offset+= buffer_size_of_cur_X_U*4
        
        C1_DSW_mat_res_ty = np.ndarray[ (buffer_size_of_C1_DSW_mat_res,), dtype_in]
        C1_DSW_mat_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(C1_DSW_mat_res_ty), sym_name="C1_DSW_mat_buffer", address=offset)
        ]
        offset+= buffer_size_of_C1_DSW_mat_res*4
        
        A_B_C_D_mat_res_ty = np.ndarray[ (buffer_size_of_A_B_C_D_mat_res, ), dtype_in]
        A_B_C_D_mat_res_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(A_B_C_D_mat_res_ty), sym_name="A_B_C_D_mat_res_buffer", address=offset)
        ]
        offset+= buffer_size_of_A_B_C_D_mat_res*4
        """
        
        
        C1_DSW_cache_size = C1_DSW_matrix_size* cachMatrixNum
        switch_diode_matrix_ty = np.ndarray[ (C1_DSW_cache_size, ), dtype_in]
        switch_diode_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(switch_diode_matrix_ty), sym_name=f"switch_diode_buffer", address=offset) 
        ]
        offset+= C1_DSW_cache_size*4
        assert offset %64 == 0
        
        A_B_C_D_cache_size= A_B_C_D_matrix_size * cachMatrixNum
        A_B_C_D_ty = np.ndarray[(A_B_C_D_cache_size,  ), dtype_in]
        A_B_C_D_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(A_B_C_D_ty), sym_name="A_B_C_D_buffer", address=offset)
        ]
        offset += A_B_C_D_cache_size*4
        assert offset %64 == 0
        
        out_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(out_data_ty), sym_name=f"out_buffer_{0}", address=offset ), # 
        ]        
        out_buffer_prod_lock = lock(ComputeTile_0_2, lock_id=10, init=2)
        out_buffer_con_lock = lock(ComputeTile_0_2, lock_id=11, init=0)
        assert offset+buffer_size_of_out_ping_pong*2*4 <= (64*1024)  # total of less than 64kB

        #TODO: lock for indicating complete transaction of C1_DSW, A_B_C_D?
        
        # Use two S2MM port for CT when receive C1_DSW, A_B_C_D matrixes
        # Thus, need to find a point for workload balances
        assert A_B_C_D_matrix_size  > C1_DSW_matrix_size
        
        # below is S2mm 0 and 1 size for single transfer of input_buffer or C1_DSW, A_B_C_D matrix 
        input_buffer_mid = buffer_size_of_in_ping_pong//2
        in0_size_for_input_buffer = input_buffer_mid
        in1_size_for_input_buffer =  buffer_size_of_in_ping_pong - input_buffer_mid
        
        A_B_C_D_mid_offset =    ((C1_DSW_matrix_size + A_B_C_D_matrix_size) // 2 )  - C1_DSW_matrix_size
        in0_size_for_C1_DSW_A_B_C_D_buffer = C1_DSW_matrix_size +A_B_C_D_mid_offset
        in1_size_for_C1_DSW_A_B_C_D_buffer = A_B_C_D_matrix_size - A_B_C_D_mid_offset
            
                
        @mem(ComputeTile_0_2)
        def m(block):
            s0 = dma_start(DMAChannelDir.S2MM, 0, dest=block[1], chain=block[2])
            with block[1]:
                use_lock(s2mm_prod_lock,action=LockAction.AcquireGreaterEqual, value=1 )
                dma_bd(in_buffer[0], offset=0, len=in0_size_for_input_buffer)  # first half of input buffer through dma 0
                use_lock(s2mm_con_lock, LockAction.Release, value=1)
                next_bd(block[1])
            with block[2]:
                s1 = dma_start(DMAChannelDir.S2MM, 1, dest=block[3], chain=block[4])
            with block[3]:
                use_lock(s2mm_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(in_buffer[0], offset=in0_size_for_input_buffer, len=in1_size_for_input_buffer)
                use_lock(s2mm_con_lock, LockAction.Release, value=1)
                next_bd(block[3])
            with block[4]:
                s2 = dma_start(DMAChannelDir.MM2S, 0, dest=block[5], chain=block[7]) # regular ping-pong for output buffer
            with block[5]:
                use_lock(out_buffer_con_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(out_buffer[0], offset=0,  len=buffer_size_of_out_ping_pong, packet=(0,7))
                use_lock(out_buffer_prod_lock, LockAction.Release, value=1)
                next_bd(block[6])
            with block[6]:
                use_lock(out_buffer_con_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(out_buffer[0], offset=buffer_size_of_out_ping_pong, len = buffer_size_of_out_ping_pong,packet=(0,7))
                use_lock(out_buffer_prod_lock, LockAction.Release, value=1)
                next_bd(block[5])
            with block[7]:
            #     s3 = dma_start(DMAChannelDir.MM2S, 1, dest=block[8], chain=block[9]) # control packet out 
            # with block[8]:
            #     use_lock(control_packet_command_out_prod_lock, LockAction.AcquireGreaterEqual, value=1)
            #     dma_bd(control_packet_command_out_buffer[0], offset=0, len=3, packet=(0,9)) #TODO: change offset to 1 for read operation???
            #     use_lock(control_packet_command_out_con_lock, LockAction.Release, value=1)
            #     next_bd(block[8])
            # with block[9]:
                EndOp()
                
                
        # CT_0_2_main_func = external_func("CT_main", inputs=[
        #     in_data_ty, out_data_ty,
        #     np.int32, np.int32, np.int32, np.int32,
        #     switch_diode_matrix_ty, A_B_C_D_ty
        # ])
        
        CT_test_func = external_func("CT_test", inputs = [
            in_data_ty, out_data_ty, 
            np.int32, np.int32, 
            np.int32, np.int32, 
            switch_diode_matrix_ty, A_B_C_D_ty,
            np.int32, np.int32
        ])

        @core(ComputeTile_0_2, "mainKernel.o", stack_size=stack_size_in_byte)
        def core_body():
            # # for _ in range_(sys.maxsize):
            # CT_0_2_main_func(
            #     in_buffer[0], out_buffer[0],
            #     constant(8),constant(9),constant(10),constant(11),
            #     switch_diode_buffer[0], A_B_C_D_buffer[0]
                
            # )
            
            CT_test_func(
                in_buffer[0], out_buffer[0],
                constant(8), constant(9),
                constant(10),constant(11),
                switch_diode_buffer[0], A_B_C_D_buffer[0],
                constant(0), constant(1)
            )

            
  

        
        if(trace_size > 0):
            tiles_to_trace = [ComputeTile_0_2] #TODO: also shimtile?
            trace_utils.configure_packet_tracing_flow(tiles_to_trace, ShimTile_1)

        # leave first 6(0-5) packet id for tracing
        packetflow( 6, source=ShimTile_0, source_port=WireBundle.DMA, source_channel=0, 
                   dest = ComputeTile_0_2, dest_port=WireBundle.DMA, dest_channel=0
                   )
        
        packetflow(7, source=ComputeTile_0_2, source_port=WireBundle.DMA, source_channel=0,
                    dest = ShimTile_0, dest_port= WireBundle.DMA, dest_channel=0
                   ) 
        
        packetflow(8, source=ShimTile_0, source_port=WireBundle.DMA, source_channel=1,
                   dest=ComputeTile_0_2, dest_port=WireBundle.DMA, dest_channel=1
                   )
        # packet 9 CT_dma1 to shimtile_control
        packetflow(pkt_id=9, source=ComputeTile_0_2, source_port=WireBundle.DMA, source_channel=1,
                   dest= ShimTile_0, dest_port=WireBundle.TileControl, dest_channel= 0 
                   )
        # packet 10 shimtile_control to CT DMA
        packetflow(pkt_id=10, source=ShimTile_0, source_port=WireBundle.TileControl, source_channel=0,
                   dest=ComputeTile_0_2, dest_port=WireBundle.DMA, dest_channel= 0   # for now
                   )
        
        
        total_input_size = ping_pong_buffer_iteration *(buffer_size_of_in_ping_pong)
        total_output_size = ping_pong_buffer_iteration *(buffer_size_of_out_ping_pong)        
        memref.global_("in_SHM_CT_0_2_0", T.memref( total_input_size,
                                                   T.f32() ), sym_visibility="public")            
        memref.global_("in_SHM_CT_0_2_1", T.memref( total_input_size, #TODO:
                                                   T.f32()), sym_visibility="public")
        memref.global_("out_CT_0_2_SHM", T.memref( total_output_size, T.f32()), sym_visibility="public" ) # result size for total simulation

     
        shim_dma_allocation("in_SHM_CT_0_2_0", DMAChannelDir.MM2S, 0, 0)        
        shim_dma_allocation("out_CT_0_2_SHM", DMAChannelDir.S2MM, 0,0)
        shim_dma_allocation("in_SHM_CT_0_2_1", DMAChannelDir.MM2S, 1, 0 )

        total_matrix_size = total_switch_diode_state*(C1_DSW_matrix_size   + A_B_C_D_matrix_size)

        @runtime_sequence(np.ndarray[(total_matrix_size, ), dtype_in], np.ndarray[(total_matrix_size, ), dtype_out], np.ndarray[(total_input_size,), dtype_in], np.ndarray[(total_output_size,), dtype_out]  )
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
                        CoreEvent.INSTR_LOAD,
                        CoreEvent.INSTR_STORE,
                        # CoreEvent.LOCK_STALL,
                    ],
                )

            # setup in_SHM_CT_0_2_0 and SHM_CT_0_2_1 to transfer the 1st buffer for input
            # leave the rest transfer to be control by control_packet method?
            
            npu_dma_memcpy_nd(metadata="in_SHM_CT_0_2_0", bd_id=0, mem=in_buf,offsets= [0,0,0,0],
                              sizes=[1,1,1, in0_size_for_input_buffer], strides=[0,0,0,1], packet=[0,6]
                              )

            npu_dma_memcpy_nd(metadata="in_SHM_CT_0_2_1", bd_id=1, mem=in_buf,offsets= [0,0,0,  in0_size_for_input_buffer],
                              sizes=[1,1,1, in1_size_for_input_buffer], strides=[0,0,0,1], packet=[0,8]
                              )

            npu_dma_memcpy_nd(metadata="out_CT_0_2_SHM", bd_id=2, mem=out_buf, offsets=[0,0,0,0], sizes=[1,1,1, total_output_size], 
                                     strides=[0,0,0,1], issue_token=True)
            npu_dma_wait("out_CT_0_2_SHM")

with mlir_mod_ctx() as ctx:
    single_mat_vect_mult()
    res = ctx.module.operation.verify()
    if res == True:
        print(ctx.module)
    else:
        print(res)

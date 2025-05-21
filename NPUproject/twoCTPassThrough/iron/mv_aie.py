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

import os
import json
import json


def custom_ceil(x, multiplier):
  return math.ceil(x / multiplier) * multiplier




kernel_mat_v_size = 16
def single_mat_vect_mult():
    dev = AIEDevice.npu2
    
    trace_size = 1024
    buffer_size = 1024
    
    total_size = 4096

    dtype_in = np.dtype[np.float32]
    dtype_out = np.dtype[np.float32]
    
    
    @device(AIEDevice.npu2)
    def device_body():


   
        # Tile declarations
        ShimTile_0 = tile(0,0)
        ShimTile_1 = tile(1, 0)
        # ComputeTile_0_2 = tile(0,2)        
        # ComputeTile_0_2 = tile(0,2, allocation_scheme="bank-aware")        
        ComputeTile_0_2 = tile(0,2, allocation_scheme="basic-sequential")

        in_data_ty = np.ndarray[ (buffer_size*2, ), dtype_in]
        out_data_ty = np.ndarray[ (buffer_size*2, ), dtype_out]

        
        #NOTE: mem_bank flag seem not working anymore after Tile() is configure to basic-sequential address mode
        offset = 1024 # reserve for stack
        assert offset %64 == 0
        in_buffer = [
          buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(in_data_ty), sym_name=f"in_buffer_{0}", address=offset),

        ]
        in_buffer_prod_lock = lock(ComputeTile_0_2, lock_id=8, init=2, sym_name="in_buffer_p_lock")
        in_buffer_con_lock = lock(ComputeTile_0_2, lock_id=9, init=0, sym_name="in_buffer_c_lock")
        offset+= buffer_size*2*4
        
        offset = custom_ceil(offset, 64)
        assert offset %64 == 0


        # out_buffer_address = (64*1024) - (buffer_size_of_out_ping_pong*2*4) # 4 byte per float
        out_buffer = [
            buffer_raw(tile=ComputeTile_0_2, buffer=try_convert_np_type_to_mlir_type(out_data_ty), sym_name=f"out_buffer_{0}", address=offset ), # 
        ]        
        out_buffer_prod_lock = lock(ComputeTile_0_2, lock_id=10, init=2)
        out_buffer_con_lock = lock(ComputeTile_0_2, lock_id=11, init=0)

        assert offset+buffer_size*2*4 <= (64*1024)  # total of less than 64kB


        
        @mem(ComputeTile_0_2)
        def m(block):
      
            s0 = dma_start( DMAChannelDir.S2MM, 0, dest=block[1], chain=block[3]) # input DMA0
            
            with block[1]:
                use_lock(in_buffer_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(in_buffer[0], offset=0, len=buffer_size)
                use_lock(in_buffer_con_lock, LockAction.Release, value=1)
                next_bd(block[2])
            with block[2]:
                use_lock(in_buffer_prod_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(in_buffer[0], offset=buffer_size, len=buffer_size)
                use_lock(in_buffer_con_lock, LockAction.Release, value=1)
                next_bd(block[1])
                
            with block[3]:
                s1 = dma_start(DMAChannelDir.MM2S, 0, dest=block[4], chain=block[6])
            with block[4]:
                use_lock(out_buffer_con_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(out_buffer[0], offset=0, len=buffer_size, packet=(0,9))
                use_lock(out_buffer_prod_lock, LockAction.Release, value=1)
                next_bd(block[5])
            with block[5]:
                use_lock(out_buffer_con_lock, LockAction.AcquireGreaterEqual, value=1)
                dma_bd(out_buffer[0], offset=buffer_size, len=buffer_size, packet=(0,9))
                use_lock(out_buffer_prod_lock, LockAction.Release, value=1)
                next_bd(block[4])
            with block[6]:
                EndOp()
                                
        passThroughTest_func = external_func("passThroughTest", inputs=[
            in_data_ty, out_data_ty, 
            np.int32, np.int32,
            np.int32, np.int32,
            np.int32, np.int32
        ])

        @core(ComputeTile_0_2, "passThrough.o", stack_size=1024)
        def core_body():
            passThroughTest_func(
                in_buffer[0], out_buffer[0],
                constant(buffer_size), constant(total_size),
                constant(8+48), constant(9+48),
                constant(10+48), constant(11+48)
            )
                

        if(trace_size > 0):
            tiles_to_trace = [ComputeTile_0_2] #TODO: also shimtile?
            trace_utils.configure_packet_tracing_flow(tiles_to_trace, ShimTile_1)

        # leave first 6(0-5) packet id for tracing
        packetflow( 6, source=ShimTile_0, source_port=WireBundle.DMA, source_channel=0, 
                   dest = ComputeTile_0_2, dest_port=WireBundle.DMA, dest_channel=0
                   )

        packetflow(9, source=ComputeTile_0_2, source_port=WireBundle.DMA, source_channel=0,
                    dest = ShimTile_0, dest_port= WireBundle.DMA, dest_channel=1
                   ) 
        
        memref.global_("in_SHM_CT_0_2_0", T.memref( total_size, T.f32() ), sym_visibility="public")            
        memref.global_("out_CT_0_2_SHM", T.memref( total_size, T.f32()), sym_visibility="public" ) # result out

     
        shim_dma_allocation("in_SHM_CT_0_2_0", DMAChannelDir.MM2S, 0, 0)        
        shim_dma_allocation("out_CT_0_2_SHM", DMAChannelDir.S2MM, 1,0)


        @runtime_sequence(np.ndarray[(total_size, ), dtype_in], np.ndarray[(total_size, ), dtype_out], np.ndarray[(1, ), dtype_in], np.ndarray[(1, ), dtype_in]  )
        def sequence(A,B, zero0, zero1):
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

            npu_dma_memcpy_nd(
                metadata="in_SHM_CT_0_2_0",
                bd_id=0,
                mem=A,
                offsets=[0,0,0,0],
                sizes=[1,1,1, total_size],
                strides=[0,0,0,1],
                packet=(0,6)
            )
            npu_dma_memcpy_nd(
                metadata="out_CT_0_2_SHM",
                bd_id=1,
                mem=B,
                offsets=[0,0,0,0],
                sizes=[1,1,1, total_size],
                strides=[0,0,0,1],
                issue_token=True
            )
            
            
            npu_dma_wait("out_CT_0_2_SHM")

with mlir_mod_ctx() as ctx:
    single_mat_vect_mult()
    res = ctx.module.operation.verify()
    if res == True:
        print(ctx.module)
    else:
        print(res)

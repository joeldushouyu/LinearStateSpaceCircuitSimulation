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

from aie._mlir_libs._mlir.ir import Attribute
from aie.dialects._aiex_ops_gen import _Dialect
from sympy import im
from torch import le

from helper_func import generate_packet_attribute, custom_ceil



def setup_CT_0_3(control_package_data_ty):
    
    # for testing: configure MM2S port
    
    ComputeTile_0_3 = tile(0, 3)
    ComputeTile_0_3.attributes["controlled_id"] = generate_packet_attribute(0, 25)

    To_CT_0_2_control_read_buffer = [
        buffer(tile=ComputeTile_0_3, datatype=control_package_data_ty, name="To_CT_0_2_control_read_buffer")
    ]
    To_CT_0_2_control_read_buffer_prod_lock = lock(ComputeTile_0_3, 
        lock_id=0, init=1, sym_name="To_CT_0_2_control_read_buffer_prod_lock"                                          
    )
    To_CT_0_2_control_read_buffer_con_lock = lock(ComputeTile_0_3,
        lock_id=1, init=0, sym_name="To_CT_0_2_control_read_buffer_con_lock"                                         
    )
    
    # for result of read operation to CT_0_2
    From_CT_0_2_control_read_res_buffer = [
        buffer(tile=ComputeTile_0_3, datatype=control_package_data_ty, name="From_CT_0_2_control_read_res_buffer")
    ]
    From_CT_0_2_controller_read_resbuffer_prod_lock = lock(ComputeTile_0_3,
        lock_id=2, init=1, sym_name="From_CT_0_2_controller_read_resbuffer_prod_lock"
    )
    From_CT_0_2_controller_read_resbuffer_con_lock = lock( ComputeTile_0_3,
        lock_id=3, init=0, sym_name="From_CT_0_2_controller_read_resbuffer_con_lock"
    )
    
    To_CT_0_2_control_write_buffer = [
        buffer(tile=ComputeTile_0_3, datatype=control_package_data_ty, name="To_CT_0_2_control_write_buffer")
    ]
    To_CT_0_2_control_write_buffer_prod_lock = lock(ComputeTile_0_3,
        lock_id=4, init=1, sym_name="To_CT_0_2_control_write_buffer_prod_lock"                                                
    )
    To_CT_0_2_control_write_buffer_con_lock = lock(ComputeTile_0_3,
        lock_id=5, init=0, sym_name="To_CT_0_2_control_write_buffer_con_lock"
    )
    
    @mem(ComputeTile_0_3)
    def m(block):
        s0 = dma_start(DMAChannelDir.MM2S, 0, dest=block[1], chain=block[2])
        
        with block[1]:
            use_lock(To_CT_0_2_control_read_buffer_con_lock, LockAction.AcquireGreaterEqual, value=1)
            dma_bd(To_CT_0_2_control_read_buffer[0], offset=0, len=1, packet= (0,10)) # for now, assume it is always an write operation
            use_lock(To_CT_0_2_control_read_buffer_prod_lock, LockAction.Release, value=1)
            next_bd(block[1])
        with block[2]:
            s2= dma_start(DMAChannelDir.S2MM, 0, dest=block[3], chain=block[4])
        with block[3]:
            use_lock(From_CT_0_2_controller_read_resbuffer_prod_lock, LockAction.AcquireGreaterEqual, value=1)
            dma_bd(From_CT_0_2_control_read_res_buffer[0], offset=0, len = 1)
            use_lock(From_CT_0_2_controller_read_resbuffer_con_lock, LockAction.Release, value=1)
            next_bd(block[3])
        with block[4]:
            s3 = dma_start(DMAChannelDir.MM2S, 1, dest=block[5], chain=block[6])
        with block[5]:
            use_lock(To_CT_0_2_control_write_buffer_con_lock, LockAction.AcquireGreaterEqual, value=1)
            dma_bd(To_CT_0_2_control_write_buffer[0], offset=0, len = 2,packet= (0,12))
            use_lock(To_CT_0_2_control_write_buffer_prod_lock, LockAction.Release, value=1)
            next_bd(block[5])
        with block[6]:
            EndOp()
    
    return ComputeTile_0_3, To_CT_0_2_control_read_buffer, From_CT_0_2_control_read_res_buffer, To_CT_0_2_control_write_buffer
    
    
    
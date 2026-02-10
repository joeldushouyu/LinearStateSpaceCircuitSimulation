
from aie.extras.context import mlir_mod_ctx
from aie.dialects.aie import *
from aie.dialects.aiex import *
from aie.helpers.dialects.ext.scf import _for as range_

from utils import mlir_context, tile_with_location, generate_tile_map, connect_dma


def mvm_i8(tile: tile_with_location, context: mlir_context):
    ct = tile.tile
    row = tile.row
    col = tile.col
    inA_fifo = context.object_fifos[f"inA_{row}_{col}"]
    inB_fifo = context.object_fifos[f"inB"]
    outC_fifo = context.object_fifos[f"outC_{row}_{col}"]
    K_div_k = context.parameters["K_div_k"]
    zero = context.funcs["zero_m_int8"]
    matvec = context.funcs["mv_int8"]

    @core(ct, f"mvm_i8.o")
    def core_body():
        for _ in range_(0xFFFFFFFF):
            elem_out = outC_fifo.acquire(ObjectFifoPort.Produce, 1)
            zero(elem_out)

            for _ in range_(K_div_k):
                elem_in_a = inA_fifo.acquire(ObjectFifoPort.Consume, 1)
                elem_in_b = inB_fifo.acquire(ObjectFifoPort.Consume, 1)
                matvec(elem_in_a, elem_in_b, elem_out)
                inA_fifo.release(ObjectFifoPort.Consume, 1)
                inB_fifo.release(ObjectFifoPort.Consume, 1)

            outC_fifo.release(ObjectFifoPort.Produce, 1)

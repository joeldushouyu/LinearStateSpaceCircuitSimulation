import numpy as np
import sys

from ml_dtypes import bfloat16
from aie.extras.context import mlir_mod_ctx
from aie.dialects.aie import *
from aie.dialects.aiex import *
from aie.helpers.dialects.ext.scf import _for as range_

from utils import mlir_context, tile_with_location, generate_tile_map, connect_dma
from mvm_i8 import mvm_i8


def my_matmul(arch: str = "npu2"):
    if arch == "npu1":
        dev = AIEDevice.npu1_4col
        total_cols = 4
        total_rows = 4
        mvm_rows = 1
        mvm_cols = 1
    elif arch == "npu2":
        dev = AIEDevice.npu2
        total_cols = 8
        total_rows = 4
        mvm_rows = 2
        mvm_cols = 2
        col_offset = 3
    else:
        raise ValueError(f"Invalid device: {arch}")

    M = 128 * mvm_cols * mvm_rows * 4
    K = 128 * 4
    m = 128
    k = 128

    n_cores = mvm_rows * mvm_cols
    K_div_k = K // k
    m_x_k = m * k
    m_x_K = m * K

    dtype_in = np.dtype[np.int8]
    dtype_out = np.dtype[np.int32]

    if (M // (mvm_rows * mvm_cols * m)) * (mvm_rows * mvm_cols * m) != M:
        raise ValueError(f"M is not divisible by mvm_rows * mvm_cols * m")

    with mlir_mod_ctx() as ctx:
        @device(dev)
        def device_body():
            ctx = mlir_context()
            inA_ty = ctx.data_ty("inA_ty", (mvm_rows * m * k,), dtype_in)
            A_ty = ctx.data_ty("A_ty", (m, k), dtype_in)
            inB_ty = ctx.data_ty("inB_ty", (k,), dtype_in)
            outC_ty = ctx.data_ty("outC_ty", (mvm_rows * m,), dtype_out)
            C_ty = ctx.data_ty("C_ty", (m,), dtype_out)

            ctx.parameter("K_div_k", K_div_k)
            # AIE Core Function declarations
            zero = ctx.func("zero_m_int8", [C_ty])
            matvec = ctx.func(
                "mv_int8",
                [A_ty, inB_ty, C_ty],
            )

            # Tile declarations
            ShimTiles, MemTiles, cores = generate_tile_map(total_rows, total_cols)

            B_ShimTile = ShimTiles[col_offset]
            B_MemTile = MemTiles[col_offset]

            # Input A
            memA_fifos = []
            for col in range(mvm_cols):
                memA_fifos.append(ctx.object_fifo(f"memA_{col + col_offset}", ShimTiles[col + col_offset], MemTiles[col + col_offset], 2, inA_ty))

            inA_fifos = []
            for col in range(mvm_cols):
                fifos = []
                for row in range(mvm_rows):
                    fifos.append(ctx.object_fifo(f"inA_{row + 2}_{col + col_offset}", MemTiles[col + col_offset], cores[row][col + col_offset], 2, A_ty, ([(k // 4, 4), (m, k), (4, 1)])))
                inA_fifos.append(fifos)
                del fifos

            for col in range(mvm_cols):
                offsets = []
                for row in range(mvm_rows):
                    offsets.append(row * m_x_k)
                object_fifo_link(memA_fifos[col], [*inA_fifos[col]], [], [*offsets])

            # Output C
            outC_fifos = []
            for col in range(mvm_cols):
                fifos = []
                for row in range(mvm_rows):
                    fifos.append(ctx.object_fifo(f"outC_{row + 2}_{col + col_offset}", cores[row][col + col_offset], MemTiles[col + col_offset], 2, C_ty))
                outC_fifos.append(fifos)
                del  fifos

            memC_fifos = []
            for col in range(mvm_cols):
                memC_fifos.append(ctx.object_fifo(f"memC_{col + col_offset}", MemTiles[col + col_offset], ShimTiles[col + col_offset], 2, outC_ty))

            for col in range(mvm_cols):
                offsets = []
                for row in range(mvm_rows):
                    offsets.append(row * m)
                object_fifo_link([*outC_fifos[col]], memC_fifos[col], [*offsets], [])

            # Input B
            memB_fifo = ctx.object_fifo(f"memB", B_ShimTile, B_MemTile, 2, inB_ty)
            core_list = []
            for col in range(mvm_cols):
                for row in range(mvm_rows):
                    core_list.append(cores[row][col + col_offset])
            inB_fifo = ctx.object_fifo(f"inB", B_MemTile, core_list, 2, inB_ty)
            object_fifo_link(memB_fifo, inB_fifo)

            # Set up compute tiles
            for col in range(mvm_cols):
                for row in range(mvm_rows):
                    mvm_i8(cores[row][col + col_offset], ctx)
            # To/from AIE-array data movement
            @runtime_sequence(
                np.ndarray[(M*K,), dtype_in],
                np.ndarray[(K,), dtype_in],
                np.ndarray[(M,), dtype_out],
            )
            def sequence(A, B, C):
                r = M // m // n_cores
                assert r * m * n_cores == M
                npu_dma_memcpy_nd(
                    metadata=memB_fifo,
                    bd_id=2,
                    mem=B,
                    offsets=[0, 0, 0, 0],
                    sizes=[M // m // n_cores, 1, 1, K],
                    strides=[0, 0, 0, 1],
                )
                for i in range(mvm_cols):
                    # M offset: each column handles M // mvm_cols row in total
                    A_offset = i * M * K // mvm_cols
                    C_offset = i * M // mvm_cols
                    npu_dma_memcpy_nd(
                        metadata=memA_fifos[i],
                        bd_id=1,
                        mem=A,
                        offsets=[0, 0, 0, A_offset],
                        sizes=[M // mvm_cols // (m * mvm_rows), K_div_k, mvm_rows * m, k],
                        strides=[m_x_K * mvm_rows, k, K, 1],
                    )
                    npu_dma_memcpy_nd(
                        metadata=memC_fifos[i],
                        bd_id=0,
                        mem=C,
                        offsets=[0, 0, 0, C_offset],
                        sizes=[1, 1, M // m // mvm_cols // mvm_rows, mvm_rows * m],
                        strides=[0, 0, mvm_rows * m, 1],
                    )
                dma_wait(*memC_fifos)

    print(ctx.module)


my_matmul(sys.argv[1])

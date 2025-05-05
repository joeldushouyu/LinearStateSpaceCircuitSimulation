module attributes {llvm.target_triple = "aie2p"} {
  llvm.mlir.global external @A_B_C_D_debug_buffer() {addr_space = 0 : i32} : !llvm.array<5376 x f32>
  llvm.mlir.global external @switch_diode_buffer_debug() {addr_space = 0 : i32} : !llvm.array<1792 x f32>
  llvm.mlir.global external @out_buffer_0() {addr_space = 0 : i32} : !llvm.array<7872 x f32>
  llvm.mlir.global external @A_B_C_D_buffer() {addr_space = 0 : i32} : !llvm.array<5376 x f32>
  llvm.mlir.global external @switch_diode_buffer() {addr_space = 0 : i32} : !llvm.array<1792 x f32>
  llvm.mlir.global external @in_buffer_0() {addr_space = 0 : i32} : !llvm.array<984 x f32>
  llvm.func @debug_i32(i32) attributes {sym_visibility = "private"}
  llvm.func @llvm.aie2p.put.ms(i32, i32) attributes {sym_visibility = "private"}
  llvm.func @llvm.aie2p.get.ss() -> !llvm.struct<(i32, i32)> attributes {sym_visibility = "private"}
  llvm.func @llvm.aie2p.mcd.write.vec(vector<16xi32>, i32) attributes {sym_visibility = "private"}
  llvm.func @llvm.aie2p.scd.read.vec(i32) -> vector<16xi32> attributes {sym_visibility = "private"}
  llvm.func @llvm.aie2p.acquire(i32, i32) attributes {sym_visibility = "private"}
  llvm.func @llvm.aie2p.release(i32, i32) attributes {sym_visibility = "private"}
  llvm.mlir.global external @in_SHM_CT_0_2_0() {addr_space = 0 : i32} : !llvm.array<3472 x f32>
  llvm.mlir.global external @in_SHM_CT_0_2_1() {addr_space = 0 : i32} : !llvm.array<19932 x f32>
  llvm.mlir.global external @B_CT_1_2_SHM() {addr_space = 0 : i32} : !llvm.array<7168 x f32>
  llvm.mlir.global external @out_CT_0_2_SHM() {addr_space = 0 : i32} : !llvm.array<129888 x f32>
  llvm.func @passThroughLine_float_0(!llvm.ptr, !llvm.ptr, i32) attributes {sym_visibility = "private"}
  llvm.func @passThroughLine_float_1(!llvm.ptr, !llvm.ptr, i32) attributes {sym_visibility = "private"}
  llvm.func @CT_main(!llvm.ptr, !llvm.ptr, i32, i32, i32, i32, !llvm.ptr) attributes {sym_visibility = "private"}
  llvm.func @core_1_2() {
    %0 = llvm.mlir.addressof @A_B_C_D_debug_buffer : !llvm.ptr
    %1 = llvm.mlir.addressof @A_B_C_D_buffer : !llvm.ptr
    %2 = llvm.mlir.addressof @switch_diode_buffer_debug : !llvm.ptr
    %3 = llvm.mlir.constant(32 : index) : i64
    %4 = llvm.mlir.constant(true) : i1
    %5 = llvm.mlir.addressof @switch_diode_buffer : !llvm.ptr
    %6 = llvm.mlir.constant(51 : i32) : i32
    %7 = llvm.mlir.constant(18 : i32) : i32
    %8 = llvm.mlir.constant(19 : i32) : i32
    %9 = llvm.mlir.constant(50 : i32) : i32
    %10 = llvm.mlir.constant(16 : i32) : i32
    %11 = llvm.mlir.constant(49 : i32) : i32
    %12 = llvm.mlir.constant(17 : i32) : i32
    %13 = llvm.mlir.constant(48 : i32) : i32
    %14 = llvm.mlir.constant(2 : i32) : i32
    %15 = llvm.mlir.constant(5376 : i32) : i32
    %16 = llvm.mlir.constant(-2 : i32) : i32
    %17 = llvm.mlir.constant(1 : i32) : i32
    %18 = llvm.mlir.constant(1792 : i32) : i32
    %19 = llvm.mlir.constant(-1 : i32) : i32
    %20 = llvm.mlir.constant(0 : index) : i64
    %21 = llvm.mlir.constant(9223372036854775807 : index) : i64
    %22 = llvm.mlir.constant(1 : index) : i64
    llvm.br ^bb1(%20 : i64)
  ^bb1(%23: i64):  // 2 preds: ^bb0, ^bb2
    %24 = llvm.icmp "slt" %23, %21 : i64
    llvm.cond_br %24, ^bb2, ^bb3
  ^bb2:  // pred: ^bb1
    llvm.call @llvm.aie2p.acquire(%13, %19) : (i32, i32) -> ()
    llvm.call @llvm.aie2p.acquire(%12, %19) : (i32, i32) -> ()
    %25 = llvm.getelementptr %5[0, 0] : (!llvm.ptr) -> !llvm.ptr, !llvm.array<1792 x f32>
    llvm.intr.assume %4 ["align"(%25, %3 : !llvm.ptr, i64)] : i1
    %26 = llvm.getelementptr %2[0, 0] : (!llvm.ptr) -> !llvm.ptr, !llvm.array<1792 x f32>
    llvm.intr.assume %4 ["align"(%26, %3 : !llvm.ptr, i64)] : i1
    llvm.call @passThroughLine_float_0(%25, %26, %18) : (!llvm.ptr, !llvm.ptr, i32) -> ()
    llvm.call @llvm.aie2p.release(%11, %17) : (i32, i32) -> ()
    llvm.call @llvm.aie2p.release(%10, %17) : (i32, i32) -> ()
    llvm.call @llvm.aie2p.acquire(%9, %19) : (i32, i32) -> ()
    llvm.call @llvm.aie2p.acquire(%8, %16) : (i32, i32) -> ()
    %27 = llvm.getelementptr %1[0, 0] : (!llvm.ptr) -> !llvm.ptr, !llvm.array<5376 x f32>
    llvm.intr.assume %4 ["align"(%27, %3 : !llvm.ptr, i64)] : i1
    %28 = llvm.getelementptr %0[0, 0] : (!llvm.ptr) -> !llvm.ptr, !llvm.array<5376 x f32>
    llvm.intr.assume %4 ["align"(%28, %3 : !llvm.ptr, i64)] : i1
    llvm.call @passThroughLine_float_1(%27, %28, %15) : (!llvm.ptr, !llvm.ptr, i32) -> ()
    llvm.call @llvm.aie2p.release(%7, %14) : (i32, i32) -> ()
    llvm.call @llvm.aie2p.release(%6, %17) : (i32, i32) -> ()
    %29 = llvm.add %23, %22 : i64
    llvm.br ^bb1(%29 : i64)
  ^bb3:  // pred: ^bb1
    llvm.return
  }
  llvm.func @core_0_2() {
    %0 = llvm.mlir.addressof @out_buffer_0 : !llvm.ptr
    %1 = llvm.mlir.addressof @switch_diode_buffer : !llvm.ptr
    %2 = llvm.mlir.constant(32 : index) : i64
    %3 = llvm.mlir.constant(true) : i1
    %4 = llvm.mlir.addressof @in_buffer_0 : !llvm.ptr
    %5 = llvm.mlir.constant(8 : i32) : i32
    %6 = llvm.mlir.constant(9 : i32) : i32
    %7 = llvm.mlir.constant(10 : i32) : i32
    %8 = llvm.mlir.constant(11 : i32) : i32
    %9 = llvm.getelementptr %4[0, 0] : (!llvm.ptr) -> !llvm.ptr, !llvm.array<984 x f32>
    llvm.intr.assume %3 ["align"(%9, %2 : !llvm.ptr, i64)] : i1
    %10 = llvm.getelementptr %1[0, 0] : (!llvm.ptr) -> !llvm.ptr, !llvm.array<1792 x f32>
    llvm.intr.assume %3 ["align"(%10, %2 : !llvm.ptr, i64)] : i1
    %11 = llvm.getelementptr %0[0, 0] : (!llvm.ptr) -> !llvm.ptr, !llvm.array<7872 x f32>
    llvm.intr.assume %3 ["align"(%11, %2 : !llvm.ptr, i64)] : i1
    llvm.call @CT_main(%9, %11, %5, %6, %7, %8, %10) : (!llvm.ptr, !llvm.ptr, i32, i32, i32, i32, !llvm.ptr) -> ()
    llvm.return
  }
}


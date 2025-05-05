; ModuleID = 'LLVMDialectModule'
source_filename = "LLVMDialectModule"
target triple = "aie2p"

@A_B_C_D_debug_buffer = external global [5376 x float]
@switch_diode_buffer_debug = external global [1792 x float]
@out_buffer_0 = external global [7872 x float]
@A_B_C_D_buffer = external global [5376 x float]
@switch_diode_buffer = external global [1792 x float]
@in_buffer_0 = external global [984 x float]
@in_SHM_CT_0_2_0 = external global [3472 x float]
@in_SHM_CT_0_2_1 = external global [19932 x float]
@B_CT_1_2_SHM = external global [7168 x float]
@out_CT_0_2_SHM = external global [129888 x float]

declare void @debug_i32(i32)

declare void @llvm.aie2p.put.ms(i32, i32)

declare { i32, i32 } @llvm.aie2p.get.ss()

declare void @llvm.aie2p.mcd.write.vec(<16 x i32>, i32)

declare <16 x i32> @llvm.aie2p.scd.read.vec(i32)

declare void @llvm.aie2p.acquire(i32, i32)

declare void @llvm.aie2p.release(i32, i32)

declare void @passThroughLine_float_0(ptr, ptr, i32)

declare void @passThroughLine_float_1(ptr, ptr, i32)

declare void @CT_main(ptr, ptr, i32, i32, i32, i32, ptr)

define void @core_1_2() {
  br label %1

1:                                                ; preds = %4, %0
  %2 = phi i64 [ %5, %4 ], [ 0, %0 ]
  %3 = icmp slt i64 %2, 9223372036854775807
  br i1 %3, label %4, label %6

4:                                                ; preds = %1
  call void @llvm.aie2p.acquire(i32 48, i32 -1)
  call void @llvm.aie2p.acquire(i32 17, i32 -1)
  call void @llvm.assume(i1 true) [ "align"(ptr @switch_diode_buffer, i64 32) ]
  call void @llvm.assume(i1 true) [ "align"(ptr @switch_diode_buffer_debug, i64 32) ]
  call void @passThroughLine_float_0(ptr @switch_diode_buffer, ptr @switch_diode_buffer_debug, i32 1792)
  call void @llvm.aie2p.release(i32 49, i32 1)
  call void @llvm.aie2p.release(i32 16, i32 1)
  call void @llvm.aie2p.acquire(i32 50, i32 -1)
  call void @llvm.aie2p.acquire(i32 19, i32 -2)
  call void @llvm.assume(i1 true) [ "align"(ptr @A_B_C_D_buffer, i64 32) ]
  call void @llvm.assume(i1 true) [ "align"(ptr @A_B_C_D_debug_buffer, i64 32) ]
  call void @passThroughLine_float_1(ptr @A_B_C_D_buffer, ptr @A_B_C_D_debug_buffer, i32 5376)
  call void @llvm.aie2p.release(i32 18, i32 2)
  call void @llvm.aie2p.release(i32 51, i32 1)
  %5 = add i64 %2, 1
  br label %1

6:                                                ; preds = %1
  ret void
}

define void @core_0_2() {
  call void @llvm.assume(i1 true) [ "align"(ptr @in_buffer_0, i64 32) ]
  call void @llvm.assume(i1 true) [ "align"(ptr @switch_diode_buffer, i64 32) ]
  call void @llvm.assume(i1 true) [ "align"(ptr @out_buffer_0, i64 32) ]
  call void @CT_main(ptr @in_buffer_0, ptr @out_buffer_0, i32 8, i32 9, i32 10, i32 11, ptr @switch_diode_buffer)
  ret void
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(inaccessiblemem: write)
declare void @llvm.assume(i1 noundef) #0

attributes #0 = { nocallback nofree nosync nounwind willreturn memory(inaccessiblemem: write) }

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}

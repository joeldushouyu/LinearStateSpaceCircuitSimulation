; ModuleID = '/home/shouyud/LinearStateSpaceCircuitSimulation/projects/circuitSimulationDemo/build/bitstream/from_iron/mv.mlir.prj/input.llpeanohack.ll'
source_filename = "LLVMDialectModule"
target datalayout = "e-m:e-p:20:32-i1:8:32-i8:8:32-i16:16:32-i32:32:32-f32:32:32-i64:32-f64:32-a:0:32-n32"
target triple = "aie2p"

@A_B_C_D_debug_buffer = external global [5376 x float]
@switch_diode_buffer_debug = external global [1792 x float]
@out_buffer_0 = external global [7872 x float]
@A_B_C_D_buffer = external global [5376 x float]
@switch_diode_buffer = external global [1792 x float]
@in_buffer_0 = external global [984 x float]

; Function Attrs: nounwind
declare void @llvm.aie2p.acquire(i32, i32) #0

; Function Attrs: nounwind
declare void @llvm.aie2p.release(i32, i32) #0

declare void @passThroughLine_float_0(ptr, ptr, i32) local_unnamed_addr

declare void @passThroughLine_float_1(ptr, ptr, i32) local_unnamed_addr

declare void @CT_main(ptr, ptr, i32, i32, i32, i32, ptr) local_unnamed_addr

define void @core_1_2() local_unnamed_addr {
  br label %1

1:                                                ; preds = %0, %1
  %2 = phi i64 [ 0, %0 ], [ %3, %1 ]
  tail call void @llvm.aie2p.acquire(i32 48, i32 -1)
  tail call void @llvm.aie2p.acquire(i32 17, i32 -1)
  call void @llvm.assume(i1 true) [ "align"(ptr @switch_diode_buffer, i64 32) ]
  call void @llvm.assume(i1 true) [ "align"(ptr @switch_diode_buffer_debug, i64 32) ]
  tail call void @passThroughLine_float_0(ptr nonnull @switch_diode_buffer, ptr nonnull @switch_diode_buffer_debug, i32 1792)
  tail call void @llvm.aie2p.release(i32 49, i32 1)
  tail call void @llvm.aie2p.release(i32 16, i32 1)
  tail call void @llvm.aie2p.acquire(i32 50, i32 -1)
  tail call void @llvm.aie2p.acquire(i32 19, i32 -2)
  call void @llvm.assume(i1 true) [ "align"(ptr @A_B_C_D_buffer, i64 32) ]
  call void @llvm.assume(i1 true) [ "align"(ptr @A_B_C_D_debug_buffer, i64 32) ]
  tail call void @passThroughLine_float_1(ptr nonnull @A_B_C_D_buffer, ptr nonnull @A_B_C_D_debug_buffer, i32 5376)
  tail call void @llvm.aie2p.release(i32 18, i32 2)
  tail call void @llvm.aie2p.release(i32 51, i32 1)
  %3 = add nuw nsw i64 %2, 1
  %.not = icmp eq i64 %3, 9223372036854775807
  br i1 %.not, label %4, label %1

4:                                                ; preds = %1
  ret void
}

define void @core_0_2() local_unnamed_addr {
  call void @llvm.assume(i1 true) [ "align"(ptr @in_buffer_0, i64 32) ]
  call void @llvm.assume(i1 true) [ "align"(ptr @switch_diode_buffer, i64 32) ]
  call void @llvm.assume(i1 true) [ "align"(ptr @out_buffer_0, i64 32) ]
  tail call void @CT_main(ptr nonnull @in_buffer_0, ptr nonnull @out_buffer_0, i32 8, i32 9, i32 10, i32 11, ptr nonnull @switch_diode_buffer)
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind willreturn memory(inaccessiblemem: write)
declare void @llvm.assume(i1 noundef) #1

attributes #0 = { nounwind }
attributes #1 = { mustprogress nocallback nofree nosync nounwind willreturn memory(inaccessiblemem: write) }

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}

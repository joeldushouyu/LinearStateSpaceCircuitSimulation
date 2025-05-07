#ifndef __COMMON_CONFIG__
#define __COMMON_CONFIG__

#define MAX_LOOP_SIZE 9223372036854775807

// TODO: modify after https://github.com/Xilinx/mlir-aie/pull/2248/files#diff-be26c52f2f7cb3bac6ef44e858d772d1006852e737704c1ad63e228792b81412 got merged
#define AIE_PREPARE_FOR_PIPELINE
#define AIE_LOOP_MIN_ITERATION_COUNT(x)                                        \
  _Pragma(__STRINGIFY(clang loop min_iteration_count(x)))
#define AIE_LOOP_MAX_ITERATION_COUNT(x)                                        \
  _Pragma(__STRINGIFY(clang loop max_iteration_count(x)))
#define AIE_LOOP_RANGE(a, ...)                                                 \
  AIE_LOOP_MIN_ITERATION_COUNT(a)                                              \
  __VA_OPT__(AIE_LOOP_MAX_ITERATION_COUNT(__VA_ARGS__))
#define AIE_LOOP_UNROLL(x) _Pragma(__STRINGIFY(clang loop unroll_count(x)))
#define AIE_LOOP_UNROLL_FULL _Pragma("clang loop unroll(full)")
#define AIE_LOOP_NO_UNROLL _Pragma("clang loop unroll(disable)")
#define AIE_LOOP_FLATTEN [[using chess: flatten_loop]]


#endif
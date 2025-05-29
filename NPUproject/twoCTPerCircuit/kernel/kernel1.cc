//===- passThrough.cc -------------------------------------------*- C++ -*-===//
//
// This file is licensed under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
// Copyright (C) 2022, Advanced Micro Devices, Inc.
//
//===----------------------------------------------------------------------===//

// #define __AIENGINE__ 1
#define NOCPP

#include <stdint.h>
#include <stdlib.h>
#include "common_macro.hpp"
#include <aie_api/aie.hpp>
#include <vector>
#include "circuitConfig.hpp"
#include "circuitSimCore.hpp"
#include <cstdlib>
#include <stdlib.h>      // <- This is necessary
#include "LinearCircuitKernelCommon.hpp"




template<uint32_t X_U_cur_vector_size>
void iteration_core(float *in, float*out, aie::vector<float, 16> *x_u_cur, 
    float*C1_DSW_Buffer, float*ABCD_buffer, uint32_t &externalSwitchDiodeState,
    uint32_t* C_D_matrix_select_buffer

){
    

    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE( ITERATION_STEP_PER_PING_PONG_BUFFER, ITERATION_STEP_PER_PING_PONG_BUFFER)
    for(uint32_t k = 0; k < ITERATION_STEP_PER_PING_PONG_BUFFER; k++){

        event0();
        uint32_t C1_Mask_Res[6] = {0};
        // read the input
        bool external_switch_toggled = update_x_u_cur_with_input(x_u_cur, in, externalSwitchDiodeState );
        in += INPUT_SIZE_PER_ITERATION;  // ABOUT 20 cycle


        // mult_with_C1_DSW<6>(
        //     retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,C1_DSW_MATRIX_SIZE  ,C1_DSW_Buffer),
        //     x_u_cur,
        //     C1_Mask_Res,
        //     out // for debug, doe snot write back anymore
        // );
        mult_with_C1_DSW_FULLY_UNROLL<6>(
            retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,C1_DSW_MATRIX_SIZE  ,C1_DSW_Buffer),
            x_u_cur,
            C1_Mask_Res,
            out // for debug, doe snot write back anymore
        );
        bool diode_change = diode_toggle_update2(
            external_switch_toggled, externalSwitchDiodeState, 
            C1_Mask_Res[0], C1_Mask_Res[1],
            C1_Mask_Res[2], C1_Mask_Res[3],
            C1_Mask_Res[4], C1_Mask_Res[5]
        );
      
        

        // write externalSwitchDiodeState_buf,
        // write external_switch_toggled_buf
        // write diode_change_buf
        *C_D_matrix_select_buffer = externalSwitchDiodeState;
        if(external_switch_toggled || !diode_change){
            *(C_D_matrix_select_buffer+1) = 1; // use bot inpulse and nonimpulse output
        }else{
               *(C_D_matrix_select_buffer+1) = 0; // use nonimpulse only
        }

        for(uint32_t i = 0; i < Vector_SIZE_OF_X_U_CUR; i++){

            aie::accum<accfloat, 16> x_acc = aie::accum<accfloat, 16>(  *(x_u_cur+i) );
            put_mcd(  x_acc, 1 ); // write to south

        }





        event0();
        float *ABCD_ptr = retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,A_B_C_D_MATRIX_SIZE  ,ABCD_buffer);

        // if( external_switch_toggled || !diode_change){
        //     mult_with_C_D_aligned_nonimpulse_and_impulse(
        //         ABCD_ptr  +(STATE_SIZE+U_SIZE)*STATE_SIZE_CEIL_TO_16,
        //         x_u_cur,
        //         out + k*OUTPUT_SIZE_PER_ITERATION
        //     );

        // }else{

        //     mult_with_C_D_aligned_nonimpulse_only(
        //         ABCD_ptr  +(STATE_SIZE+U_SIZE)*STATE_SIZE_CEIL_TO_16,
        //         x_u_cur,
        //         out + k*OUTPUT_SIZE_PER_ITERATION
        //     );
        // }


        static_assert( STATE_SIZE_CEIL_TO_16<=   X_U_cur_vector_size*16);
        // aie::vector<float, 16> x_next_temp [STATE_SIZE_CEIL_TO_16/16];

        // mult_with_A_B_To_Vector_Array<STATE_SIZE_CEIL_TO_16>(ABCD_ptr, x_u_cur, x_u_cur);
        mult_with_A_B_To_Vector_Array_FULLY_UNROLL<STATE_SIZE_CEIL_TO_16>(ABCD_ptr, x_u_cur, x_u_cur);

   

        event1();

    }

}


extern "C" {
    void CT_main(float* in, float* out,
        float *in_1, float*out_1,
        const int32_t buffer_in_prod_lock_id, const int32_t buffer_in_con_loc_id,

        const int32_t ABCD_con_lock,
        float* C1_DSW_Buffer, float *ABCD_buffer,
        uint32_t* C_D_matrix_select_buffer
    ) {

        constexpr int32_t C1_DSW_mat_size = C1_DSW_MATRIX_SIZE;
        uint32_t externalSwitchDiodeStates = 0x0;


        
        constexpr uint32_t Y_OUTPUT_ROW = (A_B_C_D_ROW_SIZE-STATE_SIZE_CEIL_TO_16)/ 16; // number of possible vector it used in mult_with_C_D
        static_assert(Vector_SIZE_OF_X_U_CUR *2 +Y_OUTPUT_ROW  < 12 ) ; //TODO: check for error  if happened use more than this number of vectors


        // Define storage for the accumulators
        aie::vector<float, 16> x_u_cur[Vector_SIZE_OF_X_U_CUR];


        for (uint32_t i = 0; i < Vector_SIZE_OF_X_U_CUR; ++i) {
            x_u_cur[i] = aie::zeros<float, 16>(); 
        }


        acquire_greater_equal(ABCD_con_lock , 2);  // all matrix are ready     

        for (uint64_t l = 0; l < PING_PONG_BUFFER_ITERATION; l++) {
            acquire_greater_equal(buffer_in_con_loc_id , 1);



      
            iteration_core<Vector_SIZE_OF_X_U_CUR>(
                in,out, x_u_cur, C1_DSW_Buffer, ABCD_buffer, externalSwitchDiodeStates, C_D_matrix_select_buffer
            );
            
            release(buffer_in_prod_lock_id , 1);


            acquire_greater_equal(buffer_in_con_loc_id , 1);
        
            iteration_core<Vector_SIZE_OF_X_U_CUR>(
                in_1,out_1 , x_u_cur, C1_DSW_Buffer, ABCD_buffer, externalSwitchDiodeStates, C_D_matrix_select_buffer
            );

            release(buffer_in_prod_lock_id , 1);
  

 



        }
    }
} // extern "C"

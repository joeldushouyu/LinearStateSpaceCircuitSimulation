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
    float*C1_DSW_Buffer, float*ABCD_buffer, uint32_t &externalSwitchDiodeState){
    

    AIE_PREPARE_FOR_PIPELINE
    #pragma clang  loop max_iteration_count( ITERATION_STEP_PER_PING_PONG_BUFFER)
    for(uint32_t k = 0; k < ITERATION_STEP_PER_PING_PONG_BUFFER; k++){
        event0();
        uint32_t C1_Mask_Res[6] = {0};
        // read the input
        bool external_switch_toggled = update_x_u_cur_with_input(x_u_cur, in, externalSwitchDiodeState );
        in += INPUT_SIZE_PER_ITERATION;  // ABOUT 20 cycle
        event0();


        mult_with_C1_DSW<6>(
            retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,C1_DSW_MATRIX_SIZE  ,C1_DSW_Buffer),
            x_u_cur,
            C1_Mask_Res,
            out // for debug, doe snot write back anymore
        );
        event0();

        bool diode_change = diode_toggle_update2(
            external_switch_toggled, externalSwitchDiodeState, 
            C1_Mask_Res[0], C1_Mask_Res[1],
            C1_Mask_Res[2], C1_Mask_Res[3],
            C1_Mask_Res[4], C1_Mask_Res[5]
        );
        event0();
        float *ABCD_ptr = retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,A_B_C_D_MATRIX_SIZE  ,ABCD_buffer);
        // // for performance reason, use the version below for now?  TODO: error if run out of registers?
        // alignas(64) float x_next_res[ STATE_SIZE_CEIL_TO_16]; //n NOTE: STATE_SIZE_CEIL_TO_16 could be smaller than X_U_cur_vector_size
        // static_assert( STATE_SIZE_CEIL_TO_16<=   X_U_cur_vector_size*16);
        // mult_with_A_B_To_Array<STATE_SIZE_CEIL_TO_16>(
        //     ABCD_ptr,
        //     x_u_cur, x_next_res

        // );

        static_assert( STATE_SIZE_CEIL_TO_16<=   X_U_cur_vector_size*16);
        aie::vector<float, 16> x_next_temp [STATE_SIZE_CEIL_TO_16/16];

        mult_with_A_B_To_Vector_Array<STATE_SIZE_CEIL_TO_16>(ABCD_ptr, x_u_cur, x_next_temp);

        event0();

        if( external_switch_toggled || !diode_change){

            mult_with_C_D_aligned_nonimpulse_and_impulse(
                ABCD_ptr  +(STATE_SIZE+U_SIZE)*STATE_SIZE_CEIL_TO_16,
                x_u_cur,
                out + k*OUTPUT_SIZE_PER_ITERATION
            );

        }else{

            mult_with_C_D_aligned_nonimpulse_only(
                ABCD_ptr  +(STATE_SIZE+U_SIZE)*STATE_SIZE_CEIL_TO_16,
                x_u_cur,
                out + k*OUTPUT_SIZE_PER_ITERATION
            );
        }

        event0();
  
        // // // for performance reason, use the version below for now?  TODO: error if run out of registers?
        // update_x_u_cur_From_Array<STATE_SIZE_CEIL_TO_16/16>(x_u_cur, x_next_res);

        update_x_u_cur_From_Vector_Array<STATE_SIZE_CEIL_TO_16/16>(x_u_cur, x_next_temp);

        event0();
        event1();
     
    }

}


extern "C" {


    void CT_test(float* in, float* out,
    const int32_t  s2mm_prod_lock, const int32_t s2mm_con_lock,
    const int32_t buffer_out_prod_lock_id, const int32_t buffer_out_con_lock_id,
    float* C1_DSW_Buffer, float *ABCD_buffer,
    int32_t * control_packet_command_out_buffer, int32_t * control_packet_command_res_buffer

    ){
        // First step: pass through of the 1st input buffer?


        for(uint64_t l = 0; l < PING_PONG_BUFFER_ITERATION;  l++){
            if( l == 0){
                acquire_greater_equal(s2mm_con_lock+48, 2); // decrement the ticket by 2 after acquired
                acquire_greater_equal(buffer_out_prod_lock_id+48, 1);

    
                    for(int32_t i = 0; i < BUFFER_SIZE_OF_IN_PING_POING; i++){
                        *(out+i) = *(in+i);

                    }
                release(s2mm_prod_lock+48, 2);
                release(buffer_out_con_lock_id+48, 1);
            }else{
                // don't event attempt to acquire input lock
                acquire_greater_equal(buffer_out_prod_lock_id+48, 1);

    
                    for(int32_t i = 0; i < BUFFER_SIZE_OF_IN_PING_POING; i++){
                        *(out+i) = l+1;

                    }

                release(buffer_out_con_lock_id+48, 1);
            }
            



                acquire_greater_equal(buffer_out_prod_lock_id+48, 1);

    
                    for(int32_t i = 0; i < BUFFER_SIZE_OF_IN_PING_POING; i++){
                        *(out+i+BUFFER_SIZE_OF_OUT_PING_PONG) = l+51;

                    }

                release(buffer_out_con_lock_id+48, 1);

        }

    }



    void CT_main(float* in, float* out,
        const int32_t buffer_in_prod_lock_id, const int32_t buffer_in_con_loc_id,
        const int32_t buffer_out_prod_lock_id, const int32_t buffer_out_con_lock_id,

        float* C1_DSW_Buffer, float *ABCD_buffer
    ) {

        constexpr int32_t C1_DSW_mat_size = C1_DSW_MATRIX_SIZE;
        uint32_t externalSwitchDiodeStates = 0x0;
        
        //TODO: check later
        constexpr uint32_t vector_size_of_x_u_cur = BUFFER_SIZE_OF_CUR_X_U / 16;
        
        constexpr uint32_t Y_OUTPUT_ROW = (A_B_C_D_ROW_SIZE-STATE_SIZE_CEIL_TO_16)/ 16; // number of possible vector it used in mult_with_C_D
        static_assert(vector_size_of_x_u_cur *2 +Y_OUTPUT_ROW  < 12 ) ; //TODO: check for error  if happened use more than this number of vectors


        // Define storage for the accumulators
        aie::vector<float, 16> x_u_cur[vector_size_of_x_u_cur];


        for (uint32_t i = 0; i < vector_size_of_x_u_cur; ++i) {
            x_u_cur[i] = aie::zeros<float, 16>(); 
        }


        for (uint64_t l = 0; l < PING_PONG_BUFFER_ITERATION; l++) {
            acquire_greater_equal(buffer_in_con_loc_id + 48, 1);
            acquire_greater_equal(buffer_out_prod_lock_id + 48, 1);


            iteration_core<vector_size_of_x_u_cur>(
                in,out, x_u_cur, C1_DSW_Buffer, ABCD_buffer, externalSwitchDiodeStates
            );
            
            release(buffer_in_prod_lock_id + 48, 1);
            release(buffer_out_con_lock_id + 48, 1);


            acquire_greater_equal(buffer_in_con_loc_id + 48, 1);
            acquire_greater_equal(buffer_out_prod_lock_id + 48, 1);
            iteration_core<vector_size_of_x_u_cur>(
                in+BUFFER_SIZE_OF_IN_PING_POING,out +BUFFER_SIZE_OF_OUT_PING_PONG , x_u_cur, C1_DSW_Buffer, ABCD_buffer, externalSwitchDiodeStates
            );

            release(buffer_in_prod_lock_id + 48, 1);
            release(buffer_out_con_lock_id + 48, 1);
        }
    }
} // extern "C"

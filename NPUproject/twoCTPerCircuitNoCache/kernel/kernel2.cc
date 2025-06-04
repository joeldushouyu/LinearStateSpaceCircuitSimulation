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



void iterationOutput(
    float*out, 
    uint32_t *C_D_matrix_select_buffer,

    const uint32_t CD_natural_matrix_prod_lock, const uint32_t CD_natural_matrix_con_lock,
    const uint32_t CD_impulse_matrix_prod_lock, const uint32_t CD_impulse_matrix_con_lock,     
    float *CD_natural_impulse_matrix_buffer

){
    aie::vector<float, 16> x_u_cur [Vector_SIZE_OF_X_U_CUR];

    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE( ITERATION_STEP_PER_PING_PONG_BUFFER, ITERATION_STEP_PER_PING_PONG_BUFFER)
    for(uint32_t k = 0; k < ITERATION_STEP_PER_PING_PONG_BUFFER; k++){

        event0();

        // No need to acquire/release buffer

        // because CT_0_3 first update externalSwitchDiodeState_buf, external_switch_toggled_buf, diode_change_buf
        // then it writes the x_u_cur to cascade.. 


        for(uint32_t i = 0; i < Vector_SIZE_OF_X_U_CUR; i++){
            // for now, convert back to vector

            aie::accum<accfloat, 16> vec2 = get_scd_v16accfloat(1);
            x_u_cur[i] =  vec2.template to_vector<float>();
        }
        uint32_t externalSwitchDiodeState = *C_D_matrix_select_buffer;


        uint32_t CD_rel_offset = externalSwitchDiodeState*A_B_C_D_MATRIX_SIZE + C1_DSW_BUFFER_SIZE + AB_MAT_SIZE;
        event0();

        if(*(C_D_matrix_select_buffer+1) == 1){
            mult_with_C_D_aligned_nonimpulse_and_impulse_lock_aware(
                CD_natural_impulse_matrix_buffer,
                x_u_cur,
                out + k*OUTPUT_SIZE_PER_ITERATION,
                CD_natural_matrix_prod_lock, CD_natural_matrix_con_lock,
                CD_impulse_matrix_prod_lock, CD_impulse_matrix_con_lock
            );
             
        }else{
            mult_with_C_D_aligned_nonimpulse_only_lock_aware(
                CD_natural_impulse_matrix_buffer,
                x_u_cur,
                out + k*OUTPUT_SIZE_PER_ITERATION,
                CD_natural_matrix_prod_lock, CD_natural_matrix_con_lock,
                CD_impulse_matrix_prod_lock, CD_impulse_matrix_con_lock                
            );
                         
        }


        event1();

    }

}


extern "C" {
    void CT_0_2_main( float* out, float*out_1,
    uint32_t *C_D_matrix_select_buffer,
    const int32_t buffer_out_prod_lock_id, const int32_t buffer_out_con_lock_id,

    const uint32_t CD_natural_matrix_prod_lock, const uint32_t CD_natural_matrix_con_lock,
    const uint32_t CD_impulse_matrix_prod_lock, const uint32_t CD_impulse_matrix_con_lock,     
    float *CD_natural_impulse_matrix_buffer
    ) {
        

        // TODO: do not acquire/realse out buffer here, since don by CT_0_3

        for (uint64_t l = 0; l < PING_PONG_BUFFER_ITERATION; l++) {
            acquire_greater_equal(buffer_out_prod_lock_id , 1);
            iterationOutput(out,C_D_matrix_select_buffer,
            
                CD_natural_matrix_prod_lock,CD_natural_matrix_con_lock,
                CD_impulse_matrix_prod_lock,CD_impulse_matrix_con_lock,     
                CD_natural_impulse_matrix_buffer            
            ); // ping
            release(buffer_out_con_lock_id , 1);

            acquire_greater_equal(buffer_out_prod_lock_id , 1);
            iterationOutput(out_1, C_D_matrix_select_buffer,
                CD_natural_matrix_prod_lock,CD_natural_matrix_con_lock,
                CD_impulse_matrix_prod_lock,CD_impulse_matrix_con_lock,     
                CD_natural_impulse_matrix_buffer                
            ); //pong
            release(buffer_out_con_lock_id , 1);
        }
    }
} // extern "C"

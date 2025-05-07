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

#define MAX_SW_DIODE_SIZE 32

inline float* retrieveMatrixOFfsetBaseOnState(const uint32_t state, const int32_t matrix_size, float* matrix_ptr) {

    return  matrix_ptr + (state * matrix_size);
}



template<typename T>
__attribute__((noinline)) void accumValue(float* restrict in, float* restrict out,
    const int32_t in_offset, const int32_t out_offset
) {

    in += in_offset;
    out += out_offset;
    // assert divide out without any remainder
    int32_t input_per_iteration_size = INPUT_SIZE_PER_ITERATION;
    int32_t output_per_iteration_size = OUTPUT_SIZE_PER_ITERATION;
    for (int32_t i = 0; i < ITERATION_STEP_PER_PING_PONG_BUFFER * PING_PONG_BUFFER_ITERATION; i++) {
        float acc = 0;
        for (int32_t k = 0; k < input_per_iteration_size; k++) {
            acc += *in;
            in++;
        }
        for (int32_t l = 0; l < output_per_iteration_size; l++) {
            *out = acc;
            out++;
        }

    }

}



void accum_float_value(float* in, float* out,
    const int32_t in_offset, const int32_t out_offset
    // uint32_t *debug_input
) {
    event0();
    accumValue<float>(in, out, in_offset, out_offset);
    event1();
}



template<uint32_t C1_RES_MASK_LEN>
void mult_with_C1_DSW(float *C1_DSW_mat, aie::vector<float, 16> *x_u_cur, uint32_t* c1_res_mask, 
    float*out // for debug
){

    static_assert(C1_RES_MASK_LEN == 6); // 6 uint32 if assume only 32 switch/diode
    
    constexpr uint32_t C1_DSW_ROW_SIZE_DIV_16 = C1_DSW_ROW_SIZE/16;
    static_assert (C1_RES_MASK_LEN >=C1_DSW_ROW_SIZE_DIV_16 );

    uint32_t c1_res_offset = 0;


    AIE_PREPARE_FOR_PIPELINE
    // #pragma clang  loop max_iteration_count( C1_DSW_ROW_SIZE_DIV_16)
    // AIE_LOOP_FLATTEN
    for(uint32_t row = 0; row < C1_DSW_ROW_SIZE_DIV_16; row++){

        aie::accum<accfloat, 16> C1_DSW_temp = aie::zeros<accfloat, 16>();


        // AIE_PREPARE_FOR_PIPELINE
        // #pragma clang  loop unroll(full)
        for(uint32_t col = 0; col < U_SIZE+ STATE_SIZE; col++){

            const uint32_t col_div_16 = col/16;
            const uint32_t col_mod_16 = col%16 ;
            
            aie::vector<float, 16> a = aie::load_v<16>(C1_DSW_mat);
            C1_DSW_mat += 16; // next column
            
            aie::vector<float, 16>b= aie::broadcast<float, 16>(   (x_u_cur+col_div_16)->get(col_mod_16)  );

            C1_DSW_temp = mac_elem_16_accuracy_safe(a,b, C1_DSW_temp,0,0,0  );
            // C1_DSW_temp = aie::mac(C1_DSW_temp, a, b);
        }
        // for now, store  back to out

        // aie::store_v(out ,C1_DSW_temp.template to_vector<float>() );
        // out += 16;

        // aie::vector<float, 16> res_vec = C1_DSW_temp.template to_vector<float>();
        aie::mask<16> lt_res = aie::lt< aie::vector<float, 16> , float>(  C1_DSW_temp ,0);
        aie::mask<16> gt_res = aie::gt< aie::vector<float, 16> , float>(  C1_DSW_temp ,0);

        if(row %2 == 0){
            c1_res_mask[c1_res_offset]=  gt_res.to_uint32() & 0x0000FFFF;
            c1_res_mask[c1_res_offset+3]=  lt_res.to_uint32() & 0x0000FFFF;


        }else{
            c1_res_mask[c1_res_offset]=  gt_res.to_uint32()  <<16;
            c1_res_mask[c1_res_offset+3]=  lt_res.to_uint32() <<16;
            c1_res_offset ++;
        }
    }

}




template<uint32_t X_NEXT_BUFFER_SIZE>
void mult_with_A_B(float *A_B_C_D_mat, aie::vector<float, 16> *x_u_cur, float *x_next_res){
    static_assert(X_NEXT_BUFFER_SIZE == STATE_SIZE_CEIL_TO_16);
    for(uint32_t row = 0; row < STATE_SIZE_CEIL_TO_16/16; row++){
        aie::accum<accfloat, 16> ABtemp = aie::zeros<accfloat, 16>();
        for(uint32_t col = 0; col < U_SIZE+STATE_SIZE; col++){


            const uint32_t col_div_16 = col/16;
            const uint32_t col_mod_16 = col%16 ;
            
            aie::vector<float, 16> a = aie::load_v<16>(A_B_C_D_mat);
            A_B_C_D_mat += 16; // next column
            
            aie::vector<float, 16>b= aie::broadcast<float, 16>(   (x_u_cur+col_div_16)->get(col_mod_16)  );

            ABtemp = mac_elem_16_accuracy_safe(a,b, ABtemp,0,0,0  );
        }
        aie::store_v(x_next_res+16*row, ABtemp.template to_vector<float>());
    }
}

template<uint32_t X_U_cur_vector_size>
void update_x_u_cur( aie::vector<float, 16> *x_u_cur, float *x_u_cur_res ){

    static_assert(BUFFER_SIZE_OF_CUR_X_U/16 == X_U_cur_vector_size);
    //now rewrite the x_u_cur wit new value from iteration
    for(uint32_t i = 0; i< X_U_cur_vector_size; i++){
        (x_u_cur+i)->load(x_u_cur_res + 16* i);
    }

}

template<bool INCLUDE_C_D_IMPULSE>
void mult_with_C_D(float *A_B_C_D_mat, aie::vector<float, 16> *x_u_cur, float*out){

    static constexpr uint32_t y_size_ceil_16 = CUSTOM_CEIL(Y_SIZE, 16);
    uint32_t num_iteration_for_y_output = (A_B_C_D_ROW_SIZE - STATE_SIZE_CEIL_TO_16)/16;
    // Recall A_B_C_D_ROW_SIZE  = STATE_SIZE_CEIL_TO_16 = CUSTOM_CEIL(2*Y_SIZE, 16);
    ///ISSUE: worst performance below?
    // static constexpr uint32_t num_iteration_for_y_output = 
    //     INCLUDE_C_D_IMPULSE 
    //     ? CUSTOM_CEIL(Y_SIZE, 16) 
    //     : ((A_B_C_D_ROW_SIZE - STATE_SIZE_CEIL_TO_16) / 16);
    static constexpr uint32_t y_size_ceil_16_div_16 = y_size_ceil_16/16;
    static_assert(OUTPUT_SIZE_PER_ITERATION  == y_size_ceil_16 );
    
    // First store the 
    aie::vector<float, 16> C_D_temp [y_size_ceil_16_div_16*2];  //TODO: check if enough vector left? llvm issues

    for(uint32_t row = 0; row < num_iteration_for_y_output; row++){

        aie::accum<accfloat, 16> ABCD_temp = aie::zeros<accfloat, 16>();
      
        for(uint32_t col = 0; col < U_SIZE+ STATE_SIZE; col++){

            const uint32_t col_div_16 = col/16;
            const uint32_t col_mod_16 = col%16 ;
            
            aie::vector<float, 16> a = aie::load_v<16>(A_B_C_D_mat);
            A_B_C_D_mat += 16; // next column
            
            aie::vector<float, 16>b= aie::broadcast<float, 16>(   (x_u_cur+col_div_16)->get(col_mod_16)  );

            ABCD_temp = mac_elem_16_accuracy_safe(a,b, ABCD_temp,0,0,0  );
        }

        uint32_t num_y_produced = (row+1)*16;
        if( !INCLUDE_C_D_IMPULSE){
            //TODO: need to constraint the size to prevent redundant writes
            // just write it back to output
            // ALSO, reacall OUTPUT_SIZE_PER_ITERATION is ceil to 16 already
            aie::store_v(  out ,ABCD_temp.template to_vector<float>() );
            out += 16; 
        }else{

            #if num_iteration_for_y_output == 1
                static_assert(2*Y_SIZE <=16);// the Y_nonimpulse and Y_impulse produced in same cycle This means 2*Y_output < 16;; ceil to 16

                aie::vector<float, 16> y_nonimpulse = ABCD_temp.template to_vector<float>();
                aie::vector<float, 16> y_impulse = aie::shuffle_down(y_nonimpulse, Y_SIZE);
                // then do element wise operation and store it back
                aie::vector<float, 16>Y_res =   aie::add(y_nonimpulse, y_impulse);
                Y_res.store(out);

            #else
                // The case need to consider both impulse and nonimpulse result of C_D
                if( num_y_produced <= Y_SIZE ){
                    // accumulate vector only contain Y_nonimpulse
                    C_D_temp[row] = ABCD_temp.to_vector<float>();
      
            
                }else{
                    if( (num_y_produced- 16) < Y_SIZE ){
                        // means contain mix of Y_nonimpulse and Y_impulse in accumulate vector
                        C_D_temp[row] = ABCD_temp.to_vector<float>(); // some extra don't care values
                        C_D_temp[row+1] = aie::shuffle_down(C_D_temp[row], Y_SIZE%16); // extract the Y_impulse data
                        
                    }else{
                        // accumulate vector only contains Y-impulse value
                        aie::vector<float, 16> temp =   ABCD_temp.to_vector<float>();
                        C_D_temp[row] = aie::shuffle_up(  temp,  16-Y_SIZE%16  ); // store Y_impulse data 

                        if(num_y_produced >= 2*Y_SIZE){
                            // last iteration
                            for(uint32_t i = 0; i < y_size_ceil_16_div_16; i++){
                                aie::vector<float, 16> res= aie::add( C_D_temp[i], C_D_temp[i+y_size_ceil_16_div_16]  ) ;
                                res.store(out);
                                out += 16;
                            }
                        }else{
                            C_D_temp[row+1] =    aie::shuffle_down(temp, Y_SIZE%16); // store Remaining Y_impulse data to the vector
                        }   
                    }
                    
                }
            #endif
        
        }

        
 
    }

    // //now rewrite the x_u_cur wit new value from iteration
    // for(uint32_t i = 0; i< X_U_cur_vector_size; i++){
    //     (x_u_cur+i)->load(x_u_cur_temp + 16* i);
    // }

    // // write back to *out for debug purpose
    // for(uint32_t i = 0; i < X_U_cur_vector_size; i++){
    //     //aie::store_v(out, (x_u_cur+i));

    //     (x_u_cur+i)->store(out);
    //     out += 16;
    // }

}

// Return true if externalSwitch toggled
bool update_x_u_cur_with_input(aie::vector<float, 16> *x_u_cur, float*in, uint32_t &externalSwitchDiodeStates){
    #pragma clang loop unroll_count(U_SIZE)
    for(auto i = STATE_SIZE; i < U_SIZE+STATE_SIZE ; i++ ){
        

        x_u_cur[ i /16 ].set(*in, i%16);
        in++;
    } 

    uint32_t *in_as_uint32 = (uint32_t*)in;
    // update the Swtich diode status 
    bool toggled = !compare_and_copy_bits<uint32_t>(externalSwitchDiodeStates, *in_as_uint32, DIODE_SIZE, SWITCH_SIZE  );

    in++;
    return toggled;
}
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

        bool diode_change = diode_toggle_update<MAX_SW_DIODE_SIZE, 6> (externalSwitchDiodeState,
            C1_Mask_Res, external_switch_toggled
        );

        event0();
            
        alignas(64) float x_next_res[ STATE_SIZE_CEIL_TO_16]; //n NOTE: STATE_SIZE_CEIL_TO_16 could be smaller than X_U_cur_vector_size
        static_assert( STATE_SIZE_CEIL_TO_16<=   X_U_cur_vector_size*16);

        float *ABCD_ptr = retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,A_B_C_D_MATRIX_SIZE  ,ABCD_buffer);
        mult_with_A_B<STATE_SIZE_CEIL_TO_16>(
            ABCD_ptr,
            x_u_cur, x_next_res

        );

        if( external_switch_toggled || !diode_change){
            mult_with_C_D<true>(
                ABCD_ptr  +(STATE_SIZE+U_SIZE)*STATE_SIZE_CEIL_TO_16 ,
                x_u_cur,
                out + k*OUTPUT_SIZE_PER_ITERATION
            );
        }else{
            mult_with_C_D<false>(
                ABCD_ptr  +(STATE_SIZE+U_SIZE)*STATE_SIZE_CEIL_TO_16 ,
                x_u_cur,
                out + k*OUTPUT_SIZE_PER_ITERATION
            );
        }

        update_x_u_cur<X_U_cur_vector_size>(x_u_cur, x_next_res);
        // if(external_switch_toggled || ! diode_toggled){
        //     // include C_D_impulse in output
        // }else{

        // }


        // for now, use both impulse and non impulse value

        // for now, write both the diode state and the C1_MASK_RES 

        // uint32_t *pt_uint32 = (uint32_t*) (out+ A_B_C_D_ROW_SIZE);
        // *pt_uint32 ++ = externalSwitchDiodeState;


        // for(uint32_t i = 0; i < 6; i++){
        //     *pt_uint32++ = C1_Mask_Res[i];
        // }

        event1();
     
    }

}


extern "C" {
    void CT_main(float* in, float* out,
        const int32_t buffer_in_prod_lock_id, const int32_t buffer_in_con_loc_id,
        const int32_t buffer_out_prod_lock_id, const int32_t buffer_out_con_lock_id,

        float* C1_DSW_Buffer, float *ABCD_buffer
    ) {

        constexpr int32_t C1_DSW_mat_size = C1_DSW_MATRIX_SIZE;
        uint32_t externalSwitchDiodeStates = 0x0;
        
        //TODO: check later
        constexpr uint32_t vector_size_of_x_u_cur = BUFFER_SIZE_OF_CUR_X_U / 16;
        
        static_assert(vector_size_of_x_u_cur < 12-4 ) ; //TODO: check for error  if happened use more than this number of vectors


        // Define storage for the accumulators
        aie::vector<float, 16> x_u_cur[vector_size_of_x_u_cur];


        for (uint32_t i = 0; i < vector_size_of_x_u_cur; ++i) {
            x_u_cur[i] = aie::zeros<float, 16>(); 
        }
        // // for testing
        // for(auto k  = 0; k < STATE_SIZE; k++){
        //     x_u_cur[0].set(10, k);
        // }


        // // //test purpose
        // float v = 10.01;
        // x_u_cur[0].set(v, 0);
        // // x_u_cur[0] = aie::add(x_u_cur[0], v);

        for (uint64_t l = 0; l < PING_PONG_BUFFER_ITERATION; l++) {
            acquire_greater_equal(buffer_in_con_loc_id + 48, 1);
            acquire_greater_equal(buffer_out_prod_lock_id + 48, 1);


            // float *test_out = out;
            // // //only do number of switch for now
            // for(uint32_t k = 0; k < 16; k++){

            //     #pragma clang loop unroll_count(U_SIZE)
            //     for(auto i = STATE_SIZE; i < U_SIZE+STATE_SIZE ; i++ ){
                    
      
            //         x_u_cur[ i /16 ].set(*in, i%16);
            //         in++;
            //     }
            //     in++; // the input switch state offset for later usage
            //     uint32_t testbuf[6];
            //     mult_with_C1_DSW<6>( retrieveMatrixOFfsetBaseOnState(k,C1_DSW_MATRIX_SIZE  ,C1_DSW_Buffer), 
            //     x_u_cur, testbuf,  test_out ); // for now write 16each time  
            //     test_out += C1_DSW_ROW_SIZE;

            //     mult_with_A_B_C_D_nonimp_imp(
            //         retrieveMatrixOFfsetBaseOnState(k, A_B_C_D_MATRIX_SIZE,ABCD_buffer),
            //         x_u_cur, test_out
            //     );
            //     test_out += A_B_C_D_ROW_SIZE;

            // }
      
            iteration_core<vector_size_of_x_u_cur>(
                in,out, x_u_cur, C1_DSW_Buffer, ABCD_buffer, externalSwitchDiodeStates
            );
            
            release(buffer_in_prod_lock_id + 48, 1);
            release(buffer_out_con_lock_id + 48, 1);

            acquire_greater_equal(buffer_in_con_loc_id + 48, 1);
            acquire_greater_equal(buffer_out_prod_lock_id + 48, 1);
            // // use buffer 0 of ping in and out
            // accum_float_value(in, out, 
            //   BUFFER_SIZE_OF_IN_PING_POING, BUFFER_SIZE_OF_OUT_PING_PONG
            // );
        
            iteration_core<vector_size_of_x_u_cur>(
                in+BUFFER_SIZE_OF_IN_PING_POING,out +BUFFER_SIZE_OF_OUT_PING_PONG , x_u_cur, C1_DSW_Buffer, ABCD_buffer, externalSwitchDiodeStates
            );

            release(buffer_in_prod_lock_id + 48, 1);
            release(buffer_out_con_lock_id + 48, 1);

 



        }
    }
} // extern "C"

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






constexpr uint32_t tm_start_addr = 0x80000;
static volatile uint32_t chess_storage(TM : tm_start_addr) addr_space_start;

void read_processor_bus(uint32_t *data, uint32_t addr, uint32_t size,
                        uint32_t stride=16) {
  for (uint32_t i = 0; i < size; i++) {
    
    #if defined(__chess__)
        uint32_t offset = addr + (i * stride);
        data[i] = *(&addr_space_start + (offset / 4));
    #elif defined(__AIECC__)
        uint32_t offset =addr  +  (i*(stride/4));    
        data[i] = read_tm(offset );
    #else
        static_assert(false, "Unexpected case here");   
    #endif
  }
}

void write_process_bus(uint32_t *data, uint32_t addr, uint32_t size, uint32_t stride=16){
  
    for (uint32_t i = 0; i < size; i++) {

        #if defined(__chess__)
            uint32_t offset = addr + (i * stride);
            *(&addr_space_start + (offset / 4)) =  data[i];
        #elif defined(__AIECC__)
            uint32_t offset =addr  +  (i*(stride/4));
            write_tm( data[i],  offset );
        #else
            static_assert(false, "Unexpected case here");   
        #endif    
    }
}

inline volatile void compiler_sync_barrier(){
    #if defined(__chess__)
        chess_separator_scheduler(2);
    #elif defined(__AIECC__)
          __builtin_aie2p_sched_barrier();    
        volatile int32_t k = 0;    
        k++;
        __builtin_aie2p_sched_barrier();     

    #else
        static_assert(false, "Unexpected case here");   
    #endif
}


inline void configure_BD_x_MM2S_y_dma_bd_len(const uint32_t BD_x_0_addr, const uint32_t MM2S_port_num,  uint32_t len, uint32_t bd_repeat_len=1 ){
    uint32_t len_mask = 0;
    uint32_t write_buffer[1];


    uint32_t MM2S_CTRL = (MM2S_port_num==0)? 0x000001DE10 : 0x000001DE18;
    uint32_t MM2S_START_QUEUE  = (MM2S_port_num == 0) ? 0x000001DE14 : 0x000001DE1C;

    read_processor_bus( write_buffer, BD_x_0_addr, 1, 16 );// first read


    len_mask = 0x3FFF;
    *write_buffer =  ( (*write_buffer) & ~len_mask) | ( (len) & len_mask);         
    write_process_bus( write_buffer, BD_x_0_addr, 1, 16 );
    compiler_sync_barrier();  

    *(write_buffer) =(1<<1);// disable MM2S-1
    write_process_bus( (uint32_t*)(write_buffer),MM2S_CTRL, 1, 16 );  
    compiler_sync_barrier();  

    *(write_buffer) =(0<1);  // renable MM2S-1
    write_process_bus( (uint32_t*)(write_buffer),MM2S_CTRL, 1, 16  ); 
    compiler_sync_barrier();  
       
    *(write_buffer) =(bd_repeat_len<<16) | (4);
    write_process_bus( (uint32_t*)(write_buffer),MM2S_START_QUEUE, 1, 16  ); 
    compiler_sync_barrier();           




}


void control_Shimtile_transfer(
    uint32_t virtual_address_base,
    uint32_t length, uint32_t address_offset,
    uint32_t control_packet_out_prod_lock, uint32_t control_packet_out_con_lock,
    uint32_t * control_packet_out_buf
){

    configure_BD_x_MM2S_y_dma_bd_len(0x000001D080,0, 3,0);//Configure MM2s-0 to send data
    // Write BD_00 and BD_01
    acquire_greater_equal(control_packet_out_prod_lock,1);
    *control_packet_out_buf = control_packet_gen( 8, 0,1, 0x1d000);
    *(control_packet_out_buf+1) = length;
    *(control_packet_out_buf+2)  = (virtual_address_base + address_offset);         
    release(control_packet_out_con_lock, 1);


    //TODO: right now BD is fixed to be 4
    configure_BD_x_MM2S_y_dma_bd_len(0x000001D080,0, 2,0);//Configure MM2s-0 to send data
    // Send write message
    acquire_greater_equal(control_packet_out_prod_lock,1);
    *control_packet_out_buf = control_packet_gen( 8, 0,0, 0x1D214);
    *(control_packet_out_buf+1) = 0x0;
    release(control_packet_out_con_lock, 1);

}



void request_C1DSW_matrix(uint32_t externalSwitchDiodeState,const uint32_t control_packet_out_prod_lock,
    const uint32_t control_packet_out_con_lock,
    uint32_t* control_packet_out_buf,
    uint32_t BD_0_1_val

){

    // first request C1_DSW matrix
    uint32_t C1_offset = externalSwitchDiodeState*C1_DSW_MATRIX_SIZE;
    control_Shimtile_transfer(BD_0_1_val, C1_DSW_MATRIX_SIZE, C1_offset*4,
    control_packet_out_prod_lock, control_packet_out_con_lock, control_packet_out_buf
    );


}




void request_AB_CD_nat_impulse(uint32_t externalSwitchDiodeState,const uint32_t control_packet_out_prod_lock,
    const uint32_t control_packet_out_con_lock,
    uint32_t* control_packet_out_buf,
    uint32_t BD_0_1_val

){
    uint32_t AB_rel_offset = externalSwitchDiodeState*A_B_C_D_MATRIX_SIZE + C1_DSW_BUFFER_SIZE;
    uint32_t CD_rel_offset = externalSwitchDiodeState*A_B_C_D_MATRIX_SIZE + C1_DSW_BUFFER_SIZE + AB_MAT_SIZE;

    //Send 16 value of AB matrix to me
    control_Shimtile_transfer(BD_0_1_val, 16, AB_rel_offset*4,
    control_packet_out_prod_lock, control_packet_out_con_lock, control_packet_out_buf
    );

    // send 16 value of CD_natural matrix to me
    control_Shimtile_transfer(BD_0_1_val, 16, CD_rel_offset*4,
    control_packet_out_prod_lock, control_packet_out_con_lock, control_packet_out_buf
    );
    // send rest of AB matrix to me
    control_Shimtile_transfer(BD_0_1_val, (AB_MAT_SIZE-16), (AB_rel_offset+16)*4,
    control_packet_out_prod_lock, control_packet_out_con_lock, control_packet_out_buf
    );        
    // send rest of CD_natural, and CD_impulse matrix to me
    control_Shimtile_transfer(BD_0_1_val, 2*CD_NAT_OR_IMP_MAT_SIZE-16, (CD_rel_offset+16)*4,
    control_packet_out_prod_lock, control_packet_out_con_lock, control_packet_out_buf
    );

}





template<uint32_t X_U_cur_vector_size>
void iteration_core(float *in, float*out, aie::vector<float, 16> *x_u_cur, 
    float*C1_DSW_Buffer, float*ABCD_buffer, uint32_t &externalSwitchDiodeState,
    uint32_t* C_D_matrix_select_buffer,

    const uint32_t control_packet_out_prod_lock, const uint32_t control_packet_out_con_lock,
    uint32_t* control_packet_out_buf,

    const uint32_t BD_0_1_val,
    const uint32_t C1_DSW_matrix_prod_lock, const uint32_t C1_DSW_matrix_con_lock,
    const uint32_t AB_matrix_prod_lock, const uint32_t AB_matrix_con_lock,
    float* C1_DSW_matrix_buffer,
    float* AB_matrix_buffer
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
        uint32_t C1_offset = externalSwitchDiodeState*C1_DSW_MATRIX_SIZE;
        request_C1DSW_matrix(externalSwitchDiodeState, control_packet_out_prod_lock, control_packet_out_con_lock, control_packet_out_buf,
            BD_0_1_val
        );
        // passThroughFunc( C1_DSW_matrix_buffer+16,  C1_DSW_Buffer+  C1_offset+16, (C1_DSW_MATRIX_SIZE-16));
        // release(C1_DSW_matrix_prod_lock, 1);
        mult_with_C1_DSW_lock_aware(
            C1_DSW_matrix_buffer, //retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,C1_DSW_MATRIX_SIZE  ,C1_DSW_Buffer),
            x_u_cur,
            C1_Mask_Res,
            out, // for debug, doe snot write back anymore
            C1_DSW_matrix_prod_lock, C1_DSW_matrix_con_lock
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


        request_AB_CD_nat_impulse(externalSwitchDiodeState, 
            control_packet_out_prod_lock, control_packet_out_con_lock,
            control_packet_out_buf, BD_0_1_val
        );
        // //Send 16 value of AB matrix to me
        uint32_t AB_rel_offset = externalSwitchDiodeState*A_B_C_D_MATRIX_SIZE + C1_DSW_BUFFER_SIZE;

        event0();
        float *AB_ptr = AB_matrix_buffer;
        float *ABCD_ptr = retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,A_B_C_D_MATRIX_SIZE  ,ABCD_buffer);
        // float *ABCD_ptr = retrieveMatrixOFfsetBaseOnState(externalSwitchDiodeState,AB_MAT_SIZE  ,ABCD_buffer);
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
        
        mult_with_A_B_To_Vector_Array_with_lock_aware<STATE_SIZE_CEIL_TO_16>(AB_ptr, x_u_cur, x_u_cur,
            AB_matrix_prod_lock, AB_matrix_con_lock
        );
        // mult_with_A_B_To_Vector_Array_with_lock_aware<STATE_SIZE_CEIL_TO_16>(ABCD_ptr, x_u_cur, x_u_cur);
        // mult_with_A_B_To_Vector_Array_FULLY_UNROLL<STATE_SIZE_CEIL_TO_16>(ABCD_ptr, x_u_cur, x_u_cur);

   

        event1();

    }

}


extern "C" {
    void CT_main(float* in, float* out,
        float *in_1, float*out_1,
        const int32_t buffer_in_prod_lock_id, const int32_t buffer_in_con_loc_id,

        const int32_t ABCD_con_lock,
        float* C1_DSW_Buffer, float *ABCD_buffer,
        uint32_t* C_D_matrix_select_buffer, // Buffer for communication with CT_0_2
        
        const uint32_t control_packet_out_prod_lock, const uint32_t control_packet_out_con_lock,
        const uint32_t control_packet_in_prod_lock, const uint32_t control_packet_in_con_lock,
        uint32_t* control_packet_out_buf,
        uint32_t* control_packet_in_buf,

        const uint32_t C1_DSW_matrix_prod_lock, const uint32_t C1_DSW_matrix_con_lock,
        const uint32_t AB_matrix_prod_lock, const uint32_t AB_matrix_con_lock,
        const uint32_t CD_natural_matrix_prod_lock, const uint32_t CD_natural_matrix_con_lock,
        const uint32_t CD_impulse_matrix_prod_lock, const uint32_t CD_impulse_matrix_con_lock,        
        float* C1_DSW_matrix_buffer,
        float* AB_matrix_buffer,
        float *CD_natural_impulse_matrix_buffer
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

        

        configure_BD_x_MM2S_y_dma_bd_len(0x000001D080,0, 1,0);
        acquire_greater_equal(control_packet_out_prod_lock,1);
        *control_packet_out_buf = control_packet_gen( 7, 1,0, 0x000001D004); // READBD_0_1
        release(control_packet_out_con_lock, 1);

        acquire_greater_equal(control_packet_in_con_lock, 1);
        uint32_t BD_0_1_val = *control_packet_in_buf;
        release(control_packet_in_prod_lock, 1);


        // control_Shimtile_transfer(
        //     BD_0_1_val, C1_DSW_BUFFER_SIZE + A_B_C_D_BUFFER_SIZE,
        //     0, 
        //     control_packet_out_prod_lock, control_packet_out_con_lock,
        //     control_packet_out_buf

        // );
        // acquire_greater_equal(ABCD_con_lock , 1);  // all matrix are ready     

        // // Now, Test to send command for shimtile to bring me data
        // for(uint32_t state_ind = 0; state_ind < TOTAL_SWITCH_DIODE_STATE; state_ind++){
        //     // // first request C1_DSW matrix

        //     uint32_t C1_offset = state_ind*C1_DSW_MATRIX_SIZE;
        //     request_C1DSW_matrix(state_ind, control_packet_out_prod_lock, control_packet_out_con_lock, control_packet_out_buf,
        //         BD_0_1_val
        //     );

        //     acquire_greater_equal(C1_DSW_matrix_con_lock, 1);
        //     passThroughFunc( C1_DSW_matrix_buffer,  C1_DSW_Buffer+  C1_offset, 16);
        //     release(C1_DSW_matrix_prod_lock, 1);

        //     acquire_greater_equal(C1_DSW_matrix_con_lock, 1);
        //     passThroughFunc( C1_DSW_matrix_buffer+16,  C1_DSW_Buffer+  C1_offset+16, (C1_DSW_MATRIX_SIZE-16));
        //     release(C1_DSW_matrix_prod_lock, 1);


        //     request_AB_CD_nat_impulse(state_ind, 
        //         control_packet_out_prod_lock, control_packet_out_con_lock,
        //         control_packet_out_buf, BD_0_1_val
        //     );
        //     // //Send 16 value of AB matrix to me
        //     uint32_t AB_rel_offset = state_ind*A_B_C_D_MATRIX_SIZE + C1_DSW_BUFFER_SIZE;
        //     acquire_greater_equal(AB_matrix_con_lock, 1);
        //     passThroughFunc(AB_matrix_buffer, ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE, 16  );
        //     release(AB_matrix_prod_lock, 1);


        //     uint32_t CD_rel_offset = state_ind*A_B_C_D_MATRIX_SIZE + C1_DSW_BUFFER_SIZE + AB_MAT_SIZE;
        // //    // send 16 value of CD_natural matrix to me
        //     acquire_greater_equal(CD_natural_matrix_con_lock, 1);
        //     passThroughFunc(CD_natural_impulse_matrix_buffer,ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE+AB_MAT_SIZE, 16  );
        //     release(CD_natural_matrix_prod_lock, 1);




        //     // // send rest of AB matrix to me
        //     acquire_greater_equal(AB_matrix_con_lock, 1);
        //     passThroughFunc(AB_matrix_buffer+16, ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE+16,  (AB_MAT_SIZE-16) );
        //     release(AB_matrix_prod_lock, 1);



        //     // // send rest of CD_natural
        //     acquire_greater_equal(CD_natural_matrix_con_lock, 1);
        //     passThroughFunc(CD_natural_impulse_matrix_buffer+16,ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE+AB_MAT_SIZE+16, CD_NAT_OR_IMP_MAT_SIZE-16  );
        //     release(CD_natural_matrix_prod_lock, 1);            

        //     // receive CD_impulse
        //     acquire_greater_equal(CD_impulse_matrix_con_lock, 1);
        //     passThroughFunc( CD_natural_impulse_matrix_buffer+CD_NAT_OR_IMP_MAT_SIZE,ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE+AB_MAT_SIZE+CD_NAT_OR_IMP_MAT_SIZE, CD_NAT_OR_IMP_MAT_SIZE   );
        //     release(CD_impulse_matrix_prod_lock, 1);
        // }   

        static_assert(PING_PONG_BUFFER_ITERATION%2 == 0);
        for (uint64_t l = 0; l < PING_PONG_BUFFER_ITERATION; l++) {
        /*
        // Now, Test to send command for shimtile to bring me data
        for(uint32_t state_ind = 0; state_ind < TOTAL_SWITCH_DIODE_STATE; state_ind++){
            // // first request C1_DSW matrix

            uint32_t C1_offset = state_ind*C1_DSW_MATRIX_SIZE;
            request_C1DSW_matrix(state_ind, control_packet_out_prod_lock, control_packet_out_con_lock, control_packet_out_buf,
                BD_0_1_val
            );

            acquire_greater_equal(C1_DSW_matrix_con_lock, 1);
            passThroughFunc( C1_DSW_matrix_buffer,  C1_DSW_Buffer+  C1_offset, 16);
            release(C1_DSW_matrix_prod_lock, 1);

            acquire_greater_equal(C1_DSW_matrix_con_lock, 1);
            passThroughFunc( C1_DSW_matrix_buffer+16,  C1_DSW_Buffer+  C1_offset+16, (C1_DSW_MATRIX_SIZE-16));
            release(C1_DSW_matrix_prod_lock, 1);


            request_AB_CD_nat_impulse(state_ind, 
                control_packet_out_prod_lock, control_packet_out_con_lock,
                control_packet_out_buf, BD_0_1_val
            );
            // //Send 16 value of AB matrix to me
            uint32_t AB_rel_offset = state_ind*A_B_C_D_MATRIX_SIZE + C1_DSW_BUFFER_SIZE;
            acquire_greater_equal(AB_matrix_con_lock, 1);
            passThroughFunc(AB_matrix_buffer, ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE, 16  );
            release(AB_matrix_prod_lock, 1);


            uint32_t CD_rel_offset = state_ind*A_B_C_D_MATRIX_SIZE + C1_DSW_BUFFER_SIZE + AB_MAT_SIZE;
        //    // send 16 value of CD_natural matrix to me
            acquire_greater_equal(CD_natural_matrix_con_lock, 1);
            passThroughFunc(CD_natural_impulse_matrix_buffer,ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE+AB_MAT_SIZE, 16  );
            release(CD_natural_matrix_prod_lock, 1);




            // // send rest of AB matrix to me
            acquire_greater_equal(AB_matrix_con_lock, 1);
            passThroughFunc(AB_matrix_buffer+16, ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE+16,  (AB_MAT_SIZE-16) );
            release(AB_matrix_prod_lock, 1);



            // // send rest of CD_natural
            acquire_greater_equal(CD_natural_matrix_con_lock, 1);
            passThroughFunc(CD_natural_impulse_matrix_buffer+16,ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE+AB_MAT_SIZE+16, CD_NAT_OR_IMP_MAT_SIZE-16  );
            release(CD_natural_matrix_prod_lock, 1);            

            // receive CD_impulse
            acquire_greater_equal(CD_impulse_matrix_con_lock, 1);
            passThroughFunc( CD_natural_impulse_matrix_buffer+CD_NAT_OR_IMP_MAT_SIZE,ABCD_buffer+ state_ind*A_B_C_D_MATRIX_SIZE+AB_MAT_SIZE+CD_NAT_OR_IMP_MAT_SIZE, CD_NAT_OR_IMP_MAT_SIZE   );
            release(CD_impulse_matrix_prod_lock, 1);
        }   */

            acquire_greater_equal(buffer_in_con_loc_id , 1);



      
            iteration_core<Vector_SIZE_OF_X_U_CUR>(
                in,out, x_u_cur, C1_DSW_Buffer, ABCD_buffer, externalSwitchDiodeStates, C_D_matrix_select_buffer,

                control_packet_out_prod_lock, control_packet_out_con_lock,
                control_packet_out_buf,

                BD_0_1_val,
                C1_DSW_matrix_prod_lock, C1_DSW_matrix_con_lock,
                AB_matrix_prod_lock, AB_matrix_con_lock,
                C1_DSW_matrix_buffer,
                AB_matrix_buffer

            );
            
            release(buffer_in_prod_lock_id , 1);


            acquire_greater_equal(buffer_in_con_loc_id , 1);
        
            iteration_core<Vector_SIZE_OF_X_U_CUR>(
                in_1,out_1 , x_u_cur, C1_DSW_Buffer, ABCD_buffer, externalSwitchDiodeStates, C_D_matrix_select_buffer,

                control_packet_out_prod_lock, control_packet_out_con_lock,
                control_packet_out_buf,
                
                BD_0_1_val,
                C1_DSW_matrix_prod_lock, C1_DSW_matrix_con_lock,
                AB_matrix_prod_lock, AB_matrix_con_lock,
                C1_DSW_matrix_buffer,
                AB_matrix_buffer                
            );

            release(buffer_in_prod_lock_id , 1);
  

 



        }
    }
} // extern "C"

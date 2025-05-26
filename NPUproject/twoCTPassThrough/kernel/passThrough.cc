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

#include <aie_api/aie.hpp>

// template <typename T, int N>
// __attribute__((noinline)) void passThrough_aie(T *restrict in, T *restrict out,
//                                                const int32_t height,
//                                                const int32_t width) {
//   event0();

//   v64uint8 *restrict outPtr = (v64uint8 *)out;
//   v64uint8 *restrict inPtr = (v64uint8 *)in;

//   for (int j = 0; j < (height * width); j += N) // Nx samples per loop
//     chess_prepare_for_pipelining chess_loop_range(6, ) { *                                                                                                                                          outPtr++ = *inPtr++; }

//   event1();
// }

template<typename T>
__attribute__((noinline)) void passThrough_simple(uint32_t *restrict in, uint32_t*restrict out, const int32_t size){
  
  // event0()  ;

  for( int32_t j = 0; j < size; j++){
    *out = *in;
    out++;
    in++;
  }
  // event1();
}
bool parity(uint32_t n) {
    uint32_t p = 0;
    while (n) {
        p += n & 1;
        n >>= 1;
    }
    return (p % 2) == 0;
}
uint32_t control_packet_gen(int32_t stream_id, int32_t operation, int32_t beats, int32_t address){
  //operation: 0 read, 1 write
  uint32_t control_packet =
        stream_id << 24 | operation << 22 | beats << 20 | address;
  control_packet |= (0x1 & parity(control_packet)) << 31;

  return control_packet;
}

extern "C" {

void passThroughTest(uint32_t *in, uint32_t *out, 
                  int32_t buffer_size, int32_t total_passThrough_size,
                  int32_t in_buffer_prod_lock, int32_t in_buffer_con_lock,
                  int32_t out_buffer_prod_lock, int32_t out_buffer_con_lock,

                  int32_t* control_read_buffer, int32_t* control_read_buffer_res,  // buffer on CT_0_3 that will send control packet to itself
                  int32_t* control_write_buffer,
                  int32_t control_packet_read_prod_lock, int32_t control_packet_read_con_lock,
                  int32_t control_packet_read_res_prod_lock, int32_t control_packet_read_res_con_lock,
                  int32_t control_packet_write_prod_lock, int32_t control_packet_write_con_lock,

                  int32_t* CT2_control_out_buffer, int32_t* CT2_control_res_buffer,
                  int32_t CT2_control_out_prod_lock, int32_t CT2_control_out_con_lock,
                  int32_t CT2_control_in_prod_lock, int32_t CT2_control_in_con_lock
                  
){
  // assume divisible and multiple of two
  for(uint32_t i = 0; i < (total_passThrough_size /buffer_size ); i += 2){

    acquire_greater_equal(in_buffer_con_lock, 1);
    if(i == 0){
        // // how about if I do it in CT_0_2?
        // #define COMPUTE_0_2_BASE 0x208000
        // #define DMA_BD_2_1_OFFSET 0x1D048
        // volatile int32_t* BD_2_1 = (volatile int32_t*)(0x200000 + 0x001D044);
        // int32_t val = *BD_2_1;

        // int32_t* MM2S_0_CTR = (int32_t*)  0x1DE10;
        // int32_t* MM2S_0_START = (int32_t*)(0x1DE14|0x200000);
        // int32_t val = *BD_2_1;
        // First, let us fix the issue in CT_0_2 through control packet
    
        acquire_greater_equal(control_packet_write_prod_lock, 1);
        *control_write_buffer =   control_packet_gen(12, 0, 0,   0x001D044 );
        *(control_write_buffer+1) = (1<<30) | (9<<19); //0x40480000; //(1<<31) | (9<<19);
        release(control_packet_write_con_lock, 1);
        // NOTE: Write did go through, but somehow did not apply to qeue?

        //Try CT fix it myself instead?
        // acquire_greater_equal(CT2_control_out_prod_lock, 1);
        // *CT2_control_out_buffer = control_packet_gen(13, 0, 0,   0x001D044 );
        // *(CT2_control_out_buffer+1)  = (1<<30) | (9<<19);
        // release(CT2_control_out_con_lock, 1);

        // auto k = get_coreid();
        
        acquire_greater_equal(control_packet_write_prod_lock, 1);
        *control_write_buffer =   control_packet_gen(12, 0, 0,   0x1DE10 );
        *(control_write_buffer+1) =  (1<<1);
        release(control_packet_write_con_lock, 1); // toggle to turn off, 

        acquire_greater_equal(control_packet_write_prod_lock, 1);
        *control_write_buffer =   control_packet_gen(12, 0, 0,   0x1DE10 );
        *(control_write_buffer+1) =  (0<<1);
        release(control_packet_write_con_lock, 1); // toggle to turn on 
  
        acquire_greater_equal(control_packet_write_prod_lock, 1);
        *control_write_buffer =   control_packet_gen(12, 0, 0,   0x1DE14 );
        *(control_write_buffer+1) =  (1<<16) | (2);
        release(control_packet_write_con_lock, 1); 


        // wrtei core contro?

  
        acquire_greater_equal(control_packet_write_prod_lock, 1);
        *control_write_buffer =   control_packet_gen(12, 0, 0,   0x0000032000 );
        *(control_write_buffer+1)   = 1;
        release(control_packet_write_con_lock, 1); 

  
        acquire_greater_equal(control_packet_write_prod_lock, 1);
        *control_write_buffer =   control_packet_gen(12, 0, 0,   0x0000032038 );
        *(control_write_buffer+1)   = 1;
        release(control_packet_write_con_lock, 1); 

        // *BD_2_1 = (1<<30) | (9<<19); //0x40480000; //(1<<31) | (9<<19);
        // *MM2S_0_CTR  = 1<<1;
        // *MM2S_0_CTR  = 0<<1;
        // *MM2S_0_START = (1<<16) | (2);
        // ERRORO read value: 2404400
        // CORRECT read value: 2400400
        

        event0();
        acquire_greater_equal(control_packet_read_prod_lock, 1);
        *control_read_buffer =   control_packet_gen(11, 1, 0,   0x001D044  );
        release(control_packet_read_con_lock, 1);
        event1();
        // see the value of it



        event0();
        acquire_greater_equal(control_packet_read_res_con_lock, 1);
        *(in) = *control_read_buffer_res;
        release(control_packet_read_res_prod_lock, 1);
        event1();

        // try to read
        
        // acquire_greater_equal(CT2_control_out_prod_lock, 1);
        // *CT2_control_out_buffer = control_packet_gen(14, 1,0,0x001D044);
        // release(CT2_control_out_con_lock, 1);

        // acquire_greater_equal(CT2_control_in_con_lock, 1);
        //  *(in) = *CT2_control_res_buffer;
        // release(CT2_control_in_prod_lock, 1);
    }else{
       volatile int32_t* BD_2_1 = (volatile int32_t*)(  (1<<25) | (1<<20) |0x1D044);
       int32_t val = *BD_2_1;
      *(in+1) = val;
    //     // event0();
    //     // acquire_greater_equal(control_packet_read_prod_lock, 1);
    //     // *control_read_buffer =   control_packet_gen(11, 1, 0,   0x001D044  );
    //     // release(control_packet_read_con_lock, 1);
    //     // event1();
    //     // // see the value of it



    //     // event0();
    //     // acquire_greater_equal(control_packet_read_res_con_lock, 1);
    //     // *(in) = *control_read_buffer_res;
    //     // release(control_packet_read_res_prod_lock, 1);
    //     // event1();
    //  auto k =  get_coreid();
    // //   volatile int32_t* cord_id_pt = (volatile int32_t*)(    (10<<3) | 0b111);
    // //   int32_t val = *cord_id_pt;
    //   *(in+2) = k;        
    }

    // *in = 0x10001;
    acquire_greater_equal(out_buffer_prod_lock, 1);
    passThrough_simple<uint32_t>(in, out, buffer_size);
    release(in_buffer_prod_lock, 1);
    release(out_buffer_con_lock, 1);

    




    acquire_greater_equal(in_buffer_con_lock, 1);
    acquire_greater_equal(out_buffer_prod_lock, 1);
    passThrough_simple<uint32_t>(in+buffer_size, out+buffer_size, buffer_size);
    release(in_buffer_prod_lock, 1);
    release(out_buffer_con_lock, 1);

  }


}


// // #endif
// void passThroughLine_float_0(float *in, float *out, int32_t lineWidth) {
//   passThrough_simple<float>( in, out, lineWidth);
// }
// void passThroughLine_float_1(float *in, float *out, int32_t lineWidth) {
//   passThrough_simple<float>( in, out, lineWidth);
// }

// void passThroughLine_float_2(float *in, float *out, int32_t lineWidth) {
//   passThrough_simple<float>( in, out, lineWidth);
// }

// void passThroughLine_float_3(float *in, float *out, int32_t lineWidth) {
//   passThrough_simple<float>( in, out, lineWidth);
// }



} // extern "C"

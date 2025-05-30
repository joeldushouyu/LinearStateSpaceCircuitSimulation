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

constexpr uint32_t tm_start_addr = 0x80000;
static volatile uint32_t chess_storage(TM : tm_start_addr) addr_space_start;

void read_processor_bus(uint32_t *data, uint32_t addr, uint32_t size,
                        uint32_t stride) {
  for (uint32_t i = 0; i < size; i++) {
    uint32_t offset = addr + (i * stride);
    #if defined(__chess__)
        data[i] = *(&addr_space_start + (offset / 4));
    #elif defined(__AIECC__)
        data[i] = read_tm(offset/4  );
    #else
        static_assert(false, "Unexpected case here");   
    #endif
  }
}

void write_process_bus(uint32_t *data, uint32_t addr, uint32_t size, uint32_t stride){
  for (uint32_t i = 0; i < size; i++) {
    uint32_t offset = addr + (i * stride);
    #if defined(__chess__)
        *(&addr_space_start + (offset / 4)) =  data[i];
    #elif defined(__AIECC__)
        write_tm( data[i],offset/4 );
    #else
        static_assert(false, "Unexpected case here");   
    #endif    
  }
}




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
bool even_parity(uint32_t n) {
    // Return true of even number of "1" bits, false otherwise
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
  control_packet |= (0x1 & even_parity(control_packet)) << 31;

  return control_packet;
}


uint32_t packet_flow_gen(uint32_t packet_type, uint32_t stream_id, uint32_t source_core_id =get_coreid()){

    //TODO: put a check on the packet_type? core=0, memtile=1, shimtile=2???
    uint32_t packet_header = (source_core_id << 16) | (packet_type<<12) | (stream_id);

    bool odd_parity  = (even_parity(packet_header)) ;
    packet_header |= (0x1 & odd_parity) << 31;

    return packet_header;
}


extern "C" {

void passThroughTest(uint32_t *in, uint32_t *out, 
                  int32_t buffer_size, int32_t total_passThrough_size,
                  int32_t in_buffer_prod_lock, int32_t in_buffer_con_lock,
                  int32_t out_buffer_prod_lock, int32_t out_buffer_con_lock,


                  int32_t* CT2_control_out_buffer, int32_t* CT2_control_res_buffer,
                  int32_t CT2_control_out_prod_lock, int32_t CT2_control_out_con_lock,
                  int32_t CT2_control_in_prod_lock, int32_t CT2_control_in_con_lock
                  
){
  // assume divisible and multiple of two
  for(uint32_t i = 0; i < (total_passThrough_size /buffer_size ); i += 2){
    //NOTE: need to enable core access to bus externally
    


    acquire_greater_equal(in_buffer_con_lock, 1);
    if(i == 0){
        //BD_ID_4 is the control packet out
        
        read_processor_bus(in+10, 0x000001D080, 1, 16); // 0
        read_processor_bus(in+11, 0x000001D084, 1, 16); // 0 
        read_processor_bus(in+12, 0x000001D088, 1, 16); // 0        
        read_processor_bus(in+13, 0x000001D08C, 1, 16); // 0
        read_processor_bus(in+14, 0x000001D090, 1, 16); // 0
        read_processor_bus(in+15, 0x000001D094, 1, 16); // 0       

        //MM2S info
        read_processor_bus(in+20, 0x000001DE18, 1, 16);
        read_processor_bus(in+21, 0x000001DE1C, 1, 16);        

        // Given the values above are all "0", it seem BD is not configured until lock is acquire??

        event0();
        acquire_greater_equal(CT2_control_out_prod_lock, 1);
        *CT2_control_out_buffer =  control_packet_gen(14, 1, 0, 0x000001D004);
        release(CT2_control_out_con_lock, 1);
        event0();

        event0();
        acquire_greater_equal(CT2_control_in_con_lock, 1);
        *(in+23) = *CT2_control_res_buffer;
        release(CT2_control_in_prod_lock, 1);
        event1();


    }else{
       
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





} // extern "C"
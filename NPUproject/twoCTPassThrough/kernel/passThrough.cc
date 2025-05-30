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
        data[i] = read_tm(addr  );
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
        write_tm( data[i],addr );
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
  uint32_t val_write[1];
  volatile uint32_t *val_write_ptr = val_write; 
  // assume divisible and multiple of two
  for(uint32_t i = 0; i < (total_passThrough_size /buffer_size ); i += 2){

    acquire_greater_equal(in_buffer_con_lock, 1);
    if(i == 0){

        // write_process_bus( (in+1),0x0000032038, 1, 1  );  
        //TODO: either enable here, or enable at runtime sequenc?
        acquire_greater_equal(control_packet_write_prod_lock, 1);
        *control_write_buffer =   control_packet_gen(12, 0, 0,   0x0000032038 );
        *(control_write_buffer+1)   = 1;
        release(control_packet_write_con_lock, 1); 


        bool FIX_ERROR_BY_CONTROL_PACKET= false;

        if(!FIX_ERROR_BY_CONTROL_PACKET){
          event0();
          *(val_write_ptr) =(1<<30) | (9<<19);
          write_process_bus( (uint32_t*)(val_write_ptr),0x001D044, 1, 4  );
          event0();           

          event0();
          *(val_write_ptr) =(1<<1);
          write_process_bus( (uint32_t*)(val_write_ptr),0x1DE10, 1, 4  );  
          event0();             

          event0();
          *(val_write_ptr) =(10<1);
          write_process_bus( (uint32_t*)(val_write_ptr),0x1DE10, 1, 4  ); 
          event0();          

          *(val_write_ptr) =(1<<16) | (2);
          write_process_bus( (uint32_t*)(val_write_ptr),0x1DE14, 1, 4  );            
      
        }else{
            acquire_greater_equal(control_packet_write_prod_lock, 1);
            *control_write_buffer =   control_packet_gen(12, 0, 0,   0x001D044 );
            *(control_write_buffer+1) = (1<<30) | (9<<19); //0x40480000; //(1<<31) | (9<<19);
            release(control_packet_write_con_lock, 1);
            
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
        }

        acquire_greater_equal(control_packet_read_prod_lock, 1);
        *control_read_buffer =   control_packet_gen(11, 1, 0,   0x001D044  );
        release(control_packet_read_con_lock, 1);

        acquire_greater_equal(control_packet_read_res_con_lock, 1);
        *(in) = *control_read_buffer_res;
        release(control_packet_read_res_prod_lock, 1);

    }else{
      event0();
      read_processor_bus(in,  0x1D044,1,4);        // NOTE: Write did go through, but somehow did not apply to qeue?0x1D044, 1, 1);
      event0();
      
     read_processor_bus(in+1,  0x0000032000,1,4);   //Prove that CT control is always enable during bitstream

      *(val_write_ptr) =(1<<30) | (9<<19) | (5<<0); // need enable packet, laso packet_type force to be 0, because is core???
      write_process_bus( (uint32_t*)(val_write_ptr),0x000001D0E4, 1, 4  );   // only give 40000000
      read_processor_bus((in+3), 0x000001D0E4, 1, 1);
        
    }


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

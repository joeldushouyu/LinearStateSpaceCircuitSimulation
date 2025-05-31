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


inline void compiler_sync_barrier(){
    #if defined(__chess__)
        chess_separator_scheduler(2);
    #elif defined(__AIECC__)
        __builtin_aie2p_sched_barrier();   
    #else
        static_assert(false, "Unexpected case here");   
    #endif
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


inline void configure_BD_4_MM2S_1_dma_bd_len(uint32_t len, uint32_t bd_repeat_len=1 ){
    uint32_t len_mask = 0;
    uint32_t write_buffer[1];



    *(write_buffer) =(1<<1);// disable MM2S-1
    compiler_sync_barrier();  
    write_process_bus( (uint32_t*)(write_buffer),0x000001DE18, 1, 16 );  
    compiler_sync_barrier();  



    // compiler_sync_barrier();  
    read_processor_bus( write_buffer, 0x000001D080, 1, 16 );// first read
    compiler_sync_barrier();  

    len_mask = 0x3FFF;
    *write_buffer =  ( (*write_buffer) & ~len_mask) | ( (len) & len_mask);  
    compiler_sync_barrier();          
    write_process_bus( write_buffer, 0x000001D080, 1, 16 );
    compiler_sync_barrier();  



    *(write_buffer) =(0<1);  // renable MM2S-1
    compiler_sync_barrier();  
    write_process_bus( (uint32_t*)(write_buffer),0x000001DE18, 1, 16  ); 
    compiler_sync_barrier();  

    event0();
    *(write_buffer) =(bd_repeat_len<<16) | (4);
    compiler_sync_barrier();         
    write_process_bus( (uint32_t*)(write_buffer),0x000001DE1C, 1, 16  ); 
    compiler_sync_barrier();           
    event0();



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

uint32_t write_buffer[1];
volatile int dummy = 0;
for (uint32_t i = 0; i < 50000; i++) {
    dummy++;  // wait for Trace to finish setting up the events
}


    uint32_t Shimtile_BD_1_1_val = 0;

    configure_BD_4_MM2S_1_dma_bd_len(1);// configure to write control packet len 
    acquire_greater_equal(CT2_control_out_prod_lock, 1);
    *CT2_control_out_buffer =  control_packet_gen(14, 1, 0, 0x000001D024);
    release(CT2_control_out_con_lock, 1);

    acquire_greater_equal(CT2_control_in_con_lock, 1);
    Shimtile_BD_1_1_val = *CT2_control_res_buffer; // Result of read control packet
    release(CT2_control_in_prod_lock, 1);


    configure_BD_4_MM2S_1_dma_bd_len(2);// configure to write control packet len

  acquire_greater_equal(CT2_control_out_prod_lock, 1);
  *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D000  );
  *(CT2_control_out_buffer+1)=   0x1000; //or 0x40308000
  release(CT2_control_out_con_lock, 1);


  acquire_greater_equal(CT2_control_out_prod_lock, 1);
  *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D004  );
  *(CT2_control_out_buffer+1)=  0x77fb9000;// Shimtile_BD_0_1_val; //0x77fb9000; //or NOTE: disable ASLR OR TODO: read from shimtile registers?
  release(CT2_control_out_con_lock, 1);

  acquire_greater_equal(CT2_control_out_prod_lock, 1);
  *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D008  );
  *(CT2_control_out_buffer+1)= 0x40308000;//  (1<<30) | (6<<19) | (0<<16) | ( 0x3FFF &Shimtile_BD_0_2_val );   //0x40308000; //or NOTE: disable ASLR
  release(CT2_control_out_con_lock, 1);

  acquire_greater_equal(CT2_control_out_prod_lock, 1);
  *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D00C  );
  *(CT2_control_out_buffer+1)=   0; //or NOTE: disable ASLR
  release(CT2_control_out_con_lock, 1);

    acquire_greater_equal(CT2_control_out_prod_lock, 1);
  *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D010  );
  *(CT2_control_out_buffer+1)=   0x40000000; //or NOTE: disable ASLR
  release(CT2_control_out_con_lock, 1);



  acquire_greater_equal(CT2_control_out_prod_lock, 1);
  *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D014  );
  *(CT2_control_out_buffer+1)=   0; //or NOTE: disable ASLR
  release(CT2_control_out_con_lock, 1);

  acquire_greater_equal(CT2_control_out_prod_lock, 1);
  *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D018  );
  *(CT2_control_out_buffer+1)=   0; //or NOTE: disable ASLR
  release(CT2_control_out_con_lock, 1);


  acquire_greater_equal(CT2_control_out_prod_lock, 1);
  *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D01C  );
  *(CT2_control_out_buffer+1)=   0x2000000; //or NOTE: disable ASLR
  release(CT2_control_out_con_lock, 1);

    // acquire_greater_equal(CT2_control_out_prod_lock, 1);
    // *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D210  );
    // *(CT2_control_out_buffer+1)=   27<<8;
    // release(CT2_control_out_con_lock, 1);

    // Now, configure MM2S0 to  send BD_0
    event0(); // Send Write packet
    acquire_greater_equal(CT2_control_out_prod_lock, 1);
    *CT2_control_out_buffer = control_packet_gen(14, 0, 0,0x000001D214  );
    *(CT2_control_out_buffer+1)=   0;  //Do not issue token, because did not setup wait at runtime sequence
    release(CT2_control_out_con_lock, 1);

  for(uint32_t i = 0; i < (total_passThrough_size /buffer_size ); i += 2){
    //NOTE: need to enable core access to bus externally    

    acquire_greater_equal(in_buffer_con_lock, 1);
    event1(); // whem Shimtile receives write packet that configures and start sending data
    if(i == 0){
        //BD_ID_4 is the control packet out
        *(in+5) = Shimtile_BD_1_1_val;
        read_processor_bus(in+10, 0x000001D080, 1, 16); // 0
        read_processor_bus(in+11, 0x000001D084, 1, 16); // 0 
        read_processor_bus(in+12, 0x000001D088, 1, 16); // 0        
        read_processor_bus(in+13, 0x000001D08C, 1, 16); // 0
        read_processor_bus(in+14, 0x000001D090, 1, 16); // 0
        read_processor_bus(in+15, 0x000001D094, 1, 16); // 0       
        read_processor_bus(in+21, 0x000001D080, 1, 16); // 0     
        // //MM2S info
        // read_processor_bus(in+20, 0x000001DE18, 1, 16);
        // read_processor_bus(in+21, 0x000001DE1C, 1, 16);        

        // NOTE: if look at MM2S-1 of CT_0_2, it is configured to send packet of len=2( for output)
        //But if we want to read it, Then we needs to change to len=1, only send read control packet
        configure_BD_4_MM2S_1_dma_bd_len(1);

        read_processor_bus(in+22, 0x000001D080, 1, 16); // 0     
        event0();
        acquire_greater_equal(CT2_control_out_prod_lock, 1);
        *CT2_control_out_buffer =  control_packet_gen(14, 1, 0, 0x000001D004);
        release(CT2_control_out_con_lock, 1);

        acquire_greater_equal(CT2_control_in_con_lock, 1);
        *(in+24) =*CT2_control_res_buffer; // Result of read control packet
        release(CT2_control_in_prod_lock, 1);
        event1();    

    }else{
       
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
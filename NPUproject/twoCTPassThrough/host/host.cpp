#include <bits/stdc++.h>
#include <boost/program_options.hpp>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdfloat>
#include "debug_utils.hpp"

#include "typedef.hpp"
#include "npu_utils.hpp"
#include "vm_args.hpp"
#include "utils.hpp"
#include "mvm_sequence.hpp"
#include "experimental/xrt_kernel.h"
#include "experimental/xrt_queue.h"
#include <nlohmann/json.hpp> // Include the nlohmann/json header
using json = nlohmann::json;
namespace po = boost::program_options;
#include <vector>
#include <cmath>    // For std::fabs, std::max
#include <algorithm> // For std::max

// #include "circuitData.hpp"
// #include "circuitSimCore.hpp"
// #include "circuitConfig.hpp"
// #include "circuitSimulationHost.hpp"
#include "host_helper.hpp"

using int32 = std::int32_t;




int main(int argc, const char *argv[]) {
    // Fix the seed to ensure reproducibility in CI.
    srand(0);

    int Iterations = 1; // NOTE: only can run one time due to matrix balance transfer on s2mm
                    // once transfer matrix, the s2mm-1 will never go back to transfer matrix mode

    // NPU instance
    npu_app npu_instance(1);
    if (VERBOSE >= 1){
        npu_instance.get_npu_power(true);
        npu_instance.print_npu_info();
    }

    accel_user_desc accel_desc_0 = {
        .xclbin_name = "build/xclbins/mv.xclbin",
        .instr_seq = npu_sequence("build/insts/mv.txt", true),
    };


    int app_id_0 = npu_instance.register_accel_app(accel_desc_0);

    npu_instance.interperate_bd(0);
    // npu_instance.interperate_bd(1);

    // compare the two sequences
    int total_size = 4096;
    int TRACE_SIZE = 8192;


    buffer<int32_t> seq_0 = accel_desc_0.instr_seq.to_bo().cast_to<int32_t>();

    buffer<dtype_in> in_0 = npu_instance.create_bo_buffer<dtype_in>( total_size, 3, app_id_0);
    buffer<dtype_out> out_0 = npu_instance.create_bo_buffer<dtype_out>(total_size, 4, app_id_0);
    buffer<dtype_in> zero_0 = npu_instance.create_bo_buffer<dtype_in>(1,5,app_id_0);
    buffer<dtype_in> zero_1 = npu_instance.create_bo_buffer<dtype_in>(1, 6, app_id_0);
    int tmp_trace_size = (TRACE_SIZE > 0) ? TRACE_SIZE :1;
    buffer<char> trace_res = npu_instance.create_bo_buffer<char>(tmp_trace_size,7, app_id_0 );



    for(uint32_t i = 0; i < total_size; i++){
        in_0[i] = i+1;
    }




    in_0.sync_to_device();
    char *bufTrace = trace_res.data();
    if(TRACE_SIZE>0){
        memset(bufTrace, 0, TRACE_SIZE);
        trace_res.sync_to_device();
    }



    auto run_0 = npu_instance.create_run(app_id_0,  in_0.bo(), out_0.bo(),  zero_0.bo(), zero_1.bo(),  trace_res.bo() );

	
    header_print("info", "Running runtime test.");
    header_print("info", "Running kernel with bare call.");
    time_utils::time_with_unit npu_time = {0.0, "us"};
	
    for (int i = 0; i < Iterations; i++) {
        time_utils::time_point start = time_utils::now();
        run_0.start();
        run_0.wait();

	    time_utils::time_point stop = time_utils::now();
	    npu_time.first += time_utils::duration_us(start, stop).first;
    }
    npu_time.first /= Iterations * 2.0;
    MSG_BONDLINE(40);
    MSG_BOX_LINE(40, "NPU time with bare call: " << npu_time.first << " us");
    MSG_BONDLINE(40);

    out_0.sync_from_device();
    if(TRACE_SIZE > 0){
        trace_res.sync_from_device();
        npu_instance.write_out_trace(((char *)bufTrace), TRACE_SIZE,
        "trace.txt");
    }

    header_print("info", "Finished running kernel");





    bool pass =true;
    // pass = are_results_close( out_0, in_0,1e-4f, 1e-3f,  total_size  );
    for(auto k = 0; k < total_size; k++){

        if (out_0[k] != in_0[k]){
            pass = false;
            std::cout << "&&&&&&&&&&&&&&" << std::endl;
            std::cout << " " << std::hex <<k << "  index for  " <<std::hex << out_0[k] << std::endl;
        }else{

        }
    
    }
    // // // debug_inspect_all(
    // // //     matrix_in, matrix_out_col_major, 
    // // //     std::pow(2, SWITCH_SIZE + DIODE_SIZE)
    // // // );

    if (pass ==false){
        std::cout <<"Fail stage 1" << std::endl;
    }else{
        printf("passed first stage input\n");
    }
    // pass &= are_results_close( out_0, out_ref_0,1e-4f, 1e-3f,  TOTAL_SWITCH_DIODE_STATE*(C1_DSW_ROW_SIZE + A_B_C_D_ROW_SIZE)  );
    // if(pass==false){
    //     std::cout << "FAil stage2" <<std::endl;
    // }
    // for (size_t i = 0; i < 16; i++) {
    //     std::cout << std::scientific      // Use exponential notation
    //               << std::setprecision(6) // Show 2 digits after decimal
    //               << "out_0[" << i << "] = " << out_0[i]
    //               << " ?= out_ref_0[" << i << "] = " << out_ref_0[i]
    //               << std::endl;
    // }



    // for(auto k = 0; k < 8000* OUTPUT_SIZE_PER_ITERATION; k++){

    //     std::cout << out_0[k] << " ";
    //     if( (k+1) % OUTPUT_SIZE_PER_ITERATION ==0  ){
    //         std::cout << std::endl;
    //     }
    // }
    // std::cout << std::endl;
    // std::cout << std::endl;

    // uint32_t offset = A_B_C_D_ROW_SIZE;
    // std::cout << "Switch states reference: " 
    // << std::bitset<sizeof(uint32_t) * 8>(std::bit_cast<uint32_t>(switch_diode_status_buffer_after_iteration[0]))
    // << " result: " 
    // << std::bitset<sizeof(float) * 8>(std::bit_cast<uint32_t>(out_0[offset]))
    //  << "  with input switch of" << std::bitset<sizeof(float) * 8>(std::bit_cast<uint32_t>(in_0[1]))  <<std::endl;

    // for(size_t i = 0; i< 6; i++ ){

    //     std::cout << "C1_mask_result reference: " <<  std::bitset<sizeof(float) * 8>(std::bit_cast<uint32_t>(C1_RES_MASK_BUFFER[i])) <<
    //     "  result fron NPU" <<std::bitset<sizeof(float) * 8>(std::bit_cast<uint32_t>(out_0[i+offset+1])) <<std::endl;

    // }
    // float *data_pt = out_0.data();
    // writeDataToCsvFile("npuSim.csv",  dataFromFile, data_pt );
    // if (pass){
    //     header_print("info", "PASSED ");
    // } else {
    //     header_print("info", "FAILED!");
    // }

    // utils::print_npu_profile(npu_time, 2.0 * float(M) * float(K) * float(N), 1000);
    return 0;
}


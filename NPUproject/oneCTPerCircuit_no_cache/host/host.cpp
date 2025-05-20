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

#include "circuitData.hpp"
#include "circuitSimCore.hpp"
#include "circuitConfig.hpp"
#include "circuitSimulationHost.hpp"
#include "host_helper.hpp"

using int32 = std::int32_t;




int main(int argc, const char *argv[]) {
    // Fix the seed to ensure reproducibility in CI.
    srand(0);


    int in_size = C1_DSW_BUFFER_SIZE  +A_B_C_D_BUFFER_SIZE;
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
    int input_iteration_size = BUFFER_SIZE_OF_IN_PING_POING * PING_PONG_BUFFER_ITERATION ;
    int output_iteration_size = BUFFER_SIZE_OF_OUT_PING_PONG * PING_PONG_BUFFER_ITERATION ;

    buffer<int32_t> seq_0 = accel_desc_0.instr_seq.to_bo().cast_to<int32_t>();
    buffer<dtype_in> matrix_in = npu_instance.create_bo_buffer<dtype_in>(in_size, 3, app_id_0);
    buffer<dtype_out> debug_buffer = npu_instance.create_bo_buffer<dtype_out>(in_size, 4, app_id_0);
    buffer<dtype_in> in_0 = npu_instance.create_bo_buffer<dtype_in>( input_iteration_size, 5, app_id_0);
    buffer<dtype_out> out_0 = npu_instance.create_bo_buffer<dtype_out>(output_iteration_size, 6, app_id_0);

    int tmp_trace_size = (TRACE_SIZE > 0) ? TRACE_SIZE :1;
    buffer<char> trace_res = npu_instance.create_bo_buffer<char>(tmp_trace_size,7, app_id_0 );


    // load data from file and so 
    CircuitData dataFromFile = CircuitData();
    float    *C1_DSW_buffer = new float   [C1_DSW_BUFFER_SIZE];
    float    *ABCD_buffer   =  new float   [A_B_C_D_BUFFER_SIZE];
    float    *input_buffers = new float   [ITERATION_STEP_NUMBER*INPUT_SIZE_PER_ITERATION];
    uint32_t *switch_diode_status_buffer_after_iteration = new uint32_t[ITERATION_STEP_NUMBER];


    prepareDataForIteration("Metadata.h5", dataFromFile, C1_DSW_buffer, ABCD_buffer, input_buffers);
    float output_simulation_buffer_reference[OUTPUT_SIZE_PER_ITERATION *ITERATION_STEP_NUMBER ];
    iteration(C1_DSW_buffer, ABCD_buffer, input_buffers, output_simulation_buffer_reference,  dataFromFile.switch_diode_status_record, 
         switch_diode_status_buffer_after_iteration,false);
    
    
    // // copy of matrix
    // for(uint32_t i = 0; i <C1_DSW_BUFFER_SIZE; i++ ){
    //     matrix_in[i] = C1_DSW_buffer[i];
    // }
    // for(uint32_t  i = 0; i < A_B_C_D_BUFFER_SIZE; i++){
    //     matrix_in[i+C1_DSW_BUFFER_SIZE ] = ABCD_buffer[i];
    // }
    // do data rearrangement at the host, so Shimtile does not have to do the reordering?
    uint32_t kernel_mat_v_size = 16;
    uint32_t matrix_in_ind = 0;
    for(uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE;  i++){
        for(uint32_t j = 0; j <  C1_DSW_ROW_SIZE/kernel_mat_v_size;  j++ ){
            for(uint32_t k = 0; k <C1_DSW_COL_SIZE; k++  ){
                for(uint32_t l = 0; l < kernel_mat_v_size;  l++){

                    matrix_in[matrix_in_ind++] = C1_DSW_buffer[
                        C1_DSW_ROW_SIZE*C1_DSW_COL_SIZE* i +
                        j* kernel_mat_v_size*C1_DSW_COL_SIZE+ 
                        1*k + 
                        C1_DSW_COL_SIZE*l
                    ];
                }
            }
        }
    }
    assert(matrix_in_ind == C1_DSW_BUFFER_SIZE);

    for(uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++ ){
        for(uint32_t j = 0; j <  A_B_C_D_ROW_SIZE/kernel_mat_v_size; j++){
            for(uint32_t k = 0; k < A_B_C_D_COL_SIZE; k++){
                for(uint32_t l = 0; l <kernel_mat_v_size; l++ ){

                    matrix_in[matrix_in_ind++] = ABCD_buffer[
                        A_B_C_D_COL_SIZE*A_B_C_D_ROW_SIZE*i +
                        j*kernel_mat_v_size*A_B_C_D_COL_SIZE+
                        1*k+
                        A_B_C_D_COL_SIZE*l

                    ];
                }
            }
        }

    }




    // copy of input
    for(uint32_t i = 0; i <ITERATION_STEP_NUMBER*INPUT_SIZE_PER_ITERATION; i++  ){
        in_0[i] = input_buffers[i];
        if(i < 20){
            std::cout << "in at i" << i << " " << in_0[i] << std::endl;
        }
    }


    matrix_in.sync_to_device();
    in_0.sync_to_device();
    char *bufTrace = trace_res.data();
    if(TRACE_SIZE>0){
        memset(bufTrace, 0, TRACE_SIZE);
        trace_res.sync_to_device();
    }


    // // only check partial result for now
    // buffer<dtype_out> out_ref_0(output_iteration_size);    
    // float* input_ptr = in_0.data();
    // float* ref_res = out_ref_0.data();
    

    // for(int i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++){

    //     float x[C1_DSW_COL_SIZE] = {0}; // for now
        
    //     for(int l = 0; l < U_SIZE; l++){
    //         x[STATE_SIZE + l] = *input_ptr++;
    //     }
    //     input_ptr++; // the external switch bit that is not used for now

    //     std::vector<float>res  = matvec_mul_row_major(
    //         C1_DSW_buffer + (i*C1_DSW_MATRIX_SIZE),x, 
    //         C1_DSW_ROW_SIZE,
    //         C1_DSW_COL_SIZE 
    //     );

    //     // STORE the reference result
    //     for(auto v :res){
    //         *ref_res++= v;
    //     }

    //     // A_B_C_D whole matrix
    //     std::vector<float> abcd_res = matvec_mul_row_major(
    //         ABCD_buffer +(i*A_B_C_D_MATRIX_SIZE),x,
    //         A_B_C_D_ROW_SIZE,
    //         A_B_C_D_COL_SIZE
    //     );
    //     // STORE the reference result
    //     for(auto v :abcd_res){
    //         *ref_res++= v;
    //     }


    // }





    auto run_0 = npu_instance.create_run(app_id_0, matrix_in.bo(),  debug_buffer.bo(), in_0.bo(), out_0.bo(),   trace_res.bo() );

	
    header_print("info", "Running runtime test.");
    header_print("info", "Running kernel with bare call.");
    time_utils::time_with_unit npu_time = {0.0, "us"};
	
    for (int i = 0; i < Iterations; i++) {
        time_utils::time_point start = time_utils::now();
        run_0.start();
        ert_cmd_state r = run_0.wait();
        if (r != ERT_CMD_STATE_COMPLETED) {
            std::cout << "Kernel did not complete. Returned status: " << r << "\n";
            return 1;
        }
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





    bool pass = are_results_close( in_0, out_0,1e-4f, 1e-3f,  BUFFER_SIZE_OF_IN_PING_POING);
    // // // debug_inspect_all(
    // // //     matrix_in, matrix_out_col_major, 
    // // //     std::pow(2, SWITCH_SIZE + DIODE_SIZE)
    // // // );

    if (pass ==false){
        std::cout <<"Fail stage 1" << std::endl;

        // for (size_t i = 0; i < BUFFER_SIZE_OF_OUT_PING_PONG* 2; i++) {
        //     std::cout << std::scientific      // Use exponential notation
        //             << std::setprecision(6) // Show 2 digits after decimal
        //             << "out_0[" << i << "] = " << out_0[i]
        //             << " ?= out_ref_0[" << i << "] = " << in_0[i]
        //             << std::endl;
        // }

        for(size_t k = 0; k < 3; k++){
            for(size_t i = 0; i < BUFFER_SIZE_OF_OUT_PING_PONG; i++){
                if(i >= BUFFER_SIZE_OF_IN_PING_POING){break;}
                
                auto index = i + k*BUFFER_SIZE_OF_OUT_PING_PONG;
                std::cout << std::scientific      // Use exponential notation
                    << std::setprecision(6) // Show 2 digits after decimal
                    << "out_0[" << index << "] = " << out_0[index  ]
                    << " ?= out_ref_0[" << index << "] = " << in_0[index]
                    << std::endl;
            }

        }

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
    float *data_pt = out_0.data();
    writeDataToCsvFile("npuSim.csv",  dataFromFile, data_pt );
    // if (pass){
    //     header_print("info", "PASSED ");
    // } else {
    //     header_print("info", "FAILED!");
    // }

    // utils::print_npu_profile(npu_time, 2.0 * float(M) * float(K) * float(N), 1000);
    return 0;
}


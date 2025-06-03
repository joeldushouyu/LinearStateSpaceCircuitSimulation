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
    float    *AB_buffer     =   new float [AB_BUFFER_SIZE];
    float    *CD_natural_impulse_buffer = new float[CD_NATURAL_IMPULSE_BUFFER_SIZE];
    static_assert(AB_BUFFER_SIZE + CD_NATURAL_IMPULSE_BUFFER_SIZE == A_B_C_D_BUFFER_SIZE);
    float    *input_buffers = new float   [ITERATION_STEP_NUMBER*INPUT_SIZE_PER_ITERATION];
    uint32_t *switch_diode_status_buffer_after_iteration = new uint32_t[ITERATION_STEP_NUMBER];


    prepareDataForIteration("Metadata.h5", dataFromFile, C1_DSW_buffer, ABCD_buffer, input_buffers);
    float output_simulation_buffer_reference[OUTPUT_SIZE_PER_ITERATION *ITERATION_STEP_NUMBER ];
    iteration(C1_DSW_buffer, ABCD_buffer, input_buffers, output_simulation_buffer_reference,  dataFromFile.switch_diode_status_record, 
         switch_diode_status_buffer_after_iteration,false);
    
    
    // Something different in this host implementation
    //Given ABCD_buffer is store in the following order
    // AB matrix, CD_natural matrix, CD_impulse_matrix, AB_matrix, CD_natural matrix, CD_imnpulse_matrix and repeat this pattern for TOTAL_SWITCH_DIODE_STATE

    // Goal is to separate two buffer of
    // AB_matrix, AB_matrix, AB_matrix, AB_matrix,
    // CD_natural_matrix, CD_impulse_matrix, CD_natural_matrix, CD_impulse_matrix, CD_natural_matrix, CD_impulse_matrix ... 

    // do data rearrangement at the host, so Shimtile does not have to do the reordering?
    constexpr  uint32_t kernel_mat_v_size = 16;
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
    
    //Recall A_B_C_D_ is store in row major order, now store in column major order with strie of kernel_mat_v_size
    for(uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++ ){

        //AB_matrix
        for(uint32_t j = 0; j <  AB_ROWS/kernel_mat_v_size; j++){
            for(uint32_t k = 0; k < A_B_C_D_COL_SIZE; k++){
                for(uint32_t l = 0; l <kernel_mat_v_size; l++ ){

                    matrix_in[matrix_in_ind +    k*kernel_mat_v_size + l   ] = ABCD_buffer[
                        A_B_C_D_COL_SIZE*A_B_C_D_ROW_SIZE*i +
                        j*kernel_mat_v_size*A_B_C_D_COL_SIZE+
                        1*k+
                        A_B_C_D_COL_SIZE*l

                    ];
            
                }
            }
            matrix_in_ind += AB_MAT_SIZE;
        }

        //CD_natural CD impulse
        
        for(uint32_t j = AB_ROWS/kernel_mat_v_size; j <     (AB_ROWS+2*CD_NAT_OR_IMP_ROWS)/kernel_mat_v_size; j++){
            for(uint32_t k = 0; k < A_B_C_D_COL_SIZE; k++){
                for(uint32_t l = 0; l <kernel_mat_v_size; l++ ){

                    matrix_in[matrix_in_ind +    k*kernel_mat_v_size + l   ] = ABCD_buffer[
                        A_B_C_D_COL_SIZE*A_B_C_D_ROW_SIZE*i +
                        j*kernel_mat_v_size*A_B_C_D_COL_SIZE+
                        1*k+
                        A_B_C_D_COL_SIZE*l

                    ];
            
                }
            }
            matrix_in_ind += CD_NAT_OR_IMP_MAT_SIZE;
        }

    }

    // static_assert( (AB_COLS == CD_NAT_OR_IMP_COLS) && ( CD_NAT_OR_IMP_COLS== A_B_C_D_COL_SIZE));

    // // First store all AB blocks for all switch-diode states
    // for (uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++) {
    //     for (uint32_t j = 0; j < AB_ROWS / kernel_mat_v_size; j++) {
    //         for (uint32_t k = 0; k < A_B_C_D_COL_SIZE; k++) {
    //             for (uint32_t l = 0; l < kernel_mat_v_size; l++) {
    //                 matrix_in[matrix_in_ind + k * kernel_mat_v_size + l] =
    //                     ABCD_buffer[
    //                         A_B_C_D_COL_SIZE * A_B_C_D_ROW_SIZE * i +
    //                         j * kernel_mat_v_size * A_B_C_D_COL_SIZE +
    //                         k +
    //                         A_B_C_D_COL_SIZE * l
    //                     ];
    //             }
    //         }
    //         matrix_in_ind += AB_MAT_SIZE;
    //     }
    // }

    // // Then store all CDnatural and CDimpulse blocks for all switch-diode states
    // for (uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++) {
    //     for (uint32_t j = AB_ROWS / kernel_mat_v_size;
    //                 j < (AB_ROWS + 2 * CD_NAT_OR_IMP_ROWS) / kernel_mat_v_size;
    //         j++) {
    //         for (uint32_t k = 0; k < A_B_C_D_COL_SIZE; k++) {
    //             for (uint32_t l = 0; l < kernel_mat_v_size; l++) {
    //                 matrix_in[matrix_in_ind + k * kernel_mat_v_size + l] =
    //                     ABCD_buffer[
    //                         A_B_C_D_COL_SIZE * A_B_C_D_ROW_SIZE * i +
    //                         j * kernel_mat_v_size * A_B_C_D_COL_SIZE +
    //                         k +
    //                         A_B_C_D_COL_SIZE * l
    //                     ];
    //             }
    //         }
    //         matrix_in_ind += CD_NAT_OR_IMP_MAT_SIZE;
    //     }
    // }




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




    auto run_0 = npu_instance.create_run(app_id_0, matrix_in.bo(),  debug_buffer.bo(), in_0.bo(), out_0.bo(),   trace_res.bo() );

	
    header_print("info", "Running runtime test.");
    header_print("info", "Running kernel with bare call.");
    time_utils::time_with_unit npu_time = {0.0, "us"};
	
   
    time_utils::time_point start = time_utils::now();
    auto start_timer = std::chrono::high_resolution_clock::now();
    run_0.start();
    run_0.wait();
    auto stop_timer = std::chrono::high_resolution_clock::now();
    time_utils::time_point stop = time_utils::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop_timer - start_timer).count();

    std::cout << std::dec << "Elapsed time: " << duration << " us" << std::endl;


    npu_time.first += time_utils::duration_us(start, stop).first;
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

    float *data_pt = out_0.data();
    writeDataToCsvFile("npuSim.csv",  dataFromFile, data_pt );

    return 0;
}


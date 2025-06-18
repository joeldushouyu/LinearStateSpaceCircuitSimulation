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



#include <iostream>
#include <vector>
#include <algorithm> // for std::rotate

void move_subrange(std::vector<float>& arr, size_t start, size_t end, size_t dest_index) {
    // Sanity checks
    if (start >= end || end > arr.size() || dest_index > arr.size()) {
        std::cerr << "Invalid indices.\n";
        return;
    }

    if (dest_index >= start && dest_index <= end) {
        std::cerr << "Destination cannot be within the range to move.\n";
        return;
    }

    if (dest_index < start) {
        // Move to earlier position
        std::rotate(arr.begin() + dest_index, arr.begin() + start, arr.begin() + end);
    } else {
        // Move to later position
        std::rotate(arr.begin() + start, arr.begin() + end, arr.begin() + dest_index);
    }
}



int main(int argc, const char *argv[]) {
    // Fix the seed to ensure reproducibility in CI.
    srand(0);
    std::string metadataFileName;
    std::string bitstreamFileName;
    std::string runtimeSequenceFileName;
    std::string csvDataFileName;
    if (argc < 4) {
        std::cout << "Argc" << argc << std::endl;
        std::cerr << "Error: Not enough arguments provided." << std::endl;
        std::cerr << "Usage arg[1] Metadata arg[2] bitstream arg[3] runtime_sequence" << std::endl;
        return -1;
    } else {
        metadataFileName = argv[1];
        bitstreamFileName = argv[2];
        runtimeSequenceFileName = argv[3];
        if (argc > 4) {
            csvDataFileName = argv[4];
        }
    }


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
        .xclbin_name = bitstreamFileName,
        .instr_seq = npu_sequence(runtimeSequenceFileName, true),
    };

    int app_id_0 = npu_instance.register_accel_app(accel_desc_0);

    // npu_instance.interperate_bd(0);
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


    prepareDataForIteration(metadataFileName.data(), dataFromFile, C1_DSW_buffer, ABCD_buffer, input_buffers);
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
    float* matrix_in_ptr = matrix_in.data();
    // Printing int pointer address
    std::cout << "Address of ptrInt (hex): " << std::hex << static_cast<void*>(matrix_in_ptr) << std::endl;

    // Printing double pointer address
    std::cout << "Address of ptrDouble (hex): " << std::hex << static_cast<void*>(matrix_in_ptr + 4*C1_DSW_MATRIX_SIZE) << std::endl;

    assert(matrix_in_ind == C1_DSW_BUFFER_SIZE);
    
    uint32_t ABCD_offset = matrix_in_ind;
    //Recall A_B_C_D_ is store in row major order, now store in column major order with strie of kernel_mat_v_size
    
    for(uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++ ){

        // Store frist 16 of AB, CD_natural matrix first, then 
        for(uint32_t j = 0; j <  A_B_C_D_ROW_SIZE/kernel_mat_v_size; j++){
            for(uint32_t k = 0; k < A_B_C_D_COL_SIZE; k++){
                for(uint32_t l = 0; l <kernel_mat_v_size; l++ ){

                    matrix_in[matrix_in_ind  + A_B_C_D_MATRIX_SIZE*i
                        + l + k*kernel_mat_v_size + j*A_B_C_D_COL_SIZE*kernel_mat_v_size
                    ] = ABCD_buffer[
                        A_B_C_D_COL_SIZE*A_B_C_D_ROW_SIZE*i +
                        j*kernel_mat_v_size*A_B_C_D_COL_SIZE+
                        1*k+
                        A_B_C_D_COL_SIZE*l

                    ];
                }
            }
        }
    
    }
    // At this point, matrix_in is stored as C1_DSW, C1_DSW .... (repeats for all case)  then (AB, CD_natural, CD_impulse) .... for all case
    // want to do some reorder here
    std::vector<float> ABCD_temp;

    for(uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE*A_B_C_D_MATRIX_SIZE; i++){
        ABCD_temp.push_back(matrix_in[i + matrix_in_ind]  );
    }

    // Do some reordering: I want to move first 16 of AB, CD_natural to infront o
    // Before, it was AB, CD_natural, CD_impulse in column order with stride of 1t
    //After:  AB_first column, CD_natural_first column, rest of AB, rest of CD_natural, CD_impulse
    for(uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++){
        uint32_t start_index = i*A_B_C_D_MATRIX_SIZE;
        move_subrange(ABCD_temp, start_index+AB_MAT_SIZE,start_index+AB_MAT_SIZE+16  , start_index+16);
        
    }
    // now write back to matrix_in
    for(uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE*A_B_C_D_MATRIX_SIZE; i++){
        matrix_in[matrix_in_ind + i] = ABCD_temp.at(i);
    }




    // copy of input
    for(uint32_t i = 0; i <ITERATION_STEP_NUMBER*INPUT_SIZE_PER_ITERATION; i++  ){
        in_0[i] = input_buffers[i];
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

    //given metadataFileName is the Metadata_half_bridge_llc_times.h5 format
    // for example :given metadataFileName is the Metadata_half_bridge_llc_0.004.h5 format
    // extract the time from the metadata name
    std::string time_str = metadataFileName.substr(metadataFileName.find_last_of('_') + 1); 
    time_str = time_str.substr(0, time_str.find_last_of('.')); // remove the .h5 part
    // convert the time_str to float
    float time_float = std::stof(time_str);
    // convert the time_float to string
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(3) << time_float;
    time_str = oss.str(); // now time_str is the time in seconds with 3 decimal places

    if(!csvDataFileName.empty()){
        append_duration_to_csv(csvDataFileName, time_str, ((float)duration)/PING_PONG_BUFFER_ITERATION);
    }
    return 0;
}


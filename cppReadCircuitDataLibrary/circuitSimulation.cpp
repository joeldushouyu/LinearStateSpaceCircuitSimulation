#include <H5Cpp.h>
#include <Eigen/Dense>
#include <nlohmann/json.hpp>
#include <vector>
#include <string>
#include <map>
#include <cmath>
#include <iostream>
#include <fstream>
#include "circuitData.hpp"
#include "circuitSimCore.hpp"
#include "circuitConfig.hpp"
using json = nlohmann::json;
#include <bitset>
#include <Eigen/Dense>
#include <iomanip>  // for std::setprecision
#include <sstream>  // for std::ostringstream
#include <iostream>
#include <cassert>
#include "circuitSimulationHost.hpp"

#include <stdlib.h>  // for malloc, free


int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <hdf5_file>" << std::endl;
        return 1;
    }

    CircuitData dataFromFile = CircuitData();
    const uint32_t iteration_steps_num = dataFromFile.switch_diode_status_record.size();

    // float C1_DSW_buffer[C1_DSW_BUFFER_SIZE];

    // float ABCD_buffer[A_B_C_D_BUFFER_SIZE];
    // float input_buffers [ITERATION_STEP_NUMBER*INPUT_SIZE_PER_ITERATION];
    // uint32_t C1_RES_MASK_BUFFER [ITERATION_STEP_NUMBER*6];
    // uint32_t switch_diode_status_buffer_after_iteration [ITERATION_STEP_NUMBER];



    // Allocate buffers on the heap
    float* C1_DSW_buffer = (float*) malloc(C1_DSW_BUFFER_SIZE * sizeof(float));
    float* ABCD_buffer = (float*) malloc(A_B_C_D_BUFFER_SIZE * sizeof(float));
    float* input_buffers = (float*) malloc(ITERATION_STEP_NUMBER * INPUT_SIZE_PER_ITERATION * sizeof(float));
    uint32_t* C1_RES_MASK_BUFFER = (uint32_t*) malloc(ITERATION_STEP_NUMBER * 6 * sizeof(uint32_t));
    uint32_t* switch_diode_status_buffer_after_iteration = (uint32_t*) malloc(ITERATION_STEP_NUMBER * sizeof(uint32_t));

    // Always check if the allocation succeeded
    if (!C1_DSW_buffer || !ABCD_buffer || !input_buffers || 
        !C1_RES_MASK_BUFFER || !switch_diode_status_buffer_after_iteration) {
        // Handle allocation failure
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }


    prepareDataForIteration(argv[1], dataFromFile, C1_DSW_buffer, ABCD_buffer, input_buffers);

    // // now doing some iteration
    // float output_buffer[OUTPUT_SIZE_PER_ITERATION *ITERATION_STEP_NUMBER ];


    float* output_buffer = (float*) malloc(OUTPUT_SIZE_PER_ITERATION * ITERATION_STEP_NUMBER * sizeof(float));
    if (!output_buffer) {
        fprintf(stderr, "Failed to allocate output_buffer\n");
        exit(EXIT_FAILURE);
    }
    


    iteration(C1_DSW_buffer, ABCD_buffer, input_buffers, output_buffer,  dataFromFile.switch_diode_status_record, C1_RES_MASK_BUFFER,switch_diode_status_buffer_after_iteration, false );
    
    
    writeDataToCsvFile("hostSim.csv", dataFromFile, output_buffer);

    return 0;
    
}   
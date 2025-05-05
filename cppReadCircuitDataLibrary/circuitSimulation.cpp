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
#include "circuiSimCore.hpp"
#include "circuitConfig.hpp"
using json = nlohmann::json;
#include <bitset>
#include <Eigen/Dense>
#include <iomanip>  // for std::setprecision
#include <sstream>  // for std::ostringstream
#include <iostream>
#include <cassert>
#include "circuitSimulationHost.hpp"
using MatrixRowMajor = Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using MatrixColMajor = Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor>;

MatrixColMajor convertToColumnMajor(const MatrixRowMajor &input)
{
    return MatrixColMajor(input);
}
MatrixRowMajor expandWithBottomRightPadding(const MatrixRowMajor &input, int newRows, int newCols)
{
    // Ensure target dimensions are valid
    if (newRows < input.rows() || newCols < input.cols())
    {
        throw std::invalid_argument("New dimensions must be greater than or equal to the input matrix dimensions.");
    }

    // Create a zero-initialized matrix of the target size
    MatrixRowMajor output = MatrixRowMajor::Zero(newRows, newCols);

    // Copy original values into the top-left block
    output.block(0, 0, input.rows(), input.cols()) = input;

    return output;
}

MatrixRowMajor formC1DSWMatrix(SwitchCaseData &data)
{

    // int C_cols = data.C_diode_explicit_der_mult_delta_t_sw.cols();
    // int D_cols = data.D_diode_explicit_der_mult_delta_t_sw.cols();
    // int C_D_rows = data.C_diode_explicit_der_mult_delta_t_sw.rows();
    // assert(C_D_rows == DIODE_SIZE);

    MatrixRowMajor C1_DSWMatrix = MatrixRowMajor::Zero(C1_DSW_ROW_SIZE, C1_DSW_COL_SIZE);

    C1_DSWMatrix.block( 0,0,  3*DIODE_SIZE,  (STATE_SIZE + U_SIZE)  ) = data.C1_DSW;
    // // std::cout << "C1_DSWMatrix block size: " << C1_DSWMatrix.rows() << "x" << C1_DSWMatrix.cols() << std::endl;
    // C1_DSWMatrix.block(0, 0, C_D_rows, C_cols) =
    //     data.C_diode_impulse_sw;

    // C1_DSWMatrix.block(0, C_cols, C_D_rows, D_cols) =
    //     MatrixRowMajor::Zero(C_D_rows, D_cols);

    // C1_DSWMatrix.block(DIODE_SIZE, 0, DIODE_SIZE, C_cols) = data.C_diode_natural_sw;
    // C1_DSWMatrix.block(C_D_rows, C_cols, DIODE_SIZE, D_cols) = data.D_diode_natural_sw;

    // C1_DSWMatrix.block(C_D_rows * 2, 0, DIODE_SIZE, C_cols) = data.C_diode_explicit_der_mult_delta_t_sw;
    // C1_DSWMatrix.block(C_D_rows * 2, C_cols, DIODE_SIZE, D_cols) = data.D_diode_explicit_der_mult_delta_t_sw;

    // std::cout << "\nMatrix: " <<" (" << C1_DSWMatrix.rows() << "x" << C1_DSWMatrix.cols() << ")" << std::endl;
    // std::cout << C1_DSWMatrix << std::endl;

    return C1_DSWMatrix;
}

MatrixRowMajor formABCDMAtrix(SwitchCaseData &data)
{

    MatrixRowMajor ABCD = MatrixRowMajor::Zero(A_B_C_D_ROW_SIZE, A_B_C_D_COL_SIZE);


    ABCD.block(0,0, 2*Y_SIZE+STATE_SIZE, STATE_SIZE+U_SIZE) = data.A_B_C_D_nonimp_imp;   
    // assert(data.x_next_with_dep_A.rows() == STATE_SIZE);
    // assert(data.x_next_with_dep_A.cols() == STATE_SIZE);
    // assert( data.x_next_with_dep_A.rows() == data.X_next_with_dep_B.rows() );


    // ABCD.block(0, 0,   STATE_SIZE, STATE_SIZE) = data.x_next_with_dep_A;
    // ABCD.block(0, STATE_SIZE,  STATE_SIZE,  U_SIZE) = data.X_next_with_dep_B;

    // ABCD.block(STATE_SIZE, 0,  Y_SIZE, STATE_SIZE ) =data.C_non_impulse;
    // ABCD.block(STATE_SIZE, STATE_SIZE, Y_SIZE, U_SIZE) = data.D_non_impulse;

    // ABCD.block(STATE_SIZE+Y_SIZE, 0,  Y_SIZE, STATE_SIZE ) = data.C_impulse;
    // ABCD.block(STATE_SIZE+Y_SIZE, STATE_SIZE, Y_SIZE, U_SIZE) = data.D_impulse;

    // // std::cout << "\nMatrix: " <<" (" << ABCD.rows() << "x" << ABCD.cols() << ")" << std::endl;
    // // std::cout << ABCD << std::endl;

    return ABCD;

}



void prepareDataForIteration(const char*fileName,   CircuitData &dataFromFile,  float*C1_DSW_Buffer, float*ABCD_buffer, float *input_buffers){

    int ret = dataFromFile.initFromFile(fileName, false);

    if (ret != 0)
    {
        std::cerr << "Error reading data from HDF5 file." << std::endl;
        throw std::runtime_error("Failed to read data from HDF5 file.");
    }

    uint32_t ABCD_buffer_init_offset = 0;
    uint32_t input_buffers_init_offset = 0;
    uint32_t C1_DSW_buffer_init_offset = 0;
    for (uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++)
    {

        auto mat = convertToColumnMajor(formC1DSWMatrix(dataFromFile.switch_cases[i]));
        std::memcpy(C1_DSW_Buffer + C1_DSW_buffer_init_offset, mat.data(), mat.size() * sizeof(float));
        C1_DSW_buffer_init_offset += mat.size();
        assert(mat.size() == C1_DSW_MATRIX_SIZE);
    }
    for (uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++)
    {   
        auto mat = convertToColumnMajor(formABCDMAtrix(dataFromFile.switch_cases[i]));
        std::memcpy(ABCD_buffer + ABCD_buffer_init_offset, mat.data(), mat.size() * sizeof(float));
        ABCD_buffer_init_offset += mat.size();
        assert(mat.size() == A_B_C_D_MATRIX_SIZE);
    }


    // reorganize th input buffers
    assert( dataFromFile.u_record.size() == U_SIZE );
    assert(dataFromFile.switch_diode_status_record.size() == ITERATION_STEP_NUMBER);
    
    for(uint32_t i = 0; i < ITERATION_STEP_NUMBER; i++)
    {
        for(uint32_t j = 0; j < INPUT_SIZE_PER_ITERATION; j++)
        {
            //TODO: when multiple inputs presents, what should be the correct order?
            //TODO: should not assume the order in the switch map/cases are corret

            if(j +1 == INPUT_SIZE_PER_ITERATION){
                uint32_t value = 0x0;
                // TODO: now assert the order of the switch is correct

                int bit_position = SWITCH_SIZE + DIODE_SIZE -1;
                for(const auto &[k, v ]: dataFromFile.switch_record){

                    if(v[i] == 1){
                        value |= (1 << bit_position);
                    }else{
                        value |= (0 << bit_position);
                    }
                    bit_position--;
                }
        

                *reinterpret_cast<uint32_t*>(&input_buffers[input_buffers_init_offset++]) = value   ;
            }else{
                for(const auto &[k, v]: dataFromFile.u_record){
                    input_buffers[input_buffers_init_offset++] = v[i];
                }
            }

        }
    }

    assert(input_buffers_init_offset ==ITERATION_STEP_NUMBER*INPUT_SIZE_PER_ITERATION );
    
}




void iteration(   float* C1_DSW_buffer, float*ABCD_buffer, float*input_buffers, float *output_buffers , std::vector<uint32_t> &switch_diode_state_reference ){


    float x_and_u_cur[BUFFER_SIZE_OF_CUR_X_U] = {0};
    float C1_DSW_mat_res[BUFFER_SIZE_OF_C1_DSW_MAT_RES] = {0};
    float ABCD_mat_res[BUFFER_SIZE_OF_A_B_C_D_MAT_RES] = {0};
    uint32_t switch_diode_state = 0x0;
    for(uint32_t i = 0; i < ITERATION_STEP_NUMBER; i++ ){

        float *cur_in = input_buffers + (i*INPUT_SIZE_PER_ITERATION);
        float *cur_out = output_buffers + (i*OUTPUT_SIZE_PER_ITERATION);
        bool externalSwitchToggled = false;        
        bool diode_change = false;
        //1. retrieve input U and external switch
        for(auto k = 0; k < INPUT_SIZE_PER_ITERATION; k++){
            if(k < U_SIZE){
                x_and_u_cur[k+ STATE_SIZE] = cur_in[k];
            }else{
                uint32_t val ;
                std::memcpy(&val, &cur_in[k], sizeof(uint32_t));

                externalSwitchToggled = !compare_and_copy_bits(  switch_diode_state,  val,  DIODE_SIZE, SWITCH_SIZE );    
            }
             
        }

        // // do a sanity check 
        std::cout << "i:" <<i << std::endl;
        std::bitset<32> binary(switch_diode_state);
        std::cout << binary.to_string() << std::endl;
        std::cout << "cur_x_u" << std::endl;
        for(auto k = 0; k < BUFFER_SIZE_OF_CUR_X_U; k++){
            std::cout << x_and_u_cur[k] << " ";
        }
        std::cout << std::endl;


        // assert(switch_diode_state_reference[i] == switch_diode_state);
        if(switch_diode_state_reference[i] != switch_diode_state){
            std::cerr << "An error occurred!" << std::endl;
            std::cerr << "mismatch at i: " << i << std::endl;
        }

        float* C1_DSW_mat = retrieveMatrixOffset(switch_diode_state, C1_DSW_MATRIX_SIZE,C1_DSW_buffer );
        print_matrix_column_major(C1_DSW_mat, C1_DSW_ROW_SIZE, C1_DSW_COL_SIZE);
        matvec_column_major(C1_DSW_mat, x_and_u_cur, C1_DSW_mat_res, C1_DSW_ROW_SIZE, C1_DSW_COL_SIZE);

        std::cout << "C1_DSW_mat_res" << std::endl;
        for(auto k = 0; k < BUFFER_SIZE_OF_C1_DSW_MAT_RES; k++){
            std::cout << C1_DSW_mat_res[k] << " ";
        }
        std::cout << std::endl; 

        // boolean logic to update diode
        //TODO: ensure the diode order is from MSB to LSB, just like switch order from MSB to KSB in switch_diode_state
        for(auto k = 0; k < DIODE_SIZE; k++){
            uint32_t diode_state_bit_ind = (DIODE_SIZE-1-k);
            uint32_t diode_state_mask = 1<<diode_state_bit_ind;

            bool diode_is_on = (switch_diode_state &diode_state_mask);
            bool impulse_is_positive = C1_DSW_mat_res[k] > 0;
            bool diode_natural_is_positive = C1_DSW_mat_res[k+DIODE_SIZE] >0 ;
            bool diode_next_is_positive =  C1_DSW_mat_res[k+2*DIODE_SIZE] > 0;
            
            bool  impulse_is_negative = C1_DSW_mat_res[k] < 0;
            bool diode_natural_is_negative = C1_DSW_mat_res[k+DIODE_SIZE] <0 ;
            bool diode_next_is_negative =  C1_DSW_mat_res[k+2*DIODE_SIZE] < 0;

            if(   (externalSwitchToggled &&   impulse_is_positive) // only when actual external switch toggleds
                  || ( !diode_is_on && diode_natural_is_positive && diode_next_is_positive  )   ){
                setBit( switch_diode_state, diode_state_bit_ind, 1);
                diode_change=true;
            }
            else if(    (externalSwitchToggled && impulse_is_negative) 
                || (diode_is_on && diode_natural_is_negative && diode_next_is_negative)  ){
                setBit( switch_diode_state, diode_state_bit_ind, 0);
                diode_change=true;
            }
        }
        std::cout <<"diode change: " <<diode_change << std::endl;

        // now x and y
        float * ABCD_mat = retrieveMatrixOffset(switch_diode_state,A_B_C_D_MATRIX_SIZE, ABCD_buffer); 




        matvec_column_major(ABCD_mat, x_and_u_cur,ABCD_mat_res,   A_B_C_D_ROW_SIZE, A_B_C_D_COL_SIZE );


        std::cout << "ABCD_mat_res" << std::endl;
        print_matrix_column_major(ABCD_mat, A_B_C_D_ROW_SIZE, A_B_C_D_COL_SIZE);
        std::cout << "cur_x_u_res" << std::endl;
        for(auto k = 0; k < BUFFER_SIZE_OF_A_B_C_D_MAT_RES; k++){
            std::cout << ABCD_mat_res[k] << " ";
        }
        std::cout << std::endl;

        // update x_cur and also write y out to array
        memcpy( x_and_u_cur,  ABCD_mat_res, sizeof(float) *(STATE_SIZE)  );

        if( externalSwitchToggled  || !diode_change){
            // either exteranl swithc toggled or non diode soft switch changed
            vector_add( ABCD_mat_res+STATE_SIZE,  cur_out, Y_SIZE  ); // vector additon of both the impulse and non-impulse response

        }else{
            memcpy(cur_out,  ABCD_mat_res+STATE_SIZE, sizeof(float) *(Y_SIZE)  );
        }
        



    
        
    }
}

int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " <hdf5_file>" << std::endl;
        return 1;
    }

    CircuitData dataFromFile = CircuitData();
    const uint32_t iteration_steps_num = dataFromFile.switch_diode_status_record.size();

    float C1_DSW_buffer[C1_DSW_BUFFER_SIZE];

    float ABCD_buffer[A_B_C_D_BUFFER_SIZE];
    float input_buffers [ITERATION_STEP_NUMBER*INPUT_SIZE_PER_ITERATION];

    prepareDataForIteration(argv[1], dataFromFile, C1_DSW_buffer, ABCD_buffer, input_buffers);

    // now doing some iteration
    float output_buffer[OUTPUT_SIZE_PER_ITERATION *ITERATION_STEP_NUMBER ];
    iteration(C1_DSW_buffer, ABCD_buffer, input_buffers, output_buffer,  dataFromFile.switch_diode_status_record);
    


    // now, write back to file


    std::ofstream myfile;

    myfile.open("hostSim.csv");
    // write the headers
    std::string header = "time";
    for(auto lab : dataFromFile.y_labels){
        header += "," + lab;
    }
    myfile << header << std::endl;
    std::cout << "header is : " << header << std::endl;

    std::cout << "iteration frequency: " << dataFromFile.general_info.iteration_frequency << std::endl;

    // now the actual data
    for (uint32_t i = 0; i < ITERATION_STEP_NUMBER; i++) {
        double iteration_time = i * (1.0 / dataFromFile.general_info.iteration_frequency);
    
        float* out_ptr = output_buffer + OUTPUT_SIZE_PER_ITERATION * i;
    
        std::ostringstream line_stream;
        line_stream << std::fixed << std::setprecision(10) << iteration_time;
    
        for (uint32_t j = 0; j < Y_SIZE; j++) {
            line_stream << "," << std::fixed << std::setprecision(10) << out_ptr[j];
        }
    
        myfile << line_stream.str() << std::endl;
    }

    
    
}   
#include "circuitSimulationHost.hpp"
#include "circuitData.hpp"
#include "circuitSimCore.hpp"
#include "circuitConfig.hpp"
#include <stdexcept>
#include <fstream>
#include <iostream>
#include <iomanip>

// // Computes y = A * x (A is column-major matrix of size rows x cols)
// void matvec_column_major(const float* A, const float* x, float* y, int rows, int cols) {
//     // Initialize output to 0
//     memset(y, 0, sizeof(float) * rows);

//     for (int col = 0; col < cols; ++col) {
//         float x_val = x[col];
//         const float* col_ptr = A + col * rows;

//         for (int row = 0; row < rows; ++row) {
//             y[row] += col_ptr[row] * x_val;
//         }
//     }
// }

// Computes y = A * x (A is row-major matrix of size rows x cols)
void matvec_row_major(const float* A, const float* x, float* y, int rows, int cols) {
    // Initialize output to 0
    memset(y, 0, sizeof(float) * rows);

    for (int row = 0; row < rows; ++row) {
        const float* row_ptr = A + row * cols;  // Pointer to current row
        float sum = 0.0f;

        for (int col = 0; col < cols; ++col) {
            sum += row_ptr[col] * x[col];  // Dot product of row and x
        }

        y[row] = sum;  // Store result in y[row]
    }
}


void vector_add(const float* a, const float*b, float *y, size_t length){
    

    for(size_t i = 0; i < length; i++){
        y[i] = a[i] + b[i];
    }


}
// void vector_add(const float* ptr, float* y, size_t length) {
//     const float* a = ptr;             // First vector
//     const float* b = ptr + length;    // Second vector

//     for (size_t i = 0; i < length; ++i) {
//         y[i] = a[i] + b[i];
//     }
// }



void print_matrix_column_major(const float* matrix, size_t rows, size_t cols) {
    for (size_t row = 0; row < rows; ++row) {
        for (size_t col = 0; col < cols; ++col) {
            // Column-major access
            std::cout << std::setw(8) << matrix[col * rows + row] << " ";
        }
        std::cout << std::endl;
    }
}

uint32_t mask_greater_than_zero(const float data[16]) {
    uint32_t mask = 0;
    for (size_t i = 0; i < 16; ++i) {
        if (data[i] > 0) {
            mask |= (1u << i);
        }
    }
    return mask;
}

uint32_t mask_less_than_zero(const float data[16]) {
    uint32_t mask = 0;
    for (size_t i = 0; i < 16; ++i) {
        if (data[i] < 0) {
            mask |= (1u << i);
        }
    }
    return mask;
}



void iteration(   float* C1_DSW_buffer, float*ABCD_buffer, float*input_buffers, float *output_buffers , std::vector<uint32_t> &switch_diode_state_reference ,
    uint32_t * C1_res_mask_Buffer, uint32_t * switch_diode_state_buffer_after_iteration, bool printDebug

){


    // float x_and_u_cur[BUFFER_SIZE_OF_CUR_X_U] = {0};
    // float C1_DSW_mat_res[BUFFER_SIZE_OF_C1_DSW_MAT_RES] = {0};
    // float ABCD_mat_res[BUFFER_SIZE_OF_A_B_C_D_MAT_RES] = {0};
    // Zero-initialized heap allocations
    float* x_and_u_cur = (float*) calloc(BUFFER_SIZE_OF_CUR_X_U, sizeof(float));
    float* C1_DSW_mat_res = (float*) calloc(BUFFER_SIZE_OF_C1_DSW_MAT_RES, sizeof(float));
    float* ABCD_mat_res = (float*) calloc(BUFFER_SIZE_OF_A_B_C_D_MAT_RES, sizeof(float));

    // Check allocation success
    if (!x_and_u_cur || !C1_DSW_mat_res || !ABCD_mat_res) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }else{
        std::cout << "begint of iteration" << std::endl;
    }



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

                externalSwitchToggled = !compare_and_copy_bits<uint32_t>(  switch_diode_state,  val,  DIODE_SIZE, SWITCH_SIZE );    
            }
             
        }

        if(printDebug){
            // // do a sanity check 
            std::cout << "i:" <<i << std::endl;
            std::bitset<32> binary(switch_diode_state);
            std::cout << binary.to_string() << std::endl;
            std::cout << "cur_x_u" << std::endl;
            for(auto k = 0; k < BUFFER_SIZE_OF_CUR_X_U; k++){
                std::cout << x_and_u_cur[k] << " ";
            }
            std::cout << std::endl;

            if(switch_diode_state_reference[i] != switch_diode_state){
                std::cerr << "An error occurred!" << std::endl;
                std::cerr << "mismatch at i: " << i << std::endl;
            }
        }

        // assert(switch_diode_state_reference[i] == switch_diode_state);


        float* C1_DSW_mat = retrieveMatrixOffset(switch_diode_state, C1_DSW_MATRIX_SIZE,C1_DSW_buffer );
        if(printDebug){
            std::cout << "Switch_diode_state" << switch_diode_state << std::endl;
            print_matrix_column_major(C1_DSW_mat, C1_DSW_ROW_SIZE, C1_DSW_COL_SIZE);
        }

        matvec_row_major(C1_DSW_mat, x_and_u_cur, C1_DSW_mat_res, C1_DSW_ROW_SIZE, C1_DSW_COL_SIZE);
        
        if(printDebug){
            std::cout << "C1_DSW_mat_res" << std::endl;
            for(auto k = 0; k < BUFFER_SIZE_OF_C1_DSW_MAT_RES; k++){
                std::cout << C1_DSW_mat_res[k] << " ";
            }
            std::cout << std::endl; 
        }

        /*
        bool debug_diode_change = false;
        uint32_t switch_diode_state_debug = switch_diode_state;
        // boolean logic to update diode
        //TODO: ensure the diode order is from MSB to LSB, just like switch order from MSB to KSB in switch_diode_state
        for(auto k = 0; k < DIODE_SIZE; k++){  // Start from Diode1, then diode 2
            uint32_t diode_state_bit_ind = (DIODE_SIZE-1-k);
            uint32_t diode_state_mask = 1<<diode_state_bit_ind;

            // bool diode_is_on = (switch_diode_state &diode_state_mask);
            // bool impulse_is_positive = C1_DSW_mat_res[k] > 0;
            // bool diode_natural_is_positive = C1_DSW_mat_res[k+DIODE_SIZE] >0 ;
            // bool diode_next_is_positive =  C1_DSW_mat_res[k+2*DIODE_SIZE] > 0;
            
            // bool  impulse_is_negative = C1_DSW_mat_res[k] < 0;
            // bool diode_natural_is_negative = C1_DSW_mat_res[k+DIODE_SIZE] <0 ;
            // bool diode_next_is_negative =  C1_DSW_mat_res[k+2*DIODE_SIZE] < 0;

            // bool diode_is_on = (switch_diode_state &diode_state_mask);
            // bool impulse_is_positive = C1_DSW_mat_res[k*3] > 0;
            // bool diode_natural_is_positive = C1_DSW_mat_res[k*3+1] >0 ;
            // bool diode_next_is_positive =  C1_DSW_mat_res[k*3+2] > 0;
            
            // bool  impulse_is_negative = C1_DSW_mat_res[k*3] < 0;
            // bool diode_natural_is_negative = C1_DSW_mat_res[k*3+1] <0 ;
            // bool diode_next_is_negative =  C1_DSW_mat_res[k*3+2] < 0;


            int offset =   ((DIODE_SIZE-k-1)/5)*16 +   ((DIODE_SIZE-k-1)%5);

            bool diode_is_on = (switch_diode_state_debug &diode_state_mask);
            bool impulse_is_positive = C1_DSW_mat_res[offset] > 0;
            bool diode_natural_is_positive = C1_DSW_mat_res[offset+5] >0 ;
            bool diode_next_is_positive =  C1_DSW_mat_res[offset + 10] > 0;
            
            bool  impulse_is_negative = C1_DSW_mat_res[offset] < 0;
            bool diode_natural_is_negative = C1_DSW_mat_res[offset+5] <0 ;
            bool diode_next_is_negative =  C1_DSW_mat_res[offset+10] < 0;
            if(   (externalSwitchToggled &&   impulse_is_positive) // only when actual external switch toggleds
                  || ( !diode_is_on && diode_natural_is_positive && diode_next_is_positive  )   ){
                setBit( switch_diode_state_debug, diode_state_bit_ind, 1);
                std::cout << "turn on diode :" << k << std::endl;
                debug_diode_change=true;
            }
            else if(    (externalSwitchToggled && impulse_is_negative) 
                || (diode_is_on && diode_natural_is_negative && diode_next_is_negative)  ){
                setBit( switch_diode_state_debug, diode_state_bit_ind, 0);
                std::cout << "turn off diode : " << k <<std::endl;
                debug_diode_change=true;
            }
        }*/
        
        static_assert(DIODE_SIZE <= 30); // for now
        uint32_t impulse_mask = 0b11111;
        uint32_t natural_mask = impulse_mask<<5;
        uint32_t diode_next_mask  = natural_mask<< 5;
        
        // use 64 bit here
        uint32_t diode_impulse_gt_0 = 0x0;
        uint32_t diode_impulse_lt_0 = 0x0;
        uint32_t diode_natural_gt_0 = 0x0;
        uint32_t diode_natural_lt_0 = 0x0;
        uint32_t diode_next_lt_0 = 0x0;
        uint32_t diode_next_gt_0 = 0x0;
        uint32_t  switch_diode_state_old = switch_diode_state;
        for(uint32_t k = 0; k < BUFFER_SIZE_OF_C1_DSW_MAT_RES/ 16; k+=16 ){
            // first 5 is the impulse

            // next 5 is the diode's natural

            // last 5 is the diode's diode_next
            uint32_t gt_res =mask_greater_than_zero(&(C1_DSW_mat_res[k]));
            uint32_t lt_res = mask_less_than_zero(&(C1_DSW_mat_res[k]));

            uint32_t iteration_bit_shift = 5*k;

            diode_impulse_gt_0 |=  (gt_res&impulse_mask)<< iteration_bit_shift;
            diode_impulse_lt_0 |=  (lt_res&impulse_mask)<< iteration_bit_shift;

            diode_natural_gt_0 |=  (((gt_res&natural_mask) >> 5) &0x1F)  << iteration_bit_shift;
            diode_natural_lt_0 |=  (((lt_res&natural_mask) >> 5) &0x1F)<< iteration_bit_shift;

            diode_next_gt_0 |= (((gt_res&diode_next_mask) >> 10) &0x1F) << iteration_bit_shift;
            diode_next_lt_0 |= (((lt_res&diode_next_mask) >>10) & 0x1F) << iteration_bit_shift;
        }

        // // okay, now to bit masking to determine diode toggling and stuff son on
        // uint32_t external_switch_toggled_bits = externalSwitchToggled ? ~0u : 0u;
        // uint32_t  diode_state_only= switch_diode_state & ((1U << DIODE_SIZE) - 1); // assume bits from MSB->LSB is switchState, then DiodeState;
        //                                                                             // for example, S1, S2, D1, D2
    
        // // now bitwise logic for doing
        // uint32_t impulse_on_force = (external_switch_toggled_bits&diode_impulse_gt_0);
        // uint32_t impulse_off_force = (external_switch_toggled_bits&diode_impulse_lt_0);

        // uint32_t diode_off_to_on_soft = (~diode_state_only) & diode_natural_gt_0 & diode_next_gt_0;
        // uint32_t diode_on_to_off_soft = (diode_state_only) & diode_natural_lt_0 & diode_next_lt_0;

        // uint32_t diode_toggle_to_on = impulse_on_force | diode_off_to_on_soft;
        // uint32_t diode_toggle_to_off = impulse_off_force | diode_on_to_off_soft;

        // // do a sanity check first
        // assert(( diode_toggle_to_on & diode_toggle_to_off) == 0);

        // constexpr uint32_t DIODE_MASK = (1u << DIODE_SIZE) - 1;
        // // simply XOR the bits to set the diode state in switch_diode_state
        // switch_diode_state ^= ( (diode_toggle_to_on | diode_toggle_to_off) & DIODE_MASK );


        // diode_change = (switch_diode_state != switch_diode_state_old );

        // if( (diode_change != debug_diode_change) || (switch_diode_state_debug != switch_diode_state)){
        //     std::cout << "different at iteration i " << i <<std::endl;
        //     assert(false);
        // }

        diode_change  =diode_toggle_update2(
            externalSwitchToggled, switch_diode_state,
            diode_impulse_gt_0, diode_impulse_lt_0,
            diode_natural_gt_0, diode_natural_lt_0,
            diode_next_gt_0, diode_next_lt_0
        );
    

        if(printDebug){
            std::cout <<"diode change: " <<diode_change << std::endl;
        }
    
        // now x and y
        float * ABCD_mat = retrieveMatrixOffset(switch_diode_state,A_B_C_D_MATRIX_SIZE, ABCD_buffer); 

        matvec_row_major(ABCD_mat, x_and_u_cur,ABCD_mat_res,   A_B_C_D_ROW_SIZE, A_B_C_D_COL_SIZE );

        if(printDebug){
            std::cout << "ABCD_mat_res" << std::endl;
            print_matrix_column_major(ABCD_mat, A_B_C_D_ROW_SIZE, A_B_C_D_COL_SIZE);
            std::cout << "cur_x_u_res used for iteration" << std::endl;
            for(auto k = 0; k < BUFFER_SIZE_OF_CUR_X_U; k++){
                std::cout << x_and_u_cur[k] << " ";
            }
            std::cout << std::endl;
        }


        // update x_cur and also write y out to array
        memcpy( x_and_u_cur,  ABCD_mat_res, sizeof(float) *(STATE_SIZE)  );
        if( externalSwitchToggled  || !diode_change){
            // either exteranl swithc toggled or non diode soft switch changed
            //vector_add( ABCD_mat_res+STATE_SIZE_CEIL_TO_16,  cur_out, Y_SIZE  ); // vector additon of both the impulse and non-impulse response

            vector_add(ABCD_mat_res+STATE_SIZE_CEIL_TO_16, ABCD_mat_res+STATE_SIZE_CEIL_TO_16+Y_SIZE_CEIL_TO_16, cur_out, Y_SIZE );
            if(printDebug){std::cout << "USE both impulse and nonimpulse in output" << std::endl;}
        }else{
            memcpy(cur_out,  ABCD_mat_res+STATE_SIZE_CEIL_TO_16, sizeof(float) *(Y_SIZE)  );
            if(printDebug){std::cout << "USE only nonimpulrse in output" << std::endl;}
        }
        
        if(printDebug){
            std::cout << "cur_x_u_res after iteration" << std::endl;
            for(auto k = 0; k < STATE_SIZE; k++){
                std::cout << ABCD_mat_res[k] << " ";
            }
            std::cout << std::endl;

            std::cout << "nonimpulse output" << std::endl;
            for(auto k = 0; k < Y_SIZE; k++){
                std::cout << ABCD_mat_res[k+STATE_SIZE_CEIL_TO_16] << " ";
            }
            std::cout << std::endl;

            std::cout << "impulse output" << std::endl;
            for(auto k = 0; k < Y_SIZE; k++){
                std::cout << ABCD_mat_res[k+STATE_SIZE_CEIL_TO_16+Y_SIZE] << " ";
            }
            std::cout << std::endl;

            std::cout << "output after iteration" << std::endl;
            for(auto i = 0; i < Y_SIZE; i++){
                std::cout << cur_out[i] << " ";
            }
            std::cout << std::endl;

        }
        
        // writing stuff back for debugging purpose
        // memcpy(  C1_res_mask_Buffer+i*6, mask_res, 6*sizeof(uint32_t));
        *switch_diode_state_buffer_after_iteration++  = switch_diode_state;

    
        
    }
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
        // std::cout <<"iteration i: " << i <<std::endl;
        auto mat = formC1DSWMatrix(dataFromFile.switch_cases[i]);
        std::memcpy(C1_DSW_Buffer + C1_DSW_buffer_init_offset, mat.data(), mat.size() * sizeof(float));
        C1_DSW_buffer_init_offset += mat.size();
        assert(mat.size() == C1_DSW_MATRIX_SIZE);
        // std::cout <<"iteration i: finished" << i <<std::endl;
    }
    for (uint32_t i = 0; i < TOTAL_SWITCH_DIODE_STATE; i++)
    {   
        auto mat = formABCDMAtrix(dataFromFile.switch_cases[i]);
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


    // The input C1_DSWMatrix's row are order in the following method 
    //  switch_impulse  (number of diode)
    //  switch non_impulse (number of diode)
    // switch next (number of diode)

    // but in this function, it will reorder the matrix in the following method

    // switch impule(of diode 1)
    // switcch non impulse(of diode 1)
    // switch next (of diode 1)
    // do similar for diode2, diode3 .... 

    // C1_DSWMatrix.block( 0,0,  3*DIODE_SIZE,  (STATE_SIZE + U_SIZE)  ) = data.C1_DSW;

    uint32_t C1_DSW_row_size = data.C1_DSW.rows();
    uint32_t C1_DSW_col_size = data.C1_DSW.cols();

    // std::cout << "C1_DSW_dimensionts cols: " << C1_DSW_col_size << " rows: " << C1_DSW_row_size<< std::endl;
    uint32_t diod_ind = 0;
    // for(auto r = 0; r < 3*DIODE_SIZE; r+= 3){
        
    //     C1_DSWMatrix.block(r,    0,  1, STATE_SIZE+U_SIZE) = data.C1_DSW.row( diod_ind   );
    //     C1_DSWMatrix.block(r+1,    0,  1, STATE_SIZE+U_SIZE) = data.C1_DSW.row( diod_ind + DIODE_SIZE   );
    //     C1_DSWMatrix.block(r+2,    0,  1, STATE_SIZE+U_SIZE) = data.C1_DSW.row( diod_ind + DIODE_SIZE*2   );

    //     diod_ind ++;
    // } 

    //since 16/3 = 5 with remainder 1
    //Thus, for each 16 rows, it contains the Impulse, natural, diode_next of 5 diode with data arranged as

    // first 5 rows (Impulse of 5 diode)
    // second 5 rows (natural of 5 diode)
    // third 5 rows (diode_next of 5 diode)


    // in order to be consistent with diode order in tue externalSwitchDiodeState representation MSB -> LSB is Switch -> DIODE: EX s1, s2 D1, D2
    // row0, 5, 15 is diode 2 in thie case
    //row 1, 6, 16, is diode 1 in this case. In other words, transform it in reverse order 

    static_assert(  C1_DSW_ROW_SIZE/3 >= DIODE_SIZE);

    for(auto row = 0; row < C1_DSW_ROW_SIZE; row+=16){
        for(auto diode_count = 0; diode_count < 5; diode_count ++){
            if(diod_ind ==DIODE_SIZE){
                break; // no more diode available
            }    
            else{
                uint32_t row_offset = (  (DIODE_SIZE-diod_ind-1) /5)*16 + ((DIODE_SIZE-diod_ind-1) %5); // -1 because diod_ind start from 0
                C1_DSWMatrix.block(row_offset, 0, 1, STATE_SIZE+U_SIZE) = data.C1_DSW.row( diod_ind );
                C1_DSWMatrix.block(row_offset+5, 0, 1, STATE_SIZE+U_SIZE) = data.C1_DSW.row( diod_ind + DIODE_SIZE);
                C1_DSWMatrix.block(row_offset+10, 0, 1, STATE_SIZE+U_SIZE) = data.C1_DSW.row( diod_ind + DIODE_SIZE*2);                
                diod_ind ++;

            }

        }

    }


    return C1_DSWMatrix;
}

MatrixRowMajor formABCDMAtrix(SwitchCaseData &data)
{

    MatrixRowMajor ABCD = MatrixRowMajor::Zero(A_B_C_D_ROW_SIZE, A_B_C_D_COL_SIZE);


    // ABCD.block(0,0, 2*Y_SIZE+STATE_SIZE, STATE_SIZE+U_SIZE) = data.A_B_C_D_nonimp_imp;   
    // assert(data.x_next_with_dep_A.rows() == STATE_SIZE);
    // assert(data.x_next_with_dep_A.cols() == STATE_SIZE);
    // assert( data.x_next_with_dep_A.rows() == data.X_next_with_dep_B.rows() );


    // ABCD.block(0,0,  STATE_SIZE, STATE_SIZE+U_SIZE) = data.A_B_C_D_nonimp_imp;
    
    // For ease of computation, the rows of A_B_C_D are defined as
    // STATE_SIZE_CEIL_16 +Y_SIZE_CEIL_16 + Y_SIZE_CEIL_16
    for(uint32_t i = 0; i<  STATE_SIZE; i++){
        ABCD.block(i,0,  1, STATE_SIZE+U_SIZE) = data.A_B_C_D_nonimp_imp.row(i);  
    }

    for(uint32_t i = 0; i < Y_SIZE; i++){
        ABCD.block( STATE_SIZE_CEIL_TO_16+i, 0, 1, STATE_SIZE+U_SIZE )
            =  data.A_B_C_D_nonimp_imp.row(STATE_SIZE+i);
    }

    for(uint32_t i = 0; i < Y_SIZE; i++){
        ABCD.block(STATE_SIZE_CEIL_TO_16+Y_SIZE_CEIL_TO_16+i, 0, 1, STATE_SIZE+U_SIZE)
            = data.A_B_C_D_nonimp_imp.row(STATE_SIZE+Y_SIZE+i);
    }

    // for(uint32_t i = 0; i < 2*Y_SIZE; i++){
    //     ABCD.block( STATE_SIZE_CEIL_TO_16+i  ,0,  1, STATE_SIZE+U_SIZE)
    //      = data.A_B_C_D_nonimp_imp.row(STATE_SIZE + i);  
    // }

    return ABCD;

}





void writeDataToCsvFile(const std::string& filename, CircuitData & dataFromFile, float*output_buffer ){


    // now, write back to file


    std::ofstream myfile;

    myfile.open(filename);
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
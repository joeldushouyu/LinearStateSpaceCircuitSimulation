#ifndef LINEAR_CIRCUIT_KERNEL
#define LINEAR_CIRCUIT_KERNEL
#define NOCPP

#include <stdint.h>
#include <stdlib.h>
#include "common_macro.hpp"
#include <aie_api/aie.hpp>
#include <vector>
#include "circuitConfig.hpp"
#include "circuitSimCore.hpp"
#include <cstdlib>
#include <stdlib.h>      // <- This is necessary
#define MAX_SW_DIODE_SIZE 32



inline float* retrieveMatrixOFfsetBaseOnState(const uint32_t state, const int32_t matrix_size, float* matrix_ptr) {

    return  matrix_ptr + (state * matrix_size);
}




float * mv_16_row_with_STATE_U_SIZE_col_parallel(float * matrix,
    aie::vector<float, 16> *x_u_cur, aie::accum<accfloat, 16> &accum_temp){
    
    constexpr uint32_t loop_iter = U_SIZE+STATE_SIZE;
    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE( loop_iter / 2, loop_iter / 2)
    for(uint32_t col = 0; col+1 <loop_iter; col+=2 ){
        const uint32_t col_div_16 = col/16;
        const uint32_t col_mod_16 = col%16 ;         

        aie::vector<float, 16> a = aie::load_v<16>(matrix);
        matrix += 16; // next column
        aie::vector<float, 16>b= aie::broadcast<float, 16>(   (x_u_cur+col_div_16)->get(col_mod_16)  );
        // C_D_temp = mac_elem_16_accuracy_safe(a,b, C_D_temp,0,0,0  );

        const uint32_t col_div_16_2 = (col+1) / 16;
        const uint32_t col_mod_16_2 = (col+1) % 16;
        aie::vector<float, 16> a2 = aie::load_v<16>(matrix);
        matrix += 16; // next column
        aie::vector<float, 16>b2= aie::broadcast<float, 16>(   (x_u_cur+col_div_16_2)->get(col_mod_16_2)  );
        accum_temp = mac_elem_16_accuracy_safe(a2,b2,  mac_elem_16_accuracy_safe(a,b, accum_temp,0,0,0  ),0,0,0  );

    }
    #if (U_SIZE+STATE_SIZE)%2 == 1
        constexpr uint32_t last = (U_SIZE + STATE_SIZE) - 1;
        constexpr uint32_t col_div_16 = (last)/16;
        constexpr uint32_t col_mod_16 = (last)%16 ;         

        aie::vector<float, 16> a = aie::load_v<16>(matrix);
        matrix += 16; // next column
        aie::vector<float, 16>b= aie::broadcast<float, 16>(   (x_u_cur+col_div_16)->get(col_mod_16)  );
        accum_temp = mac_elem_16_accuracy_safe(a,b, accum_temp,0,0,0  );
    #endif

    return matrix;
}

template<uint32_t C1_RES_MASK_LEN>
void mult_with_C1_DSW(float *C1_DSW_mat, aie::vector<float, 16> *x_u_cur, uint32_t* c1_res_mask, 
    float*out // for debug
){

    static_assert(C1_RES_MASK_LEN == 6); // 6 uint32 if assume only 32 switch/diode
    
    constexpr uint32_t C1_DSW_ROW_SIZE_DIV_16 = C1_DSW_ROW_SIZE/16;
    static_assert (C1_RES_MASK_LEN >=C1_DSW_ROW_SIZE_DIV_16 );

    uint32_t c1_res_offset = 0;


    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE(C1_DSW_ROW_SIZE_DIV_16,C1_DSW_ROW_SIZE_DIV_16)    
    for(uint32_t row = 0; row < C1_DSW_ROW_SIZE_DIV_16; row++){

        aie::accum<accfloat, 16> C1_DSW_temp = aie::zeros<accfloat, 16>();

        C1_DSW_mat = mv_16_row_with_STATE_U_SIZE_col_parallel(
            C1_DSW_mat, x_u_cur, C1_DSW_temp
        );

        aie::mask<16> lt_res_mask = aie::lt< aie::vector<float, 16> , float>(  C1_DSW_temp ,0);
        aie::mask<16> gt_res_mask = aie::gt< aie::vector<float, 16> , float>(  C1_DSW_temp ,0);


        uint32_t impulse_mask = 0b11111;
        uint32_t natural_mask = impulse_mask<<5;
        uint32_t diode_next_mask  = natural_mask<< 5;
        
        uint32_t gt_res = gt_res_mask.to_uint32() & 0x0000FFFF;
        uint32_t lt_res = lt_res_mask.to_uint32() & 0x0000FFFF;
        uint32_t iteration_bit_shift = 5*row;

        c1_res_mask[0] |=  (gt_res&impulse_mask)<< iteration_bit_shift;
        c1_res_mask[1] |=  (lt_res&impulse_mask)<< iteration_bit_shift;

        c1_res_mask[2] |=  (((gt_res&natural_mask) >> 5) &0x1F)  << iteration_bit_shift;
        c1_res_mask[3] |=  (((lt_res&natural_mask) >> 5) &0x1F)<< iteration_bit_shift;

        c1_res_mask[4] |= (((gt_res&diode_next_mask) >> 10) &0x1F) << iteration_bit_shift;
        c1_res_mask[5] |= (((lt_res&diode_next_mask) >>10) & 0x1F) << iteration_bit_shift;
    }

}




template<uint32_t X_NEXT_BUFFER_SIZE>
void mult_with_A_B_To_Vector_Array(float *A_B_C_D_mat, aie::vector<float, 16> *x_u_cur,  aie::vector<float, 16> *x_next_res){
    static_assert(X_NEXT_BUFFER_SIZE == STATE_SIZE_CEIL_TO_16);
    constexpr uint32_t loop_iteration = STATE_SIZE_CEIL_TO_16/16;
    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE(loop_iteration, loop_iteration)
    for(uint32_t row = 0; row < loop_iteration; row++){
        aie::accum<accfloat, 16> ABtemp = aie::zeros<accfloat, 16>();
        A_B_C_D_mat = mv_16_row_with_STATE_U_SIZE_col_parallel(
            A_B_C_D_mat, 
            x_u_cur,
            ABtemp
        );


        *(x_next_res+row) = ABtemp.template to_vector<float>(); 
    }
}


template<uint32_t X_NEXT_BUFFER_SIZE>
void mult_with_A_B_To_Array(float *A_B_C_D_mat, aie::vector<float, 16> *x_u_cur, float *x_next_res){
    static_assert(X_NEXT_BUFFER_SIZE == STATE_SIZE_CEIL_TO_16);
    constexpr uint32_t loop_iteration = STATE_SIZE_CEIL_TO_16/16;
    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE(loop_iteration, loop_iteration)
    for(uint32_t row = 0; row < loop_iteration; row++){
        aie::accum<accfloat, 16> ABtemp = aie::zeros<accfloat, 16>();
        A_B_C_D_mat = mv_16_row_with_STATE_U_SIZE_col_parallel(
            A_B_C_D_mat, 
            x_u_cur,
            ABtemp
        );

        aie::store_v(x_next_res+16*row, ABtemp.template to_vector<float>());
    }
}

template<uint32_t X_U_cur_vector_size>
void update_x_u_cur_From_Array( aie::vector<float, 16> *x_u_cur, float *x_u_cur_res ){

    static_assert(STATE_SIZE_CEIL_TO_16/16 == X_U_cur_vector_size);
    //now rewrite the x_u_cur wit new value from iteration
    AIE_LOOP_UNROLL(X_U_cur_vector_size) 
    for(uint32_t i = 0; i< X_U_cur_vector_size; i++){
        (x_u_cur+i)->load(x_u_cur_res + 16* i);
    }

}


template<uint32_t X_U_cur_vector_size>
void update_x_u_cur_From_Vector_Array( aie::vector<float, 16> *x_u_cur, aie::vector<float, 16> *x_u_cur_res ){

    static_assert(STATE_SIZE_CEIL_TO_16/16 == X_U_cur_vector_size);
    //now rewrite the x_u_cur wit new value from iteration
    AIE_LOOP_UNROLL(X_U_cur_vector_size) 
    for(uint32_t i = 0; i< X_U_cur_vector_size; i++){
        *(x_u_cur+i) = *(x_u_cur_res+i);
    }

}


void mult_with_C_D_aligned_nonimpulse_only(float *C_D_mat, aie::vector<float, 16> *x_u_cur, float*out){

    static_assert(Y_SIZE_CEIL_TO_16%16 == 0);
    constexpr uint32_t num_of_iteration = Y_SIZE_CEIL_TO_16/16;

    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE( num_of_iteration, num_of_iteration)
    for(uint32_t row = 0; row < num_of_iteration; row++){
        aie::accum<accfloat, 16> C_D_temp = aie::zeros<accfloat, 16>();
           
        C_D_mat= mv_16_row_with_STATE_U_SIZE_col_parallel(
            C_D_mat, 
            x_u_cur,
            C_D_temp
        );
        // now write the result back to out, since only consider the non-impulse response result
        aie::store_v(out, C_D_temp.template to_vector<float>());    
        out += 16;
    }


}


void mult_with_C_D_aligned_nonimpulse_and_impulse(float *C_D_mat, aie::vector<float, 16> *x_u_cur, float*out){

    static_assert(Y_SIZE_CEIL_TO_16%16 == 0);
    constexpr uint32_t num_of_iteration = (2*Y_SIZE_CEIL_TO_16)/16;
    constexpr uint32_t Y_SIZE_CEIL_TO_16_DIV_16 = Y_SIZE_CEIL_TO_16/16;


    aie::vector<float, 16> C_D_nonimp_res [Y_SIZE_CEIL_TO_16_DIV_16];
    
    // loop one, write the c_D_nonimpulse result to C_D_nonimp_res
    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE( num_of_iteration/2, num_of_iteration/2)
    for(uint32_t row = 0; row < num_of_iteration/2; row++){
        event0();
        aie::accum<accfloat, 16> C_D_temp = aie::zeros<accfloat, 16>();
       
        
        C_D_mat = mv_16_row_with_STATE_U_SIZE_col_parallel(C_D_mat, x_u_cur, C_D_temp);

        C_D_nonimp_res[row] = C_D_temp.template to_vector<float>();
        event0();        
    }

    // another loop that calculdate C_D_impulse result
    // loop one, write the c_D_nonimpulse result to C_D_nonimp_res
    AIE_PREPARE_FOR_PIPELINING
    AIE_LOOP_RANGE( num_of_iteration/2, num_of_iteration/2)
    for(uint32_t row = 0; row < num_of_iteration/2; row++){
        event0();        
        aie::accum<accfloat, 16> C_D_temp = aie::zeros<accfloat, 16>();
        C_D_mat =  mv_16_row_with_STATE_U_SIZE_col_parallel(
            C_D_mat, 
            x_u_cur,
            C_D_temp
        );

        // do elementwise addition with C_D_nonimpulse_res and write back to output
        aie::vector<float, 16> res = aie::add(C_D_temp,  C_D_nonimp_res[row] );
        res.store(out);
        out+=16;
        event0();
    }
}



// Return true if externalSwitch toggled
bool update_x_u_cur_with_input(aie::vector<float, 16> *x_u_cur, float*in, uint32_t &externalSwitchDiodeStates){
    AIE_LOOP_UNROLL(U_SIZE)
    for(auto i = STATE_SIZE; i < U_SIZE+STATE_SIZE ; i++ ){
        

        x_u_cur[ i /16 ].set(*in, i%16);
        in++;
    } 

    uint32_t *in_as_uint32 = (uint32_t*)in;
    // update the Swtich diode status 
    bool toggled = !compare_and_copy_bits<uint32_t>(externalSwitchDiodeStates, *in_as_uint32, DIODE_SIZE, SWITCH_SIZE  );

    in++;
    return toggled;
}
#endif
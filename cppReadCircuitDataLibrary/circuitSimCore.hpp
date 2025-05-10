#ifndef CIRCUIT_SIM_CORE_HPP
#define CIRCUIT_SIM_CORE_HPP
// ideally, share with host and kernel
#include <stdlib.h>
#include <stdint.h>
#include <bitset>
#include "circuitConfig.hpp"
#include "common_macro.hpp"

#define CUSTOM_CEIL(x, mult) (((x) + (mult) - 1) / (mult) * (mult))

inline constexpr uint32_t custom_ceil(uint32_t x, uint32_t mult) {
  return ((x + mult - 1) / mult) * mult;
}




template <typename T>
T min(T a, T b) {
  return (a < b) ? a : b;
}

template <typename T>
T max(T a, T b) {
  return (a > b) ? a : b;
}
inline float* retrieveMatrixOffset(const uint32_t state, const int32_t matrix_size, float* matrix_ptr) {

  return  matrix_ptr + (state * matrix_size);
}


template <typename T>
bool compare_and_copy_bits(T& dst, T src, T pos, T num_bits) {
  static_assert( std::is_same<T, uint32_t >::value);
  // Create mask for the bit range
  uint32_t mask = ((1u << num_bits) - 1) << pos;

  // Extract masked bits from both src and dst
  bool bits_equal = (dst & mask) == (src & mask);

  // Set bits in dst to match src
  dst = (dst & ~mask) | (src & mask);

  return bits_equal;
}

// inline void setBit(uint32_t &num, uint8_t bitIndex, bool value) {
//   if (value) {
//       num |= (1U << bitIndex);  // Set the bit to 1
//   } else {
//       num &= ~(1U << bitIndex); // Clear the bit to 0
//   }
// }

inline void setBit(uint32_t &num, uint8_t bitIndex, bool value) {
  uint32_t mask = 1U << bitIndex;
  uint32_t vmask = 0 - static_cast<uint32_t>(value); // original idea, using cast
  num = (num & ~mask) | (vmask & mask);
}




// Extract 3 bits starting at bit_pos (0=LSB) in an N‑word buffer,
// where data[0] is the least-significant word and data[N-1] the most.
template <typename T, size_t N>
uint32_t extract_3bits_lsb_first(const T* data, T bit_pos) {
  static_assert( std::is_same<T, uint32_t >::value);
  const int total_bits = N * 32;

  // Which bit within the whole buffer:
  int offset = bit_pos;                 
  size_t word_idx = offset / 32;        // which uint32_t  
  int in_word_off = offset % 32;        // bit within that word (0=LSB…31=MSB)
  
  if (in_word_off <= 29) {
      // All 3 bits sit in data[word_idx]
      return (data[word_idx] >> in_word_off) & 0x7;
  } else {
      // They spill into the next word
      int bits_low  = 32 - in_word_off;   // how many in this word
      int bits_high = 3 - bits_low;       // rest from data[word_idx+1]
      uint32_t lo = (data[word_idx] >> in_word_off) & ((1U << bits_low) - 1);
      uint32_t hi = (data[word_idx+1] & ((1U << bits_high) - 1)) << bits_low;
      return lo | hi;
  }
}

inline bool diode_toggle_update2(bool externalSwitchToggled, uint32_t &switch_diode_state,
  const uint32_t  diode_impulse_gt_0, const uint32_t diode_impulse_lt_0,
  const uint32_t diode_natural_gt_0, const uint32_t diode_natural_lt_0,
  const uint32_t diode_next_gt_0, const uint32_t diode_next_lt_0
){
  uint32_t switch_diode_state_old = switch_diode_state;

  // okay, now to bit masking to determine diode toggling and stuff son on
  uint32_t external_switch_toggled_bits = externalSwitchToggled ? ~0u : 0u;
  uint32_t  diode_state_only= switch_diode_state & ((1U << DIODE_SIZE) - 1); // assume bits from MSB->LSB is switchState, then DiodeState;
                                                                              // for example, S1, S2, D1, D2

  // now bitwise logic for doing
  uint32_t impulse_on_force = (external_switch_toggled_bits&diode_impulse_gt_0);
  uint32_t impulse_off_force = (external_switch_toggled_bits&diode_impulse_lt_0);

  uint32_t diode_off_to_on_soft = (~diode_state_only) & diode_natural_gt_0 & diode_next_gt_0;
  uint32_t diode_on_to_off_soft = (diode_state_only) & diode_natural_lt_0 & diode_next_lt_0;

  uint32_t diode_toggle_to_on = impulse_on_force | diode_off_to_on_soft;
  uint32_t diode_toggle_to_off = impulse_off_force | diode_on_to_off_soft;

  // // do a sanity check first
  // assert(( diode_toggle_to_on & diode_toggle_to_off) == 0);

  constexpr uint32_t DIODE_MASK = (1u << DIODE_SIZE) - 1;
  // simply XOR the bits to set the diode state in switch_diode_state
  switch_diode_state ^= ( (diode_toggle_to_on | diode_toggle_to_off) & DIODE_MASK );


  return  (switch_diode_state != switch_diode_state_old );

}



template<uint32_t max_diode_switch_size, uint32_t C1_RES_MASK_SIZE>
bool diode_toggle_update( uint32_t &switch_diode_state, uint32_t *C1_res_mask, const  bool externalSwitchToggled ){
    static_assert(max_diode_switch_size == 32) ;// for now,assume now more than 32 switch and diode
    static_assert(C1_RES_MASK_SIZE == 6); 
    // given it only support max of 32 switch/diode
    // this means uint32_t can representas all switch/diode state

    // C1_RES_MASK_Size == 6 because
    // 3 uint32_t, where each uint32_t are for Diode_impulse, diode_natural, and diode_next
    // 2*3 because need status bit for Diode_impuse <0, diode_impulse>0, diode_natural <0, diode_natural > 0, diode_next <0 and >0
    

    // assuming of C1_res_mask
    // C1_res_mask[0-2] store gt_mask
    // C1_res_mask[3-5] store lt_mask

    // For example, for diode 1
    // bits 2-0 in C1_res_mask[0] stores the gt of diode_next, diode_natural, diode_impulse
    // bit 2-0 of C1_res_mask[3] store the lt of diode_next, diode_natural, diode_impulse
    bool diode_change = false;

    constexpr uint32_t  imp_mask = 0b001;
    constexpr uint32_t natural_mask = 0b010;
    constexpr uint32_t diode_next_mask = 0b100;

    
    #pragma clang  loop unroll(full)
    for(uint32_t k= 0; k <  DIODE_SIZE; k++){
        uint32_t start_bit = 3 * k;

        uint32_t gt_bits = extract_3bits_lsb_first<uint32_t,3>(C1_res_mask, start_bit); 
        uint32_t lt_bits = extract_3bits_lsb_first<uint32_t,3>(C1_res_mask+3, start_bit);


        uint32_t diode_state_bit_ind = (DIODE_SIZE-1-k);
        uint32_t diode_state_mask = 1<<diode_state_bit_ind;
        bool diode_is_on = (switch_diode_state &diode_state_mask);
        

        bool diode_imp_on = externalSwitchToggled && (imp_mask&gt_bits);
        bool diode_imp_off =  (externalSwitchToggled&&( imp_mask&lt_bits));
        // bool diode_soft_on = !diode_is_on && (natural_mask&gt_bits) &&(diode_next_mask&gt_bits);
        //bool diode_soft_off = diode_is_on &&( natural_mask&lt_bits) && (diode_next_mask &lt_bits  ) ;
        bool diode_soft_on = ((gt_bits & (natural_mask | diode_next_mask)) == (natural_mask | diode_next_mask)) &&!diode_is_on;        
        bool diode_soft_off = ((lt_bits & (natural_mask | diode_next_mask)) == (natural_mask | diode_next_mask)) && diode_is_on;

        if( diode_imp_on ||diode_soft_on
        ){
            setBit( switch_diode_state, diode_state_bit_ind, 1);
            diode_change=true;
        }else if(  diode_imp_off ||diode_soft_off
        ){
            setBit( switch_diode_state, diode_state_bit_ind, 0);
            diode_change=true;
        }
    }
    return diode_change;

}
#endif
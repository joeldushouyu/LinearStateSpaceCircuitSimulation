#include "circuiSimCore.hpp"



/**
 * @brief Compare and copy a specific bit range from src to dst.
 *
 * This function compares `num_bits` starting at bit position `pos`
 * between `dst` and `src`. If the bits are different, it updates
 * `dst` to match `src` in that range. The rest of `dst` remains unchanged.
 *
 * @param dst Reference to the destination 32-bit unsigned integer (will be modified).
 * @param src The source 32-bit unsigned integer (read-only).
 * @param pos The starting bit position (0 = least significant bit).
 * @param num_bits The number of bits to compare and copy.
 * 
 * @return true if the specified bits in `dst` were already equal to those in `src`,
 *         false if `dst` was modified.
 *
 * @note Bits are numbered from 0 (LSB) to 31 (MSB). Behavior is undefined
 *       if `pos + num_bits > 32`.
 */
bool compare_and_copy_bits(uint32_t& dst, uint32_t src, uint32_t pos, uint32_t num_bits) {
    // Create mask for the bit range
    uint32_t mask = ((1u << num_bits) - 1) << pos;

    // Extract masked bits from both src and dst
    bool bits_equal = (dst & mask) == (src & mask);

    // Set bits in dst to match src
    dst = (dst & ~mask) | (src & mask);

    return bits_equal;
}

void setBit(uint32_t &num, uint8_t bitIndex, bool value) {
    if (value) {
        num |= (1U << bitIndex);  // Set the bit to 1
    } else {
        num &= ~(1U << bitIndex); // Clear the bit to 0
    }
}


float* retrieveMatrixOffset(const uint32_t state, const int32_t matrix_size, float* matrix_ptr) {

    return  matrix_ptr + (state * matrix_size);
}

#ifndef CIRCUIT_SIM_CORE_HPP
#define CIRCUIT_SIM_CORE_HPP
#include <vector>
#include <string>
#include <map>
#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdint>
// ideally, share with host and kernel


float* retrieveMatrixOffset(const uint32_t state, const int32_t matrix_size, float* matrix_ptr);


bool compare_and_copy_bits(uint32_t& dst, uint32_t src, uint32_t pos, uint32_t num_bits);
void setBit(uint32_t &num, uint8_t bitIndex, bool value);

#endif
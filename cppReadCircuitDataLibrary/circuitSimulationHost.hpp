#ifndef CIRCUIT_SIMULATION_HOST_HPP
#define CIRCUIT_SIMULATION_HOST_HPP

// file with function specific for host verification

#include <cstring>  // for std::memcpy
#include <cstdlib>  // for std::malloc, std::free
#include <stdexcept>
//y= A * x (A is column-major matrix of size rows x cols)
void matvec_column_major(const float* A, const float* x, float* y, int rows, int cols);

void vector_add(const float* ptr, float* y, size_t length) ;

void print_matrix_column_major(const float* matrix, size_t rows, size_t cols) ;
#endif
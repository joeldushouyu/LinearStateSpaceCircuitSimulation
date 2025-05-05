#include "circuitSimulationHost.hpp"
#include <stdexcept>

#include <iostream>
#include <iomanip>

// Computes y = A * x (A is column-major matrix of size rows x cols)
void matvec_column_major(const float* A, const float* x, float* y, int rows, int cols) {
    // Initialize output to 0
    memset(y, 0, sizeof(float) * rows);

    for (int col = 0; col < cols; ++col) {
        float x_val = x[col];
        const float* col_ptr = A + col * rows;

        for (int row = 0; row < rows; ++row) {
            y[row] += col_ptr[row] * x_val;
        }
    }
}



void vector_add(const float* ptr, float* y, size_t length) {
    const float* a = ptr;             // First vector
    const float* b = ptr + length;    // Second vector

    for (size_t i = 0; i < length; ++i) {
        y[i] = a[i] + b[i];
    }
}



void print_matrix_column_major(const float* matrix, size_t rows, size_t cols) {
    for (size_t row = 0; row < rows; ++row) {
        for (size_t col = 0; col < cols; ++col) {
            // Column-major access
            std::cout << std::setw(8) << matrix[col * rows + row] << " ";
        }
        std::cout << std::endl;
    }
}

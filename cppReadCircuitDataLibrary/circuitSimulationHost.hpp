#ifndef CIRCUIT_SIMULATION_HOST_HPP
#define CIRCUIT_SIMULATION_HOST_HPP

// file with function specific for host verification

#include <cstring> // for std::memcpy
#include <cstdlib> // for std::malloc, std::free
#include <stdexcept>
#include "circuitSimulationHost.hpp"
#include "circuitData.hpp"
#include "circuiSimCore.hpp"
#include "circuitConfig.hpp"
#include <stdexcept>
#include <bitset>
#include <Eigen/Dense>
#include <iomanip> // for std::setprecision
#include <sstream> // for std::ostringstream
#include <iostream>
#include <cassert>
#include <iostream>
#include <iomanip>

using MatrixRowMajor = Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;
using MatrixColMajor = Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor>;

// y= A * x (A is column-major matrix of size rows x cols)
void matvec_column_major(const float *A, const float *x, float *y, int rows, int cols);

void vector_add(const float *ptr, float *y, size_t length);

void print_matrix_column_major(const float *matrix, size_t rows, size_t cols);

void iteration(float *C1_DSW_buffer, float *ABCD_buffer, float *input_buffers, float *output_buffers, std::vector<uint32_t> &switch_diode_state_reference);
void prepareDataForIteration(const char *fileName, CircuitData &dataFromFile, float *C1_DSW_Buffer, float *ABCD_buffer, float *input_buffers);
MatrixColMajor convertToColumnMajor(const MatrixRowMajor &input);
MatrixRowMajor expandWithBottomRightPadding(const MatrixRowMajor &input, int newRows, int newCols);
MatrixRowMajor formC1DSWMatrix(SwitchCaseData &data);
MatrixRowMajor formABCDMAtrix(SwitchCaseData &data);
void writeDataToCsvFile(const std::string &filename, CircuitData &dataFromFile, float *output_buffer);
#endif
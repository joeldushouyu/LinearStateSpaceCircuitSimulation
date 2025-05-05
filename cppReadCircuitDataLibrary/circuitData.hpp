
# ifndef CIRCUITDATA_HPP
#define CIRCUITDATA_HPP
#include <H5Cpp.h>
#include <Eigen/Dense>
#include <nlohmann/json.hpp>
#include <vector>
#include <string>
#include <map>
#include <cmath>
#include <iostream>

using json = nlohmann::json;
using MatrixRowMajor = Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

struct GeneralInfo
{
    int y_size;
    int u_size;
    int state_size;
    float iteration_frequency;
    int diode_size;
    int switch_size;
    float end_time;
    int iteration_step_number;
};


// Convert to JSON
inline void to_json(nlohmann::json& j, const GeneralInfo& info) {
    j = nlohmann::json{
        {"y_size", info.y_size},
        {"u_size", info.u_size},
        {"state_size", info.state_size},
        {"iteration_frequency", info.iteration_frequency},
        {"diode_size", info.diode_size},
        {"switch_size", info.switch_size},
        {"end_time", info.end_time},
        {"trace_size", 0},
        {"iteration_step_number", info.iteration_step_number}
    };
}

struct SwitchCaseData
{   
    MatrixRowMajor C1_DSW;
    MatrixRowMajor A_B_C_D_nonimp_imp;
    // MatrixRowMajor C_diode_impulse_sw;
    // MatrixRowMajor C_diode_natural_sw;
    // MatrixRowMajor D_diode_natural_sw;
    // MatrixRowMajor C_diode_explicit_der_mult_delta_t_sw;
    // MatrixRowMajor D_diode_explicit_der_mult_delta_t_sw;
    // MatrixRowMajor x_next_with_dep_A;
    // MatrixRowMajor X_next_with_dep_B;
    // MatrixRowMajor C_impulse;
    // MatrixRowMajor C_non_impulse;
    // MatrixRowMajor D_impulse;
    // MatrixRowMajor D_non_impulse;
};

void read_matrix(H5::Group &group, const std::string &dataset_name, MatrixRowMajor &matrix);

void read_vlen_string_dataset(H5::DataSet &dataset, std::vector<std::string> &result);

// Generic version (for float, uint32_t, etc.)
template <typename T_DATA>
void read_group_datasets(H5::H5File &file, const std::string &group_name,
                         std::map<std::string, std::vector<T_DATA>> &data_map) {
    H5::Group group = file.openGroup(group_name);
    hsize_t num_obj;
    H5Gget_num_objs(group.getId(), &num_obj);

    for (hsize_t i = 0; i < num_obj; ++i) {
        char name[1024];
        H5Gget_objname_by_idx(group.getId(), i, name, 1024);
        H5::DataSet dataset = group.openDataSet(name);
        H5::DataSpace dataspace = dataset.getSpace();

        int ndims = dataspace.getSimpleExtentNdims();
        if (ndims != 1) {
            throw std::runtime_error("Only 1D datasets are supported.");
        }

        hsize_t dims[1];
        dataspace.getSimpleExtentDims(dims);
        std::vector<T_DATA> buffer(dims[0]);

        if constexpr (std::is_same<T_DATA, float>::value) {
            dataset.read(buffer.data(), H5::PredType::NATIVE_FLOAT);
        } else if constexpr (std::is_same<T_DATA, uint32_t>::value) {
            dataset.read(buffer.data(), H5::PredType::NATIVE_UINT32);
        }else if constexpr (std::is_same<T_DATA, uint8_t>::value){
            dataset.read(buffer.data(), H5::PredType::NATIVE_UINT8);
        } 
        else {
            throw std::runtime_error("Unsupported data type in generic template");
        }

        data_map[std::string(name)] = std::move(buffer);
    }
}

// Generic version (for float, uint32_t, etc.)
template <typename T_DATA>
// Helper function to print time series data
void print_time_series(const std::map<std::string, std::vector<T_DATA>>& data, const std::string& title) {
    std::cout << "\n=== " << title << " ===" << std::endl;
    for (const auto& [key, values] : data) {
        std::cout << "Dataset: " << key << std::endl;
        std::cout << "Values: ";
        for (size_t i = 0; i < values.size(); ++i) {
            std::cout << values[i];
            if (i != values.size() - 1) std::cout << ", ";
            if (i > 10) {  // Limit output for large datasets
                std::cout << "... [truncated]";
                break;
            }
        }
        std::cout << std::endl;
    }
}







// Helper function to print time series data
void print_general_info(const GeneralInfo &info);
void print_labels(const std::vector<std::string> &labels, const std::string &title);
void print_matrix(const MatrixRowMajor &mat, const std::string &name);
void print_switch_case(const SwitchCaseData &data, const std::string &case_name);





class CircuitData
{
private:

public:

    std::map<uint32_t, SwitchCaseData> switch_cases;
    GeneralInfo general_info;

    std::map<std::string, std::vector<float>> u_record;
    std::vector<uint32_t> switch_diode_status_record;
    std::map<std::string, std::vector<uint32_t>> switch_record;
    std::vector<std::string> y_labels;
    std::vector<std::string> s_labels;    
    CircuitData();
    int initFromFile(const char *filename, bool print_data = false);
};




#endif
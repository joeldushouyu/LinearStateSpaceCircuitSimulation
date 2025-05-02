
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
};


// Convert to JSON
void to_json(nlohmann::json& j, const GeneralInfo& info) {
    j = nlohmann::json{
        {"y_size", info.y_size},
        {"u_size", info.u_size},
        {"state_size", info.state_size},
        {"iteration_frequency", info.iteration_frequency},
        {"diode_size", info.diode_size},
        {"switch_size", info.switch_size},
        {"end_time", info.end_time},
        {"trace_size", 0}
    };
}

struct SwitchCaseData
{
    MatrixRowMajor C_diode_impulse_sw;
    MatrixRowMajor C_diode_natural_sw;
    MatrixRowMajor D_diode_natural_sw;
    MatrixRowMajor C_diode_explicit_der_mult_delta_t_sw;
    MatrixRowMajor D_diode_explicit_der_mult_delta_t_sw;
    MatrixRowMajor x_next_with_dep_A;
    MatrixRowMajor X_next_with_dep_B;
    MatrixRowMajor C_impulse;
    MatrixRowMajor C_non_impulse;
    MatrixRowMajor D_impulse;
    MatrixRowMajor D_non_impulse;
};

void read_matrix(H5::Group &group, const std::string &dataset_name, MatrixRowMajor &matrix);

void read_vlen_string_dataset(H5::DataSet &dataset, std::vector<std::string> &result);

void read_group_datasets(H5::H5File &file, const std::string &group_name,
                         std::map<std::string, std::vector<float>> &data_map);

// Helper function to print time series data
void print_general_info(const GeneralInfo &info);
void print_labels(const std::vector<std::string> &labels, const std::string &title);
void print_matrix(const MatrixRowMajor &mat, const std::string &name);
void print_switch_case(const SwitchCaseData &data, const std::string &case_name);
void print_time_series(const std::map<std::string, std::vector<float>> &data, const std::string &title);




class CircuitData
{
private:

public:

    std::map<std::string, SwitchCaseData> switch_cases;
    GeneralInfo general_info;

    
    CircuitData();
    int initFromFile(const char *filename, bool print_data = false);
};




#endif
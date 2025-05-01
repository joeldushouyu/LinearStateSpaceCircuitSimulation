#include <highfive/H5File.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <filesystem>
#include <fstream>

using namespace HighFive;
namespace fs = std::filesystem;

void print_vector(const std::vector<float>& data, const std::string& label, size_t cols = 0) {
    std::cout << label << " (size = " << data.size() << "):\n";
    for (size_t i = 0; i < data.size(); ++i) {
        std::cout << std::setw(8) << data[i] << " ";
        if (cols && (i + 1) % cols == 0) std::cout << "\n";
    }
    std::cout << "\n";
}

int main() {
    std::string file_path = "Metadata.h5";  // replace with your actual path
    File file(file_path, File::ReadOnly);

    // --- Read metadata ---
    std::vector<std::string> y_labels;
    std::vector<std::string> s_labels;

    file.getDataSet("metadata/y_labels").read(y_labels);
    file.getDataSet("metadata/s_labels").read(s_labels);

    std::cout << "\n== y_labels ==\n";
    for (const auto& y : y_labels) std::cout << y << " ";
    std::cout << "\n== s_labels ==\n";
    for (const auto& s : s_labels) std::cout << s << " ";
    std::cout << "\n\n";

    // --- Loop over all switch cases ---
    size_t s_labels_size = s_labels.size();
    size_t total_cases = 1 << s_labels_size;

    std::vector<std::string> dataset_names = {
        "C_diode_impulse_sw", "C_diode_natural_sw", "D_diode_natural_sw",
        "C_diode_explicit_der_mult_delta_t_sw", "D_diode_explicit_der_mult_delta_t_sw",
        "x_next_with_dep_A", "X_next_with_dep_B",
        "C_impulse", "C_non_impulse", "D_impulse", "D_non_impulse"
    };
    for (size_t case_id = 0; case_id < total_cases; ++case_id) {
        std::string case_str;
        for (int bit = s_labels_size - 1; bit >= 0; --bit)
            case_str += ((case_id >> bit) & 1) ? '1' : '0';
    
        std::cout << "Saving case: " << case_str << "\n";
        fs::create_directory(case_str);  // Create folder for this case
    
        for (const auto& dname : dataset_names) {
            std::string full_path = case_str + "/" + dname;
    
            if (!file.exist(full_path)) {
                std::cerr << "Missing: " << full_path << "\n";
                continue;
            }
    
            DataSet ds = file.getDataSet(full_path);
            auto dims = ds.getSpace().getDimensions();
    
            if (dims.size() == 1) {
                std::vector<float> data;
                ds.read(data);
    
                std::ofstream fout(case_str + "/" + dname + ".txt");
                for (float val : data)
                    fout << val << " ";
                fout << "\n";
            } else if (dims.size() == 2) {
                std::vector<std::vector<float>> data;
                ds.read(data);
    
                std::ofstream fout(case_str + "/" + dname + ".csv");
                for (const auto& row : data) {
                    for (size_t j = 0; j < row.size(); ++j) {
                        fout << row[j];
                        if (j + 1 < row.size()) fout << ",";
                    }
                    fout << "\n";
                }
            } else {
                std::cerr << "Unsupported dataset dimensions: " << dims.size() << "\n";
            }
        }
    }
    

    return 0;
}

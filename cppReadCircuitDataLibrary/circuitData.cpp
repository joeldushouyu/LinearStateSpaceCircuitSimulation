

#include "circuitData.hpp"
// Function for reading data from H5 file


void read_matrix(H5::Group &group, const std::string &dataset_name, MatrixRowMajor &matrix) {
    H5::DataSet dataset = group.openDataSet(dataset_name);
    H5::DataSpace dataspace = dataset.getSpace();
    int ndims = dataspace.getSimpleExtentNdims();
    hsize_t dims[2];
    dataspace.getSimpleExtentDims(dims);

    // Read data into a temporary double buffer
    hsize_t num_elements = (ndims == 1) ? dims[0] : dims[0] * dims[1];
    std::vector<double> buffer(num_elements);
    dataset.read(buffer.data(), H5::PredType::NATIVE_DOUBLE);

    // Resize Eigen matrix and cast to float
    if (ndims == 1) {
        matrix.resize(dims[0], 1);
    } else {
        matrix.resize(dims[0], dims[1]);
    }
    for (hsize_t i = 0; i < num_elements; ++i) {
        matrix.data()[i] = static_cast<float>(buffer[i]);
    }
}

void read_vlen_string_dataset(H5::DataSet &dataset, std::vector<std::string> &result) {
    H5::DataType dtype = dataset.getDataType();
    H5::DataSpace dataspace = dataset.getSpace();

    // Get the number of elements in the dataset
    hsize_t size;
    dataspace.getSimpleExtentDims(&size);

    // Allocate a buffer of char* using std::vector (no raw new)
    std::vector<char*> rdata(size);

    // Read the dataset
    dataset.read(rdata.data(), dtype);

    // Convert each C-string to std::string
    result.resize(size);
    for (hsize_t i = 0; i < size; ++i) {
        result[i] = std::string(rdata[i]);
    }

    // Reclaim memory allocated by HDF5
    H5Dvlen_reclaim(dtype.getId(), dataspace.getId(), H5P_DEFAULT, rdata.data());
}

void read_group_datasets(H5::H5File &file, const std::string &group_name,
                         std::map<std::string, std::vector<float>> &data_map) {
    H5::Group group = file.openGroup(group_name);
    hsize_t num_obj;
    H5Gget_num_objs(group.getId(), &num_obj);
    for (hsize_t i = 0; i < num_obj; ++i) {
        char name[1024];
        H5Gget_objname_by_idx(group.getId(), i, name, 1024);
        H5::DataSet dataset = group.openDataSet(name);
        H5::DataSpace dataspace = dataset.getSpace();
        hsize_t dims[1];
        dataspace.getSimpleExtentDims(dims);

        // Read into double buffer and cast to float
        std::vector<double> buffer(dims[0]);
        dataset.read(buffer.data(), H5::PredType::NATIVE_DOUBLE);
        std::vector<float> data(dims[0]);
        for (hsize_t j = 0; j < dims[0]; ++j) {
            data[j] = static_cast<float>(buffer[j]);
        }
        data_map[std::string(name)] = data;
    }
}






// debug function to check if the data is correct


// Helper function to print GeneralInfo
void print_general_info(const GeneralInfo& info) {
    std::cout << "\n=== General Simulation Info ===" << std::endl;
    std::cout << "y_size: " << info.y_size << std::endl;
    std::cout << "u_size: " << info.u_size << std::endl;
    std::cout << "state_size: " << info.state_size << std::endl;
    std::cout << "iteration_frequency: " << info.iteration_frequency << " Hz" << std::endl;
    std::cout << "diode_size: " << info.diode_size << std::endl;
    std::cout << "switch_size: " << info.switch_size << std::endl;
    std::cout << "end_time: " << info.end_time << " seconds" << std::endl;
}

// Helper function to print labels
void print_labels(const std::vector<std::string>& labels, const std::string& title) {
    std::cout << "\n=== " << title << " ===" << std::endl;
    for (size_t i = 0; i < labels.size(); ++i) {
        std::cout << "[" << i << "] " << labels[i] << std::endl;
    }
}

// Helper function to print matrices
void print_matrix(const MatrixRowMajor& mat, const std::string& name) {
    std::cout << "\nMatrix: " << name << " (" << mat.rows() << "x" << mat.cols() << ")" << std::endl;
    std::cout << mat << std::endl;
}

// Helper function to print switch case data
void print_switch_case(const SwitchCaseData& data, const std::string& case_name) {
    std::cout << "\n==== Switch Case: " << case_name << " ====" << std::endl;
    print_matrix(data.C_diode_impulse_sw, "C_diode_impulse_sw");
    print_matrix(data.C_diode_natural_sw, "C_diode_natural_sw");
    print_matrix(data.D_diode_natural_sw, "D_diode_natural_sw");
    print_matrix(data.C_diode_explicit_der_mult_delta_t_sw, "C_diode_explicit_der_mult_delta_t_sw");
    print_matrix(data.D_diode_explicit_der_mult_delta_t_sw, "D_diode_explicit_der_mult_delta_t_sw");
    print_matrix(data.x_next_with_dep_A, "x_next_with_dep_A");
    print_matrix(data.X_next_with_dep_B, "X_next_with_dep_B");
    print_matrix(data.C_impulse, "C_impulse");
    print_matrix(data.C_non_impulse, "C_non_impulse");
    print_matrix(data.D_impulse, "D_impulse");
    print_matrix(data.D_non_impulse, "D_non_impulse");
}

// Helper function to print time series data
void print_time_series(const std::map<std::string, std::vector<float>>& data, const std::string& title) {
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




CircuitData::CircuitData() {
}
// class CircuitData
int CircuitData::initFromFile(const char* fileName,  bool print_data ) {

    try {
        H5::H5File file(fileName, H5F_ACC_RDONLY);

        // Read general_info
        H5::DataSet general_info_ds = file.openDataSet("json_data/general_info");
        H5::DataType dtype = general_info_ds.getDataType();
        std::string general_info_str;
        general_info_ds.read(general_info_str, dtype);
        json general_info_json = json::parse(general_info_str);
        


        
        this->general_info  = GeneralInfo{
            general_info_json["y_size"].get<int>(),
            general_info_json["u_size"].get<int>(),
            general_info_json["state_size"].get<int>(),
            general_info_json["iteration_frequency"].get<float>(),
            general_info_json["diode_size"].get<int>(),
            general_info_json["switch_size"].get<int>(),
            general_info_json["end_time"].get<float>()
        };


        // Read and print labels
        H5::DataSet y_labels_ds = file.openDataSet("metadata/y_labels");
        std::vector<std::string> y_labels;
        read_vlen_string_dataset(y_labels_ds, y_labels);


        H5::DataSet s_labels_ds = file.openDataSet("metadata/s_labels");
        std::vector<std::string> s_labels;
        read_vlen_string_dataset(s_labels_ds, s_labels);

        // Read and print switch cases
        const int total_switch_cases = pow(2, general_info.state_size);
        
        for (int case_num = 0; case_num < total_switch_cases; ++case_num) {
            std::string binary_str;
            for (int i = general_info.state_size - 1; i >= 0; --i) {
                binary_str.push_back((case_num & (1 << i)) ? '1' : '0');
            }

            if (!H5Lexists(file.getId(), binary_str.c_str(), H5P_DEFAULT)) continue;

            H5::Group case_group = file.openGroup(binary_str);
            SwitchCaseData data;
            
            read_matrix(case_group, "C_diode_impulse_sw", data.C_diode_impulse_sw);
            read_matrix(case_group, "C_diode_natural_sw", data.C_diode_natural_sw);
            read_matrix(case_group, "D_diode_natural_sw", data.D_diode_natural_sw);
            read_matrix(case_group, "C_diode_explicit_der_mult_delta_t_sw", data.C_diode_explicit_der_mult_delta_t_sw);
            read_matrix(case_group, "D_diode_explicit_der_mult_delta_t_sw", data.D_diode_explicit_der_mult_delta_t_sw);
            read_matrix(case_group, "x_next_with_dep_A", data.x_next_with_dep_A);
            read_matrix(case_group, "X_next_with_dep_B", data.X_next_with_dep_B);
            read_matrix(case_group, "C_impulse", data.C_impulse);
            read_matrix(case_group, "C_non_impulse", data.C_non_impulse);
            read_matrix(case_group, "D_impulse", data.D_impulse);
            read_matrix(case_group, "D_non_impulse", data.D_non_impulse);

            this->switch_cases[binary_str] = data;
        }


        // Read and print time series data
        std::map<std::string, std::vector<float>> u_record;
        read_group_datasets(file, "input_data", u_record);


        std::map<std::string, std::vector<float>> switch_diode_status_record;
        read_group_datasets(file, "state", switch_diode_status_record);


        std::map<std::string, std::vector<float>> switch_record;
        read_group_datasets(file, "switches", switch_record);


        if(print_data){

            print_general_info(general_info);

            print_labels(s_labels, "S Labels");
            print_labels(y_labels, "Y Labels");
            // Print switch cases
            for (const auto& [case_name, case_data] : switch_cases) {
                print_switch_case(case_data, case_name);
            }            

            print_time_series(u_record, "Input Data (u_record)");
            print_time_series(switch_diode_status_record, "Switch/Diode Status");
            print_time_series(switch_record, "Switch States");
        }

    } catch (H5::FileIException &e) {
        std::cerr << "HDF5 File Exception: " << e.getCDetailMsg() << std::endl;
        return 1;
    } catch (H5::DataSetIException &e) {
        std::cerr << "HDF5 DataSet Exception: " << e.getCDetailMsg() << std::endl;
        return 1;
    } catch (std::exception &e) {
        std::cerr << "Standard Exception: " << e.what() << std::endl;
        return 1;
    }

    return 0;

}
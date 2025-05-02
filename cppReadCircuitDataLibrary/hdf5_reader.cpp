#include <H5Cpp.h>
#include <Eigen/Dense>
#include <nlohmann/json.hpp>
#include <vector>
#include <string>
#include <map>
#include <cmath>
#include <iostream>
#include <fstream>
#include "circuitData.hpp"
using json = nlohmann::json;
using MatrixRowMajor = Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>;

    

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <hdf5_file>" << std::endl;
        return 1;
    }




    CircuitData dataFromFile = CircuitData();

    int ret = dataFromFile.initFromFile(argv[1], true);


    if (ret != 0) {
        std::cerr << "Error reading data from HDF5 file." << std::endl;
        return 1;
    }

    nlohmann::json j;
    to_json(j, dataFromFile.general_info);  // Explicit call

    std::ofstream file("config.json");
    file << j.dump(4); // Indent by 4 spaces
    file.close();

    std::cout << "Saved explicitly via to_json to general_info.json\n";



    // Now, the data is loaded into, run simulation at this momemnt?
    

    
}
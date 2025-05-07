# File: cppReadCircuitDataLibrary/Makefile

# Compiler and flags
CXX := g++

# Include directories
EIGEN_INCLUDE ?= /usr/include/eigen3
JSON_INCLUDE ?= /usr/include/nlohmann

# Compiler and linker flags
CXXFLAGS = -std=c++20 -g -O0 -Wall -Wextra -pedantic -march=native -ffast-math
CXXFLAGS += -I../highfive/include -I/usr/include/hdf5/serial -I$(EIGEN_INCLUDE) -I$(JSON_INCLUDE)
CXXFLAGS += -Wno-unused-variable -Wno-ignored-attributes
LDFLAGS = -L/usr/lib/x86_64-linux-gnu/hdf5/serial
LIBS = -lhdf5_cpp -lhdf5

# Precision define
PRECISION := -DEIGEN_DEFAULT_TO_ROW_MAJOR

# Source files
COMMON_SRC := circuitData.cpp  circuitSimulationHost.cpp # Replace with actual shared .cpp files
READER_SRC := hdf5_reader.cpp
TEST_SRC := test.cpp
SIM_SRC := circuitSimulation.cpp

# Object files
COMMON_OBJ := $(COMMON_SRC:.cpp=.o)
READER_OBJ := $(READER_SRC:.cpp=.o) $(COMMON_OBJ)
SIM_OBJ := $(SIM_SRC:.cpp=.o) $(COMMON_OBJ)
TEST_OBJ := $(TEST_SRC:.cpp=.o) $(COMMON_OBJ)
# Targets
HDF5_READER := hdf5_reader
SIMULATION_MAIN := simulation_main

.PHONY: all clean

all: $(HDF5_READER) $(SIMULATION_MAIN)

$(HDF5_READER): $(READER_OBJ)
	$(CXX) $(READER_OBJ) -o $@ $(LDFLAGS) $(LIBS)

$(SIMULATION_MAIN): $(SIM_OBJ)
	$(CXX) $(SIM_OBJ) -o $@ $(LDFLAGS) $(LIBS)
test_main: $(TEST_OBJ)
	$(CXX) $(TEST_OBJ) -o $@ $(LDFLAGS) $(LIBS)
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(PRECISION) -c $< -o $@

clean:
	rm -f $(HDF5_READER) $(SIMULATION_MAIN) *.o
	rm -f *.log
	rm -f *.json
	rm -f hostSim.csv
	rm -f *.txt
	rm -f npuSim.csv
	

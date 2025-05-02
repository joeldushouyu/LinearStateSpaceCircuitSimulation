# File: cppReadCircuitDataLibrary/Makefile
# Compiler and flags
CXX := g++

LDFLAGS = -L/usr/lib/x86_64-linux-gnu/hdf5/serial -lhdf5 -lhdf5_cpp
CXXFLAGS = -std=c++17  -g -O2 -Wall -Wextra -pedantic -march=native -ffast-math -I../highfive/include -I/usr/include/hdf5/serial
CXXFLAGS += -Wno-unused-variable -Wno-ignored-attributes # suppress warning about unused variables
LIBS := -lhdf5_cpp -lhdf5

# Adjust these paths according to your system
EIGEN_INCLUDE ?= /usr/include/eigen3
JSON_INCLUDE ?= /usr/include/nlohmann

# Source files
SRC := hdf5_reader.cpp circuitData.cpp

# Object files (derived from source files)
OBJ := $(SRC:.cpp=.o)

# Target executable
TARGET := hdf5_reader

# Default precision (already set to float in code)
PRECISION := -DEIGEN_DEFAULT_TO_ROW_MAJOR

all: $(TARGET)

# Rule to link object files into the target executable
$(TARGET): $(OBJ)
	$(CXX) $(OBJ) -o $@ $(LDFLAGS) $(LIBS)

# Rule to compile .cpp files into .o files
# This uses make's implicit rules for compiling .cpp to .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(PRECISION) $(INCLUDES) -I$(EIGEN_INCLUDE) -I$(JSON_INCLUDE) -c $< -o $@

clean:
	rm -f $(TARGET) $(OBJ)

.PHONY: all clean

CXX = g++
CXXFLAGS = -std=c++17 -I./highfive/include -I/usr/include/hdf5/serial -Wall -O2
LDFLAGS = -L/usr/lib/x86_64-linux-gnu/hdf5/serial -lhdf5 -lhdf5_cpp
TARGET = hdf5_reader
SRC = hdf5_reader.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f $(TARGET)

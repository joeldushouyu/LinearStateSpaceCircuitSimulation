
This project contain a state-space HIL(hardware-in-the-loop) Simulation



## Setup Procedure
1. Setup the [poetry environment](https://python-poetry.org/docs/basic-usage/) 
2. Do a git submodule
2. Run main.py  for pure python simulation
    There are few avaible circut-netlist in the main.py. By default, it will run a half-bridge-llc converter with a oversampling factor of x20.


## For running the npu code
1. source bash to [iron environment](https://github.com/Xilinx/mlir-aie)  NOTE: tested at c339bf8cd53d22ac7ec413bf298f5bab020e17d8 commit
2. cd to the cppReadCircuitDataLibrary and run make
```bash
# might need to run ubuntu_install.sh under cppReadCircuitDataLibrary
~/LinearStateSpaceCircuitSimulation/cppReadCircuitDataLibrary$ make hdf5_reader 
```
3. Run config on a file  
 Note: config_two_CT_no_bank_conflict_only.sh is for cached version, config_two_CT_no_cache.sh is for runtime fetching version
```bash
(ironenv) shouyud@shouyud-NucBox-EVO-X1:~/LinearStateSpaceCircuitSimulation/cppReadCircuitDataLibrary$ ./config_two_CT_no_bank_conflict_only.sh ../Metadata_half_bridge_llc_0.004.h5 
make: 'hdf5_reader' is up to date.
Successfully loaded the JSON data from 'config.json':
{'diode_size': 2, 'end_time': 0.004000000189989805, 'iteration_frequency': 2000000.0, 'iteration_step_number': 8000, 'state_size': 6, 'switch_size': 2, 'trace_size': 16384, 'u_size': 1, 'y_size': 14}
Total number of ping pong buffer:  8000

```
4. CD to the corresponding npu workfile
Note: twoCTPerCircuit is the cached version  and twoCTPerCircuitNoCache is the runtime fetching version
``` bash
(ironenv) shouyud@shouyud-NucBox-EVO-X1:~/LinearStateSpaceCircuitSimulation/NPUproject/twoCTPerCircuit$ make clean

make

make run
```
5. CD back to cppReadCircuitDataLibrary folder to run the C++ simulation under (Poerty environment, see the change in the python environment)
```bash
(non-package-mode-py3.12) shouyud@shouyud-NucBox-EVO-X1:~/LinearStateSpaceCircuitSimulation/cppReadCircuitDataLibrary$ make
 ./runSim.sh ../Metadata_half_bridge_llc_0.004.h5 


```



## Known Issue
Under some circumstances, the current implementation requires a much higher oversampling iteration frequency than other commercial software such as PLECS.
For example, for the full-bridge demo in main.py, the author noticed it requres a oversampling iteration frequency of x200 in order to have similar output from PLECS.
The authoer address the issue by adding 2 parallel capacitors with the 2 diodes in the circuit.


## TODO List
1. Refactor the code and documentation
2. Add more detail example in future
3. Finish the [technical document](./docs/AlgorithmDetail.pdf) that describe the algorithm.
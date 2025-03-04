
This project contain a state-space HIL(hardware-in-the-loop) Simulation



## Setup Procedure
1. Setup the [poetry environment](https://python-poetry.org/docs/basic-usage/) 
2. Run main.py 
    There are few avaible circut-netlist in the main.py. By default, it will run a half-bridge-llc converter with a oversampling factor of x20.

## Known Issue
Under some circumstances, the current implementation requires a much higher oversampling iteration frequency than other commercial software such as PLECS.
For example, for the full-bridge demo in main.py, the author noticed it requres a oversampling iteration frequency of x200 in order to have similar output from PLECS.
The authoer address the issue by adding 2 parallel capacitors with the 2 diodes in the circuit.


## TODO List
1. Refactor the code and documentation
2. Add more detail example in future
3. Finish the [technical document](./docs/AlgorithmDetail.pdf) that describe the algorithm.
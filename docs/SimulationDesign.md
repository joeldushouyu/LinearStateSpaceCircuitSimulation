## General overview
The general simulation topology is show ![below](../figure/Simulation%20Topology.png)

In this simulation framework, modules are arrange into directed acyclic graph(DAG) to reflect the message dependency between each modules. 

### System Clock Module
This module responsible for notify/updaing the simulation system clock to all other modules

### Switch PWM Output Module
This module outputs the switch states (On/OFF) of all external switches base on current simulation time and each switches' parameters.

### Voltage Current Source Module
This module outputs the voltage/current of all voltage/current source base on current simulation time and each voltage/source parameters.

### Switch OVersampling Module
In order to simulate/reflect the sampling issues that exist in realtime, Hardware-in-the-loop(HIL) simulation, this modules acts as a realtime sampler that samples the input switch signal at certain frequency.
By configuring the samples frequency carefully, user can observe how oversampling/undersampling affects the simuation.

### State Space Iteration Module
This module simulates the circuit based on the sampled switch states and the input voltage/current at each simulation iteration.

## Implementation detail
In order to preserve the message dependency shown in the picture, especially in future multi-thread use case, the message notification mechanism is implemented in [Observer Design Pattern](https://refactoring.guru/design-patterns/observer) using Python's [Priority Queue](https://docs.python.org/3/library/queue.html) module.
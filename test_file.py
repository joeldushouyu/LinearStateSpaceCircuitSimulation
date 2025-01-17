import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the state-space matrices
A = np.array([[-1000, 1], 
              [0, -1]])  # State matrix (stiff system)
B = np.array([[1], 
              [0]])      # Input matrix
C = np.array([[1, 0]])   # Output matrix
D = np.array([[0]])      # Feedthrough matrix

# Initial state vector
x0 = np.array([0, 0])  # Initial state

# Input vector (constant or time-varying)
u = np.array([1])  # Constant input

# Define the state-space dynamics
def state_space_dynamics(t, x):
    """
    Compute the derivative of the state vector.
    :param t: Time (not used in LTI systems, but required by the solver).
    :param x: Current state vector.
    :return: Derivative of the state vector.
    """
    dxdt = np.dot(A, x) + np.dot(B, u)
    return dxdt

# Time step and simulation duration
dt = 0.01  # Time step
t_end = 10.0  # End time

# Initialize arrays to store results
time_points = []
state_history = []
output_history = []

# Initialize the current state and time
x_current = x0
t_current = 0.0

# Perform step-by-step integration
while t_current < t_end:
    # Solve for one step using Radau IIA
    sol = solve_ivp(state_space_dynamics, [t_current, t_current + dt], x_current, method='Radau')

    # Update the current state and time
    x_current = sol.y[:, -1]  # Take the last state from the solution
    t_current += dt

    # Store results
    time_points.append(t_current)
    state_history.append(x_current)

    # Compute output
    y = np.dot(C, x_current) + np.dot(D, u)
    output_history.append(y)

# Convert results to NumPy arrays for easier analysis
time_points = np.array(time_points)
state_history = np.array(state_history)
output_history = np.array(output_history)

# Plot state trajectories
plt.figure()
for i in range(A.shape[0]):
    plt.plot(time_points, state_history[:, i], label=f'State {i+1}')
plt.xlabel('Time')
plt.ylabel('State')
plt.legend()
plt.title('State Trajectories (Radau IIA, Step-by-Step)')
plt.grid()
plt.show()

# Plot output trajectory
plt.figure()
plt.plot(time_points, output_history, label='Output')
plt.xlabel('Time')
plt.ylabel('Output')
plt.legend()
plt.title('Output Trajectory (Radau IIA, Step-by-Step)')
plt.grid()
plt.show()
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define system matrices
A = np.array([[7.60080475605129E-65, -0.0104347451790634],
              [0.0104347451790634, 7.60080475605129E-65]])
B = np.array([[1], [0]])
C = np.array([[1, 0]])
D = np.array([[0]])

# Function to perform one step of Radau integration
def radau_integration_step(x_cur: np.ndarray, A: np.ndarray, B: np.ndarray, u: np.ndarray, time_t: float, dt: float) -> np.ndarray:
    """
    Perform one step of numerical integration using Radau's method.

    Args:
        x_cur (np.ndarray): Current state vector (shape: (n,)).
        A (np.ndarray): System matrix (shape: (n, n)).
        B (np.ndarray): Input matrix (shape: (n, m)).
        u (np.ndarray): Input vector (shape: (m,)).
        time_t (float): Current time.
        dt (float): Time step size.

    Returns:
        np.ndarray: Updated state vector after one integration step (shape: (n,)).
    """
    def system_dynamics(t, x):
        return A @ x + B @ u

    t_span = (time_t, time_t + dt)
    sol = solve_ivp(system_dynamics, t_span, x_cur, method='Radau')
    return sol.y[:, -1]

# Simulation parameters
dt = 0.01  # Time step
T = 10  # Total simulation time
t = np.arange(0, T, dt)  # Time vector
x0 = np.array([1, 0])  # Initial state (flattened)
u = np.zeros((len(t), 1))  # Input vector (assuming zero input for simplicity)

# Initialize state and output arrays
x = np.zeros((len(A), len(t)))  # State vector over time
x[:, 0] = x0  # Set initial state
y = np.zeros((len(t), 1))  # Output vector over time

# Perform numerical integration using Radau's method
for i in range(1, len(t)):
    x[:, i] = radau_integration_step(x[:, i-1], A, B, u[i-1], t[i-1], dt)
    y[i] = C @ x[:, i].reshape(-1, 1) + D @ u[i]

# Plot results
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, x[0, :], label='State x1')
plt.plot(t, x[1, :], label='State x2')
plt.xlabel('Time')
plt.ylabel('State')
plt.legend()
plt.title('State Variables')

plt.subplot(2, 1, 2)
plt.plot(t, y, label='Output y')
plt.xlabel('Time')
plt.ylabel('Output')
plt.legend()
plt.title('System Output')

plt.tight_layout()
plt.show()
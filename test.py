# import numpy as np
# import matplotlib.pyplot as plt

# # Define the PWM function
# def pwm_at_time_t(pwm_frequency, pwm_ratio, time_t) -> bool:
#     if not (0.0 <= pwm_ratio <= 1.0):
#         raise ValueError("pwm_ratio must be between 0.0 and 1.0 inclusive.")
#     if pwm_frequency <= 0:
#         raise ValueError("pwm_frequency must be a positive number.")
    
#     period = 1 / pwm_frequency  # Period of the PWM signal
#     time_in_period = time_t % period  # Time within the current PWM period
#     high_duration = pwm_ratio * period  # Duration of the "high" state in one period

#     return time_in_period < high_duration

# # Parameters for the example
# frequency = 50  # 50 Hz
# duty_cycle = 0.6  # 60% duty cycle
# time_duration = 0.1  # Total time to simulate (in seconds)

# # Generate time points and PWM states
# time_points = np.linspace(0, time_duration, 1000)  # 1000 points within the duration
# pwm_states = [pwm_at_time_t(frequency, duty_cycle, t) for t in time_points]

# # Plot the PWM signal
# plt.figure(figsize=(10, 4))
# plt.plot(time_points, pwm_states, drawstyle='steps-pre', label="PWM Signal")
# plt.title(f"PWM Signal (Frequency: {frequency} Hz, Duty Cycle: {duty_cycle * 100:.1f}%)")
# plt.xlabel("Time (s)")
# plt.ylabel("State")
# plt.yticks([0, 1], ["Low", "High"])
# plt.grid(True, linestyle='--', alpha=0.6)
# plt.legend()
# plt.show()
def is_rise_edge(frequency, time_t) -> bool:
    """
    Determines if a rising edge of a square wave occurs at the given time.

    Parameters:
    - frequency (float): Frequency of the square wave in Hz.
    - time_t (float): Time in seconds to evaluate.

    Returns:
    - bool: True if the time corresponds to a rising edge, False otherwise.
    """
    if frequency <= 0:
        raise ValueError("frequency must be a positive number.")
    
    period = 1 / frequency  # Period of the square wave
    epsilon = 1e-9  # Tolerance for numerical precision issues
    
    # Determine if the time is an integer multiple of the period
    time_in_period = time_t % period
    return abs(time_in_period) < epsilon or abs(time_in_period - period) < epsilon
print(is_rise_edge(200, 0.015)) 
import pandas as pd
import matplotlib.pyplot as plt

def plot_diode_data(file1: str, file2: str):
    # Read the CSV files into pandas DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Create subplots for diode1 and diode2
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot diode1 data from both files
    ax1.plot(df1['time'], df1['diode1_map_value'], label='Diode 1 (File 1)', marker='o')
    ax1.plot(df2['time'], df2['diode1_map_value'], label='Diode 1 (File 2)', marker='x')
    ax1.set_title('Time vs Diode 1 Value')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Diode 1 Value')
    ax1.legend()
    ax1.grid(True)

    # Plot diode2 data from both files
    ax2.plot(df1['time'], df1['diode2_map_value'], label='Diode 2 (File 1)', marker='o')
    ax2.plot(df2['time'], df2['diode2_map_value'], label='Diode 2 (File 2)', marker='x')
    ax2.set_title('Time vs Diode 2 Value')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Diode 2 Value')
    ax2.legend()
    ax2.grid(True)

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()

# Example usage
file1 = 'csv_data/diode_switch_at_x30.csv'  # Replace with the path to your first CSV file
file2 = 'csv_data/diode_switch_at_x20.csv'  # Replace with the path to your second CSV file
plot_diode_data(file1, file2)
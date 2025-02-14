import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import pandas as pd
    
def plot_csv_columns(csv_file1, csv_file2, x_col1, y_col1, x_col2, y_col2, title=""):
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)

    # Extract the specified columns using iloc
    x1 = df1.iloc[:, x_col1].values  # Convert to numpy array
    y1 = df1.iloc[:, y_col1].values  # Convert to numpy array
    x2 = df2.iloc[:, x_col2].values  # Convert to numpy array
    y2 = df2.iloc[:, y_col2].values  # Convert to numpy array
    print(df1.columns)
    print(df2.columns)
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x1, y1, label=f"{df1.columns[x_col1]} vs {df1.columns[y_col1]} -Python simulation")
    plt.plot(x2, y2, label=f"{df2.columns[x_col2]} vs {df2.columns[y_col2]} -PLEC")

    # Add labels, title, and legend
    plt.xlabel( "Time [second]")
    plt.ylabel("Voltage/Current [V/A]")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()
    
def plot_csv_3columns(csv_file1, csv_file2, csv_file3, x_col1, y_col1, x_col2, y_col2, x_col3, y_col3, y1_label: str = "python", y2_label: str = "PLEC", y3_label: str = "PLEC-HIL", 
                     title: str = "", y_label: str = "", save_path: str = None):
    """Plot three columns from CSV with interactive checkboxes to show/hide lines.
    
    Parameters
    ----------
    csv_path : str
        Path to the CSV file containing the data
    y1_label : str, optional
        Label for first y-axis data, by default "y1"
    y2_label : str, optional
        Label for second y-axis data, by default "y2"
    y3_label : str, optional
        Label for third y-axis data, by default "y3"
    title : str, optional
        Plot title, by default ""
    y_label : str, optional
        Y-axis label, by default ""
    save_path : str, optional
        Path to save the plot, by default None
    """
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    df3 = pd.read_csv(csv_file3)
    # Read CSV file
    # Extract the specified columns using iloc
    x1 = df1.iloc[:, x_col1].values  # Convert to numpy array
    y1_data = df1.iloc[:, y_col1].values  # Convert to numpy array
    x2 = df2.iloc[:, x_col2].values  # Convert to numpy array
    y2_data = df2.iloc[:, y_col2].values  # Convert to numpy array
    x3 = df3.iloc[:, x_col3].values
    y3_data = df3.iloc[:, y_col3].values
    
    print(df1.columns)
    print(df2.columns)
    print(df3.columns)

    # Create the main figure and axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(30, 15))  # Specify 2 rows, 1 column
    plt.subplots_adjust(left=0.25)  # Make room for checkboxes
    
    # Plot all lines initially
    line1, = ax1.plot(x1, y1_data, 'b-', label=y1_label)
    line2, = ax1.plot(x2, y2_data, 'r-', label=y2_label)
    line3, = ax1.plot(x3, y3_data, 'g-', label=y3_label)
    
    # Calculate differences
    y_diff_hil = y1_data - y2_data[:len(y1_data)]
    y_diff_standard = y1_data - y3_data[:len(y1_data)]
    y3_y2_diff = y3_data - y2_data
    
    # Plot difference lines
    line_diff_hil, = ax2.plot(x1, y_diff_hil, 'c--', label=f'{y1_label}-{y2_label}')
    line_diff_standard, = ax2.plot(x1, y_diff_standard, 'm--', label=f'{y1_label}-{y3_label}')
    line_y3_y2, = ax2.plot(x3, y3_y2_diff, 'y--', label=f'{y3_label}-{y2_label}')
    
    # Create lines dictionary for easy reference
    lines = {
        y1_label: line1,
        y2_label: line2,
        y3_label: line3,
        f'{y1_label}-{y2_label}': line_diff_hil,
        f'{y1_label}-{y3_label}': line_diff_standard,
        f'{y3_label}-{y2_label}': line_y3_y2
    }
    
    # Set up check buttons
    rax = plt.axes([0.05, 0.4, 0.15, 0.3])  # Position of checkbox panel
    check = CheckButtons(
        ax=rax,
        labels=lines.keys(),
        actives=[True] * len(lines)  # All lines visible initially
    )
    
    def update_visibility(label):
        """Update line visibility when checkbox is clicked"""
        lines[label].set_visible(not lines[label].get_visible())
        plt.draw()
    
    # Connect callback function to check buttons
    check.on_clicked(update_visibility)
    
    # Set labels and title for first subplot (main signals)
    ax1.set_xlabel('Time')
    ax1.set_ylabel(y_label)
    ax1.set_title(f"{title} - Main Signals")
    ax1.grid(True)
    ax1.legend(loc='upper right')
    
    # Set labels and title for second subplot (differences)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Difference')
    ax2.set_title(f"{title} - Differences")
    ax2.grid(True)
    ax2.legend(loc='upper right')
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path)
    
    plt.show()  
# def plot_csv_3columns(csv_file1, csv_file2, csv_file3, x_col1, y_col1, x_col2, y_col2, x_col3, y_col3, title=""):
#     # Read the CSV files into DataFrames
#     df1 = pd.read_csv(csv_file1)
#     df2 = pd.read_csv(csv_file2)
#     df3 = pd.read_csv(csv_file3)
    
#     # Extract the specified columns using iloc
#     x1 = df1.iloc[:, x_col1].values  # Convert to numpy array
#     y1 = df1.iloc[:, y_col1].values  # Convert to numpy array
#     x2 = df2.iloc[:, x_col2].values  # Convert to numpy array
#     y2 = df2.iloc[:, y_col2].values  # Convert to numpy array
#     x3 = df3.iloc[:, x_col3].values
#     y3 = df3.iloc[:, y_col3].values
    
#     print(df1.columns)
#     print(df2.columns)
#     print(df3.columns)
    
#     # Create the main plot
#     plt.figure(figsize=(10, 12))
    
#     # Main plot
#     plt.subplot(2, 1, 1)  # 2 rows, 1 column, first subplot
#     plt.plot(x1, y1, label=f"{df1.columns[x_col1]} vs {df1.columns[y_col1]} - Python simulation")
#     plt.plot(x2, y2, label=f"{df2.columns[x_col2]} vs {df2.columns[y_col2]} - PLEC")
#     plt.plot(x3, y3, label=f"{df3.columns[x_col3]} vs {df3.columns[y_col3]} - PLEC-HIL")
#     plt.xlabel("Time [second]")
#     plt.ylabel("Voltage/Current [V/A]")
#     plt.title(title)
#     plt.legend()
#     plt.grid(True)
    
#     # Subplot for the difference between y1 and y2
#     plt.subplot(2, 1, 2)  # 2 rows, 1 column, second subplot
    
#     # Interpolate y2 to match the x1 values
#     # y2_interp = np.interp(x1, x2, y2)
    
#     # Calculate the difference
#     y_diff_from_hil = y1 - y3[:len(y1)]
#     y_diff_from_standard = y1-y2[:len(y1)]
#     # Plot the difference
#     plt.plot(x1, y_diff_from_hil, label="Difference (Python simulation - PLECHIL)", color='red')
#     plt.plot(x1, y_diff_from_standard, label="Difference (Python simulation - PLEC)", color='green')    
#     plt.plot(x2, y3-y2, label="Difference (PLEC-hil, PLEC)", color='blue')        
#     plt.xlabel("Time [second]")
#     plt.ylabel("Difference [V/A]")
#     plt.title("Difference between Python simulation and PLEC")
#     plt.legend()
#     plt.grid(True)
    
#     # Show the plot
#     plt.tight_layout()
#     plt.show()
    
def HalfBridgeComparsion2():
    
    # csv_file1 = "Half-bridge-llc-x30.csv"
    # csv_file2 = "half-bridge-plec-x30.csv"
    # csv_file3 = "half-bridge-plec-hil-x30.csv"
    
    csv_file1 = "Half-bridge-llc.csv"
    csv_file2 = "half-bridge-plec.csv"
    csv_file3 = "half-bridge-plec-hil.csv"
    
    
    x_col1 = 0
    x_col2 = 0
    x_col3 = 0
    
    #VSW 1
    y_col1 = 5
    y_col2=12
    y_col3=3
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VSs1"
                    )
    #VSW 2
    y_col1=6
    y_col2=13
    y_col3 = 4
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VSs2"
                    )
    # VS1
    y_col1 = 11  # Voltage: VMS1 (List 1)
    y_col2 = 3   # Vs1:Measured voltage (List 2)
    y_col3 = 8   # Vs1:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VS1"
                    )

    # VS2
    y_col1 = 13  # Voltage: VMS2 (List 1)
    y_col2 = 4   # Vs2:Measured voltage (List 2)
    y_col3 = 9   # Vs2:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VS2"
                    )

    # VML1
    y_col1 = 7   # Voltage: VML1 (List 1)
    y_col2 = 14  # VL1:Measured voltage (List 2)
    y_col3 = 5   # VL1:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VML1"
                    )

    # Vout
    y_col1 = 14  # Voltage: VMout (List 1)
    y_col2 = 1   # Vmout:Measured voltage (List 2)
    y_col3 = 2   # Vmout:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="Vout"
                    )

    # AML1
    y_col1 = 1   # Current: AML1 (List 1)
    y_col2 = 10  # AML1:Measured current (List 2)
    y_col3 = 14  # AML1:Measured current (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="AML1"
                    )

    # AMD1
    y_col1 = 2   # Current: AMD1 (List 1)
    y_col2 = 7   # AM_D1:Measured current (List 2)
    y_col3 = 12  # AM_D1:Measured current (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="AMD1"
                    )

    # AMD2
    y_col1 = 3   # Current: AMD2 (List 1)
    y_col2 = 8   # AM_D2:Measured current (List 2)
    y_col3 = 13  # AM_D2:Measured current (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="AMD2"
                    )

    # AMIout
    y_col1 = 4   # Current: AMIout (List 1)
    y_col2 = 11  # AMI0:Measured current (List 2)
    y_col3 = 1   # AMI0:Measured current (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="AMIout"
                    )

    # VMC1
    y_col1 = 8   # Voltage: VMC1 (List 1)
    y_col2 = 9   # VC1:Measured voltage (List 2)
    y_col3 = 6   # VC1:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VMC1"
                    )

    # VMp
    y_col1 = 9   # Voltage: VMp (List 1)
    y_col2 = 2   # Vp:Measured voltage (List 2)
    y_col3 = 7   # Vp:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VMp"
                    )

    # VMD1
    y_col1 = 10  # Voltage: VMD1 (List 1)
    y_col2 = 5   # VD1:Measured voltage (List 2)
    y_col3 = 10  # VD1:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VMD1"
                    )

    # VMS1
    y_col1 = 11  # Voltage: VMS1 (List 1)
    y_col2 = 3   # Vs1:Measured voltage (List 2)
    y_col3 = 8   # Vs1:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VMS1"
                    )

    # VMD2
    y_col1 = 12  # Voltage: VMD2 (List 1)
    y_col2 = 6   # VD2:Measured voltage (List 2)
    y_col3 = 11  # VD2:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VMD2"
                    )

    # VMS2
    y_col1 = 13  # Voltage: VMS2 (List 1)
    y_col2 = 4   # Vs2:Measured voltage (List 2)
    y_col3 = 9   # Vs2:Measured voltage (List 3)
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    title="VMS2"
                    )
# def HalfBridgeComparsion():
    
#     csv_file1 = "Half-bridge-llc.csv"
#     csv_file2 = "half-bridge-plec.csv"
#     csv_file3 = "halfBridgeMatlab.csv"
    
    
#     x_col1 = 0
#     x_col2 = 0
#     x_col3 = 0
    
#     y_col1 = 1
#     y_col2 = 2
#     y_col3 = 5
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="Vout"
#                       )
#     # y_col1 = 10
#     # y_col2 = 10
#     # y_col3 = 9
#     # plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#     #                   x_col1=x_col1, y_col1=y_col1,
#     #                   x_col2=x_col2, y_col2=y_col2,
#     #                   x_col3=x_col3, y_col3=y_col3,
#     #                   title="AML1"
#     #                   )
#     y_col1 = 2
#     y_col2 = 1
#     y_col3 = 10
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="AMD1"
                      
#                       )
#     y_col1 = 3
#     y_col2 = 13
#     y_col3 = 8
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="AMD2"
#                       )
#     y_col1 = 11
#     y_col2 = 1
#     y_col3 = 6
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="AMIout"
#                       )
    
#     y_col1 = 9
#     y_col2 = 6
#     y_col3 = 7
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="VMC1"
#                       )
#     y_col1 = 4
#     y_col2 = 7
#     y_col3 = 4
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="VMp"
#                       )
    
#     y_col1 = 7
#     y_col2 = 10
#     y_col3 = 11
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="VMD1"
#                       )
    
#     y_col1 = 5
#     y_col2 = 8
#     y_col3 = 2
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="VMS1"
#                       )
    
#     y_col1 = 8
#     y_col2 = 11
#     y_col3 = 1
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="VMD2"
#                       )
    
#     y_col1 = 6
#     y_col2 = 9
#     y_col3 = 3
#     plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
#                       x_col1=x_col1, y_col1=y_col1,
#                       x_col2=x_col2, y_col2=y_col2,
#                       x_col3=x_col3, y_col3=y_col3,
#                       title="VMS2"
#                       )
def FullBridgeComparsion():
    csv_file1 = "full-bridge-llc.csv"
    csv_file2 = "full-bridge-llc-plec.csv"
    csv_file3 = "fullBridgeMatlab.csv"
    
    
    x_col1 = 0
    x_col2 = 0
    x_col3 = 0
    
    y_col1 = 11
    y_col2 = 1
    y_col3 = 1
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                      x_col1=x_col1, y_col1=y_col1,
                      x_col2=x_col2, y_col2=y_col2,
                      x_col3=x_col3, y_col3=y_col3,
                      title="Vout"
                      )
    y_col1 = 8
    y_col2 = 10
    y_col3 = 3
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                      x_col1=x_col1, y_col1=y_col1,
                      x_col2=x_col2, y_col2=y_col2,
                      x_col3=x_col3, y_col3=y_col3,
                      title="VCr"
                      )
    y_col1 = 6
    y_col2 = 12
    y_col3 = 2
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                      x_col1=x_col1, y_col1=y_col1,
                      x_col2=x_col2, y_col2=y_col2,
                      x_col3=x_col3, y_col3=y_col3,
                      title="Io"
                      )
    y_col1 = 3
    y_col2 = 11
    y_col3 = 4
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3,
                      x_col1=x_col1, y_col1=y_col1,
                      x_col2=x_col2, y_col2=y_col2,
                      x_col3=x_col3, y_col3=y_col3,
                      title="ILr"
                      )
    
    
# file1 = "Half-bridge-llc-switch-only.csv"   
# file2 = "Half-bridge-llc-switch-only-plec.csv"

# x_col1 = 0
# x_col2 = 4
# y_col1 = 0
# y_col2 = 2
# plot_csv_columns(file1, file2, x_col1=x_col1, y_col1=x_col2, x_col2=y_col1, y_col2=y_col2, title="Vout")


# x_col1 = 0
# x_col2 = 1
# y_col1 = 0
# y_col2 = 3
# plot_csv_columns(file1, file2, x_col1=x_col1, y_col1=x_col2, x_col2=y_col1, y_col2=y_col2, title="AMRIN")


# x_col1 = 0
# x_col2 = 5
# y_col1 = 0
# y_col2 = 1
# plot_csv_columns(file1, file2, x_col1=x_col1, y_col1=x_col2, x_col2=y_col1, y_col2=y_col2, title="VML")

# x_col1 = 0
# x_col2 = 2
# y_col1 = 0
# y_col2 = 4
# plot_csv_columns(file1, file2, x_col1=x_col1, y_col1=x_col2, x_col2=y_col1, y_col2=y_col2, title="S1")

# x_col1 = 0
# x_col2 = 3
# y_col1 = 0
# y_col2 = 5
# plot_csv_columns(file1, file2, x_col1=x_col1, y_col1=x_col2, x_col2=y_col1, y_col2=y_col2, title="S2")
HalfBridgeComparsion2()
# FullBridgeComparsion()

# # # Example usage
# csv_file1 = "Half-bridge-llc.csv"
# csv_file2 = "half-bridge-plec.csv"
# x_col1 = 0  
# y_col1 = 9  
# x_col2 = 0  
# y_col2 = 1  

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "Vout")

# x_col1 = 0  
# y_col1 = 4
# x_col2 = 0  
# y_col2 = 2 

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "Vp")



# x_col1 = 0  
# y_col1 = 6
# x_col2 = 0  
# y_col2 = 3
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VS1")


# x_col1 = 0  
# y_col1 = 8
# x_col2 = 0  
# y_col2 = 4
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VS2")

# x_col1 = 0  
# y_col1 = 5
# x_col2 = 0  
# y_col2 = 5
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VD1")

# x_col1 = 0  
# y_col1 = 7
# x_col2 = 0  
# y_col2 = 6
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VD2")

# x_col1 = 0  
# y_col1 = 3
# x_col2 = 0  
# y_col2 = 9
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VC1")


# x_col1 = 0  
# y_col1 = 1
# x_col2 = 0  
# y_col2 = 7
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD1")

# x_col1 = 0  
# y_col1 = 2
# x_col2 = 0  
# y_col2 = 8
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD2")



# csv_file1 = "Three-winding-transformer-rc.csv"
# csv_file2 = "Three-winding-transformer-rc-plec.csv"
# x_col1 = 0  
# y_col1 = 8
# x_col2 = 0  
# y_col2 = 1  

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "Vmout")


# x_col1 = 0  
# y_col1 = 3
# x_col2 = 0  
# y_col2 = 4

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "Vp")

# x_col1 = 0  
# y_col1 = 5
# x_col2 = 0  
# y_col2 = 2

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "Vs1")

# x_col1 = 0  
# y_col1 = 7
# x_col2 = 0  
# y_col2 = 3

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "Vs2")

# x_col1 = 0  
# y_col1 = 1
# x_col2 = 0  
# y_col2 = 5

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD1")

# x_col1 = 0  
# y_col1 = 2
# x_col2 = 0  
# y_col2 = 6

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD2")




# # full bridge rectifier rc
# csv_file1 = "full-bridge-rectifier-rc.csv"
# csv_file2 = "full-bridge-rectifice-rc-plec.csv"
# x_col1 = 0  
# y_col1 = 1
# x_col2 = 0  
# y_col2 = 1  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AM1-source")
 
 
# x_col1 = 0  
# y_col1 = 2
# x_col2 = 0  
# y_col2 = 2  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD1")

# x_col1 = 0  
# y_col1 = 3
# x_col2 = 0  
# y_col2 = 3  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD4")

# x_col1 = 0  
# y_col1 = 4
# x_col2 = 0  
# y_col2 = 4  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD3")

# x_col1 = 0  
# y_col1 = 5
# x_col2 = 0  
# y_col2 = 5  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD2")

# x_col1 = 0  
# y_col1 = 6
# x_col2 = 0  
# y_col2 = 6  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMD1")

# x_col1 = 0  
# y_col1 = 7
# x_col2 = 0  
# y_col2 = 7  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMD4")

# x_col1 = 0  
# y_col1 = 8
# x_col2 = 0  
# y_col2 = 8  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMD3")

# x_col1 = 0  
# y_col1 = 9
# x_col2 = 0  
# y_col2 = 9  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMD2")

# x_col1 = 0  
# y_col1 = 10
# x_col2 = 0  
# y_col2 = 10 
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VM1-C1")

# x_col1 = 0  
# y_col1 = 11
# x_col2 = 0  
# y_col2 = 11 
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VM12-Rt")

# # # Example usage
# csv_file1 = "full-bridge-llc-simplified.csv"
# csv_file2 = "full-bridge-llc-simplified-plec.csv"
# x_col1 = 0  
# y_col1 = 5
# x_col2 = 0  
# y_col2 = 1  

# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMout")


# x_col1 = 0  
# y_col1 = 3
# x_col2 = 0  
# y_col2 = 2
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMD1")

# x_col1 = 0  
# y_col1 = 4
# x_col2 = 0  
# y_col2 = 3
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMD2")

# x_col1 = 0  
# y_col1 = 1
# x_col2 = 0  
# y_col2 = 4
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD1")

# x_col1 = 0  
# y_col1 = 2
# x_col2 = 0  
# y_col2 = 5
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD2")







# # # 
# csv_file1 = "full-bridge-llc-simplified.csv"
# csv_file2 = "full-bridge-llc-simplified-plec.csv"
# x_col1 = 0  
# y_col1 = 9
# x_col2 = 0  
# y_col2 = 1  
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMout")


# x_col1 = 0  
# y_col1 = 7
# x_col2 = 0  
# y_col2 = 2
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMD1")


# x_col1 = 0  
# y_col1 = 8
# x_col2 = 0  
# y_col2 = 3
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMD2")



# x_col1 = 0  
# y_col1 = 4
# x_col2 = 0  
# y_col2 = 4
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD1")


# x_col1 = 0  
# y_col1 = 5
# x_col2 = 0  
# y_col2 = 5
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMD2") 


# x_col1 = 0  
# y_col1 = 3
# x_col2 = 0  
# y_col2 = 6
# plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "AMLr") 
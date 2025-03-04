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
    
def plot_csv_4columns(csv_file1, csv_file2, csv_file3, csv_file4, x_col1, y_col1, x_col2, y_col2, x_col3, y_col3,  x_col4, y_col4,
                      file1_label: str = "python", file2_label: str = "PLEC", file3_label: str = "PLEC-HIL", file4_label:str="Matlab",
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
    df4 = pd.read_csv(csv_file4)
    # Read CSV file
    # Extract the specified columns using iloc
    x1 = df1.iloc[:, x_col1].values  # Convert to numpy array
    y1_data = df1.iloc[:, y_col1].values  # Convert to numpy array
    x2 = df2.iloc[:, x_col2].values  # Convert to numpy array
    y2_data = df2.iloc[:, y_col2].values  # Convert to numpy array
    x3 = df3.iloc[:, x_col3].values
    y3_data = df3.iloc[:, y_col3].values
    
    x4 = df4.iloc[:, x_col4].values
    y4_data = df4.iloc[:, y_col4].values
    
    
    print(df1.columns)
    print(df2.columns)
    print(df3.columns)
    print(df4.columns)

    # Create the main figure and axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(30, 15))  # Specify 2 rows, 1 column
    plt.subplots_adjust(left=0.25)  # Make room for checkboxes
    
    # Plot all lines initially
    line1, = ax1.plot(x1, y1_data, 'b-', label=file1_label)
    line2, = ax1.plot(x2, y2_data, 'r-', label=file2_label)
    line3, = ax1.plot(x3, y3_data, 'g-', label=file3_label)
    line4, = ax1.plot(x4, y4_data, 'y-', label=file4_label)
    # Calculate differences
    y_diff_hil = y1_data - y2_data[:len(y1_data)]
    y_diff_standard = y1_data - y3_data[:len(y1_data)]
    y3_y2_diff = y3_data - y2_data
    
    # Plot difference lines
    line_diff_hil, = ax2.plot(x1, y_diff_hil, 'c--', label=f'{file1_label}-{file2_label}')
    line_diff_standard, = ax2.plot(x1, y_diff_standard, 'm--', label=f'{file1_label}-{file3_label}')
    line_y3_y2, = ax2.plot(x3, y3_y2_diff, 'y--', label=f'{file3_label}-{file2_label}')
    
    # Create lines dictionary for easy reference
    lines = {
        file1_label: line1,
        file2_label: line2,
        file3_label: line3,
        file4_label: line4,
        f'{file1_label}-{file2_label}': line_diff_hil,
        f'{file1_label}-{file3_label}': line_diff_standard,
        f'{file3_label}-{file2_label}': line_y3_y2
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
def plot_csv_3columns(csv_file1, csv_file2, csv_file3, x_col1, y_col1, x_col2, y_col2, x_col3, y_col3, title=""):
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
    line1, = ax1.plot(x1, y1_data, 'b-', label=csv_file1)
    line2, = ax1.plot(x2, y2_data, 'r-', label=csv_file2)
    line3, = ax1.plot(x3, y3_data, 'g-', label=csv_file3)

    # Calculate differences
    y_diff_hil = y1_data - y2_data[:len(y1_data)]
    y_diff_standard = y1_data - y3_data[:len(y1_data)]
    y3_y2_diff = y3_data - y2_data
    
    # Plot difference lines
    line_diff_hil, = ax2.plot(x1, y_diff_hil, 'c--', label=f'{csv_file1}-{csv_file2}')
    line_diff_standard, = ax2.plot(x1, y_diff_standard, 'm--', label=f'{csv_file1}-{csv_file3}')
    line_y3_y2, = ax2.plot(x3, y3_y2_diff, 'y--', label=f'{csv_file3}-{csv_file2}')
    
    # Create lines dictionary for easy reference
    lines = {
        csv_file1: line1,
        csv_file2: line2,
        csv_file3: line3,
        f'{csv_file1}-{csv_file2}': line_diff_hil,
        f'{csv_file1}-{csv_file3}': line_diff_standard,
        f'{csv_file3}-{csv_file2}': line_y3_y2
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
    ax1.set_ylabel("Voltage/Current")
    ax1.set_title(f"{title} - Main Signals")
    ax1.grid(True)
    ax1.legend(loc='upper right')
    
    # Set labels and title for second subplot (differences)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Difference')
    ax2.set_title(f"{title} - Differences")
    ax2.grid(True)
    ax2.legend(loc='upper right')
    

    plt.show()  
    
def HalfBridgeComparsion2():
    
    # by default are all x20 oversampling factor
    csv_file1 = "csv_data/Half-bridge-llc.csv"
    csv_file2 = "csv_data/half-bridge-plec.csv"
    csv_file3 = "csv_data/half-bridge-plec-hil.csv"
    csv_file4 = "csv_data/halfBridgeMatlab.csv"
    # csv_file1 = "Half-bridge-llc-x30-parallel.csv"
    # csv_file2 = "half-bridge-plec-x30.csv"
    # csv_file3 = "half-bridge-plec-hil-x30.csv"
    # csv_file4 = "halfBridgeMatlab.csv"
    
    # csv_file1 = "Half-bridge-llc-x30.csv"
    # csv_file2 = "half-bridge-plec-x30.csv"
    # csv_file3 = "half-bridge-plec-hil-x30.csv"
    
    # csv_file1 = "Half-bridge-llc-x100.csv"
    # csv_file2 = "half-bridge-plec-x100.csv"
    # csv_file3 = "half-bridge-plec-hil-x100.csv"
    # csv_file4 = "halfBridgeMatlab.csv"
    
    x_col1 = 0
    x_col2 = 0
    x_col3 = 0
    x_col4 = 0
    #VSW 1
    y_col1 = 5
    y_col2=12
    y_col3=3
    y_col4 = 11
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VSs1"
                    )
    #VSW 2
    y_col1=6
    y_col2=13
    y_col3 = 4
    y_col4 = 5
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VSs2"
                    )
    # VS1
    y_col1 = 11  # Voltage: VMS1 (List 1)
    y_col2 = 3   # Vs1:Measured voltage (List 2)
    y_col3 = 8   # Vs1:Measured voltage (List 3)
    y_col4=2
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VS1"
                    )

    # VS2
    y_col1 = 13  # Voltage: VMS2 (List 1)
    y_col2 = 4   # Vs2:Measured voltage (List 2)
    y_col3 = 9   # Vs2:Measured voltage (List 3)
    y_col4= 3
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VS2"
                    )

    # VML1
    y_col1 = 7   # Voltage: VML1 (List 1)
    y_col2 = 14  # VL1:Measured voltage (List 2)
    y_col3 = 5   # VL1:Measured voltage (List 3)
    y_col4=6
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VML1"
                    )

    # Vout
    y_col1 = 14  # Voltage: VMout (List 1)
    y_col2 = 1   # Vmout:Measured voltage (List 2)
    y_col3 = 2   # Vmout:Measured voltage (List 3)
    y_col4=7
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="Vout"
                    )

    # AML1
    y_col1 = 1   # Current: AML1 (List 1)
    y_col2 = 10  # AML1:Measured current (List 2)
    y_col3 = 14  # AML1:Measured current (List 3)
    y_col4 = 12
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="AML1"
                    )

    # AMD1
    y_col1 = 2   # Current: AMD1 (List 1)
    y_col2 = 7   # AM_D1:Measured current (List 2)
    y_col3 = 12  # AM_D1:Measured current (List 3)
    y_col4= 13
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="AMD1"
                    )

    # AMD2
    y_col1 = 3   # Current: AMD2 (List 1)
    y_col2 = 8   # AM_D2:Measured current (List 2)
    y_col3 = 13  # AM_D2:Measured current (List 3)
    y_col4=10
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="AMD2"
                    )

    # AMIout
    y_col1 = 4   # Current: AMIout (List 1)
    y_col2 = 11  # AMI0:Measured current (List 2)
    y_col3 = 1   # AMI0:Measured current (List 3)
    y_col4 = 8
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="AMIout"
                    )

    # VMC1
    y_col1 = 8   # Voltage: VMC1 (List 1)
    y_col2 = 9   # VC1:Measured voltage (List 2)
    y_col3 = 6   # VC1:Measured voltage (List 3)
    y_col4 = 9
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VMC1"
                    )

    # VMp
    y_col1 = 9   # Voltage: VMp (List 1)
    y_col2 = 2   # Vp:Measured voltage (List 2)
    y_col3 = 7   # Vp:Measured voltage (List 3)
    y_col4 = 4
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VMp"
                    )

    # VMD1
    y_col1 = 10  # Voltage: VMD1 (List 1)
    y_col2 = 5   # VD1:Measured voltage (List 2)
    y_col3 = 10  # VD1:Measured voltage (List 3)
    y_col4 = 14
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VMD1"
                    )

    # VMS1
    y_col1 = 11  # Voltage: VMS1 (List 1)
    y_col2 = 3   # Vs1:Measured voltage (List 2)
    y_col3 = 8   # Vs1:Measured voltage (List 3)
    y_col4= 2
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VMS1"
                    )

    # VMD2
    y_col1 = 12  # Voltage: VMD2 (List 1)
    y_col2 = 6   # VD2:Measured voltage (List 2)
    y_col3 = 11  # VD2:Measured voltage (List 3)
    y_col4 = 1
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VMD2"
                    )

    # VMS2
    y_col1 = 13  # Voltage: VMS2 (List 1)
    y_col2 = 4   # Vs2:Measured voltage (List 2)
    y_col3 = 9   # Vs2:Measured voltage (List 3)
    y_col4 = 3
    plot_csv_4columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, csv_file4=csv_file4,
                    x_col1=x_col1, y_col1=y_col1,
                    x_col2=x_col2, y_col2=y_col2,
                    x_col3=x_col3, y_col3=y_col3,
                    x_col4=x_col4, y_col4=y_col4,
                    title="VMS2"
                    )

def FullBridgeComparsion():

    csv_file1 = "csv_data/full-bridge-llc-x30.csv"
    csv_file2 = "csv_data/Full-bridge-llc-simplified-hil-with-capacitorx30.csv"
    csv_file3 = "csv_data/Full-bridge-llc-simplified-hil-x30.csv"
    x_col1 = 0
    x_col2 = 0
    x_col3 = 0
    x_col4 = 0
    y_col1 = 11#9
    y_col2 = 1
    y_col3 = 1
    y_col4 = 1
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, x_col1=x_col1, y_col1=y_col1, x_col2=x_col2, y_col2=y_col2, x_col3=x_col3, y_col3=y_col3,title="Vout")
    # plot_csv_4columns(csv_file1=csv_file1,csv_file2=csv_file2,
    #                   csv_file3=csv_file3, csv_file4=csv_file4,
    #                   x_col1=x_col1, y_col1=y_col1,
    #                   x_col2=x_col2, y_col2=y_col2,
    #                   x_col3=x_col3, y_col3=y_col3,
    #                   x_col4=x_col4, y_col4=y_col4,
                      
    #                   )
    
    # y_col1 = 6
    # y_col2 = 12
    # y_col3 = 12
    # plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, x_col1=x_col1, y_col1=y_col1, x_col2=x_col2, y_col2=y_col2, x_col3=x_col3, y_col3=y_col3, title="Amout")

    y_col1 = 3
    y_col2 = 2
    y_col3 = 4#6
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, x_col1=x_col1, y_col1=y_col1, x_col2=x_col2, y_col2=y_col2, x_col3=x_col3, y_col3=y_col3, title="AMLR")    
    
    
    y_col1 = 9
    y_col2 = 0
    y_col3 = 2
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, x_col1=x_col1, y_col1=y_col1, x_col2=x_col2, y_col2=y_col2, x_col3=x_col3, y_col3=y_col3, title="VMD1")  
    y_col1 = 10
    y_col2 = 0
    y_col3 = 3
    plot_csv_3columns(csv_file1=csv_file1, csv_file2=csv_file2, csv_file3=csv_file3, x_col1=x_col1, y_col1=y_col1, x_col2=x_col2, y_col2=y_col2, x_col3=x_col3, y_col3=y_col3, title="VMD2")  

# HalfBridgeComparsion2()
FullBridgeComparsion()

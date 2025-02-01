import pandas as pd
import matplotlib.pyplot as plt

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
    plt.plot(x1, y1, label=f"{df1.columns[x_col1]} vs {df1.columns[y_col1]} (File 1)")
    plt.plot(x2, y2, label=f"{df2.columns[x_col2]} vs {df2.columns[y_col2]} (File 2)")

    # Add labels, title, and legend
    plt.xlabel("X-Axis")
    plt.ylabel("Y-Axis")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

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







# # 
csv_file1 = "full-bridge-llc.csv"
csv_file2 = "full-bridge-llc-plec.csv"
x_col1 = 0  
y_col1 = 9
x_col2 = 0  
y_col2 = 1  

plot_csv_columns(csv_file1, csv_file2, 0, y_col1, 0, y_col2, "VMout")



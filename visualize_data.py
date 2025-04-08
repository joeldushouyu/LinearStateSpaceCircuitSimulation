import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

def plot_csv_ncolumns(csv_files, x_cols, y_cols, labels=None,
                      title: str = "", y_label: str = "", save_path: str = None):
    """Plot N columns from CSV files with interactive checkboxes to show/hide lines.
    
    Parameters
    ----------
    csv_files : list of str
        List of paths to CSV files
    x_cols : list of int
        List of column indices for x-axis data (one per file)
    y_cols : list of int
        List of column indices for y-axis data (one per file)
    labels : list of str, optional
        Labels for each dataset (default: "Data 1", "Data 2", etc.)
    title : str, optional
        Plot title
    y_label : str, optional
        Y-axis label
    save_path : str, optional
        Path to save the plot
    """
    # Default labels if not provided
    if labels is None:
        labels = [f'Data {i+1}' for i in range(len(csv_files))]
    
    # Read all CSV files and extract data
    dfs = [pd.read_csv(f) for f in csv_files]
    x_data = [df.iloc[:, x_col].values for df, x_col in zip(dfs, x_cols)]
    y_data = [df.iloc[:, y_col].values for df, y_col in zip(dfs, y_cols)]
    
    # Print column names for debugging
    for i, df in enumerate(dfs):
        print(f"File {i+1} columns:", df.columns.tolist())
    
    # Create figure and axes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(30, 15))
    plt.subplots_adjust(left=0.25)
    
    # Plot all main lines
    lines = {}
    colors = plt.cm.tab10.colors  # Use a color cycle
    for i, (x, y, label) in enumerate(zip(x_data, y_data, labels)):
        lines[label], = ax1.plot(x, y, '-', color=colors[i % len(colors)], label=label)
    
    # Calculate and plot differences (all combinations)
    diff_lines = {}
    diff_colors = plt.cm.Set2.colors  # Different color cycle for differences
    color_idx = 0
    
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            # Ensure we're comparing arrays of the same length
            min_len = min(len(y_data[i]), len(y_data[j]))
            diff = y_data[i][:min_len] - y_data[j][:min_len]
            diff_label = f'{labels[i]}-{labels[j]}'
            diff_lines[diff_label], = ax2.plot(
                x_data[i][:min_len], diff, '--', 
                color=diff_colors[color_idx % len(diff_colors)],
                label=diff_label
            )
            color_idx += 1
    
    # Combine all lines for checkbox control
    all_lines = {**lines, **diff_lines}
    
    # Set up check buttons
    rax = plt.axes([0.05, 0.4, 0.15, 0.3])
    check = CheckButtons(
        ax=rax,
        labels=list(all_lines.keys()),
        actives=[True] * len(all_lines)
    )
    
    def update_visibility(label):
        """Update line visibility when checkbox is clicked"""
        all_lines[label].set_visible(not all_lines[label].get_visible())
        plt.draw()
    
    check.on_clicked(update_visibility)
    
    # Configure plot appearance
    ax1.set_xlabel('Time')
    ax1.set_ylabel(y_label)
    ax1.set_title(f"{title} - Main Signals")
    ax1.grid(True)
    ax1.legend(loc='upper right')
    
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Difference')
    ax2.set_title(f"{title} - Differences")
    ax2.grid(True)
    ax2.legend(loc='upper right')
    
    if save_path:
        plt.savefig(save_path)
    
    plt.show()
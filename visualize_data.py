import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons


import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
import numpy as np

def plot_csv_ncolumns_ieee(
    csv_files, x_cols, y_cols, labels=None,
    title: str = "", y_label: str = "", save_path: str = None
):
    """Plot N columns from CSV files, optimized for IEEE double-column format."""
    import matplotlib as mpl
    # Use Times New Roman if available
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif', 'serif']
    mpl.rcParams['mathtext.fontset'] = 'dejavuserif'
    mpl.rcParams['axes.unicode_minus'] = False

    if labels is None:
        labels = [f'Data {i+1}' for i in range(len(csv_files))]

    dfs = [pd.read_csv(f) for f in csv_files]
    x_data = [df.iloc[:, x_col].values for df, x_col in zip(dfs, x_cols)]
    y_data = [df.iloc[:, y_col].values for df, y_col in zip(dfs, y_cols)]

    ieee_colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    plt.rc('axes', prop_cycle=cycler(color=ieee_colors))

    fig, ax = plt.subplots(figsize=(3.45, 2.5))

    markers = ['o', 's', 'D', '^', 'v', 'X', 'P', '*']
    for i, (x, y, label) in enumerate(zip(x_data, y_data, labels)):
        ax.plot(
            x, y,
            label=label,
            linewidth=0.9,
            marker=markers[i % len(markers)],
            markersize=2.5,
            markevery=max(1, len(x) // 30),
            markerfacecolor='white',
            markeredgecolor=ieee_colors[i % len(ieee_colors)],
            markeredgewidth=0.7
        )

    ax.set_xlabel('Time (Second)', fontsize=8)
    ax.set_ylabel(y_label, fontsize=8)
    # No title for IEEE double column

    ax.grid(True, linestyle=':', alpha=0.5, linewidth=0.5, zorder=0)
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, 1.02),
        fontsize=7,
        frameon=False,
        ncol=2 if len(labels) > 3 else 1,
        labelspacing=0.2,
        columnspacing=1.0,
        handlelength=1.2,
        handletextpad=0.4,
        borderaxespad=0.2
    )

    ax.tick_params(axis='both', which='major', labelsize=8, width=0.7, length=2.5)
    ax.tick_params(axis='both', which='minor', labelsize=8, width=0.5, length=1.5)
    ax.minorticks_on()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.7)
    ax.spines['bottom'].set_linewidth(0.7)

    fig.tight_layout(pad=0.5)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', transparent=True)
        # Save a zoomed-in image from x=0.002 to x=0.0021
        x_min, x_max =0.002, 0.0021  #0,0.0001# 0.002, 0.0021
        ax.set_xlim(x_min, x_max)
        zoom_path = save_path.replace('.png', '_zoom.png') if save_path.endswith('.png') else save_path + '_zoom.png'
        # Save zoomed-in image at 1/4 size but with same font size
        orig_size = fig.get_size_inches()
        zoom_size = orig_size / 2.5  # 0.4 width and 0.4 height = 1/4 area
        fig.set_size_inches(zoom_size, forward=True)
        # Change x-axis to ms for zoomed-in image
        x_ticks = ax.get_xticks()
        ax.set_xticklabels([f"{(tick * 1e3):.2f}" for tick in x_ticks])
        ax.set_xlabel('Time (ms)', fontsize=8)
        # Remove legend for zoomed-in image
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
        plt.savefig(zoom_path, dpi=300, bbox_inches='tight', transparent=True)
        fig.set_size_inches(orig_size, forward=True)  # Restore original size
        ax.set_xlim(auto=True)  # Reset xlim for further use
        ax.set_xlabel('Time (Second)', fontsize=8)  # Restore label
    # plt.show()

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
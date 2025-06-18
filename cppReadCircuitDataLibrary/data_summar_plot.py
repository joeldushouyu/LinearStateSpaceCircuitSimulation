import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
def plot_box_with_stats(csv_path, title=None, output_path=None):
    """
    Create a row of box plots for each numeric column in a CSV file.
    The whiskers extend to the absolute min and max values, and
    annotated statistics (Min, 25th, Median, Mean, 75th, Max percentiles)
    are included on each plot.

    Parameters:
    - csv_path (str): Path to the CSV file.
    - title (str): Optional plot title.
    - output_path (str): Optional path to save the figure (e.g., 'plot.png').
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Select only numeric columns for plotting
    df_numeric = df.select_dtypes(include=[np.number])

    # Check if there's any numeric data to plot
    if df_numeric.empty:
        print(f"No numeric data found in {csv_path}. Skipping plot generation.")
        return

    # Limit to the first 4 numeric columns to avoid overly wide plots
    columns_to_plot = df_numeric.columns[:4]
    num_cols = len(columns_to_plot)

    # Increase the height of each box plot by setting a larger height in figsize
    fig, axes = plt.subplots(1, num_cols, figsize=(num_cols * 4, 10), sharey=False)

    # If there's only one column, axes will not be an array, so make it a list for consistent iteration
    if num_cols == 1:
        axes = [axes]

    # Set Seaborn style for better aesthetics
    sns.set(style="whitegrid", context="talk", font_scale=1.2)  # Increased font_scale

    # Define styles for the statistical markers including Min, Median, and Max
    stat_styles = {
        "Min": {"color": "blue"},
        "25%": {"color": "orange"},
        "Median": {"color": "teal"},
        "Mean": {"color": "red"},
        "75%": {"color": "purple"},
        "Max": {"color": "green"}
    }

    # Iterate through each column to create a box plot
    for i, column in enumerate(columns_to_plot):
        ax = axes[i] # Get the current subplot axis
        col_data = df_numeric[column].dropna() # Get data for the column, dropping NaN values

        # Create the box plot using seaborn
        # 'whis=(0, 100)' makes the whiskers extend to the 0th (min) and 100th (max) percentiles.
        # This effectively includes all data points and shows no outliers.
        sns.boxplot(y=col_data, ax=ax, color="lightgray", width=0.3, whis=(0, 100))

        # Compute the statistics to be annotated
        stats = {
            "Min": col_data.min(),
            "25%": col_data.quantile(0.25),
            "Median": col_data.median(),
            "Mean": col_data.mean(),
            "75%": col_data.quantile(0.75),
            "Max": col_data.max()
        }

        # Sort the stats by their value to maintain a consistent order for plotting markers
        sorted_stats = sorted(list(stats.items()), key=lambda item: item[1])

        # Initialize a list to store the y-positions of already placed annotations.
        # This helps in preventing overlaps by adjusting subsequent annotation positions.
        placed_annotations_y = []
        # Estimate text height as a small fraction of the y-axis range.
        # This is a heuristic to determine how much space each text annotation occupies vertically.
        text_height_estimate = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.03

        # Annotate all computed statistics on the plot
        for j, (label, value) in enumerate(sorted_stats):
            style = stat_styles[label]

            # Plot a marker for the statistic on the box plot
            ax.plot(0, value, 'o',
                    label=label,
                    markersize=7,
                    markeredgecolor='black',
                    markerfacecolor=style["color"])

            # Set the initial y position for the text annotation to the statistic's value
            text_y_position = value

            # Loop through previously placed annotations to check for and resolve overlaps.
            # If the current annotation's position is too close to a previous one,
            # its y-position is adjusted upwards to ensure visibility.
            for prev_y in placed_annotations_y:
                if abs(text_y_position - prev_y) < text_height_estimate:
                    text_y_position = prev_y + text_height_estimate * 1.2 # Adjust up with a buffer

            # Add the final adjusted y-position to the list of placed annotations
            placed_annotations_y.append(text_y_position)

            # Define horizontal alignment and a small x-offset for the text.
            # The text is aligned to the left and placed slightly to the right of the marker.
            h_align ='left'
            x_offset = 0.03

            # Add the text annotation to the plot.
            # The text includes the label and the formatted value,
            # with a bounding box for better readability against the plot background.
            ax.text(x_offset, text_y_position, f'{label}: {value:.4f}us',
                    verticalalignment='center', horizontalalignment=h_align, fontsize=14,
                    bbox=dict(boxstyle="round,pad=0.3", fc=style["color"], ec="black", lw=0.5, alpha=0.7))

        # Set the title and y-axis label for the current subplot.
        ax.set_title(f"Simulation {column} Second", fontsize=14)
        ax.set_ylabel("Per Iteration time (us)", fontsize=14)
        # Remove x-axis ticks as they are not relevant for single box plots.
        ax.set_xticks([])
        # Enable grid lines for better readability of values.
        ax.grid(True)
        # Set the font size for y-axis tick labels.
        ax.tick_params(axis='y', labelsize=14)

    # Adjust the layout to prevent titles and labels from overlapping across subplots.
    # The 'rect' parameter leaves a small space at the top for a potential overall figure title.
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Add a single legend to the last subplot if there are handles (i.e., markers with labels).
    # This centralizes the legend for all statistics displayed across the plots.
    handles, labels = axes[-1].get_legend_handles_labels()
    if handles:
        axes[-1].legend(
            handles, labels,
            loc='upper center',
            bbox_to_anchor=(0.8, 0.95), # Position the legend relative to the axes
            borderaxespad=0.2,
            title="Statistics",
            fontsize=14,
            title_fontsize=14,
            ncol=1, # Display legend items in a single column
            facecolor='lightgrey' # Set background color for the legend
        )

    # Adjust the overall figure size based on the number of columns to ensure adequate spacing.
    fig.set_size_inches(num_cols * 4, 10, forward=True)

    # Save the plot to a specified file path or display it.
    if output_path:
        plt.savefig(output_path, dpi=300) # Save with high DPI for better quality
        print(f"Saved plot to {output_path}")
    else:
        plt.show() # Display the plot

def plot_violin_with_stats(csv_path, title=None, output_path=None):
    """
    Create a row of violin plots for each numeric column in a CSV file.
    Only the rightmost plot includes annotated statistics with custom styling.

    Parameters:
    - csv_path (str): Path to the CSV file.
    - title (str): Optional plot title.
    - output_path (str): Optional path to save the figure (e.g., 'plot.png').
    """
    df = pd.read_csv(csv_path)
    df_numeric = df.select_dtypes(include=[np.number])

    if df_numeric.empty:
        print(f"No numeric data found in {csv_path}. Skipping.")
        return

    columns_to_plot = df_numeric.columns[:4]
    num_cols = len(columns_to_plot)

    fig, axes = plt.subplots(1, num_cols, figsize=(num_cols * 4, 6), sharey=False)
    if num_cols == 1:
        axes = [axes]

    sns.set(style="whitegrid", context="talk", font_scale=1.1)

    # Define style for markers
    stat_styles = {
        "Min": {"color": "blue"},
        "25%": {"color": "orange"},
        "Mean": {"color": "red"},
        "75%": {"color": "purple"},
        "Max": {"color": "green"}
    }

    for i, column in enumerate(columns_to_plot):
        ax = axes[i]
        col_data = df_numeric[column].dropna()

        sns.violinplot(y=col_data, ax=ax, inner=None, color="skyblue")

        # if i == num_cols - 1:
        stats = {
            "Min": col_data.min(),
            "25%": col_data.quantile(0.25),
            "Mean": col_data.mean(),
            "75%": col_data.quantile(0.75),
            "Max": col_data.max()
        }

        for label, value in stats.items():
            style = stat_styles[label]
            ax.plot(0, value, 'o',
                    label=label,
                    markersize=5,
                    markeredgecolor='black',
                    markerfacecolor=style["color"])

            ax.text(0.1, value, f'{label}: {value:.3f}us',
                    verticalalignment='center', horizontalalignment='left', fontsize=8)
        ax.set_title(f"{column} Second", fontsize=12)
        ax.set_ylabel("Value")
        ax.set_xticks([])
        ax.grid(True)

    plot_title = title or f"Violin Plot: {os.path.basename(csv_path)}"
    fig.suptitle(plot_title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Legend on the last subplot
    handles, labels = axes[-1].get_legend_handles_labels()
    if handles:
        axes[-1].legend(
            handles, labels,
            loc='upper center',           # Move legend to the top inside the axis
            bbox_to_anchor=(0.2, 0.99),   # Centered horizontally, near the top
            borderaxespad=0.2,
            title="Statistics",
            fontsize=9,
            title_fontsize=10,
            ncol=1                        # Single column for compactness
        )


    if output_path:
        plt.savefig(output_path, dpi=300)
        print(f"Saved plot to {output_path}")
    else:
        plt.show()






# plot_violin_with_stats("result_cachex100_low_nice.csv", "MatrixCachedVersion", "MatrixCachedViolinPlot.png" )
# plot_violin_with_stats("result_nocachex100_low_nice.csv", "MatrixNoCachedVersion", "MatrixNoCachedViolinPlot.png" )


# plot_violin_with_stats("result_cachex100_low_nice.csv", "MatrixCachedVersionNewDriver", "MatrixCachedNewDriverViolinPlot.png" )
# plot_violin_with_stats("result_nocachex100_low_nice.csv", "MatrixNoCachedVersionNewDriver", "MatrixNoCachedNewDriverViolinPlot.png" )


plot_box_with_stats("result_cachex100_low_nice_cur_driver.csv", "MatrixCachedVersion",  "MatrixCachedBoxPlot.png"  )

plot_box_with_stats( "result_nocachex100_low_nice_cur_driver.csv",  "MatrixNoCachedVersion", "MatrixNoCachedBoxPlot.png" )
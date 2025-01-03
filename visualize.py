import matplotlib.pyplot as plt
def on_pick(event, line_map, fig):
    line = event.artist
    xdata, ydata = line_map[line]
    ind = event.ind[0]  # Get the index of the selected point
    x, y = xdata[ind], ydata[ind]
    print(f"Selected point: x={x}, y={y}")
    # Optionally, add a marker or annotation at the clicked point
    ax = line.axes
    ax.annotate(f'({x:.2f}, {y:.2f})', xy=(x, y), xytext=(10, 10),
                textcoords='offset points', arrowprops=dict(arrowstyle='->'))
    fig.canvas.draw_idle()

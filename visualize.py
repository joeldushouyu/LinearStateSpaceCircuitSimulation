import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

# class DraggableWidget:
#     def __init__(self, widget):
#         self.widget = widget
#         self.press = None
#         self.background = None
#         # Connect event handlers to the canvas
#         self.cidpress = widget.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
#         self.cidrelease = widget.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
#         self.cidmotion = widget.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

#     def on_press(self, event):
#         if event.inaxes != self.widget.ax:
#             return
#         contains, _ = self.widget.ax.contains(event)
#         if not contains:
#             return
#         self.press = (self.widget.ax, event.x, event.y)
#         self.background = self.widget.ax.figure.canvas.copy_from_bbox(self.widget.ax.bbox)

#     def on_release(self, event):
#         self.press = None
#         self.background = None
#         self.widget.ax.figure.canvas.draw()

#     def on_motion(self, event):
#         if self.press is None:
#             return
#         if event.inaxes != self.widget.ax:
#             return
#         ax, xpress, ypress = self.press
#         dx = event.x - xpress
#         dy = event.y - ypress
#         ax.set_position([ax.get_position().x0 + dx / ax.figure.bbox.width,
#                          ax.get_position().y0 + dy / ax.figure.bbox.height,
#                          ax.get_position().width,
#                          ax.get_position().height])
#         self.widget.ax.figure.canvas.restore_region(self.background)
#         self.widget.ax.figure.canvas.blit(self.widget.ax.bbox)


# def on_pick(event, line_map, fig):
#     """
#     Event handler for mouse clicks on lines in a plot.
# `
#     Args:
#         event: The pick event triggered by a click.
#         line_map: A dictionary mapping line objects to their data.
#         fig: The matplotlib figure object.
#     """
#     line = event.artist
#     xdata, ydata = line_map[line]
#     ind = event.ind[0]  # Get the index of the selected point
#     x, y = xdata[ind], ydata[ind]
#     print(f"Selected point: x={x}, y={y}")
#     # Optionally, add a marker or annotation at the clicked point
#     ax = line.axes
#     ax.annotate(f'({x:.2f}, {y:.2f})', xy=(x, y), xytext=(10, 10),
#                 textcoords='offset points', arrowprops=dict(arrowstyle='->'))
#     fig.canvas.draw_idle()


# def toggle_visibility(label, line_map, fig):
#     """
#     Toggles the visibility of a line in a plot.

#     Args:
#         label: The label of the line to toggle.
#         line_map: A dictionary mapping line objects to their data.
#         fig: The matplotlib figure object.
#     """
#     for line in line_map:
#         if line.get_label() == label:
#             line.set_visible(not line.get_visible())
#     fig.canvas.draw_idle()
def on_pick(event, line_maps, fig):
    """
    Event handler for mouse clicks on lines in a plot.

    Args:
        event: The pick event triggered by a click.
        line_maps: A list of dictionaries mapping line objects to their data.
        fig: The matplotlib figure object.
    """
    line = event.artist

    # Search across all line maps for the clicked line
    for line_map in line_maps:
        if line in line_map:
            xdata, ydata = line_map[line]
            ind = event.ind[0]  # Get the index of the selected point
            x, y = xdata[ind], ydata[ind]
            print(f"Selected point: x={x}, y={y}")

            # Optionally, add a marker or annotation at the clicked point
            ax = line.axes
            ax.annotate(f'({x:.2f}, {y:.2f})', xy=(x, y), xytext=(10, 10),
                        textcoords='offset points', arrowprops=dict(arrowstyle='->'))
            fig.canvas.draw_idle()
            return  # Exit after handling the event
def toggle_visibility(label, line_maps, fig):
    """
    Toggles the visibility of a line in a plot.

    Args:
        label: The label of the line to toggle.
        line_maps: A list of dictionaries mapping line objects to their data.
        fig: The matplotlib figure object.
    """
    for line_map in line_maps:
        for line in line_map:
            if line.get_label() == label:
                line.set_visible(not line.get_visible())
    fig.canvas.draw_idle()

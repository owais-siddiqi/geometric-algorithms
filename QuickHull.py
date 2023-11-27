import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time


class QuickHullGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("QuickHull Convex Hull Finder")

        self.points = []
        self.convex_hull = []

        self.create_widgets()

    def create_widgets(self):
        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear_points)
        self.clear_button.pack(side=tk.BOTTOM)

        self.compute_button = tk.Button(self.master, text="Compute Convex Hull", command=self.compute_convex_hull)
        self.compute_button.pack(side=tk.BOTTOM)

        self.animating = False

    def clear_points(self):
        self.points = []
        self.convex_hull = []
        self.ax.clear()
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.canvas.draw()

    def on_click(self, event):
        if self.animating:
            return

        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            self.points.append((x, y))
            self.ax.plot(x, y, 'ro')
            self.canvas.draw()

    def compute_convex_hull(self):
        if self.animating or len(self.points) < 3:
            return

        self.animating = True
        self.compute_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)

        self.convex_hull = quick_hull(self.points, self.ax)
        self.plot_convex_hull()

    def plot_convex_hull(self):
        if not self.convex_hull:
            return

        hull_points = np.array(self.convex_hull + [self.convex_hull[0]])
        x, y = hull_points[:, 0], hull_points[:, 1]
        self.ax.plot(x, y, 'g-')
        self.canvas.draw()

        self.master.after(1000, self.restore_interface)

    def restore_interface(self):
        self.compute_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)
        self.animating = False


def quick_hull(points, ax):
    def get_orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or counterclockwise

    def hull_recursive(points, p, q, hull_set):
        max_dist = 0
        farthest_point = None
        for r in points:
            d = get_orientation(p, q, r)
            if d == 2:
                dist = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
                if dist > max_dist:
                    max_dist = dist
                    farthest_point = r

        if farthest_point is not None:
            hull_recursive(points, p, farthest_point, hull_set)
            hull_set.append(farthest_point)
            hull_recursive(points, farthest_point, q, hull_set)

            hull_points = np.array(hull_set + [hull_set[0]])
            x, y = hull_points[:, 0], hull_points[:, 1]
            ax.plot(x, y, 'g-')
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.figure.canvas.draw()
            time.sleep(0.5)

    points.sort()
    if len(points) < 3:
        return points

    hull = []
    hull.append(points[0])
    hull.append(points[-1])

    upper_hull = []
    lower_hull = []
    for point in points:
        orientation = get_orientation(hull[0], hull[-1], point)
        if orientation == 2:
            upper_hull.append(point)
        elif orientation == 1:
            lower_hull.append(point)

    hull_recursive(upper_hull, hull[0], hull[-1], hull)
    hull_recursive(lower_hull, hull[-1], hull[0], hull)

    return hull


def main():
    root = tk.Tk()
    app = QuickHullGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

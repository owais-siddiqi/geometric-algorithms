import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np

class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull using Graham Scan")

        self.points = []
        self.convex_hull = []

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()

        self.info_label = tk.Label(root, text="Click on the canvas to add points.")
        self.info_label.pack()

        self.plot_button = tk.Button(root, text="Plot Convex Hull", command=self.plot_convex_hull)
        self.plot_button.pack()

        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)

    def on_canvas_click(self, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            self.points.append((x, y))
            self.ax.plot(x, y, 'bo')
            self.canvas.draw()

    def plot_convex_hull(self):
        if len(self.points) < 3:
            self.info_label.config(text="At least 3 points are required.")
            return

        self.info_label.config(text="Calculating Convex Hull...")
        self.convex_hull = self.graham_scan(self.points)

        self.ax.clear()
        self.ax.plot(*zip(*self.points), 'bo', label='Points')
        self.ax.plot(*zip(*self.convex_hull, self.convex_hull[0]), 'r-', label='Convex Hull')
        self.ax.legend()
        self.canvas.draw()

        self.info_label.config(text="Convex Hull Plotted.")

    def graham_scan(self, points):
        def ccw(p1, p2, p3):
            return (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])

        points.sort()
        upper_hull = []
        for p in points:
            while len(upper_hull) >= 2 and ccw(upper_hull[-2], upper_hull[-1], p) <= 0:
                upper_hull.pop()
            upper_hull.append(p)

        lower_hull = []
        for p in reversed(points):
            while len(lower_hull) >= 2 and ccw(lower_hull[-2], lower_hull[-1], p) <= 0:
                lower_hull.pop()
            lower_hull.append(p)

        return upper_hull[:-1] + lower_hull[:-1]


if __name__ == "__main__":
    root = tk.Tk()
    app = ConvexHullApp(root)
    root.mainloop()

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import sys

class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull using Jarvis March")
        self.root.geometry("600x600")  # Set initial window size

        self.points = []
        self.convex_hull = []

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])

        self.canvas.draw()

        self.info_label = tk.Label(root, text="Click on the canvas to add points.", bg="#f0f0f0", pady=10)
        self.info_label.pack()

        self.plot_button = tk.Button(root, text="Plot Convex Hull", command=self.plot_convex_hull, bg="#4caf50", fg="white")
        self.plot_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset, bg="#ff5722", fg="white")
        self.reset_button.pack(pady=5)

        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)

        root.protocol("WM_DELETE_WINDOW", self.close_window)

    def on_canvas_click(self, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            self.points.append((x, y))
            self.ax.plot(x, y, 'bo')
            self.update_plot_limits()
            self.canvas.draw()

    def update_plot_limits(self):
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])

    def plot_convex_hull(self):
        if len(self.points) < 3:
            self.info_label.config(text="At least 3 points are required.", fg="red")
            return

        self.info_label.config(text="Calculating Convex Hull...", fg="black")
        self.convex_hull = self.jarvis_march(self.points)

        self.ax.clear()
        self.ax.plot(*zip(*self.points), 'bo', label='Points')
        self.ax.legend()
        self.update_plot_limits()
        self.canvas.draw()

        self.draw_edges_one_by_one(0)

    def draw_edges_one_by_one(self, index):
        if index < len(self.convex_hull):
            edge_start = self.convex_hull[index]
            edge_end = self.convex_hull[(index + 1) % len(self.convex_hull)]

            self.ax.plot([edge_start[0], edge_end[0]], [edge_start[1], edge_end[1]], 'r-')
            self.canvas.draw()

            self.root.after(1000, self.draw_edges_one_by_one, index + 1)
        else:
            self.info_label.config(text="Convex Hull Plotted.", fg="green")

    def jarvis_march(self, points):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            return 0 if val == 0 else 1 if val > 0 else 2

        n = len(points)
        if n < 3:
            return points

        hull = []
        l = min(range(n), key=lambda i: (points[i][1], points[i][0]))

        p = l
        while True:
            hull.append(points[p])
            q = (p + 1) % n
            for i in range(n):
                if orientation(points[p], points[i], points[q]) == 2:
                    q = i
            p = q
            if p == l:
                break

        return hull

    def reset(self):
        self.root.after_cancel(self.root.after_id) if hasattr(self.root, 'after_id') else None
        self.points = []
        self.convex_hull = []
        self.ax.clear()
        self.info_label.config(text="Click on the canvas to add points.", fg="black")
        self.canvas.draw()

    def close_window(self):
        self.root.after_cancel(self.root.after_id) if hasattr(self.root, 'after_id') else None
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvexHullApp(root)
    root.mainloop()

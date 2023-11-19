import tkinter as tk
import math

class ConvexHullApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Convex Hull - Jarvis March")
        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="white")
        self.canvas.pack()

        self.points = []
        self.convex_hull = []

        self.canvas.bind("<Button-1>", self.add_point)
        self.btn_compute_hull = tk.Button(self.master, text="Compute Convex Hull", command=self.compute_convex_hull)
        self.btn_compute_hull.pack()

        self.btn_reset = tk.Button(self.master, text="Reset Graph", command=self.reset_graph)
        self.btn_reset.pack()

        # Draw x and y axes
        self.canvas.create_line(50, 350, 550, 350, width=2)  # x-axis
        self.canvas.create_line(50, 350, 50, 50, width=2)     # y-axis

        # Label x-axis
        for i in range(0, 550, 50):
            self.canvas.create_text(50 + i, 355, text=str(i), anchor="n")

        # Label y-axis
        for i in range(0, 300, 50):
            self.canvas.create_text(45, 350 - i, text=str(i), anchor="e")

    def add_point(self, event):
        x, y = event.x, event.y

        # Check if the point is within the bounds of the graph
        if 50 <= x <= 550 and 50 <= y <= 350:
            # Add new point to the list
            self.points.append((x, y))

            # Draw x and y axes
            self.canvas.create_line(50, 350, 550, 350, width=2)  # x-axis
            self.canvas.create_line(50, 350, 50, 50, width=2)     # y-axis

            # Label x-axis
            for i in range(0, 550, 50):
                self.canvas.create_text(50 + i, 355, text=str(i), anchor="n")

            # Label y-axis
            for i in range(0, 300, 50):
                self.canvas.create_text(45, 350 - i, text=str(i), anchor="e")

            # Draw convex hull (if available)
            self.draw_convex_hull()

            # Draw all points
            for x, y in self.points:
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")


    def compute_convex_hull(self):
        # Clear canvas
        self.canvas.delete("all")

        if len(self.points) < 3:
            # Draw x and y axes
            self.canvas.create_line(50, 350, 550, 350, width=2)  # x-axis
            self.canvas.create_line(50, 350, 50, 50, width=2)     # y-axis

            # Label x-axis
            for i in range(0, 550, 50):
                self.canvas.create_text(50 + i, 355, text=str(i), anchor="n")

            # Label y-axis
            for i in range(0, 300, 50):
                self.canvas.create_text(45, 350 - i, text=str(i), anchor="e")

            # Draw all points
            for x, y in self.points:
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
        else:
            self.convex_hull = self.jarvis_march(self.points)
            self.draw_convex_hull()

    def draw_convex_hull(self):
        if not self.convex_hull:
            return

        # Draw x and y axes
        self.canvas.create_line(50, 350, 550, 350, width=2)  # x-axis
        self.canvas.create_line(50, 350, 50, 50, width=2)     # y-axis

        # Label x-axis
        for i in range(0, 550, 50):
            self.canvas.create_text(50 + i, 355, text=str(i), anchor="n")

        # Label y-axis
        for i in range(0, 300, 50):
            self.canvas.create_text(45, 350 - i, text=str(i), anchor="e")

        # Draw remaining points
        for x, y in self.points:
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

        # Draw convex hull with labels and connect the last and first points
        for i, point in enumerate(self.convex_hull):
            x, y = point
            label = f"{i + 1}"
            self.canvas.create_text(x, y - 10, text=label, anchor="s", fill="blue")
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")

            if i > 0:
                prev_point = self.convex_hull[i - 1]
                self.canvas.create_line(prev_point, point, fill="blue")

        # Connect the last and first points
        first_point = self.convex_hull[0]
        self.canvas.create_line(self.convex_hull[-1], first_point, fill="blue")



    def jarvis_march(self, points):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # colinear
            return 1 if val > 0 else 2  # clock or counterclockwise

        n = len(points)
        if n < 3:
            return []

        hull = []

        # Find the leftmost point
        l = min(range(n), key=lambda x: points[x][0])

        p = l
        q = 0
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

    def reset_graph(self):
        # Clear canvas and reset points and convex hull
        self.canvas.delete("all")
        self.points = []
        self.convex_hull = []

        # Draw x and y axes
        self.canvas.create_line(50, 350, 550, 350, width=2)  # x-axis
        self.canvas.create_line(50, 350, 50, 50, width=2)     # y-axis

        # Label x-axis
        for i in range(0, 550, 50):
            self.canvas.create_text(50 + i, 355, text=str(i), anchor="n")

        # Label y-axis
        for i in range(0, 300, 50):
            self.canvas.create_text(45, 350 - i, text=str(i), anchor="e")


def main():
    root = tk.Tk()
    app = ConvexHullApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
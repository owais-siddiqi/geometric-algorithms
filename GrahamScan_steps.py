import tkinter as tk
from tkinter import ttk
import math

class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convex Hull Visualization")

        self.points = []

        self.canvas = tk.Canvas(root, width=700, height=700, bg="#001F3F", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.calculate_button = ttk.Button(root, text="Calculate Convex Hull", command=self.calculate_convex_hull)
        self.calculate_button.pack(pady=5)

        self.reset_button = ttk.Button(root, text="Reset Graph", command=self.reset_graph)
        self.reset_button.pack(pady=5)

        self.canvas.bind("<Button-1>", self.add_point)

        self.draw_axes()

    def add_point(self, event):
        x, y = event.x, 700 - event.y  # Invert the Y-coordinate
        if 50 <= x <= 650 and 50 <= 700 - y <= 650:  # Bounds to prevent points outside the canvas
            new_point = (x, 700 - y)  # Invert the Y-coordinate for storing in the points list
            self.points.append(new_point)
            self.redraw_canvas()

    def redraw_canvas(self):
        # Clear previous points and lines
        self.canvas.delete("all")
        self.draw_axes()
        self.draw_points()

    def draw_axes(self):
        for i in range(50, 701, 50):
            # x-axis
            self.canvas.create_line(i, 650, i, 655, fill="white", width=1)
            self.canvas.create_text(i, 665, text=str(int(i - 50)), fill="white", anchor=tk.N)

            # y-axis
            self.canvas.create_line(650, i, 655, i, fill="white", width=1)
            self.canvas.create_text(665, i, text=str(int(650 - i)), fill="white", anchor=tk.W)

    def draw_points(self):
        for point in self.points:
            self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill="#FFD700",
                                    outline="#FFD700")

    def calculate_convex_hull(self):
        if len(self.points) < 3:
            print("Convex hull requires at least three points.")
            return

        hull_points = self.graham_scan(self.points)

        # Draw convex hull lines with a delay
        for i in range(len(hull_points)):
            next_idx = (i + 1) % len(hull_points)
            x1, y1 = hull_points[i][0], hull_points[i][1]
            x2, y2 = hull_points[next_idx][0], hull_points[next_idx][1]
            self.root.after(i * 500, lambda x1=x1, y1=y1, x2=x2, y2=y2: self.draw_line(x1, y1, x2, y2))

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, fill="#FF5733", width=2)
        self.root.update()

    def reset_graph(self):
        self.points = []
        self.redraw_canvas()

    def graham_scan(self, points):
        def polar_angle(point):
            # Calculate polar angle with respect to the lowest point
            x, y = point
            return math.atan2(y - lowest_point[1], x - lowest_point[0])

        def ccw(p1, p2, p3):
            return (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])

        # Find the lowest point (bottommost point)
        lowest_point = min(points, key=lambda p: (p[1], p[0]))

        # Sort points based on polar angle
        points.sort(key=polar_angle, reverse=True)  # Sort in reverse order

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

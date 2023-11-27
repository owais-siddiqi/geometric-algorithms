import tkinter as tk

class QuickHullVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Quick Hull Visualization")
        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.points = []
        self.lines = []

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_click)

        # Create a button to start the algorithm
        self.start_button = tk.Button(master, text="Start Quick Hull", command=self.start_quick_hull)
        self.start_button.pack()

        # Draw axis and set limits
        self.draw_axis()

    def on_click(self, event):
        x, y = event.x, event.y
        # Check if the point is within the limits
        if 50 < x < 550 and 50 < y < 550:
            self.points.append((x, y))
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

    def start_quick_hull(self):
        if len(self.points) < 3:
            print("At least 3 points are required.")
            return

        # Clear previous lines
        for line in self.lines:
            self.canvas.delete(line)

        # Sort points based on x-coordinate
        self.points.sort()

        # Find convex hull
        hull_points = self.quick_hull(self.points)

        # Draw convex hull in steps
        for i in range(len(hull_points) - 1):
            self.draw_line_step(hull_points[i], hull_points[i + 1], i * 500)
        self.draw_line_step(hull_points[-1], hull_points[0], (len(hull_points) - 1) * 500)

    def quick_hull(self, points):
        if len(points) <= 1:
            return points

        # Find the leftmost and rightmost points
        leftmost = points[0]
        rightmost = points[-1]

        # Divide the points into two subsets, left and right
        left_set = [point for point in points if self.orientation(leftmost, rightmost, point) == -1]
        right_set = [point for point in points if self.orientation(leftmost, rightmost, point) == 1]

        # Find the convex hull for the two subsets
        left_hull = self.quick_hull(left_set)
        right_hull = self.quick_hull(right_set)

        # Concatenate the results
        return [leftmost] + left_hull + [rightmost] + right_hull

    @staticmethod
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    def draw_line_step(self, p, q, delay):
        x1, y1 = p
        x2, y2 = q
        line = self.canvas.create_line(x1, y1, x2, y2, fill="red", state=tk.HIDDEN)
        self.lines.append(line)
        self.master.after(delay, lambda: self.show_line(line))

    def show_line(self, line):
        self.canvas.itemconfig(line, state=tk.NORMAL)

    def draw_axis(self):
        # Draw x-axis with scale
        for i in range(50, 551, 50):
            self.canvas.create_line(i, 550, i, 570)
            self.canvas.create_text(i, 580, text=str(i-50), anchor=tk.N)

        # Draw y-axis with scale
        for i in range(50, 551, 50):
            self.canvas.create_line(50, i, 70, i)
            self.canvas.create_text(30, i, text=str(550-i), anchor=tk.E)

def main():
    root = tk.Tk()
    app = QuickHullVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

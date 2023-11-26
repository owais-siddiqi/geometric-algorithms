import tkinter as tk

class CustomPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def calculate_slope(p1, p2):
    if p2.x - p1.x == 0:
        return float('inf')  # Vertical line, slope is infinity
    return (p2.y - p1.y) / (p2.x - p1.x)

def check_intersection(line1, line2):
    slope1 = calculate_slope(line1[0], line1[1])
    slope2 = calculate_slope(line2[0], line2[1])

    if slope1 == slope2:
        return False  # Lines are either parallel or coincident

    # Check if the intersection point is within the line segments
    x_intersect = (
        (slope1 * line1[0].x - slope2 * line2[0].x + line2[0].y - line1[0].y) /
        (slope1 - slope2)
    )
    y_intersect = slope1 * (x_intersect - line1[0].x) + line1[0].y

    x_range_line1 = min(line1[0].x, line1[1].x), max(line1[0].x, line1[1].x)
    y_range_line1 = min(line1[0].y, line1[1].y), max(line1[0].y, line1[1].y)

    x_range_line2 = min(line2[0].x, line2[1].x), max(line2[0].x, line2[1].x)
    y_range_line2 = min(line2[0].y, line2[1].y), max(line2[0].y, line2[1].y)

    return (
        x_range_line1[0] <= x_intersect <= x_range_line1[1] and
        y_range_line1[0] <= y_intersect <= y_range_line1[1] and
        x_range_line2[0] <= x_intersect <= x_range_line2[1] and
        y_range_line2[0] <= y_intersect <= y_range_line2[1]
    )

class LineDrawerApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400, bg="#001F3F")  # Pastel background color
        self.canvas.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.custom_points = []
        self.custom_lines = []

        # Draw axes
        self.canvas.create_line(0, 200, 400, 200, fill="gray")  # Horizontal axis (pastel gray)
        self.canvas.create_line(200, 0, 200, 400, fill="gray")  # Vertical axis (pastel gray)

        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x, y = event.x, event.y
        self.custom_points.append(CustomPoint(x, y))
        self.draw_custom_point(x, y)

        if len(self.custom_points) == 2:
            self.draw_custom_line(self.custom_points)
            self.custom_lines.append((self.custom_points[0], self.custom_points[1]))
            self.custom_points = []

            if len(self.custom_lines) == 2:
                if check_intersection(self.custom_lines[0], self.custom_lines[1]):
                    self.show_result("Lines intersect!")
                else:
                    self.show_result("Lines do not intersect!")

    def draw_custom_point(self, x, y):
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")  # Pastel purple

    def draw_custom_line(self, points):
        x1, y1 = points[0].x, points[0].y
        x2, y2 = points[1].x, points[1].y
        self.canvas.create_line(x1, y1, x2, y2, fill="red")  # Pastel blue

    def show_result(self, result):
        self.canvas.create_text(200, 20, text=result, fill="green", font=("Helvetica", 12))  # Pastel pink
        self.root.after(2000, self.reset)  # Reset after 2000 milliseconds (2 seconds)

    def reset(self):
        self.canvas.delete("all")

        # Draw axes
        self.canvas.create_line(0, 200, 400, 200, fill="gray")  # Horizontal axis (pastel gray)
        self.canvas.create_line(200, 0, 200, 400, fill="gray")  # Vertical axis (pastel gray)

        self.custom_points = []
        self.custom_lines = []

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Custom Slope Method")

    app = LineDrawerApp(root)

    root.mainloop()

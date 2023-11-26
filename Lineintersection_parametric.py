import tkinter as tk

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def parametric_intersect(l1, l2):
    x1, y1 = l1[0].x, l1[0].y
    x2, y2 = l1[1].x, l1[1].y
    x3, y3 = l2[0].x, l2[0].y
    x4, y4 = l2[1].x, l2[1].y

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return False  # Lines are parallel

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

    return 0 <= t <= 1 and 0 <= u <= 1

class LineDrawer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=500, bg="#001F3F")  # Light blue background color
        self.canvas.pack()

        self.reset_button = tk.Button(root, text="Clear", command=self.reset)
        self.reset_button.pack()

        self.points = []
        self.lines = []

        # Draw coordinate grid
        self.canvas.create_line(0, 250, 500, 250, fill="gray")  # Horizontal axis
        self.canvas.create_line(250, 0, 250, 500, fill="gray")  # Vertical axis

        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x, y = event.x, event.y
        self.points.append(Point(x, y))
        self.draw_point(x, y)

        if len(self.points) == 2:
            self.draw_line(self.points)
            self.lines.append((self.points[0], self.points[1]))
            self.points = []

            if len(self.lines) == 2:
                if parametric_intersect(self.lines[0], self.lines[1]):
                    self.show_result("Lines Intersect!")
                else:
                    self.show_result("Lines do not intersect!")

    def draw_point(self, x, y):
        self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="red")

    def draw_line(self, points):
        x1, y1 = points[0].x, points[0].y
        x2, y2 = points[1].x, points[1].y
        self.canvas.create_line(x1, y1, x2, y2, fill="red")  # red color for lines

    def show_result(self, result):
        self.canvas.create_text(250, 20, text=result, fill="green", font=("Helvetica", 14))
        self.root.after(2000, self.reset)  # Reset after 2000 milliseconds (2 seconds)

    def reset(self):
        self.canvas.delete("all")

        # Draw coordinate grid
        self.canvas.create_line(0, 250, 500, 250, fill="gray")  # Horizontal axis
        self.canvas.create_line(250, 0, 250, 500, fill="gray")  # Vertical axis

        self.points = []
        self.lines = []

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Line Intersection Checker")

    line_drawer = LineDrawer(root)

    root.mainloop()

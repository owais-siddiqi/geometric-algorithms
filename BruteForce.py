import tkinter as tk

def brute_force_convex_hull(points):
    if len(points) < 3:
        return points

    def on_the_left(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0

    hull = []
    non_hull = []
    for i in range(len(points)):
        for j in range(len(points)):
            if i != j:
                left_side = True
                for k in range(len(points)):
                    if k != i and k != j:
                        if not on_the_left(points[i], points[j], points[k]):
                            left_side = False
                            break
                if left_side:
                    hull.append((points[i], points[j]))
                else:
                    non_hull.append((points[i], points[j]))
    return hull, non_hull

def on_canvas_click(event):
    x, y = event.x, event.y
    points.append((x, y))
    draw_point(x, y)

def draw_point(x, y):
    canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='white', outline='white')

def draw_hull_lines(lines, color):
    for line in lines:
        canvas.create_line(line[0], line[1], tags='line', fill=color, width=2)
        canvas.update()
        canvas.after(250)

def draw_hull(hull, non_hull):
    canvas.delete('line')
    draw_hull_lines(non_hull, 'black')
    draw_hull_lines(hull, 'red')

def draw_axes():
    # Draw x-axis
    canvas.create_line(50, 350, 550, 350, tags='axis', fill='gray', width=2)
    for i in range(11):
        x = 50 + i * 50
        canvas.create_line(x, 345, x, 355, tags='axis', fill='gray', width=2)
        canvas.create_text(x, 370, text=str(i), anchor=tk.N, tags='axis', fill='white', font=("Arial", 10, "bold"))

    # Draw y-axis
    canvas.create_line(50, 350, 50, 20, tags='axis', fill='gray', width=2)
    for i in range(11):
        y = 350 - i * 30
        canvas.create_line(45, y, 55, y, tags='axis', fill='gray', width=2)
        canvas.create_text(40, y, text=str(i), anchor=tk.E, tags='axis', fill='white', font=("Arial", 10, "bold"))

def reset_graph():
    global points
    canvas.delete('all')
    draw_axes()
    points = []

def calculate_hull():
    hull, non_hull = brute_force_convex_hull(points)
    draw_hull(hull, non_hull)

root = tk.Tk()
root.title("Convex Hull - Brute Force")
root.configure(bg='lightgrey')  # Set background color

canvas = tk.Canvas(root, width=600, height=400, bg="#001F3F")
canvas.pack()
canvas.bind('<Button-1>', on_canvas_click)

calculate_button = tk.Button(root, text="Calculate Convex Hull", command=calculate_hull, bg='navy', fg='white', font=("Arial", 12, "bold"))
calculate_button.pack()

reset_button = tk.Button(root, text="Reset Graph", command=reset_graph, bg='firebrick', fg='white', font=("Arial", 12, "bold"))
reset_button.pack()

points = []

# Draw x and y axes
draw_axes()

root.mainloop()

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import subprocess

class AlgorithmRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Runner")

        style = ThemedStyle(self.root)
        style.set_theme("plastik")

        self.algorithm_var = tk.StringVar()
        self.sub_algorithm_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding=(20, 10))
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Algorithm Label and Combobox
        algorithm_label = ttk.Label(main_frame, text="Select Algorithm:")
        algorithm_label.grid(row=0, column=0, pady=10, sticky=tk.W)

        algorithm_combobox = ttk.Combobox(main_frame, values=["convex_hull", "line_intersection"], textvariable=self.algorithm_var, state="readonly")
        algorithm_combobox.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

        # Sub-Algorithm Label and Combobox
        sub_algorithm_label = ttk.Label(main_frame, text="Select Sub-Algorithm:")
        sub_algorithm_label.grid(row=1, column=0, pady=10, sticky=tk.W)

        self.sub_algorithm_combobox = ttk.Combobox(main_frame, values=[], textvariable=self.sub_algorithm_var, state="readonly")
        self.sub_algorithm_combobox.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)

        # Run Button
        run_button = ttk.Button(main_frame, text="Run Algorithm", command=self.run_algorithm)
        run_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Events
        algorithm_combobox.bind("<<ComboboxSelected>>", self.update_sub_algorithms)

    def update_sub_algorithms(self, event):
        main_choice = self.algorithm_var.get()

        if main_choice == "convex_hull":
            sub_algorithms = ["Brute Force", "Graham Scan", "Jarvis March", "Quick Hull","Monotone Chain"]
        elif main_choice == "line_intersection":
            sub_algorithms = ["Parametric", "Slope", "CCW"]
        else:
            sub_algorithms = []

        self.sub_algorithm_var.set("")  # Reset sub-algorithm choice
        self.sub_algorithm_combobox["values"] = sub_algorithms

    def run_algorithm(self):
        main_choice = self.algorithm_var.get()
        sub_choice = self.sub_algorithm_var.get()

        if main_choice == "convex_hull":
            self.run_convex_hull(sub_choice)
        elif main_choice == "line_intersection":
            self.run_line_intersection(sub_choice)

    def run_convex_hull(self, sub_algorithm):
        if sub_algorithm == "Brute Force":
            subprocess.run(["python", "D:/Documents/University/Fall_23/Algorithms Project/alpha_algo/BruteForce.py"])
        elif sub_algorithm == "Graham Scan":
            subprocess.run(["python", "D:/Documents/University/Fall_23/Algorithms Project/alpha_algo/GrahamScan.py"])
        elif sub_algorithm == "Jarvis March":
            subprocess.run(["python", "D:/Documents/University/Fall_23/Algorithms Project/alpha_algo/JarvisMarch.py"])
        elif sub_algorithm == "Quick Hull":
            subprocess.run(["python", "D:/Documents/University/Fall_23/Algorithms Project/alpha_algo/QuickHull.py"])
        elif sub_algorithm == "Monotone Chain":
            subprocess.run(["python", "D:/Documents/University/Fall_23/Algorithms Project/alpha_algo/MonotoneChain.py"])
            
    def run_line_intersection(self, sub_algorithm):
        if sub_algorithm == "Parametric":
            subprocess.run(["python", "D:/Documents/University/Fall_23/Algorithms Project/alpha_algo/Lineintersection_parametric.py"])
        elif sub_algorithm == "Slope":
            subprocess.run(["python", "D:/Documents/University/Fall_23/Algorithms Project/alpha_algo/Lineintersection_slope.py"])
        elif sub_algorithm == "CCW":
            subprocess.run(["python", "D:/Documents/University/Fall_23/Algorithms Project/alpha_algo/Lineintersection_ccw.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmRunnerApp(root)
    root.mainloop()
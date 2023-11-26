import tkinter as tk
from tkinter import ttk
import subprocess

class AlgorithmRunnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Runner")

        self.algorithm_var = tk.StringVar()
        self.sub_algorithm_var = tk.StringVar()

        self.algorithm_label = tk.Label(root, text="Select Algorithm:")
        self.algorithm_label.pack()

        self.algorithm_combobox = ttk.Combobox(root, values=["convex_hull", "line_intersection"], textvariable=self.algorithm_var)
        self.algorithm_combobox.pack()

        self.sub_algorithm_label = tk.Label(root, text="Select Sub-Algorithm:")
        self.sub_algorithm_label.pack()

        self.sub_algorithm_combobox = ttk.Combobox(root, values=[], textvariable=self.sub_algorithm_var)
        self.sub_algorithm_combobox.pack()

        self.run_button = tk.Button(root, text="Run Algorithm", command=self.run_algorithm)
        self.run_button.pack()

        self.algorithm_combobox.bind("<<ComboboxSelected>>", self.update_sub_algorithms)

    def update_sub_algorithms(self, event):
        main_choice = self.algorithm_var.get()

        if main_choice == "convex_hull":
            sub_algorithms = ["Brute Force", "Graham Scan", "Jarvis March"]
        elif main_choice == "line_intersection":
            sub_algorithms = ["Parametric", "Slope"]
        else:
            sub_algorithms = []

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
            subprocess.run(["python", "BruteForce.py"])
        elif sub_algorithm == "Graham Scan":
            subprocess.run(["python", "GrahamScan.py"])
        elif sub_algorithm == "Jarvis March":
            subprocess.run(["python", "JarvisMarch.py"])

    def run_line_intersection(self, sub_algorithm):
        if sub_algorithm == "Parametric":
            subprocess.run(["python", "Lineintersection_parametric.py"])
        elif sub_algorithm == "Slope":
            subprocess.run(["python", "Lineintersection_slope.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmRunnerApp(root)
    root.mainloop()

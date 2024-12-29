import tkinter as tk
from tkinter import ttk, filedialog, messagebox
# import networkx as nx
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

import Demo
from FSA_Operations import FSA_Operations
from NFSA import *
from DFSA import *


class AutomataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFA Determinization Tool")
        self.root.geometry("1100x640")

        # Frames
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.grid(row=0, column=0, sticky="nsew")

        self.canvas_frame = ttk.Frame(root, padding="10")
        self.canvas_frame.grid(row=0, column=1, sticky="nsew")

        # Control frame
        ttk.Label(self.control_frame, text="NFA Determinization Tool", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        # load nfa
        self.load_button = ttk.Button(self.control_frame, text="Load Automaton", command=self.load_automaton)
        self.load_button.grid(row=1, column=0, pady=5, sticky="ew")

        # determinize
        self.determinize_button = ttk.Button(self.control_frame, text="Determinize", command=self.determinize)
        self.determinize_button.grid(row=4, column=0, pady=5, sticky="ew")

        # extract dfa
        self.extract_button = ttk.Button(self.control_frame, text="Extract Automaton", command=self.extract_automaton)
        self.extract_button.grid(row=7, column=0, pady=5, sticky="ew")

        # demo 1
        self.demo_1_button = ttk.Button(self.control_frame, text="Load Demo automaton 1", command=self.demo_automation_1)
        self.demo_1_button.grid(row=10, column=0, pady=5, sticky="ew")

        # demo 2
        self.demo_2_button = ttk.Button(self.control_frame, text="Load Demo automaton 2", command=self.demo_automation_2)
        self.demo_2_button.grid(row=13, column=0, pady=5, sticky="ew")

        # demo 3
        self.demo_3_button = ttk.Button(self.control_frame, text="Load Demo automaton 3", command=self.demo_automation_3)
        self.demo_3_button.grid(row=16, column=0, pady=5, sticky="ew")

        # info
        self.info_button = ttk.Button(self.control_frame, text="Information and guide", command=self.show_info)
        self.info_button.grid(row=19, column=0, pady=5, sticky="ew")

        # Canvas
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=800, height=600)
        self.h_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scroll = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")

        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)
        self.image_id = None
        # self.image_label = tk.Label(self.canvas_frame)
        # self.image_label.pack(fill=tk.BOTH, expand=True)

        self.fsa = None

    def load_automaton(self):
        file_path = filedialog.askopenfilename(title="Select Automaton File", filetypes=[("Text Files", "*.txt"), ("Json Files", "*.json")])
        if not file_path:
            return

        try:
            self.fsa = self.parse_automaton(file_path)
            self.draw_automaton("fsa_img/current_NFA")
            # messagebox.showinfo("Success", "Automaton loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load fsa: {e}")

    def extract_automaton(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")])
        if file_path:
            if file_path.endswith('.json'):
                try:
                    self.fsa.write_json(file_path)
                except Exception as e:
                    messagebox.showerror("There was no determinization", "Determinize automation to extract")

            elif file_path.endswith('.txt'):
                try:
                    self.fsa.write_txt(file_path)
                except Exception as e:
                    messagebox.showerror("There was no determinization", "Determinize automation to extract")

    def parse_automaton(self, file_path):
        format = file_path.split('.')[-1]
        try:
            if format == 'txt':
                return NFSA.read_txt(file_path)
            elif format == 'json':
                return NFSA.read_json(file_path)
            else:
                raise Exception('idk what format it is')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read fsa: {e}")

    def draw_automaton(self, image_path):
        """Draws the fsa graph and displays its image."""
        try:
            fmt = 'png'
            dot = self.fsa.visualize()
            dot.render(image_path, format=fmt, cleanup=True)

            # Load and display the PNG image
            image = Image.open(image_path + f'.{fmt}')
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            # self.image_label.configure(image=photo)
            # self.image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize fsa: {e}")

    def determinize(self):
        if not self.fsa:
            messagebox.showwarning("Warning", "Load an fsa first.")
            return
        try:
            self.fsa = FSA_Operations.determinization(self.fsa)
            self.draw_automaton("fsa_img/current_DFA")
            # messagebox.showinfo("Success", "Determinization complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to determinize fsa: {e}")

    def demo_automation_1(self):
        self.fsa = Demo.nfa_example_1
        self.draw_automaton("fsa_img/current_DFA")

    def demo_automation_2(self):
        self.fsa = Demo.nfa_example_2
        self.draw_automaton("fsa_img/current_DFA")

    def demo_automation_3(self):
        self.fsa = Demo.nfa_example_3
        self.draw_automaton("fsa_img/current_DFA")

    def show_info(self):
        messagebox.showinfo("Информация о программе", ''.join(
            ["Эта программа реализует алгоритм детерминизации НКА\n",
            "Интерфейс содержит кнопки загрузки, детерминизации НКА и сохранения итогового ДКА,",
            "а также три демонстрационных автомата и кнопку, показывающую это сообщение\n\n",
                            
            "Поддерживает возможность загрузки НКА из файла .json/.txt\n",
            "И сохранение полученного ДКА\n",
            "Формат файлов:",
             """
             
                .txt format:
             a, b              ->  alphabet
             q0, q1, q2        ->  states
             q0                -> start state
             q2, q1            -> final states
             q0, a, q1, q2     -> from 'q0' with 'a' to 'q1' and 'q2'
             q0, b, q2         -> etc.
             q1, a, q2
             q2, b, q0
             
                .json format: 
             {
                 "states": ["q0", "q1", "q2"],
                 "alphabet": ["a", "b"],
                 "start": "q0",
                 "accepting": ["q2"],
                 "transitions": {
                     "q0": {
                         "a": ["q1"],
                         "b": ["q2"]
                     },
                     "q1": {
                         "a": ["q2"]
                     },
                     "q2": {
                         "b": ["q0"]
                     }
                 }
             }
             """
            ])
                            )
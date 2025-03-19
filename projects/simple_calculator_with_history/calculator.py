import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator with History")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        self.current_expression = ""
        self.history = []
        
        self.create_frames()
        
        self.create_display()
        
        self.create_buttons()
        
        self.create_history_display()

    def create_frames(self):

        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.calculator_frame = ttk.Frame(self.main_container)
        self.calculator_frame.pack(side="left", expand=True, fill="both", padx=(0, 5))
        
        self.history_frame = ttk.Frame(self.main_container)
        self.history_frame.pack(side="right", expand=True, fill="both", padx=(5, 0))

    def create_display(self):

        self.display = ttk.Entry(self.calculator_frame, justify="right", font=("Arial", 20))
        self.display.pack(fill="x", padx=5, pady=5)

    def create_buttons(self):

        button_frame = ttk.Frame(self.calculator_frame)
        button_frame.pack(expand=True, fill="both")
        
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('←', 5, 1), ('(', 5, 2), (')', 5, 3),
        ]
        
        for (text, row, col) in buttons:
            button = ttk.Button(button_frame, text=text, command=lambda t=text: self.button_click(t))
            button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

    def create_history_display(self):

        history_label = ttk.Label(self.history_frame, text="History", font=("Arial", 14))
        history_label.pack(pady=5)
        
        self.history_listbox = tk.Listbox(self.history_frame, font=("Arial", 12))
        self.history_listbox.pack(expand=True, fill="both")
        
        clear_history_btn = ttk.Button(self.history_frame, text="Clear History", command=self.clear_history)
        clear_history_btn.pack(pady=5)

    def button_click(self, value):
        if value == "=":
            try:
                result = eval(self.current_expression)

                history_entry = f"{self.current_expression} = {result}"
                self.history.append(history_entry)
                self.history_listbox.insert(0, history_entry)

                self.current_expression = str(result)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, self.current_expression)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current_expression = ""
        elif value == "C":
            self.current_expression = ""
            self.display.delete(0, tk.END)
        elif value == "←":
            self.current_expression = self.current_expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)
        else:
            self.current_expression += value
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)

    def clear_history(self):
        self.history = []
        self.history_listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    style = ttk.Style()
    style.theme_use('clam')
    root.mainloop() 
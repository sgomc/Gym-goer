import tkinter as tk
from tkinter import simpledialog

class MultiInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompts):
        self.prompts = prompts
        super().__init__(parent, title)

    def body(self, master):
        self.entries = []
        for prompt in self.prompts:
            row = tk.Frame(master)
            lab = tk.Label(row, width=15, text=prompt)
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            self.entries.append(ent)
        return self.entries[0] 

    def apply(self):
        name = str(self.entries[0].get())
        
        sport= str(self.entries[1].get())

        weight = float(self.entries[2].get())
        
        self.result = [name, sport,weight]
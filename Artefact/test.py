import os
import tkinter as tk
from tkinter import ttk, scrolledtext,messagebox
import pandas as pd
def Workoutlists_maker():
    def CanvasFile(*args):
        selected_file = selectedFileVar.get()
        if selected_file:
            file_path = os.path.join(os.getcwd(), selected_file)
            try:
                df = pd.read_csv(file_path)
                
                SecondaryWindow = tk.Toplevel(root)
                SecondaryWindow.title(f"CSV File Viewer - {selected_file}")

                
                textWidget = scrolledtext.ScrolledText(SecondaryWindow, height=15, width=60)
                textWidget.insert(tk.END, str(df[["Title", "Desc"]]))
                textWidget.pack(fill=tk.BOTH, expand=True)
            except pd.errors.EmptyDataError:
                messagebox.showerror("Error","Selected CSV file is empty.")

    def show_error(message):
        
        messagebox.showerror("Error", message)

    def on_combobox_selected(event):
        
        CanvasFile()



   
    root = tk.Tk()
    root.title("CSV File Viewer")

    
    file_pattern = "workout_list.csv"

    
    all_files = os.listdir()

    
    csv_files = [file for file in all_files if file.endswith(file_pattern)]

    
    selectedFileVar = tk.StringVar(root)
    selectedFileVar.set("Select a CSV file")
    
    file_combobox = ttk.Combobox(root, textvariable=selectedFileVar, values=csv_files)
    file_combobox.pack(pady=10)

    file_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)



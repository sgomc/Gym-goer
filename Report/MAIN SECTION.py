import pandas as pd
import random
from PIL import Image, ImageTk
import os
import csv
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from Multidialog import MultiInputDialog
from MOdelling import workout
from test import Workoutlists_maker
from bmitesting import visualbmi
from AmountPpl import AmountPplEstimation
def get_advice_for_sport_and_muscle(sport):
    adviceDict = {
        'FOOTBALL': "To succeed on the field, emphasize lower body strength and agility.",
        'RUNNING': "In order to improve your running performance, prioritize your lower body conditioning.",
        'WEIGHLIFTING': "Build your upper body strength for effective weightlifting.",
        'NONE': "Build strength in your upper body to begin your fitness journey.",
        'BODYBUILDING': 'Focus on upper body exercises when you first start your bodybuilding adventure.',
        'SWIMMING': 'Build upper body strength as you start your swimming training.',
        'BASKETBALL': 'Strengthening your upper body and core will improve your agility and power.',
        'TENNIS': 'Start by strengthening your upper body, particularly your arms and forearms, to improve your tennis game.',
        'CYCLING': 'First, focus on the quadriceps in your lower body.',
        'BASEBALL': 'Pay attention to your upper body and core strength.',
        'SOCCER': 'Focus on improving your cardiovascular endurance and lower body strength.',
        'GOLF': 'For a balanced swing, prioritize your core strength and flexibility.',
        'VOLLEYBALL': 'Focus on developing arm strength and agility while strengthening your lower body.',
        'TRIATHLON': 'Incorporate running, cycling, and swimming into your overall endurance training regimen.',
        'WRESTLING': 'Develop strength throughout your body, concentrating on your upper and core regions.',
        'HOCKEY': 'Build strength in your upper and lower body, paying special attention to your cardiovascular system.',
        'ATHLETICS': 'Use a mix of speed and strength training to prepare for particular events.',
        'MARTIAL_ARTS': 'Put your entire strength, flexibility, and agility into focus.',
        'ROWING': 'Develop strong legs, back, and core muscles for efficient rowing form.',
        'ICE_SKATING': 'Strengthen your legs and focus on your flexibility and balance.',
    }
    if sport not in adviceDict:
        sport = 'Unknown'
    return adviceDict.get(sport, 'Unknown')

muscleDict = {
    'ABDOMINALS': 'Abdominals',
    'ADDUCTORS': 'Adductors',
    'ABDUCTORS': 'Abductors',
    'BICEPS': 'Biceps',
    'CALVES': 'Calves',
    'CHEST': 'Chest',
    'FOREARMS': 'Forearms',
    'GLUTES': 'Glutes',
    'HAMSTRINGS': 'Hamstrings',
    'LATS': 'Lats',
    'LOWER BACK': 'Lower Back',
    'MIDDLE BACK': 'Middle Back',
    'TRAPS': 'Traps',
    'NECK': 'Neck',
    'QUADRICEPS': 'Quadriceps',
    'SHOULDERS': 'Shoulders',
    'TRICEPS': 'Triceps'
}

levelDict = {
    'EXPERT': 'Expert',
    'INTERMEDIATE': 'Intermediate',
    'BEGINNER': 'Beginner'
}

exercise_intensity_calories = {
    'Strength': {'Beginner': 4, 'Intermediate': 6, 'Expert': 8},
    'Plyometrics': {'Beginner': 8, 'Intermediate': 10, 'Expert': 12},
    'Cardio': {'Beginner': 10, 'Intermediate': 12, 'Expert': 15},
    'Stretching': {'Beginner': 2, 'Intermediate': 3, 'Expert': 4},
    'Powerlifting': {'Beginner': 5, 'Intermediate': 7, 'Expert': 8},
    'Strongman': {'Beginner': 10, 'Intermediate': 12, 'Expert': 15},
    'Olympic Weightlifting': {'Beginner': 6, 'Intermediate': 8, 'Expert': 10}
}
def retry_operation(prompts):
    try:
        root = tk.Tk()
        root.withdraw()
        result =  MultiInputDialog(root, "Input", prompts)
        return result
    except:
        retry_operation(prompts)
    root.mainloop()


def calculate_calories(row):
    exercise_type = row['Type']
    intensity_level = row['Level']
    duration_minutes = random.randint(20, 45)

    calories_per_minute = exercise_intensity_calories.get(exercise_type, {}).get(intensity_level, 0)
    calories_burned = calories_per_minute * duration_minutes
    return calories_burned
canvas_visible = True
def toggle_visibility(canvas_widget,a):
    global canvas_visible
    if canvas_visible:
        canvas_widget.pack_forget()
        a.pack_forget()
    else:
        canvas_widget.pack()
    canvas_visible = not canvas_visible

activation_count = 0
activation_count2 = 0
def generate_workout_plan():
    def get_user_input():
        root = tk.Tk()
        root.withdraw()
        prompts = ["Enter your Name", "Enter your sport:", "Enter current weight:"]
        dialog = retry_operation(prompts)
        result = dialog.result
        name,sport,Weight = result
        Weight = int(Weight)
        sport = sport.upper()
        Age = simpledialog.askfloat("Age", "How old are you?")
        Age = int(Age)
        Gender =""
        while Gender not in ["male","female"]:
            Gender = simpledialog.askstring("Gender", "Are you a Male or a Female? Pls choose the one that Describes you best on a Anatomical level the most")

        df = pd.read_csv("megaGymDataset.csv")
    
        Level_Work = simpledialog.askstring("Level Input", f"What level would you like to work? {df['Level'].unique()}")
        while Level_Work not in df['Level'].unique():
            Level_Work = simpledialog.askstring("Level Input", f"Please choose from the following: {df['Level'].unique()}")
        Level_Work = Level_Work.upper() 

        Muscle = simpledialog.askstring("Muscle Input", f"Please choose between the following groups: {df['BodyPart'].unique()}")
        while Muscle not in df['BodyPart'].unique():
            Muscle  = simpledialog.askstring("Muscle Input", f"Please choose from the following: {df['BodyPart'].unique()}")
        Muscle = Muscle.upper()  


        Level = df[(df['Level'] == levelDict.get(Level_Work)) & (df["BodyPart"] == muscleDict.get(Muscle))]
        return Weight, Level,sport, name,Muscle,Age,Gender


    def display_advice(sport):
        advice = get_advice_for_sport_and_muscle(sport.upper())
        messagebox.showinfo("Advice", f"Advice for {sport.capitalize()}: {advice}")
    def listchooser(Level,Muscle,name):
        if Level.empty:
            messagebox.showinfo("Empty List", "Seems like there is no exercise for what you were looking for\nRestate new data")
            Addmore()
        else:
            On_house = messagebox.askyesno("On_house Input", f"Do you want to choose it yourself?")

            if not On_house:
                WorkoutList = Level.sample(n=simpledialog.askinteger("n Input", f"how many Exercises? "), random_state=42)
                WorkoutList.to_csv(f'{name}{Muscle}workout_list.csv', index=False)
            else:
                messagebox.showinfo("List", f"Here is a list of Exercise you could do {Level}")
                LevelList = tk.Toplevel(root)
                LevelList.title("List of exercises")
                textWidget = tk.Text(LevelList)
                textWidget.insert(tk.END, str(Level))
                textWidget.pack(fill=tk.BOTH, expand=True)
                WorkoutList= pd.DataFrame()
                while True:
                    try:
                        selected_row_number = simpledialog.askinteger("Row Selection", f"Enter the number corresponding to the row you want to select: ")
                        if 0 <= selected_row_number < len(Level):
                            selected_row = Level.iloc[selected_row_number]
                            messagebox.showinfo("Row selected", f"{selected_row_number}:")
                            WorkoutList = pd.concat([WorkoutList, selected_row.to_frame().transpose()], ignore_index=True)
                            WorkoutList.to_csv(f'{name}{Muscle}workout_list.csv', index=False)
                        else:
                            messagebox.showinfo("Invalid Selection", "Please enter a valid row number.")
                    except ValueError:
                        messagebox.showinfo("Invalid Number", "Please enter a valid number.")
                    Exit = messagebox.askyesno("Add", "Do you want to add another one?")
                    if not Exit:
                        break

    def display_workout_list(Level,Muscle,name):
        
        
        if not os.path.exists(f"{name}{Muscle}workout_list.csv"):
            listchooser(Level,Muscle,name)
        else:
            answer = messagebox.askyesno("Existing path",f"{name}{Muscle}workout_list.csv\nDo you want to modify this path?")
            if answer:
                WorkoutListWindow = tk.Toplevel(root)
                WorkoutListWindow.title("Workout List")
                listchooser(Level,Muscle,name)

                if not os.path.exists(f"{name}{Muscle}workout_list.csv"):
                    textWidget = tk.Text(WorkoutListWindow)
                    textWidget.insert(tk.END, str(WorkoutList))
                    textWidget.pack(fill=tk.BOTH, expand=True)
                else:
                    WorkoutList = pd.read_csv(f"{name}{Muscle}workout_list.csv")
                    textWidget = tk.Text(WorkoutListWindow)
                    textWidget.insert(tk.END, str(WorkoutList))
                    textWidget.pack(fill=tk.BOTH, expand=True)
            


    def display_estimated_weight(Level,Weight,Muscle,name,Hydrated,Age,Gender):
        if not os.path.exists(f'{name}{Muscle}workout_list.csv'):
            messagebox.showinfo("File has not been set up yet", "Set up")
            display_workout_list(Level,Muscle,name)
        pattern = "workout_list.csv"
        multiplier = 1
        if Hydrated:
            if Age < 45 and Gender == "male":
                multiplier = 1.2
            if Age >= 45 and Gender == "male":
                multiplier = 0.9
            if Age < 40 and Gender == "female":
                multiplier = 1.15
            if Age >= 45 and Gender == "female":
                multiplier = 0.95
        else:
            if Age < 45 and Gender == "male":
                multiplier = 1.15
            if Age >= 45 and Gender == "male":
                multiplier = 0.95
            if Age < 40 and Gender == "female":
                multiplier = 1.10
            if Age >= 40 and Gender == "female":
                multiplier = 0.9
        
        all_files = os.listdir()


        fileArray = [file for file in all_files if file.endswith(pattern)]
        Muscle = simpledialog.askstring("Muscle", f"Please choose the muscle affiliated to the csv file?{fileArray} ")
        WorkoutList = pd.read_csv(f'{name}{Muscle}workout_list.csv')
        
        if WorkoutList.empty:
            messagebox.showinfo("Empty List","Your Workoutlist is empty")
        else:
            WorkoutList['CaloriesBurned'] = WorkoutList.apply(calculate_calories, axis=1)*multiplier
            estimated_final_weight = Weight - (WorkoutList['CaloriesBurned'].sum() * 0.00013)

            minY = int(min(Weight, estimated_final_weight))
            maxY = int(max(Weight, estimated_final_weight)) + 1

            fig, ax = plt.subplots()
            labels = ['Current Weight', 'Estimated Final Weight']
            weights = [Weight, estimated_final_weight]
            ax.bar(labels, weights, color=['blue', 'green'])
            ax.set_title('Estimated Weight After Training')
            ax.set_ylabel('Weight (kg)')
            ax.set_yticks(np.arange(minY, maxY, 1))
            ax.set_ylim(Weight - 1, estimated_final_weight + 1)

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()
          
            toggle_button = tk.Button(root, text="Hide", command=lambda: toggle_visibility(canvas_widget,toggle_button))
            toggle_button.pack()

    def Addmore():
        df = pd.read_csv("megaGymDataset.csv")

        Level_Work = simpledialog.askstring("Level Input", f"What level would you like to work? {df['Level'].unique()}")
        Level_Work = Level_Work.upper() 


        Muscle = simpledialog.askstring("Muscle Input", f"Please choose between the following groups: {df['BodyPart'].unique()}")
        Muscle = Muscle.upper()  

        Level = df[(df['Level'] == levelDict.get(Level_Work)) & (df["BodyPart"] == muscleDict.get(Muscle))]
        display_workout_list(Level,Muscle,name)               
    

    csv_pattern = '_dataa.csv'
  
    BoolLocationFile = os.listdir('.')
    fileArray = [file for file in BoolLocationFile if '_dataa.csv' in file]
    if not fileArray:
        Weight, Level , sport , name, Muscle , Age , Gender = get_user_input()

        with open(f'{name}{csv_pattern}', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([Weight,  sport,name,Muscle, Age , Gender])
            Level.to_csv('Level.csv')
    else:
        with open(fileArray[0], 'r') as csvfile:
            
            reader = csv.reader(csvfile)
            for row in reader:

                
                Weight, sport,name, Muscle, Age , Gender = row[:6]
                break

            Level = pd.read_csv('Level.csv')
            Weight = float(Weight)


    root = tk.Tk()
    root.title("New Life")
    root.geometry("400x400")
    
    button_container = tk.Frame(root)
    button_container.pack(pady=10)  


    
    filePath = f'{name}{csv_pattern}'
    with open(filePath, 'r') as csvfile:
        
        reader = csv.reader(csvfile)

        
        firstrow = next(reader)
    
    if 'True' in firstrow:
        
        options = ["Select Action", "BMI","People prediction","Display Advice","Display Workout Lists", "Display Estimated Weight","Work out","Add WorkoutList",]
    else:
        
        options = ["Select Action", "BMI","People prediction", "Display Advice", "Display Workout List", "Display Estimated Weight","Work out"]
        


    selectedOption = tk.StringVar(root)
    selectedOption.set(options[0])  

    menu = tk.OptionMenu(button_container, selectedOption, *options)
    menu.pack(side=tk.LEFT, padx=10)

    def OnDropChange(*args):
        with open(fileArray[0], 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        Weight, sport,name, Muscle, Age , Gender = row[:6]
                        break
        selectedAction = selectedOption.get()
        if selectedAction == "Display Advice":
            display_advice(sport)
        elif selectedAction == "Display Workout Lists":
            try:
                Workoutlists_maker()
            except:
                messagebox.showinfo("Box closed","Something went wrong")
        elif selectedAction == "Work out":
            try:
                root.withdraw()
                workout(name)
                root.deiconify()
            except:
                 messagebox.showinfo("Box closed","Either MicroBit Serial port not connected or box closed")
                 root.deiconify()
        elif selectedAction == "Display Workout List":
            with open(f'{name}{csv_pattern}', 'r') as file:
                lines = file.readlines()
                strippedLines = [line.strip() for line in lines]
                strippedLines = [x for x in strippedLines[0].split(',')]
                strippedLines.append("True")
            with open(f'{name}{csv_pattern}', 'w') as file:
                file.write('')
            with open(f'{name}{csv_pattern}', 'w') as file:
                writer = csv.writer(file)
                writer.writerow(strippedLines)
                display_workout_list(Level,Muscle,name)
        elif selectedAction == "Display Estimated Weight":
            try:
                
                hydrated = messagebox.askyesno("Hydration","Do you want to see a hydration display or no?")
                if not isinstance(Weight, float):
                    Weight = float(Weight)
                if not isinstance(Age, int):
                    Age = int(Age)
                if not isinstance(Gender, str):
                    Gender = str(Gender)
                if not isinstance(hydrated, bool):
                    hydrated = bool(hydrated)
                display_estimated_weight(Level,Weight,Muscle,name,hydrated,Age,Gender)
            except:
                messagebox.showinfo("Box closed",Exception)
        elif selectedAction == "Add WorkoutList":
            try:
                Addmore()
            except:
                messagebox.showinfo("Box closed","Something went wrong")
        elif selectedAction == "BMI":
            try:
                Height = simpledialog.askfloat("Height","What is your height?(meters)")
                visualbmi(Weight,Height,name)
            except:
                messagebox.showinfo("Box closed","Something went wrong")
        elif selectedAction == "People prediction":
            try:
                AmountPplEstimation()
            except FileNotFoundError:
                messagebox.showinfo("Box closed","Something went wrong")
        if selectedAction == "Display Workout List":
            options = ["Select Action", "Display Advice", "Display Workout List","People prediction", "Display Estimated Weight","Work out"]
            options.remove("Display Workout List")
            options.append("Display Workout Lists")  
            options.append("Add WorkoutList")  
            selectedOption.set(options[0])  
            menu['menu'].delete(0, 'end')
            options[1:] = sorted(options[1:])  
            for option in options:
                menu['menu'].add_command(label=option, command=tk._setit(selectedOption, option))
        

    selectedOption.trace_add("write", OnDropChange)
    root.mainloop()
generate_workout_plan()
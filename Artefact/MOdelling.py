import serial
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from tkinter import simpledialog, messagebox
import serial.tools.list_ports
import warnings



def workout(user_name):
    file_pattern = "workout_list.csv"
    all_files = os.listdir()
    csv_files = [file for file in all_files if file.endswith(file_pattern)]
    Muscle = simpledialog.askstring("workout", f"Please choose the muscle affiliated to the csv file you want to workout?{csv_files}")
    while not os.path.exists(f"{user_name}{Muscle}workout_list.csv"):
        Muscle = simpledialog.askstring("workout", f"Please choose the muscle affiliated to the csv file you want to workout?{csv_files}")
    WorkoutList = pd.read_csv(f'{user_name}{Muscle}workout_list.csv')

    
    if os.path.exists("data.csv"):
        os.remove("data.csv")

    if not os.path.exists("data.csv"):
        headerList = ['Name','Date', 'Time', 'Day','Hour','Taken']
        my_df = pd.DataFrame(columns =  headerList)
        my_df.to_csv("data.csv", index=False)
    
    workoutdf = pd.read_csv(f'{user_name}{Muscle}workout_list.csv')
    workoutdf.name = f'{user_name}{Muscle}workout_list.csv'.strip(".csv").strip("Samir")

    n=0
    ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'COM' in p.description 
    ]
    if len(ports) > 1:
        messagebox.showwarning("Multiple COM ports",'Multiple Serial COM ports found - using the first')

    connection = serial.Serial(ports[0],115200)
    while n<len(workoutdf["Title"]):
        print(f"Workout timer:\nWorkout number {n+1} in {workoutdf.name}")
        data = connection.readline().decode().strip()
        while 'start' not in data:
            print(data)
            data = connection.readline().decode().strip()
        start = datetime.datetime.now()
        print(start)
        Workout = messagebox.showinfo(f"Workout Number {n+1}  {workoutdf['Title'][n]}", f"{str(workoutdf['Desc'][n]).rjust(20)} ")
        n+=1
        while  'end' not in data:
            data = connection.readline().decode().strip()
        print('Finished')
        end = datetime.datetime.now()
        print(end)
        taken = end-start
        print(f"Time taken: {round(taken.total_seconds(),3)}")
        date = end.strftime('%x')
        time = end.strftime('%X')
        day = end.strftime('%w')
        hour = end.strftime('%H')
        
        
        with open('data.csv', 'a+') as file:
            file.write(str(workoutdf['Title'][n-1])+','+str(date)+','+str(time)+','+str(day)+','+str(hour)+','+str(taken.total_seconds())+'\n')
        df = pd.read_csv('data.csv')
        print(f"Mean Time per exercise:{round(df['Taken'].mean(),2)}")
        if taken.total_seconds() < df['Taken'].mean():
            print('Quicker than your average on this some of these exercises')
        else:
            print('Keep Pushing')
        dfhour = df.loc[df['Hour'] == int(hour)]
    print("good work that's enough for today")
    end_Total = datetime.datetime.now()
    Total_Time = end_Total-start
    plt.scatter(df["Name"],df["Taken"])
    plt.title("Time taken")
    plt.xlabel("Date")
    plt.ylabel("Time")
    plt.show()
    print(round(Total_Time.total_seconds()))
    if not os.path.exists("AvgTimeWorkouts.csv"):
        headerList = ['Time']
        Time_df = pd.DataFrame(columns =  headerList)
        Time_df.to_csv("AvgTimeWorkouts.csv", index=False)
    with open('AvgTimeWorkouts.csv', 'a+') as file:
        file.write(str(round(Total_Time.total_seconds()))+"\n")





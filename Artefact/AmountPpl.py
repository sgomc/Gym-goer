import pandas as pd
from tkinter import simpledialog, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
def AmountPplEstimation():
    CurrentTemp=""
    try:
        currentTemp = pd.read_csv('microbit.csv')
    
        data = pd.read_csv("Somethingelse.csv")
        data['temperature(fareheit)'] = pd.cut(data['temperature'], bins=range(35, 100, 5), right=False)
        for item in data['temperature(fareheit)'].value_counts().index:
            if ((currentTemp['temperature'].mean()* 9/5) + 32)in item:
                location = item
                break
        Filter= data[(data['temperature'] >= location.left) & (data['temperature'] <= location.right)]
        Inp = datetime.now()
        hour = int(Inp.strftime('%H'))
        minute = int(Inp.strftime('%M'))*60
        seconds = int(Inp.strftime('%S'))
        weather=""
        while weather not in ["Good","Bad"]:
            weather = simpledialog.askstring("Weather","What is the weather condition? Good/Bad")
        weekend = messagebox.askyesno("Weekend","is it weekend?")
        if not isinstance(weekend, bool):
            weekend = bool(weekend)
        if len(Filter[Filter['hour'] == hour]['number_people'])== 0:
            messagebox.showinfo("Free Gym",f"At {hour} O'Clock  with a temperature between {round(((location.left-32)*5/9),2)} and {(round(((location.right-32)*5/9),2))} nobody is expected there")
        else:
            if Filter[Filter['hour'] == hour]['number_people'].dtype == int:  
                messagebox.showinfo("Maximum/Minimum and Average",f"Maximum expected amount of people at {hour} O'Clock with a temperature between {round(((location.left-32)*5/9),2)} and {(round(((location.right-32)*5/9),2))}  is {max(Filter[Filter['hour'] == hour]['number_people'])} ± {standard_deviation(max(Filter[Filter['hour'] == hour]['number_people']),weather,weekend)}\nMinimum expected amount of people at {hour} O'Clockwith a temperature between {round(((location.left-32)*5/9),2)} and {(round(((location.right-32)*5/9),2))}  {min(Filter[Filter['hour'] == hour]['number_people'])} ± {standard_deviation(min(Filter[Filter['hour'] == hour]['number_people']),weather,weekend)}\nthe average amount of people at {hour} O'Clockwith a temperature between {round(((location.left-32)*5/9),2)} and {(round(((location.right-32)*5/9),2))}  {round(Filter[Filter['hour'] == hour]['number_people'].mean(),2)} ± {standard_deviation(round(Filter[Filter['hour'] == hour]['number_people'].mean(),2),weather,weekend)}")
                try:
                    TimetakenModel = pd.read_csv("AvgTimeWorkouts.csv")
                

                    if TimetakenModel["Time"].mean()+(hour*60*60) >23*60*60:
                        messagebox.showinfo("Estimated finish time",f"you will finish at {str(datetime.fromtimestamp((TimetakenModel['Time'].mean()+(hour*60*60)+minute+seconds-24*60*60))).split(' ')[1]}")
                    else:
                        fig, ax = plt.subplots()
                        messagebox.showinfo("Estimated finish time",f"you will finish at {str(datetime.fromtimestamp(TimetakenModel['Time'].mean()+(hour*60*60)+minute+seconds)).split(' ')[1]}")
                        ax.bar(["Max","Mean","Min"], [max(Filter[Filter['hour'] == hour]['number_people'])+ standard_deviation(max(Filter[Filter['hour'] == hour]['number_people']),weather,weekend),round(Filter[Filter['hour'] == hour]['number_people'].mean(),2)+ standard_deviation(round(Filter[Filter['hour'] == hour]['number_people'].mean(),2),weather,weekend),min(Filter[Filter['hour'] == hour]['number_people'])+ standard_deviation(min(Filter[Filter['hour'] == hour]['number_people']),weather,weekend)], color = "green",label='plus Standard deviation')
                        ax.bar(["Max","Mean","Min"], [max(Filter[Filter['hour'] == hour]['number_people']),round(Filter[Filter['hour'] == hour]['number_people'].mean(),2),min(Filter[Filter['hour'] == hour]['number_people'])], color = "yellow",label='No Standard deviation')
                        ax.bar(["Max","Mean","Min"], [max(Filter[Filter['hour'] == hour]['number_people'])- standard_deviation(max(Filter[Filter['hour'] == hour]['number_people']),weather,weekend),round(Filter[Filter['hour'] == hour]['number_people'].mean(),2)- standard_deviation(round(Filter[Filter['hour'] == hour]['number_people'].mean(),2),weather,weekend),min(Filter[Filter['hour'] == hour]['number_people'])- standard_deviation(min(Filter[Filter['hour'] == hour]['number_people']),weather,weekend)], color = "red", label='minus Standard deviation')
                        ax.set_xlabel('AmountPPl')
                        ax.set_title(f"Prediction People and Standard Deviation")
                        ax.legend()
                        plt.show()
                except Exception as e: 
                    messagebox.showinfo("Workout",e)
    except:
        messagebox.showerror("TempFile","Microbit.csv is not in the path location")
def standard_deviation(AmountofPPl,weather,weekend):
    if weekend:
        AmountofPPl= AmountofPPl*.75
    StandardDeviation = 0.5 * AmountofPPl**1/2
    if weather == "Bad":
        StandardDeviation = StandardDeviation + StandardDeviation*0.5
    elif weather == "Good":
        StandardDeviation = StandardDeviation + StandardDeviation*0.25
    return StandardDeviation
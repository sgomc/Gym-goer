import matplotlib.pyplot as plt
from tkinter import simpledialog, messagebox
import math
def visualbmi(Weight,Height,user_name):

    bmiCategoriesDict = {
        'Underweight/Overweight': (24.0, 16.0),
        'Slightly Underweight/Overweight': (24.0, 12.0),
        'Morbidly Obese':(29.0, 2.0),
        'Normal': (21.75, 6.5)
    }
    

    BMI = float(Weight)/math.pow(float(Height),2)


    for category, (threshold, width) in bmiCategoriesDict.items():
        if BMI <= threshold:
            break

    
    colors = {
        'Underweight/Overweight': 'red',
        'Morbidly Obese':'orange',
        'Slightly Underweight/Overweight': 'yellow',
        'Normal': 'greenyellow'
    }

   
    fig, ax = plt.subplots()


    for cat, (value, bar_width) in bmiCategoriesDict.items():
        color = colors[cat]
        ax.bar(value, 1, color=color, label=cat, width=bar_width)

 
    ax.axvline(x=BMI, color='black', linestyle='--')

   
    plt.text(BMI, 1.1, f'{BMI:.1f}', color='black', ha='center', va='center', fontsize=12, fontweight='bold')

  
    ax.set_ylim(0, 1)


    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)


    ax.set_xlim(16, 32)


    ax.legend()
    ax.set_title(f"{user_name}s BMI result")

    plt.show()







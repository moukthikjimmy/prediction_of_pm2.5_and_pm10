import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
from PIL import ImageTk
selected_mine = ""

def on_select(selection):
    global selected_mine
    selected_mine = selection

def predict_PM(list_x, index):
    # Handling missing mining parameters by replacing with 0.0
    list_x_numeric = [float(x) if str(x).replace('.', '', 1).isdigit() else 0.0 for x in list_x]
    xls = pd.ExcelFile(excelfile)
    mydata = pd.read_excel(xls, filename)
    
    # Handling missing meteorological parameters by replacing with average values
  
    x_train = mydata.iloc[:, :10]
    y_train = mydata.iloc[:, 10 + index]
    x_train, _, y_train, _ = train_test_split(x_train, y_train, test_size=0.05, random_state=50)
    
    mybagmodel = RandomForestRegressor(criterion='squared_error', max_features='sqrt')
    mybagmodel.fit(x_train, y_train)
    
    list_x_arr = np.array(list_x_numeric).reshape(1, -1)
    pred = mybagmodel.predict(list_x_arr)
    
    return pred[0]


def get_output_fields():
    if selected_mine == "BPA OC":
        return ["CHP", "WS", "Khairagpura", "Sonapur", "Bijal", "Gampalapalli"]
    elif selected_mine == "GK OC":
        return ["CHP", "WS", "Sitampet", "Penagadapa", "Tippanapalli", "RDP Colony"]
    elif selected_mine == "JVR OC":
        return ["CHP", "WS", "Kistaram", "Pallewada", "Sathupally", "Venkatapuram"]
    elif selected_mine == "KHG OC":
        return ["CHP", "WS", "Goverguda", "Ullipitta", "Chopri", "Ontimamidi"]
    elif selected_mine == "RG OC":
        return ["CHP", "WS", "Gunjapadugu", "Sector-III", "Julapalli", "Mulakalapalli"]
    else:
        return ["CHP", "WS", "Srirampur", "Ramaraopet", "Indaram", "Sitarampalli"]

def get_values():
    global output_frame
    global filename
    global excelfile
    global selected_mine
    
    # Check if a mine is selected
    if selected_mine == "Select":
        return
    
    mining_values = [mining_entry_vars[i].get() if mining_entry_vars[i].get() else 0.0 for i in range(5)]
    meteorological_values = [meteorological_entry_vars[i].get() if meteorological_entry_vars[i].get() else None for i in range(5)]
    
    values = mining_values + meteorological_values
    
    season = ""
    if radio_var1.get() == 1:
        season = "Sumr"
    elif radio_var1.get() == 2:
        season = "Rain"
    elif radio_var1.get() == 3:
        season = "Wint"
        
    predict = "PM 2.5" if radio_var2.get() == 1 else "PM 10"
    
    filename = f"{selected_mine} {predict} {season}"
    excelfile = f"{selected_mine}_for_programming.xlsx"
    
    output_label.config(text="")
    xls = pd.ExcelFile(excelfile)
    mydata = pd.read_excel(xls, filename)
    
    # Compute the average values of meteorological parameters
    avg_meteorological_values = mydata.iloc[:, 5:10].mean().tolist()
    
    # Replace missing meteorological parameters with the average values
    for i, val in enumerate(meteorological_values):
        if val is None:
            meteorological_values[i] = avg_meteorological_values[i]
    
    values = mining_values + meteorological_values
    output_fields = get_output_fields()
    predictions = [round(predict_PM(values, i), 2) for i in range(len(output_fields))]  # Round predictions to 2 decimal points
    
    for i, prediction in enumerate(predictions):
        output_entry_vars[i].set(prediction)
    
    for i, field in enumerate(output_fields):
        label = ttk.Label(output_frame, text=field)
        label.grid(row=i+1, column=0, padx=10, sticky="w")
    
    # Only display the output frame if a mine is selected
    if selected_mine != "":
        output_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    
    output = f"Mine: {selected_mine}\n Season: {season}\n Parameter: {predict}\n Excel file: {excelfile}"
    output_label.config(text=output)


primary_color = "#3498db"
secondary_color = "#2980b9"
background_color = "#006400"  # Define the green color hex code

root = tk.Tk()
root.title("PREDICTION OF PM 10 AND PM 2.5")
root.configure(bg="light green")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.9)
window_height = int(screen_height * 0.9)
x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
root.configure(bg="light green")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

style = ttk.Style()
style.configure("Bordered.TFrame", borderwidth=2, relief=tk.SOLID)

main_frame = ttk.Frame(root, style="Green.TFrame")
main_frame.pack(fill=tk.BOTH, expand=True)

input_frame1 = ttk.Frame(main_frame, style="Bordered.TFrame")
input_frame1.grid(row=0, column=0, padx=10, pady=10)

input_frame2 = ttk.Frame(main_frame, style="Bordered.TFrame")
input_frame2.grid(row=0, column=1, padx=10, pady=10)

input_frame3 = ttk.Frame(main_frame, style="Bordered.TFrame")
input_frame3.grid(row=0, column=2, padx=10, pady=10)

output_frame = tk.Frame(main_frame, bg='light green', bd=2, relief=tk.SOLID)
output_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")
output_frame.grid_remove()

line_label = ttk.Label(input_frame1, text="Select the mine, PM & season ", font=("Arial", 14, "bold"))
line_label.grid(row=0, column=0, pady=0, padx=0, sticky="w")

variable = tk.StringVar(root)
options = ["Select", "BPA OC", "KHG OC", "SRP OC", "RG OC", "GK OC", "JVR OC"]
variable.set("Select")  
dropdown = ttk.OptionMenu(input_frame1, variable, "Select", *options, command=lambda value: on_select(value))
dropdown.grid(row=1, column=0, pady=5, padx=0, sticky="w")

radio_frame = ttk.Frame(input_frame1)
radio_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

radio_var1 = tk.IntVar()
radio_var2 = tk.IntVar()

radio_label2 = ttk.Label(radio_frame, text="Predict :")
radio_label2.grid(row=0, column=0, sticky="w")
radio2_option1 = ttk.Radiobutton(radio_frame, text="PM 2.5", variable=radio_var2, value=1)
radio2_option1.grid(row=1, column=0, sticky="w")
radio2_option2 = ttk.Radiobutton(radio_frame, text="PM 10", variable=radio_var2, value=2)
radio2_option2.grid(row=2, column=0, sticky="w")

radio_label1 = ttk.Label(radio_frame, text="Enter the season :")
radio_label1.grid(row=3, column=0, sticky="w")
radio1_option1 = ttk.Radiobutton(radio_frame, text="Summer", variable=radio_var1, value=1)
radio1_option1.grid(row=4, column=0, sticky="w")
radio1_option2 = ttk.Radiobutton(radio_frame, text="Rainy", variable=radio_var1, value=2)
radio1_option2.grid(row=5, column=0, sticky="w")
radio1_option3 = ttk.Radiobutton(radio_frame, text="Winter", variable=radio_var1, value=3)
radio1_option3.grid(row=6, column=0, sticky="w")

mining_parameters_label = ttk.Label(input_frame2, text="Mining Parameters", font=("Arial", 14, "bold"))
mining_parameters_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

mining_titles = [
    "Production (Coal+OB) [in Te/day]",
    "Area contributing to pollution [in hectares]",
    "Max. Quarry depth [in m]",
    "Max. Dump height [in m]",
    "Lead distance [in km]"
]
mining_entry_vars = [tk.StringVar() for _ in range(5)]
mining_frame = ttk.Frame(input_frame2)
mining_frame.grid(row=1, column=0, pady=5, padx=10, sticky="w")

for i in range(5):
    title_label = ttk.Label(mining_frame, text=mining_titles[i])
    title_label.grid(row=i, column=0, padx=10, sticky="w")
    entry = ttk.Entry(mining_frame, textvariable=mining_entry_vars[i])
    entry.grid(row=i, column=1, sticky="w")

meteorological_parameters_label = ttk.Label(input_frame3, text="Meteorological Parameters", font=("Arial", 14, "bold"))
meteorological_parameters_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

meteorological_titles = [
    "Predominant wind direction [in degrees]",
    "Avg Temp [in degree Celsius]",
    "Avg Humidity [in %]",
    "Avg Rainfall [in mm]",
    "Avg Wind speed [in m/s]"
]
meteorological_entry_vars = [tk.StringVar() for _ in range(5)]
meteorological_frame = ttk.Frame(input_frame3)
meteorological_frame.grid(row=1, column=0, pady=5, padx=10, sticky="w")

for i in range(5):
    title_label = ttk.Label(meteorological_frame, text=meteorological_titles[i])
    title_label.grid(row=i, column=0, padx=10, sticky="w")
    entry = ttk.Entry(meteorological_frame, textvariable=meteorological_entry_vars[i])
    entry.grid(row=i, column=1, sticky="w")

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=2, column=0, columnspan=3, pady=10)

style = ttk.Style()
style.configure('DarkGreen.TButton', foreground='black', background='#006400')

get_values_button = ttk.Button(button_frame, text="Predict", command=get_values, style='DarkGreen.TButton')
get_values_button.pack()

output_label = ttk.Label(output_frame, text="Output Values", font=("Arial", 14, "bold"))
output_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

output_entry_vars = [tk.StringVar() for _ in range(6)]

for i in range(6):
    entry = ttk.Entry(output_frame, textvariable=output_entry_vars[i])
    entry.grid(row=i+1, column=1, padx=10, sticky="w")

root.mainloop()

import pandas as pd
import numpy as np
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#     df = pd.read_csv("Example.csv")
   

def open_file():
    filename = filedialog.askopenfilename(
    title = "Choose your file",
    filetypes = (("csv files", "*.csv"), ("all files", "*.*")),
    defaultextension = '.csv',
    initialdir = '.')
    return filename


def save_file():
    filename = filedialog.asksaveasfilename(
    title = "Save file",
    filetypes = (("csv files", "*.csv"), ("all files", "*.*")),
    defaultextension = '.csv',
    initialdir = '.',
    initialfile = 'transformed.csv' )
    if filename != "":
        df.to_csv(filename)


def hacer(event):
    global df

    fich = open_file()
    id_entry.set (fich)
    df = pd.read_csv (fich)
#    print("Original Data Frame:\n", df)

    nan = ttk.Label(win_root, text = "Convert 'NaN' to '0'?:")
    nan.grid(row=1, column=0, sticky=tk.E)
    nanrad1 = tk.Radiobutton(win_root, text="Yes", variable = nanrad, value=1)
    nanrad2 = tk.Radiobutton(win_root, text="No", variable = nanrad, value=0)
    nanrad1.grid(row=1, column = 1, sticky=tk.W)
    nanrad2.grid(row=1, column = 1)
    nanrad1.deselect()
    nanrad2.select()
    button.grid(row=1, column=2, sticky=tk.W)

def cleannan():
    global df
    global c
    if nanrad.get():
        df.fillna(0, inplace=True)
        label.config(text = "STATE: NaN deleted" )
    button.config(state="disabled")

    c=0
    for column in df.columns:
        if df[column].dtypes in ["object"]:
            change = True
            for i in range (0,len(df)):
                if (re.match(r"[-+]?\d+(\.\d+)?$", str(df[column][i]).strip()) is None):
                    if (not pd.isnull(df[column][i]) and df[column][i].strip() != ''):
                        change = False
            if change:
                a = tk.Label(win_root, text="Remove whitespaces from numeric columns:")
                a.grid(row=4, column=0, sticky=tk.W, columnspan=2)
                a = tk.Label(win_root, text=column)
                a.grid(row=5+c, column=0, sticky=tk.E)
                enval = tk.StringVar()
                en1 = tk.Radiobutton(win_root, text="Yes", variable = enval, value=column)
                en2 = tk.Radiobutton(win_root, text="No", variable = enval, value="_NO_")
                en1.grid(row=5+c, column = 1, sticky=tk.W)
                en2.grid(row=5+c, column = 1)
                en1.deselect()
                en2.select()
                entriesval.append(enval)
        c += 1
#    print("Antes de cleanwhitespaces\n", df)
    button2.grid(row=4+c, column=2, sticky=tk.W)


def cleanspaces():
    global df
    global c2
    
    button2.config(state="disabled")
    mess = "STATE: "
    for entry in entriesval:
        e = entry.get()
        if (e>"_NO_"):
            df[e].replace(r"^\s+$", '0', regex=True, inplace=True)
            df[e].replace(r"\s+", '', regex=True, inplace=True)
            df[e] = pd.to_numeric(df[e], errors='coerce')
        mess += str(entry.get())
    label.config(text = mess )

    # Detect outliers and calculates the possible values to sustitute them
    data = {}
    c2=0
    first = True
    for column in df.columns:
        if df[column].dtypes in ["int64", "float64"]:
            max = np.max(df[column])        
            p75 = df[column].quantile(0.75)
            p50 = df[column].quantile(0.5)
            p25 = df[column].quantile(0.25)
            min = np.min(df[column])        
            mean = df[column].mean()
            iqr = p75 - p25
            valueslist = [p25-1.5*iqr, min, p25, p50, mean, p75, max, p75 + 1.5*iqr]
            tagslist = ["LOWER", "MIN", "P25", "P50", "Mean", "P75", "MAX", "UPPER"]
            data.update({column : pd.Series([df[column].dtypes]+valueslist, index=["Type"]+tagslist)})
            for i in range (0,len(df)):
                if (df[column][i] > (p75 + 1.5*iqr)) or (df[column][i] < (p25 - 1.5*iqr)):
                    if first:
                        a = tk.Label(win_root, text="Process outliers:")
                        a.grid(row=5+c, column=0, sticky=tk.W)
                        first=False
                    a = tk.Label(win_root, text=column + ": " + str(df[column][i]))
                    a.grid(row=6+c+c2, column=0, sticky=tk.E)
                    choice = tk.StringVar()
                    chosen = ttk.Combobox(win_root, width=12, textvariable=choice, value=column, state="readonly")
                    chosenlist = ["ITSELF: " + str(df[column][i])]
                    for j in range (0,len(tagslist)):
                        chosenlist.append(tagslist[j] + ": " + str(valueslist[j]))
                    chosen['values']= tuple(chosenlist)
                    chosen.grid(row=6+c+c2, column=1)
                    c2 += 1
                    chosen.current(0)
                    choices.append([column, i, choice])
    button3.grid(row=7+c+c2, column=2, sticky=tk.W)

def processoutliers():
    global df
    
    mess = "STATE: "
    for choice in choices:
        col = choice[0]
        i = choice[1]
        ch = choice[2].get().split()[1]
        df.set_value(i, col, ch)
        mess += col + "," + str(i) + ": " +str(ch) + "; "
    label.config(text = mess )
    print("Transformed Data Frame\n", df)
    print(df.dtypes)
    button4=tk.Button(win_root,text="Save Restults",command=lambda: save_file())
    button4.grid(row=8+c+c2, column=1)
    
    
# START MAIN
np.seterr(invalid='ignore')
entriesval = []
choices = []
df = pd.DataFrame

#Create main window
win_root = tk.Tk() 

win_root.title("Data Cleaning")
win_root.geometry("800x800")
win_root.resizable(width=True, height=True)

label1 = ttk.Label(win_root, text="File to clean:",font=("Helvetica", 10), foreground="black")
label1.grid(row=0,column=0)

id_entry = tk.StringVar()
id_entered = ttk.Entry(win_root, width = 30, textvariable = id_entry)
id_entered.grid(row = 0, column = 1, sticky = tk.E)

but = ttk.Button(win_root, text = "Browse computer")
but.bind ("<Button-1>", hacer)
but.grid(row=0, column=2, sticky=tk.E)
but.focus()

nanrad = tk.IntVar()
button=tk.Button(win_root,text="Clean NaN",command=lambda: cleannan())
button2=tk.Button(win_root,text="Clean Whitespaces",command=lambda: cleanspaces())
button3=tk.Button(win_root,text="Process Outliers",command=lambda: processoutliers())

label = ttk.Label(win_root, text="STATE:")
label.grid(row=1000, column=0, columnspan=3, sticky=tk.W)

win_root.mainloop()
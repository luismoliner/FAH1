import pandas as pd
import numpy as np
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#     data = pd.read_csv("Example.csv")
   
def total(data):
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
        initialfile = 'transformed.csv')
        if filename != "":
            data.to_csv(filename, index=False)
    
    
    def start():
        global data
    
#        fich = open_file()
#        id_entry.set (fich)
#        data = pd.read_csv (fich)
        print("Original Data Frame:\n", data)
    
    # Prepare interface to ask about NaN
        nan = ttk.Label(win_root, text = "Convert 'NaN'?:")
        nan.grid(row=1, column=0, sticky=tk.E)
        nanrad1 = tk.Radiobutton(win_root, text="No", variable = nanrad, value=0)
        nanrad2 = tk.Radiobutton(win_root, text="0", variable = nanrad, value=1)
        nanrad3 = tk.Radiobutton(win_root, text="Most Freq", variable = nanrad, value=2)
        nanrad1.grid(row=1, column = 1, sticky=tk.W)
        nanrad2.grid(row=1, column = 1)
        nanrad3.grid(row=1, column = 1, sticky=tk.E)
        nanrad1.deselect()
        nanrad2.select()
        nanrad3.deselect()
        button1.grid(row=1, column=2, sticky=tk.W)
        state.config(text = "\nHow to proceed with NaN?" )
    
    
    def cleannan():
        global data
        global c
    # NaN are not replaced
        if nanrad.get() == 0:
            state.config(text = "NaN not converted. Select columns to remove whitespaces." )
    # NaN are replaced by 0
        if nanrad.get() == 1:
            data.fillna(0, inplace=True)
            state.config(text = "'NaN' -> 0. Select columns to remove whitespaces." )
    # NaN are replaced by the most frequent vlaue: mode
        if nanrad.get() == 2:
            modes = data.mode()
            for column in data.columns:
                data[column].fillna(modes[column][0], inplace=True)
            state.config(text = "NaN to Most Frequent. Select columns to remove whitespaces." )
        button1.config(state="disabled")
#        button0.config(state="disabled")
        button2.focus()
    
    # Prepare intereface to remove whitespaces from columns if all the values can be numeric
        c=0
        first = True
        for column in data.columns:
            if data[column].dtypes in ["object"]:
                change = True
                for i in range (0,len(data)):
                    if (re.match(r"[-+]?\d+(\.\d+)?$", str(data[column][i]).strip()) is None):
                        if (not pd.isnull(data[column][i]) and data[column][i].strip() != ''):
                            change = False
                if change:
                    if first:
                        a = tk.Label(win_root, text="Do you want to remove whitespaces from numeric columns?")
                        a.grid(row=4, column=0, sticky=tk.W, columnspan=2)
                        first=False
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
        button2.grid(row=4+c, column=2, sticky=tk.W)
    
    
    def cleanspaces():
        global data
        global c2
        
        button2.config(state="disabled")
        button3.focus()
        mess = "Whitespaces removed from: "
        for entry in entriesval:
            e = entry.get()
            if (e != "_NO_"):
    # If the value is a set of whitespaces, they are replaced by 0, otherwise
    # whitespaces are deleted and finally the column type is changed to numeric
                data[e].replace(r"^\s+$", '0', regex=True, inplace=True)
                data[e].replace(r"\s+", '', regex=True, inplace=True)
                data[e] = pd.to_numeric(data[e], errors='coerce')
                mess += str(entry.get() + ", ")
        mess = mess[:-2] + ". What about outliers?"
        state.config(text = mess )
    
    # Prepares interface to process outliers. Calculates possible values to sustitute outliers
        datadict = {}
        c2=0
        first = True
        for column in data.columns:
            if data[column].dtypes in ["int64", "float64"]:
                max = np.max(data[column])        
                p75 = data[column].quantile(0.75)
                p50 = data[column].quantile(0.5)
                p25 = data[column].quantile(0.25)
                min = np.min(data[column])        
                mean = data[column].mean()
                iqr = p75 - p25
                valueslist = [p25-1.5*iqr, min, p25, p50, mean, p75, max, p75 + 1.5*iqr]
                tagslist = ["LOWER", "MIN", "P25", "P50", "Mean", "P75", "MAX", "UPPER"]
                datadict.update({column : pd.Series([data[column].dtypes]+valueslist, index=["Type"]+tagslist)})
    # If it is binary don't detect outliers
                if (set(data[column]) == {0,1}):
                    continue
    # Loops the values in a column looking for extreme values
    # When it finds extreme values prepares the interface to sustitute them, offering several choices
                for i in range (0,len(data)):
                    if (data[column][i] > (p75 + 1.5*iqr)) or (data[column][i] < (p25 - 1.5*iqr)):
                        if first:
                            a = tk.Label(win_root, text="How do you want to process outliers?")
                            a.grid(row=5+c, column=0, columnspan=2, sticky=tk.W)
                            first=False
                        a = tk.Label(win_root, text=column + ": " + str(data[column][i]))
                        a.grid(row=6+c+c2, column=0, sticky=tk.E)
                        choice = tk.StringVar()
                        chosen = ttk.Combobox(win_root, width=12, textvariable=choice, value=column, state="readonly")
    # There is a choice "ITSELF" if this outlier is not desired to be changed
                        chosenlist = ["ITSELF: " + str(data[column][i])]
                        for j in range (0,len(tagslist)):
                            chosenlist.append(tagslist[j] + ": " + str(valueslist[j]))
                        chosen['values']= tuple(chosenlist)
                        chosen.grid(row=6+c+c2, column=1)
                        c2 += 1
                        chosen.current(0)
                        choices.append([column, i, choice])
        button3.grid(row=7+c+c2, column=2, sticky=tk.W)
    
    def processoutliers():
        global data
        
        mess = "\nOutliers replaced:\n"
    # Changes outliers for the selected values
        for choice in choices:
            col = choice[0]
            i = choice[1]
            ch = choice[2].get().split()[1]
            data.set_value(i, col, ch)
            mess += "- " + col + "[" + str(i) + "] -> " +str(ch) + "\n"
        mess = mess + "New changes can be proposed.\n"
        mess = mess + "Click 'Save Results' after.\n"
        mess = mess + "Thank you for using this program!!!"
        state.config(text = mess )
        print("Transformed Data Frame\n", data)
    #    print(data.dtypes)
        button4=tk.Button(win_root,text="Save Restults",command=lambda: save_file())
        button4.grid(row=8+c+c2, column=1, sticky=tk.W)
        button5=tk.Button(win_root,text="Exit",command=lambda: root.destroy())
        button5.grid(row=8+c+c2, column=1, sticky=tk.E)
        button4.focus()
    
    
    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    
    # START MAIN
    np.seterr(invalid='ignore')
    entriesval = []
    choices = []
#    data = pd.DataFrame
    
    # Creates main window
    root = tk.Tk()
    root.title("Data Cleaning")
    root.geometry("600x800")
    root.resizable(width=True, height=True)
    canvas = tk.Canvas(root, borderwidth=0) #, background="#ffffff")
    win_root = tk.Frame(canvas) #, background="#ffffff")
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    vsb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=vsb.set)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=win_root, anchor="nw")
    win_root.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    
    label1 = ttk.Label(win_root, text="- Human Assisted Cleaner -\n",font=("Helvetica", 12), foreground="black")
    label1.grid(row=0,column=1)
#    
#    id_entry = tk.StringVar()
#    id_entered = ttk.Entry(win_root, width = 30, textvariable = id_entry)
#    id_entered.grid(row = 0, column = 1, sticky = tk.E)
    
#    button0 = tk.Button(win_root, text = "Browse computer")
#    button0.bind ("<Button-1>", start)
#    button0.grid(row=0, column=2, sticky=tk.W)
#    button0.focus()
    button1 = tk.Button(win_root,text = "Go", command=lambda: cleannan())
    button2 = tk.Button(win_root,text = "Go", command=lambda: cleanspaces())
    button3 = tk.Button(win_root,text = "Go", command=lambda: processoutliers())
    
    nanrad = tk.IntVar()
    
    state = ttk.Label(win_root, text="\nPlease, press \"Browse computer\" to select a file to clean.")
    state.grid(row=1000, column=0, columnspan=3, sticky=tk.W)
    
    start()
    root.mainloop()


data = pd.read_csv("Example.csv")
total (data)

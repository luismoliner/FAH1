import pandas as pd
import numpy as np
import re
import tkinter as tk
from tkinter import messagebox as mBox
from tkinter import ttk
from tkinter import filedialog


#from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt
#from sklearn.decomposition import PCA
#import pylab as pl
#import pylab as p
#import matplotlib


def funcion ():
    df = pd.read_csv("Example.csv")
    #pd.set_option('display.max_rows', len(df))
    print("Original Data Frame\n", df)
    
    # Replace all NaN with 0
    df.fillna(0, inplace=True)
    
    # If all the values in the column are float and whitespaces (one or several), replaces the latter with 0
    # Removes spaces before or after the numbers
    # print(df)
    for column in df.columns:
        if df[column].dtypes in ["object"]:
            change = True
            for i in range (0,len(df)):
    #            if not df[column][i].replace('.','',1).isdigit(): Fails with NEG
                if df[column][i].strip() != '':
                    continue
                if (re.match(r"[-+]?\d+(\.\d+)?$", df[column][i].strip()) is None):
    #                    print (column, i, df[column][i])
                    change = False
    #        print (column, change)
            if change:
                df[column]= df[column].replace(r"\s+", 0, regex=True)
                df[column] = pd.to_numeric(df[column], errors='coerce')
    
    ## Fuerza la conversión de la columna a número sustituyendo strings por NaN
    #######################33
    #    df["var3"] = pd.to_numeric(df["var3"], errors='coerce')
    
    
    # Replace outliers and out of range, for the border values
    data = {}
    for column in df.columns:
    #    print (column, df[column].dtypes)
        if df[column].dtypes in ["int64", "float64"]:
    #        print ("Vale")
            max = np.max(df[column])        
            p75 = df[column].quantile(0.75)
            p50 = df[column].quantile(0.5)
            p25 = df[column].quantile(0.25)
            min = np.min(df[column])        
            mean = df[column].mean()
            iqr = p75 - p25
            data.update({column : pd.Series([df[column].dtypes, min, p25, p50, mean, p75, max], index=["Type", "MIN", "P25", "P50", "Mean", "P75", "MAX"])})
    #        print (column, df[column].dtypes, p25, p50, p75, mean)
            for i in range (0,len(df)):
                if (df[column][i] > (p75 + 1.5*iqr)):
                    df.set_value(i, column, p75 + 1.5*iqr)
                if (df[column][i] < (p25 - 1.5*iqr)):
                    df.set_value(i, column, p25 - 1.5*iqr)
    print ("\nInfo about the columns to transform:\n", pd.DataFrame(data),"\n")
    
    print("Transformed Data Frame\n", df)


def v_save_file():
    filename = filedialog.asksaveasfilename(
    #initialdir = r"C:\Users\Rangga Ugahari\Desktop\Pythoncode",
    title = "save file",
    filetypes = (("dat files", "*.dat"), ("all files", "*.*")),
    defaultextension = '.dat',
    initialdir = './files',
    initialfile = 'pos.dat' )
    return filename


def v_open_file():
    filename = filedialog.askopenfilename(
    #initialdir = r"C:\Users\Rangga Ugahari\Desktop\Pythoncode",
    title = "Choose your file",
    filetypes = (("csv files", "*.csv"), ("all files", "*.*")),
    defaultextension = '.csv',
    initialdir = '.')
#   , initialfile = 'pos.dat' )
    return filename


def sel():
    selection = "You selected the option " + str(nanrad.get())
    label.config(text = selection)


def selcols(c, selcols):
    selection = "You selected the option " + str(radcols[c].get())
    label.config(text = selection)
    selcols[c] = 4
    selection = "You selected the option " + str(selcols)


def hacer(event):
#    mBox.showinfo('Info inputed', 'Name:'+id_entry.get()+"Student:"+chstvar.get()+"Male"+chmalevar.get()+"Female"+chfemalevar.get())
    fich = v_open_file()
    id_entry.set (fich)
    df = pd.read_csv (fich)
    df.is_copy = False
    print("Original Data Frame:\n", df)

    nan = ttk.Label(win_root, text = "Convert 'NaN' to '0'?:")
    nan.grid(row=1, column=0, sticky=tk.W)
#    nanrad=1
#    nanrad = tk.IntVar()
    nanrad1 = tk.Radiobutton(win_root, text="Yes", variable = nanrad, value=1, command=sel)
    nanrad2 = tk.Radiobutton(win_root, text="No", variable = nanrad, value=0, command=sel)
    nanrad1.grid(row=1, column = 1, sticky=tk.W)
    nanrad2.grid(row=1, column = 1)
    button=tk.Button(win_root,text="Clean NaN",command=lambda: cleannan(df))
    button.grid(row=1, column=2)
#      command= lambda: analyze("BACKUP")  

def cleannan(df):
    df.is_copy = False
    print ("En cleannan:\n", df)
    if nanrad.get():
        df.fillna(0, inplace=True)
    print ("En cleannan2:\n", df)

    c=0







    for column in df.columns:
        if df[column].dtypes in ["object"]:
            change = True
            for i in range (0,len(df)):
    #            if not df[column][i].replace('.','',1).isdigit(): Fails with NEG
    #            print (column, i)
                if (re.match(r"[-+]?\d+(\.\d+)?$", str(df[column][i]).strip()) is None):
#                if (re.match(r"[-+]?\d+(\.\d+)?$", df[column][i].strip()) is None):
                    if (not pd.isnull(df[column][i]) and df[column][i].strip() != ''):
#                    if (not pd.isnull(df[column][i]) and df[column][i].strip() != ''):
    #                    print (column, i, df[column][i])
                        change = False
    #        print (column, change)
#            v = tk.StringVar()
#            v.set("L")
            if change:
                a = tk.Label(win_root, text="Remove spacces from numeric columns:")
                a.grid(row=4, column=0)
                a = tk.Label(win_root, text=column)
                a.grid(row=5+c, column=0)
#                nan.grid(row=1, column=0, sticky=tk.W)
                enval = tk.IntVar()
                en1 = tk.Radiobutton(win_root, text="Yes", variable = enval, value=c+1) #, command=selcols(c, selcols))
                en2 = tk.Radiobutton(win_root, text="No", variable = enval, value=0) #, command=selcols(c, selcols))
                en1.grid(row=5+c, column = 1, sticky=tk.W)
                en2.grid(row=5+c, column = 1)
                entriesval.append(enval)
                entries.append(en1)
                entries.append(en2)
#                print(c)
        c += 1
    print("Antes de cleanwhitespaces\n", df)
    button=tk.Button(win_root,text="Clean Whitespaces",command=lambda: cleanspaces(df))
    button.grid(row=4+c, column=2)
              
                
#                choice = tk.StringVar()
#                chosen = ttk.Combobox(win_root, width=12, textvariable="HI", state="readonly")
#                chosen["values"] = (1,2,4,42)
#                chosen.grid(row=5+c, column=1)
#                chosen.current(0)
#                df[column]= df[column].replace(r"\s+", 0, regex=True)
#                df[column] = pd.to_numeric(df[column], errors='coerce')


def cleanspaces(df):
    pd.options.mode.chained_assignment = None
    df.is_copy = False
    print ("En cleanspaces:\n", df)
    mess = ""
    for entry in entriesval:
        e = entry.get()
        print ("e:", e, "mess:", mess)
        if (e>0):
            print ("df[[(e-1)]]:\n", df[[(e-1)]], df)
#            df[[(e-1)]] = df[[(e-1)]].replace(r"^\s+$", '0', regex=True)
            df[[(e-1)]].replace(r"^\s+$", '0', regex=True, inplace=True)
            print("HOLA\n", df[[(e-1)]], df)
#            df[[(e-1)]]= df[[(e-1)]].replace(r"\s+", '', regex=True)
            df[[(e-1)]].replace(r"\s+", '', regex=True, inplace=True)
            print("HOLA2\n", df[[(e-1)]], df)
#            df[[(e-1)]] = pd.to_numeric(df[[(e-1)]], errors='coerce')
#            df[[(e-1)]].to_numeric(df[[(e-1)]], errors='coerce', inplace=True)
            df.apply(lambda x: pd.to_numeric(x, errors='ignore'))
#        print(entry.get())
        mess += str(entry.get())
    label.config(text = mess )
    print("Transformed Data Frame\n", df)
    

#Create main window
np.seterr(invalid='ignore')
pd.set_option('mode.chained_assignment','raise')
# selcols = np.zeros(len(df.columns))
entries = []
entriesval = []
df = pd.DataFrame

win_root = tk.Tk() 

win_root.title("Data Cleaning")
win_root.geometry("800x200")
win_root.resizable(width=True, height=True)

label1 = ttk.Label(win_root, text="File to clean:",font=("Helvetica", 10), foreground="black")
label1.grid(row=0,column=0)

id_entry = tk.StringVar()
id_entered = ttk.Entry(win_root, width = 50, textvariable = id_entry)

id_entered.grid(row = 0, column = 1)

#chstvar = tk.StringVar()
#chst = ttk.Checkbutton(win_root, text ="Student", variable = chstvar)
#chst.grid(row=2, column=0, sticky=tk.W)
#chmalevar = tk.StringVar()
#chmale = ttk.Checkbutton(win_root, text ="Male", variable = chmalevar)
#chmale.grid(row=2, column=1)
#chfemalevar = tk.StringVar()
#chfemale = ttk.Checkbutton(win_root, text ="Female", variable = chfemalevar)
#chfemale.grid(row=2, column=2)

but = ttk.Button(win_root, text = "Browse computer")
but.bind ("<Button-1>", hacer)
but.grid(row=0, column=2)
but.focus()

nanrad = tk.IntVar()

label = ttk.Label(win_root, text="Initial text")
label.grid(row=100, column=0, sticky=tk.W)

#    if rad.get():
#        print ("Yes")
#    else:
#        print ("No")
# 

win_root.mainloop()

#    ncols = len(df.columns)
#    selcols = np.zeros(ncols)
#mask = array([0,1,1,0,0,1,0,0], dtype=bool)


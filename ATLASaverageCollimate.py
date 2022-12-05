import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os

import matplotlib.pyplot as plt
import numpy as np

import math

def avgCompile(catapult, tarmac):
    """
    WARNING: run this only on files that already have daily values written on. The program relies on the
    "this is an averaged point" flag, and will give you nothing if that flag doesn't exist.
    """
    
    files = os.listdir(catapult)

    nameOnly = files[0][:-20]
    #print(nameOnly)
    output = tarmac + "/" + nameOnly + "_avgCompile.csv"
    response = open(output, "w")

    headerCatch1 = open(catapult + "/" + files[0], "r")
    headerCatch2 = headerCatch1.readlines()
    header = headerCatch2[0]    #i write header first
    response.write(header)      #this is a trick that has taken me embarrassingly long to notice. investigate how this can be propagated.
                                #i DID notice it. i also noticed it causes newlines at the end. should not propagate.
    
    for file in files[:-1]:     #but maybe this could: do for all files/lines but the last; treat last line
        if file[-4:] != ".csv":
            continue

        source = catapult + "/" + file
        template = open(source, "r")

        inlines = template.readlines()

        if len(inlines) < 3:
            response.write(inlines[1]+"\n")
            continue
        
        for line in inlines[1:]:
            if line[-3:] == "11\n":
                response.write(line)
        
        template.close()

    source = catapult + "/" + files[-1]
    template = open(source, "r")

    inlines = template.readlines()

    if len(inlines) < 3:
        response.write(inlines[1])

    for line in inlines[1:]:
        if line[-3:] == "11\n":
            response.write(line[:-1])
    
    template.close()

    

    #response.readlines()[-1] = response.readlines()[-1][:-1]
    
    response.close()

    messagebox.showinfo("Finished","Average value compilation complete. Check destination folder.")

def main():
    #try:
        appWindow = tk.Tk()

        # Build a list of tuples for each file type the file dialog should display
        compatFiletypes = [('All files', '.*'), ('Comma-separated value files (.csv)', '.csv')]

        # Ask the user to select a single file name.
        #template = filedialog.askopenfilename(parent=appWindow,
        #                                    initialdir=os.getcwd(),
        #                                    title="Please select source file:",
        #                                    filetypes=compatFiletypes)


        takeoff = filedialog.askdirectory(parent=appWindow,
                                 initialdir=os.getcwd(),
                                 title="Please select source folder:")


        landing = filedialog.askdirectory(parent=appWindow,
                                 initialdir=os.getcwd(),
                                 title="Please select destination folder:")


        #if template[-4:] != ".csv":
        #    raise FileNotFoundError

        avgCompile(takeoff, landing)
        appWindow.destroy()

main()
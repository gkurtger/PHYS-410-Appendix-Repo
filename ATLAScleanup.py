import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os

import matplotlib.pyplot as plt
import numpy as np

import math



def MJDtoMMJD(source, tarmac):
    """
    Adds 0.5 to the MJD value in dataset.
    Day leaps that may result are not addressed.
    """
    template = open(source, "r")
    inlines = template.readlines()
    outlines = []
    response = open(tarmac, "w")
    
    inlines[0] = inlines[0][3:]     #should get rid of the pound signs

    for line in inlines:
        putline = line
        putline = line.split(",")
        putline.insert(1, "")
        outlines.append(putline)

    outlines[0][1] = "RJD"

    for line in outlines[1:]:   #FAR more efficient way of ignoring header. i should paste this to the other programs.
        mjd = float(line[0])
        mmjd = mjd+0.5
        line[1] = str(mmjd)

    for line in outlines:
        for item in line:
            if line!=outlines[-1]:
                if item == line[-1]:
                    data = item
                else:
                    data = item + ","
                response.write(data)
            else:
                if item == line[-1]:
                    if item[-1] != "\n":
                        data = item
                    else:
                        data = item[:-1]
                else:
                    data = item + ","
                response.write(data)
    

def sig3col(source, tarmac):
    """
    Adds a 3-sigma magnitude column to the datafile.
    """
    template = open(source, "r")
    inlines = template.readlines()
    outlines = []
    response = open(tarmac, "w")

    for line in inlines:
        putline = line
        putline = line.split(",")
        putline.insert(17, "")
        outlines.append(putline)

    outlines[0][17] = "mag3sig"

    for line in outlines[1:]:   #FAR more efficient way of ignoring header. i should paste this to the other programs.
        duJy = float(line[5])
        if(duJy > 0):
            mag3sig = math.log10(duJy)
            mag3sig = mag3sig * -2.5
            mag3sig = mag3sig + 23.9
            line[17] = str(mag3sig)
        else:
            line[17] = "N/A"

    for line in outlines:
        for item in line:
            if line!=outlines[-1]:
                if item == line[-1]:
                    data = item
                else:
                    data = item + ","
                response.write(data)
            else:
                if item == line[-1]:
                    if item[-1] != "\n":
                        data = item
                    else:
                        data = item[:-1]
                else:
                    data = item + ","
                response.write(data)

def timeError(source, tarmac):
    """
    Adds a time error column to the datafile -relevant to weighted average step-.
    """
    template = open(source, "r")
    inlines = template.readlines()
    outlines = []
    response = open(tarmac, "w")
    
    for line in inlines:
        putline = line
        putline = line.split(",")
        putline.insert(7, "")
        outlines.append(putline)

    outlines[0][7] = "dt"

    for line in outlines[1:]:   #FAR more efficient way of ignoring header. i should paste this to the other programs.
        line[7] = "0"
        
    for line in outlines:
        for item in line:
            if line!=outlines[-1]:
                if item == line[-1]:
                    data = item
                else:
                    data = item + ","
                response.write(data)
            else:
                if item == line[-1]:
                    if item[-1] != "\n":
                        data = item
                    else:
                        data = item[:-1]
                else:
                    data = item + ","
                response.write(data)

def putFlags(source, tarmac):
    """
    UNDER CONSTRUCTION.
    Adds a column to the datafile populated by flags that will determine inclusion in final results.
    Flags:
    0 - Clear
    1 - Point was beyond a 3-sigma measurement
    2 - Point was beyond a 5-sigma measurement
    3 - Error bars were too large
    4 - Magnitude value beyond what is sensible
    
    
    9 - A placeholder for values that created problems within previous steps 
    """
    template = open(source, "r")
    inlines = template.readlines()
    outlines = []
    response = open(tarmac, "w")

    for line in inlines:
        putline = line
        putline = line.split(",")
        putline[-1] = putline[-1][:-1] + ","
        putline.append("\n")
        outlines.append(putline)

    outlines[0][22] = "flag\n"

    for line in outlines[1:]:
        try:
            naCheck = float(line[17])
            if float(line[2]) > 20 or float(line[2]) < 0:    #this sets our tolerance to 0th to 20th magnitude, moddable
                line[22] = "4"
            elif float(line[3]) >= 0.5:      #this sets our error bar tolerance at 0.5 magnitudes, moddable
                line[22] = "3"
            elif float(line[4]) < 3*float(line[5]):          #works to see if uJy > 3duJy; as per 5sig requirements
                line[22] = "2"
            elif float(line[4]) < 5*float(line[5]):          #works to see if uJy > 5duJy; as per 3sig requirements
                line[22] = "1"
            else:
                line[22] = "0"

            if line != outlines[-1]:
                line[22] = line[22] + "\n"         #this is a fix to a bug that entailed an extraneous comma on EOF

        except ValueError:
            line[22] = "9\n"

    for line in outlines:
        idx = 0
        for item in line:
            if line!=outlines[-1]:
                if item == line[-1]:
                    data = item
                else:
                    data = item + ","
                response.write(data)
            else:
                if item == line[-1] and idx == len(line)-1:     #since the flag for the last line is 0, this erased a column that was also 0
                    if item[-1] != "\n":
                        data = item
                    else:
                        data = item[:-1]
                else:
                    data = item + ","
                response.write(data)
            idx += 1

def refiner(source, tarmac):
    """
    Function to execute the steps of initial refinement in order.
    """

    initialN = source
    nameOnly = source.split("/")
    finalN = tarmac + "/" + nameOnly[-1][:-4] + "_clean.csv"

    MJDtoMMJD(initialN, finalN)     #this function reads in the initial file, creates final file
    sig3col(finalN, finalN)        #argument placement not a typo: ensures these two functions work in-place on the final file
    timeError(finalN, finalN)
    putFlags(finalN, finalN)





def main():
    #try:
        appWindow = tk.Tk()

        # Build a list of tuples for each file type the file dialog should display
        compatFiletypes = [('All files', '.*'), ('Comma-separated value files (.csv)', '.csv')]

        # Ask the user to select a single file name.
        template = filedialog.askopenfilename(parent=appWindow,
                                            initialdir=os.getcwd(),
                                            title="Please select source file:",
                                            filetypes=compatFiletypes)


        #takeoff = filedialog.askdirectory(parent=appWindow,
        #                         initialdir=os.getcwd(),
        #                         title="Please select source folder:")


        landing = filedialog.askdirectory(parent=appWindow,
                                 initialdir=os.getcwd(),
                                 title="Please select destination folder:")


        if template[-4:] != ".csv":
            raise FileNotFoundError

        refiner(template, landing)
        messagebox.showinfo("Finished","Initial refinements complete. Check destination folder.")

    #except FileNotFoundError:
    #    messagebox.showerror("Error", "File does not exist, or is incompatible. Exiting.")
    #    appWindow.destroy()


main()
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os

import matplotlib.pyplot as plt
import numpy as np

import math


def writeAvg(catapult, tarmac):
    """
    Writes the weighted average calculated onto an output CSV.
    """
    files = os.listdir(catapult)

    for file in files:
        if file[-4:] != ".csv":     #this way, non-csv are ignored
            continue

        source = catapult + "/" + file
        template = open(source, "r")
        nameOnly = source.split("/")
        output = tarmac + "/" + nameOnly[-1][:-4] + "_avgTamper.csv"
        response = open(output, "w")

        inlines = template.readlines()
        outlines = []

        if len(inlines) < 3:
            for line in inlines:
                outlines.append(line.split(","))
            for line in outlines:
                idx = 0
                for item in line:
                    #print(item)
                    if line!=outlines[-1]:
                        if item == line[-1]:
                            data = item
                        else:
                            data = item + ","
                        response.write(data)
                    else:
                        if item == line[-1] and idx == len(line)-1:
                            if item[-1] != "\n":
                                data = item
                            else:
                                data = item[:-1]
                        else:
                            data = item + ","
                        response.write(data)
                    idx += 1
            response.close()

            continue        #if file has one observation, simply copies it
        
        avgLine = []

        for line in inlines:
            outlines.append(line.split(","))
        
        #outlines = outlines[1:]        #dangerous: don't just throw the header away

        MJDStampMid = ( float(outlines[1][0]) + float(outlines[-1][0]) ) / 2
        avgLine.append(str(MJDStampMid))
        avgLine.append(str(MJDStampMid+0.5))     #populate MJD and AddMJD

        weightDict = {}
        for line in outlines[1:]:
            try:
                weightDict[line[0]] = 1 / (float(line[5])**2)
            except ZeroDivisionError:
                weightDict[line[0]] = 0      #this is good: assigning zero weight to the line where it's all zeros ignores it

        avgNum = 0
        avgDenom = 0

        for line in outlines[1:]:
            item = weightDict[line[0]] * float(line[4])
            avgNum += item
        
        for k in weightDict:
            avgDenom += weightDict[k]

        uJyBar = avgNum/avgDenom
        duJyBar = math.sqrt(1/avgDenom)
        if(uJyBar>0):
            mBar = -2.5 * math.log10(uJyBar) + 23.9
        else:
            mBar = -1
        dmBar = 0       #HYPERCRITICAL!
        if(duJyBar>0):
            m3s = -2.5 * math.log10(3*duJyBar) + 23.9
            m5s = -2.5 * math.log10(5*duJyBar) + 23.9
        else:
            m3s = 0
            m5s = 0
        flag = "8"

        avgLine.append(str(mBar))        #self-explanatory
        avgLine.append(str(dmBar))       #self-explanatory
        avgLine.append(str(uJyBar))      #self-explanatory
        avgLine.append(str(duJyBar))     #self-explanatory
        avgLine.append(outlines[1][6])            #F
        avgLine.append("0")         #err
        avgLine.append("0")         #chi/N
        avgLine.append(outlines[1][10])         #RA
        avgLine.append(outlines[1][11])         #Dec
        avgLine.append("0")           #x
        avgLine.append("0")           #y
        avgLine.append("0")         #maj
        avgLine.append("0")         #min
        avgLine.append("0")         #phi
        avgLine.append("0")       #apfit
        avgLine.append(str(m3s))         #mag3sig
        avgLine.append(str(m5s))         #mag5sig
        avgLine.append("0")         #Sky
        avgLine.append("abc")         #Obs
        avgLine.append(flag + "\n")        #self-explanatory

        #MJD, AddMJD, m, dm, uJy, duJy, F, err, chi/N, RA, Dec, x, y, maj, min, phi, apfit, m3s, m5s, Sky, Obs, flag

        outlines.append(avgLine)
        outlines2 = outlines[1:]
        outlines2.sort(key=lambda x: float(x[0]))
        #print(outlines2)

        outlinesFinal = []
        outlinesFinal.append(outlines[0])
        for line in outlines2:
            outlinesFinal.append(line)
        #print(outlinesFinal)

        for line in outlinesFinal:
            idx = 0
            for item in line:
                #print(item)
                if line!=outlinesFinal[-1]:
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
        response.close()
    
    messagebox.showinfo("Finished","Average point write complete. Check destination folder.")    




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

        writeAvg(takeoff, landing)
        messagebox.showinfo("Finished","Average point write complete. Check destination folder.")
        appWindow.destroy()

    #except FileNotFoundError:
    #    messagebox.showerror("Error", "File does not exist, or is incompatible. Exiting.")
    #    appWindow.destroy()


main()
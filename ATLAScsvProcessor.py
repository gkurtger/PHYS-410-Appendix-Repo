import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os

import matplotlib.pyplot as plt
import numpy as np

def cleanup(source, tarmac):
    """Currently defunct. Refer to ATLAScleanup.py."""
    template = open(source, "r")
    inlines = template.readlines()
    outlines = []

    for line in inlines:
        outlines.append(line.split(","))

    

def filterSeparate(source, tarmac):
    """
    Reads in main source file and creates two output files separated by filter. The filter is denoted in output file name.
    CAVEAT: This function assumes there are only o and c filters in the dataset.
    """
    template = open(source, "r")

    nameOnly = source.split("/")
    trueSource = tarmac + "/" + nameOnly[-1][:-4]

    trueSourceO = trueSource + "_o.csv"
    trueSourceC = trueSource + "_c.csv"

    responseO = open(trueSourceO, "w")
    responseC = open(trueSourceC, "w")

    inlines = template.readlines()
    outlines = []
    outlinesO = []
    outlinesC = []              #to eliminate extraneous newlines, separation of lines before the write process is necessary

    for line in inlines:
        outlines.append(line.split(","))
    
    outlinesO.append(outlines[0])
    outlinesC.append(outlines[0])


    for line in outlines:
        if line[6] == "o":
            outlinesO.append(line)
            
        elif line[6] == "c":
            outlinesC.append(line)      #these two loops completely populate outlinesC and outlinesO with list representations of each line


    for line in outlinesO:
        for item in line:
            if line!=outlinesO[-1]:
                if item == line[-1]:
                    data = item
                else:
                    data = item + ","
                responseO.write(data)
            else:
                if item == line[-1]:
                    if item[-1] != "\n":
                        data = item
                    else:
                        data = item[:-1]
                else:
                    data = item + ","
                responseO.write(data)

    for line in outlinesC:
        for item in line:
            if line!=outlinesC[-1]:
                if item == line[-1]:
                    data = item
                else:
                    data = item + ","
                responseC.write(data)
            else:
                if item == line[-1]:
                    if item[-1] != "\n":
                        data = item
                    else:
                        data = item[:-1]
                else:
                    data = item + ","
                responseC.write(data)

    template.close()
    responseC.close()
    responseO.close()

    
    messagebox.showinfo("Finished","Filter separation complete. Check destination folder.")
    
    #note to self: separate window-creating functions that take appWindow as an arg to destroy() on end after calling a separator may be in order


def MJDSeparate(source, tarmac):
    template = open(source, "r")
    
    nameOnly = source.split("/")
    response = tarmac + "/" + nameOnly[-1][:-4]


    inlines = template.readlines()
    outlines = []
    

    for line in inlines:
        outlines.append(line.split(","))    #populates outlines as was in filterSeparation

    mindate = int(float(outlines[1][0]))                #extracts MJD of first observation
    maxdate = int(float(outlines[-1][0]))               #extracts MJD of last observation

    scandate = mindate
    scanline = 1

    while(scanline < len(outlines)):
        lineFunnel = []
        lineFunnel.append(outlines[0])
        responseScan = open(response + "_" + str(int(float(outlines[scanline][0]))) + ".csv", "w")  #the computer scientist in me weeps
        while(scanline < len(outlines) and int(float(outlines[scanline][0])) == scandate):
            lineFunnel.append(outlines[scanline])
            scanline+=1

        for line in lineFunnel:
            for item in line:
                if line!=lineFunnel[-1]:
                    if item == line[-1]:
                        data = item
                    else:
                        data = item + ","
                    responseScan.write(data)
                else:
                    if item == line[-1]:
                        data = item[:-1]
                    else:
                        data = item + ","
                    responseScan.write(data)

        responseScan.close()
        
        scandate+=1

    template.close()

    messagebox.showinfo("Finished","MJD separation complete. Check destination folder.")


def dailyPlot(catapult, tarmac):
    files = os.listdir(catapult)

    for file in files:
        if file[-4:] != ".csv":     #this way, non-csv are ignored
            continue

        source = catapult + "/" + file
        template = open(source, "r")
        nameOnly = source.split("/")
        response = tarmac + "/" + nameOnly[-1][:-4] + ".png"

        inlines = template.readlines()
        outlines = []

        xVals = []
        yVals = []
        yErr = []

        for line in inlines:
            outlines.append(line.split(","))
        outlines = outlines[1:]

        for line in outlines:
            xVals.append(float(line[0]))
            yVals.append(float(line[2]))
            yErr.append(float(line[3]))

        xVals = np.array(xVals)
        #print(xVals)
        yVals = np.array(yVals)
        #print(yVals)

        plt.plot(xVals, yVals, 'o')
        plt.xlabel("JD-2459000")
        plt.ylabel("Magnitude")
        plt.errorbar(xVals, yVals, yerr = yErr, fmt ='o')

        plt.savefig(response)
        plt.clf()
        plt.cla()           #i don't know why, but in the absence of these two lines, every day is mushed together
        template.close()

    messagebox.showinfo("Finished","Daily plotting complete. Check destination folder.")



def main():
    #try:
        appWindow = tk.Tk()

        # Build a list of tuples for each file type the file dialog should display
        compatFiletypes = [('All files', '.*'), ('Comma-separated value files (.csv)', '.csv')]

        # Ask the user to select a single file name.
    #    template = filedialog.askopenfilename(parent=appWindow,
    #                                        initialdir=os.getcwd(),
    #                                        title="Please select source file:",
    #                                        filetypes=compatFiletypes)


        takeoff = filedialog.askdirectory(parent=appWindow,
                                 initialdir=os.getcwd(),
                                 title="Please select source folder:")


        landing = filedialog.askdirectory(parent=appWindow,
                                 initialdir=os.getcwd(),
                                 title="Please select destination folder:")


        #if template[-4:] != ".csv":
        #    raise FileNotFoundError
        
        
        #filterSeparate(template, landing)
        #MJDSeparate(template, landing)

        #print(template)
        #print(landing)

        dailyPlot(takeoff, landing)

    #except FileNotFoundError:
    #    messagebox.showerror("Error", "File does not exist, or is incompatible. Exiting.")
    #    appWindow.destroy()


main()
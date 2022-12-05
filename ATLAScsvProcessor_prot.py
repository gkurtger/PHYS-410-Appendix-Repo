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
        putline[-1] = putline[-1][:-1]
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

def modFlags(source, tarmac):
    """
    UNDER CONSTRUCTION.
    Modifies the flag column.
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
        putline = line.split(",")
        outlines.append(putline)


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

def cleanPassOne(source, tarmac):
    """
    Function to execute the first pass of initial refinement.
    Adds RJD, mag3sig, dt, and flag columns.
    """

    initialN = source
    nameOnly = source.split("/")
    finalN = tarmac + "/" + nameOnly[-1][:-4] + "_cleanp.csv"

    MJDtoMMJD(initialN, finalN)     #this function reads in the initial file, creates final file
    sig3col(finalN, finalN)        #argument placement not a typo: ensures these two functions work in-place on the final file
    timeError(finalN, finalN)
    putFlags(finalN, finalN)


def cleanPassTwo(source, tarmac):
    """
    Function to execute the second pass of initial refinement.
    Only modifies flag column.
    """

    initialN = source
    nameOnly = source.split("/")
    finalN = tarmac + "/" + nameOnly[-1][:-4] + "_doublecleanp.csv"

    modFlags(initialN, finalN)

def refiner():
    """
    Function to execute the steps of initial refinement in order.
    """

    source = filedialog.askopenfilename(parent=tk.Tk(),
                                        initialdir=os.getcwd(),
                                        title="Please select source file:")

    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")

    template = open(source, "r")
    inlines = template.readlines()
    header = inlines[0]
    headerL = header.split(",")

    if len(headerL) == 19:
        cleanPassOne(source, tarmac)
    elif len(headerL) == 23:
        cleanPassTwo(source, tarmac)

    messagebox.showinfo("Finished","Initial refinements complete. Check destination folder.")



def filterSeparate():     #this function assumes there are only o and c filters in the data

    compatFiletypes = [('All files', '.*'), ('Comma-separated value files (.csv)', '.csv')]

    # Ask the user to select a single file name.
    source = filedialog.askopenfilename(parent=tk.Tk(),
                                        initialdir=os.getcwd(),
                                        title="Please select source file:")

    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")


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




def MJDSeparate():
    compatFiletypes = [('All files', '.*'), ('Comma-separated value files (.csv)', '.csv')]

    # Ask the user to select a single file name.
    source = filedialog.askopenfilename(parent=tk.Tk(),
                                        initialdir=os.getcwd(),
                                        title="Please select source file:")

    landing = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")


    template = open(source, "r")
    
    nameOnly = source.split("/")
    response = landing + "/" + nameOnly[-1][:-4]


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
            idx = 0
            for item in line:
                if line!=lineFunnel[-1]:
                    if item == line[-1]:
                        data = item
                    else:
                        data = item + ","
                    responseScan.write(data)
                else:
                    if item == line[-1] and idx == len(line)-1:
                        data = item
                    else:
                        data = item + ","
                    responseScan.write(data)
                idx+=1

        responseScan.close()
        
        scandate+=1

    template.close()

    messagebox.showinfo("Finished","MJD separation complete. Check destination folder.")


def dailyPlot():

    catapult = filedialog.askdirectory(parent=tk.Tk(),
                                 initialdir=os.getcwd(),
                                 title="Please select source folder:")


    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")



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
        xErr = []
        yErr = []

        for line in inlines:
            outlines.append(line.split(","))
        outlines = outlines[1:]

        for line in outlines:
            xVals.append(float(line[0]))
            yVals.append(float(line[2]))
            xErr.append(float(line[7]))
            yErr.append(float(line[3]))

        xVals = np.array(xVals)
        #print(xVals)
        yVals = np.array(yVals)
        #print(yVals)

        plt.plot(xVals, yVals, 'o')
        plt.xlabel("JD-2459000")
        plt.ylabel("Magnitude")
        plt.errorbar(xVals, yVals, xerr = xErr, yerr = yErr, fmt ='o')

        plt.savefig(response)
        plt.clf()
        plt.cla()           #i don't know why, but in the absence of these two lines, every day is mushed together
        template.close()

    messagebox.showinfo("Finished","Daily plotting complete. Check destination folder.")

def writeAvg():
    """
    Writes the weighted average calculated for each file onto an output CSV.
    """

    catapult = filedialog.askdirectory(parent=tk.Tk(),
                                 initialdir=os.getcwd(),
                                 title="Please select source folder:")


    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")


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
        
        if(uJyBar-duJyBar>0 and uJyBar+duJyBar>0):
            mBarM = (-2.5 * math.log10(uJyBar - duJyBar) + 23.9) - mBar
            mBarP = mBar - (-2.5 * math.log10(uJyBar + duJyBar) + 23.9)
            dmBar = max(mBarM, mBarP)
        else:
            dmBar = 0
        
        if(duJyBar>0):
            m3s = -2.5 * math.log10(3*duJyBar) + 23.9
            m5s = -2.5 * math.log10(5*duJyBar) + 23.9
        else:
            m3s = 0
            m5s = 0
        
        flag = 11

        dt = MJDStampMid - float(outlines[1][0])

        avgLine.append(str(mBar))        #self-explanatory
        avgLine.append(str(dmBar))       #self-explanatory
        avgLine.append(str(uJyBar))      #self-explanatory
        avgLine.append(str(duJyBar))     #self-explanatory
        avgLine.append(outlines[1][6])            #F
        avgLine.append(str(dt))
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
        avgLine.append(str(flag) + "\n")        #self-explanatory

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
        template.close()
        response.close()
    messagebox.showinfo("Finished","Average point write complete. Check destination folder.")

def avgCompile():
    """
    WARNING: run this only on files that already have daily values written on. The program relies on the
    "this is an averaged point" flag, and will give you nothing if that flag doesn't exist.
    """

    catapult = filedialog.askdirectory(parent=tk.Tk(),
                                 initialdir=os.getcwd(),
                                 title="Please select source folder:")


    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")
    
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
    
    for file in files[:-1]:     #but maybe this could: do for all files/lines but the last; treat last file/line
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

#def main():
    #having main is completely meaningless because tkinter sucks

class csvProcess():
    def __init__(self):
        self.appWindow = tk.Tk()
        self.appWindow.title("ATLAS .csv Processor")
        self.makeWidgets()


    

    def makeWidgets(self):
        # Create some room around all the internal frames
        self.appWindow['padx'] = 5
        self.appWindow['pady'] = 5

        #pickTgtButton = tk.Button(self.appWindow, text="Change Source File")
        #pickTgtButton.grid(row=1, column=0)

        #pickDestButton = tk.Button(self.appWindow, text="Change Destination")
        #pickDestButton.grid(row=1, column=1)

        cleanupButton = tk.Button(self.appWindow, text="Initial clean-up", command=refiner)
        cleanupButton.grid(row=2, column=0)
        
        filterSepButton = tk.Button(self.appWindow, text="Separate by Filter", command=filterSeparate)
        filterSepButton.grid(row=2, column=1)

        MJDSepButton = tk.Button(self.appWindow, text="Separate by MJD", command=MJDSeparate)
        MJDSepButton.grid(row=2, column=2)

        dayPlotButton = tk.Button(self.appWindow, text="Make Diagnostic Plots", command=dailyPlot)
        dayPlotButton.grid(row=3, column=0)

        avgWriteButton = tk.Button(self.appWindow, text="Write Daily Weighted Averages", command=writeAvg)
        avgWriteButton.grid(row=3, column=1)

        avgCompileButton = tk.Button(self.appWindow, text="Compile Weighted Averages", command=avgCompile)
        avgCompileButton.grid(row=3, column=2)

        quitButton = ttk.Button(self.appWindow, text="Quit", command=self.appWindow.destroy)
        quitButton.grid(row=4, column=0)


processor = csvProcess()

processor.appWindow.mainloop()


#no funcs on tgt and designator!
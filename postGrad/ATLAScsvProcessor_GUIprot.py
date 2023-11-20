import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os

import matplotlib.pyplot as plt
import numpy as np


import ATLAScsvMaker as csvmake
import ATLAScleanup as clnp
import ATLAScsvFilterSeparator as filsep
import ATLAScsvMJDSeparator as mjdsep
import ATLASDailyPlotter as dayplt
import ATLASDayAvg as davg
import ATLASaverageCollimate as avgcoll

def makeCsv():
    """
    Relevant UI step: 'Convert to CSV'

    No translation: functional by virtue of file import; pandas irrelevant to solution
    """
    # Ask the user to select a single file name.
    source = filedialog.askopenfilename(parent=tk.Tk(),
                                        initialdir=os.getcwd(),
                                        title="Please select source file:")

    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")
    
    templateName = source.split("/")[-1]
    tarmac = tarmac + "/" + templateName[:-4] + ".csv"
    
    csvmake.convert(source, tarmac)


    messagebox.showinfo("Finished","txt-csv conversion complete. Check destination folder.")



def refiner():
    """
    Relevant UI step: 'Initial clean-up'

    Translation complete.
    """

    source = filedialog.askopenfilename(parent=tk.Tk(),
                                        initialdir=os.getcwd(),
                                        title="Please select source file:")

    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")

    messagebox.showinfo("Finished",clnp.refiner(source, tarmac))


def filterSeparate():     #this function assumes there are only o and c filters in the data
    """
    Relevant UI step: 'Separate by Filter'

    Translation complete.
    """

    compatFiletypes = [('All files', '.*'), ('Comma-separated value files (.csv)', '.csv')]

    # Ask the user to select a single file name.
    source = filedialog.askopenfilename(parent=tk.Tk(),
                                        initialdir=os.getcwd(),
                                        title="Please select source file:")

    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")


    filsep.filterSeparate(source, tarmac)
    
    messagebox.showinfo("Finished","Filter separation complete. Check destination folder.")
    
    #note to self: separate window-creating functions that take appWindow as an arg to destroy() on end after calling a separator may be in order




def MJDSeparate():
    """
    Relevant UI step: 'Separate by MJD'

    Translation complete.
    """
    compatFiletypes = [('All files', '.*'), ('Comma-separated value files (.csv)', '.csv')]

    # Ask the user to select a single file name.
    source = filedialog.askopenfilename(parent=tk.Tk(),
                                        initialdir=os.getcwd(),
                                        title="Please select source file:")

    landing = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")
    
    mjdsep.MJDSeparate(source, landing)

    messagebox.showinfo("Finished","MJD separation complete. Check destination folder.")


def dailyPlot():
    """
    Translation in progress: the function is identical, but moved to external module for readability/tidiness

    Relevant UI step: 'Make Diagnostic Plots'
    """

    catapult = filedialog.askdirectory(parent=tk.Tk(),
                                 initialdir=os.getcwd(),
                                 title="Please select source folder:")


    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")

    dayplt.dailyPlot(catapult, tarmac)

    messagebox.showinfo("Finished","Daily plotting complete. Check destination folder.")

def writeAvg():
    """
    Relevant UI step: 'Write Daily Weighted Averages'

    Translation complete.
    """

    catapult = filedialog.askdirectory(parent=tk.Tk(),
                                 initialdir=os.getcwd(),
                                 title="Please select source folder:")


    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")


    davg.writeAvg(catapult, tarmac)
    messagebox.showinfo("Finished","Average point write complete. Check destination folder.")

def avgCompile():
    """
    Relevant UI step: 'Compile Weighted Averages'

    WARNING: run this only on files that already have daily values written on. The program relies on the
    "this is an averaged point" flag, and will give you nothing if that flag doesn't exist.

    Translation complete.
    """

    catapult = filedialog.askdirectory(parent=tk.Tk(),
                                 initialdir=os.getcwd(),
                                 title="Please select source folder:")


    tarmac = filedialog.askdirectory(parent=tk.Tk(),
                                initialdir=os.getcwd(),
                                title="Please select destination folder:")
    
    avgcoll.avgCompile(catapult, tarmac)

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

        csvMakeButton = tk.Button(self.appWindow, text="Convert to CSV", command=makeCsv)
        csvMakeButton.grid(row=4, column=0)

        quitButton = ttk.Button(self.appWindow, text="Quit", command=self.appWindow.destroy)
        quitButton.grid(row=5, column=0)


processor = csvProcess()

processor.appWindow.mainloop()


#no funcs on tgt and designator!
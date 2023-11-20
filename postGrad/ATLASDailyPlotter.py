import os

import matplotlib.pyplot as plt
import numpy as np


def dailyPlot(catapult, tarmac):
    """
    Creates JD-by-JD graphs.
    Algorithm:
    -Obtain list of files, distinguish CSVs
    -For each CSV, read in columns of date and magnitude
    -Create plot, save as .png
    """
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

        scatter = plt.scatter(xVals, yVals, c="black")
        ax = scatter.axes
        ax.invert_yaxis()
        plt.errorbar(xVals, yVals, xerr = xErr, yerr = yErr, fmt="o", color="black")
        

        plt.savefig(response)
        plt.clf()
        plt.cla()           #i don't know why, but in the absence of these two lines, every day is mushed together
        template.close()
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
        nameOnly = source.split("/")
        output = tarmac + "/" + nameOnly[-1][:-4] + "_avgTamper.csv"

        template = pd.read_csv(source)
        #template.reset_index(drop=True, inplace=True)
        #print(template)
        

        if template.shape[0]==1:
            template.to_csv(output, index=False)
            continue        #if file has one observation, simply copies it
        
        # avgLine = []

        # print(template.head(1)['MJD'])
        # print(template.tail(1)['MJD'])

        MJDStampMid = (template['MJD'][0] + template['MJD'][template.shape[0]-1]) / 2
        

        # avgLine.append(MJDStampMid)
        # avgLine.append(MJDStampMid+0.5)     #populate MJD and RJD

        #print(MJDStampMid)

        # begin uJy & duJy generation on avgLine
        weightDict = {}

        rows = template.iterrows()      #bad practice, couldn't avoid it; will look for ways to do so
        for idx, row in rows:
            try:
                weightDict[row['MJD']] = 1 / (row['duJy'])**2
            except ZeroDivisionError:
                weightDict[row['MJD']] = 0      #this is good: assigning zero weight to the line where it's all zeros ignores it


        avgNum = 0
        avgDenom = 0

        rows = template.iterrows()
        for idx, row in rows:
            item = weightDict[row['MJD']] * row['uJy']
            avgNum += item
        
        for k in weightDict:
            avgDenom += weightDict[k]

        uJyBar = avgNum/avgDenom
        duJyBar = math.sqrt(1/avgDenom)
        # end uJy & duJy generation on avgLine
        
        # begin m & dm generation on avgLine
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
        # end m & dm generation on avgLine
        
        # begin mag3sig & mag5sig generation on avgLine
        if(duJyBar>0):
            m3s = -2.5 * math.log10(3*duJyBar) + 23.9
            m5s = -2.5 * math.log10(5*duJyBar) + 23.9
        else:
            m3s = 0
            m5s = 0
        # end mag3sig & mag5sig generation on avgLine
        
        flag = 11

        dt = MJDStampMid - template['MJD'][0]

        # avgLine.append(mBar)        #self-explanatory
        # avgLine.append(dmBar)       #self-explanatory
        # avgLine.append(uJyBar)      #self-explanatory
        # avgLine.append(duJyBar)     #self-explanatory
        # avgLine.append(template.head(1)['F'])
        # avgLine.append(dt)
        # avgLine.append(0)         #err
        # avgLine.append(0)         #chi/N
        # avgLine.append(template.head(1)['RA'])
        # avgLine.append(template.head(1)['Dec'])
        # avgLine.append(0)           #x
        # avgLine.append(0)           #y
        # avgLine.append(0)         #maj
        # avgLine.append(0)         #min
        # avgLine.append(0)         #phi
        # avgLine.append(0)       #apfit
        # avgLine.append(m3s)         #mag3sig
        # avgLine.append(m5s)         #mag5sig
        # avgLine.append(0)         #Sky
        # avgLine.append("abc")         #Obs
        # avgLine.append(flag)        #self-explanatory

        #MJD, RJD, m, dm, uJy, duJy, F, err, chi/N, RA, Dec, x, y, maj, min, phi, apfit, mag3sig, mag5sig, Sky, Obs, flag

        avgSer = pd.Series(data={
                                'MJD':MJDStampMid,
                                'RJD':MJDStampMid+0.5,
                                'm':mBar,
                                'dm':dmBar,
                                'uJy':uJyBar,
                                'duJy':duJyBar,
                                'F':template['F'][0],
                                'dt':dt,
                                'err':0,
                                'chi/N':0,
                                'RA':template['RA'][0],
                                'Dec':template['Dec'][0],
                                'x':0,
                                'y':0,
                                'maj':0,
                                'min':0,
                                'phi':0,
                                'apfit':0,
                                'mag3sig':m3s,
                                'mag5sig':m5s,
                                'Sky':0,
                                'Obs':"abc",
                                'flag':flag})   #this is lopsided but it's the exact way the documentation shows


        response = pd.concat([template, avgSer.to_frame().T], ignore_index=True)
        #response.reset_index(drop=True, inplace=True)
        response.sort_values(by='MJD', inplace=True)
        response.to_csv(output, index=False)

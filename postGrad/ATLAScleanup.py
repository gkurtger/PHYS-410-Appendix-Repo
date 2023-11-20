import numpy as np
import pandas as pd
import math



def MJDtoRJD(collect):
    """
    Adds 0.5 to the MJD value in dataset.
    Day leaps that may result are not addressed.

    Takes: collect: Pandas DataFrame
    Returns: collect: Pandas DataFrame (.insert() appears to work in-place.)
    """
    collect.rename(columns={'###MJD':'MJD'}, inplace=True)
    mjdCol = collect['MJD']
    rjdCol = mjdCol.add(0.5)
    collect.insert(1, "RJD", rjdCol)
    return collect

def sig3col(collect):
    """
    Adds a 3-sigma magnitude column to the datafile.
    
    Takes: collect: Pandas DataFrame
    Returns: collect: Pandas DataFrame (.insert() appears to work in-place.)
    """
    #print(collect.head(1)['duJy'])
    mag3sigCol = collect.apply(lambda row: (math.log10(3*row['duJy']) * -2.5)+23.9 if row['duJy']>0 else "N/A" , axis=1 )
    collect.insert(17, "mag3sig", mag3sigCol)
    return collect

def timeError(collect):
    """
    Adds a time error column to the datafile -relevant to weighted average step-.

    Takes: collect: Pandas DataFrame
    Returns: collect: Pandas DataFrame (.insert() appears to work in-place.)
    """
    dtCol = np.zeros(collect.shape[0])
    collect.insert(7, "dt", dtCol)
    return collect

def defineFlags(row):
    """
    The transformer to pass to the DF.apply() call inside putFlags().
    """
    try:
        naCheck = float(row['mag3sig'])
        if row['m'] > 20 or row['m'] < 0:    #this sets our tolerance to 0th to 20th magnitude, moddable
            return 4
        elif row['dm'] >= 0.5:                  #this sets our error bar tolerance at 0.5 magnitudes, moddable
            return 3
        elif row['uJy'] < 3*row['duJy']:          #works to see if uJy > 3duJy; as per 5sig requirements
            return 2
        elif row['uJy'] < 5*row['duJy']:          #works to see if uJy > 5duJy; as per 3sig requirements
            return 1
        else:
            return 0        

    except ValueError:
        return 9
    
def putFlags(collect):
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

    Pandas will add the flag column if it doesn't exist, and modify it if it does. This simplifies the
    implementation of the second pass considerably.
    """
    collect['flag'] = collect.apply(defineFlags, axis=1)
    return collect

def cleanPassOne(source, template, tarmac):
    """
    First-pass refiner.

    Takes: template: Pandas DataFrame
    Returns: Nothing, but creates a csv from Pandas DataFrame response, onto path tarmac
    """

    nameOnly = source.split("/")
    responseName = tarmac + "/" + nameOnly[-1][:-4] + "_cleanp.csv"

    response = MJDtoRJD(template)
    response = sig3col(response)
    response = timeError(response)
    response = putFlags(response)

    response.to_csv(responseName, index=False)

def cleanPassTwo(source, template, tarmac):
    """
    Second-pass refiner.

    Takes: source: file path
           template: Pandas DataFrame
    Returns: Nothing, but creates a csv from Pandas DataFrame response, onto path tarmac
    """

    nameOnly = source.split("/")
    responseName = tarmac + "/" + nameOnly[-1][:-4] + "_doublecleanp.csv"

    response = putFlags(template)

    response.to_csv(responseName, index=False)


def refiner(source, tarmac):
    """
    Fully pass-aware refinement executor.

    Takes: source: file path.
    Returns: The message to be displayed by the UI notification.
    """
    template = pd.read_csv(source)
    

    if template.shape[1] == 19:
        cleanPassOne(source, template, tarmac)
        return "Initial refinements complete. Check destination folder."
    elif template.shape[1] == 23:
        cleanPassTwo(source, template, tarmac)
        return "Second-pass refinements complete. Check destination folder."
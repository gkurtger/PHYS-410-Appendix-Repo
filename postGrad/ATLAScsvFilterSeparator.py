import pandas as pd

def filterSeparate(source, tarmac):     #this function assumes there are only o and c filters in the data
    template = pd.read_csv(source)

    nameOnly = source.split("/")
    trueSource = tarmac + "/" + nameOnly[-1][:-4]

    trueSourceO = trueSource + "_o.csv"
    trueSourceC = trueSource + "_c.csv"

    responseO = template[template['F']=='o']
    responseC = template[template['F']=='c']

    responseO.to_csv(trueSourceO, index=False)
    responseC.to_csv(trueSourceC, index=False)
import os
import pandas as pd

def avgCompile(catapult, tarmac):
    """
    WARNING: run this only on files that already have daily values written on. The program relies on the
    "this is an averaged point" flag, and will give you nothing if that flag doesn't exist.
    """    
    files = os.listdir(catapult)
    nameOnly = files[0][:-20]
    #print(nameOnly)
    output = tarmac + "/" + nameOnly + "_avgCompile.csv"

    response = pd.DataFrame()

    for file in files:
        if file[-4:] != ".csv":
            continue

        template = pd.read_csv(catapult + "/" + file)
        
        if template.shape[0]==1:
            response = pd.concat([response, template], ignore_index=True)
            

        avgLine = template[template['flag']==11]
        response = pd.concat([response, avgLine], ignore_index=True)

        response.to_csv(output, index=False)

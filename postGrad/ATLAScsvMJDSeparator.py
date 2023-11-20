import pandas as pd

def MJDSeparate(source, tarmac):
    template = pd.read_csv(source)
    
    nameOnly = source.split("/")
    response = tarmac + "/" + nameOnly[-1][:-4]

    mindate = int(template['MJD'].min())                #extracts MJD of first observation
    maxdate = int(template['MJD'].max())               #extracts MJD of last observation

    #print(template['MJD'])

    scanStart = mindate

    while scanStart<=maxdate:
        scanStop = scanStart+1
        #print(scanStart)
        outDF = template[template['MJD']>=scanStart]
        outDF = outDF[outDF['MJD']<scanStop]

        if outDF.empty:
            scanStart += 1
            continue

        outDF.to_csv(response + "_" + str(scanStart) + ".csv", index=False)
        scanStart += 1

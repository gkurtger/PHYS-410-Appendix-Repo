def convert(collect, emit):
    infile = open(collect)
    outfile = open(emit, "w")

    inlines = infile.readlines()
    outlines = []

    for line in inlines:
        outlines.append(line.split())

    for line in outlines:       #easy to split loops to cases of last-not last with slicing outlines
        for item in line:
            if line!=outlines[-1]:
                if item == line[-1]:
                    data = item + "\n"
                else:
                    data = item + ","
                outfile.write(data)
            else:
                if item == line[-1]:
                    data = item
                else:
                    data = item + ","
                outfile.write(data)


    infile.close()
    outfile.close()
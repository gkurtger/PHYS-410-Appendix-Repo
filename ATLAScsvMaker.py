import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os



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

def main():
    try:
        appWindow = tk.Tk()

        # Build a list of tuples for each file type the file dialog should display
        compatFiletypes = [('All files', '.*'), ('Text files (.txt)', '.txt')]

        # Ask the user to select a single file name.
        template = filedialog.askopenfilename(parent=appWindow,
                                            initialdir=os.getcwd(),
                                            title="Please select a file:",
                                            filetypes=compatFiletypes)

        landing = filedialog.askdirectory(parent=appWindow,
                                 initialdir=os.getcwd(),
                                 title="Please select destination folder:")

        templateName = template.split("/")[-1]
        
        response = landing + "/" + templateName[:-4] + ".csv"

        if template[-4:] != ".txt":
            raise FileNotFoundError
        
        convert(template, response)
        
        messagebox.showinfo("Finished","txt-csv conversion complete. Check destination folder.")
        appWindow.destroy()

    except FileNotFoundError:
        messagebox.showerror("Error", "File does not exist, or is incompatible. Exiting.")
        appWindow.destroy()


main()
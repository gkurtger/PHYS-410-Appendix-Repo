# ***************************************************************************
# *****************************  GOOD_GRAPH_GUI  ****************************
# ***************************************************************************
#
#      A Python GUI to graph (and analyze) ALFALFA related datasets.
#
#     Version 1.3.4, 2020 July 03, BY THOMAS J. BALONEK (COLGATE UNIVERISTY)
#
#                        *** a work in progress! ***
#
# Requires a folder 'good_graph' in the folder containing this program
#
# You may modify and distribute this program to colleagues, 
#      but please keep above information.
#      ... and keep me informed of your changes so I can modify my code!!
# Developed in Anaconda Jupyter notebook.


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from astropy.table import Table
from astropy.io import ascii
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import filedialog
import sys
import os
from tkinter import Menu

# ******************************************************************************************************
# *************** Setup GUI ****************************************************************************
# ******************************************************************************************************

%matplotlib qt5
#%matplotlib inline

Good_Graph = tk.Tk()
Good_Graph.geometry ('1020x720')
Good_Graph.resizable (1, 1)
vers = 'v1.3.4'
GGvers = 'GG_'+vers
Good_Graph.title ('Good_Graph ('+vers+')')


# ******************************************************************************************************
# *************** Select and read the Data File ********************************************************
# ******************************************************************************************************

lbl_0a = tk.Label(Good_Graph, text=' Select Data File ',font=('Arial Bold', 12))
lbl_0a.grid(column=0, row=0, sticky=tk.E)

data_file_name = filedialog.askopenfilename()
if not data_file_name: 
    lbl_help = tk.Label(Good_Graph, text='No file selected. You need to restart the kernal and run again!',\
                        font=('Arial Bold', 28))
    lbl_help.grid(column=0, row=4, columnspan=3)
    sys.exit()

# check for .txt file. assume it might be .csv file, so note it as csv file format and try
extension = os.path.splitext(data_file_name)[1]

#shortfilename = filename[:12]

filename = os.path.basename(data_file_name)
lbl_0 = tk.Label(Good_Graph, text='File Selected:'+filename,font=('Arial Bold', 14))
lbl_0.grid(column=0, row=0, columnspan=4, sticky=tk.W)

if extension != '.txt':
    datatable = Table.read (data_file_name)
    
# assume txt files are really csv files, so try opening as a csv file
if extension == '.txt':
    lbl_0t = tk.Label(Good_Graph, text='File Selected:'+filename+'  (read txt file as csv file)',\
                     font=('Arial Bold', 14))
    lbl_0t.grid(column=0, row=0, columnspan=4, sticky=tk.W)
    datatable = Table.read (data_file_name, format = 'csv')

#if Table.read has problems, use ascii.read
#datatable = ascii.read (data_file_name, format='csv')
# determine number of columns
Count = 0
for char in datatable.colnames:
       Count+=1

        
# ******************************************************************************************************
# *************** Select datacolumns to analyze and graph **********************************************
# ******************************************************************************************************

# select the data columns (x, y, y2) to plot *************

lbl_x = tk.Label(Good_Graph, text='Select x-axis:',font=('Arial Bold', 12))
lbl_x.grid(column=0, row=1, sticky=tk.E)
combo_x = ttk.Combobox(Good_Graph)
combo_x['values']= (datatable.colnames)
combo_x.current() 
combo_x.grid(column=1, row=1, sticky=tk.W)

lbl_y = tk.Label(Good_Graph, text='Select y-axis:',font=('Arial Bold', 12))
lbl_y.grid(column=2, row=1, sticky=tk.E)
combo_y = ttk.Combobox(Good_Graph)
combo_y['values']= (datatable.colnames)
combo_y.current() 
combo_y.grid(column=3, row=1, sticky=tk.W)

second_y_axis = tk.IntVar()
second_y_axis.set(0)
chk_second_y_axis = tk.Checkbutton(Good_Graph, text='second y:', \
                    font=('Arial Bold', 12), onvalue = 1, offvalue = 0, variable=second_y_axis)
chk_second_y_axis.grid(column=4, row=1, sticky=tk.E)
combo_y2 = ttk.Combobox(Good_Graph)
combo_y2['values']= (datatable.colnames)
combo_y2.current() 
combo_y2.grid(column=5, row=1, sticky=tk.W)


# select the associated errors ************************

x_axis_error = tk.IntVar()
x_axis_error.set(0)
chk_x_axis_error = tk.Checkbutton(Good_Graph, text='x-axis error:', \
                    font=('Arial Bold', 12), onvalue = 1, offvalue = 0, variable=x_axis_error)
chk_x_axis_error.grid(column=0, row=2, sticky=tk.E)
combo_x_axis_error = ttk.Combobox(Good_Graph)
combo_x_axis_error['values']= (datatable.colnames)
combo_x_axis_error.current() 
combo_x_axis_error.grid(column=1, row=2, sticky=tk.W)

y_axis_error = tk.IntVar()
y_axis_error.set(0)
chk_y_axis_error = tk.Checkbutton(Good_Graph, text='y-axis error:', \
                    font=('Arial Bold', 12), onvalue = 1, offvalue = 0, variable=y_axis_error)
chk_y_axis_error.grid(column=2, row=2, sticky=tk.E)
combo_y_axis_error = ttk.Combobox(Good_Graph)
combo_y_axis_error['values']= (datatable.colnames)
combo_y_axis_error.current() 
combo_y_axis_error.grid(column=3, row=2, sticky=tk.W)

y2_axis_error = tk.IntVar()
y2_axis_error.set(0)
chk_y2_axis_error = tk.Checkbutton(Good_Graph, text='second y error:', \
                    font=('Arial Bold', 12), onvalue = 1, offvalue = 0, variable=y2_axis_error)
chk_y2_axis_error.grid(column=4, row=2, sticky=tk.E)
combo_y2_axis_error = ttk.Combobox(Good_Graph)
combo_y2_axis_error['values']= (datatable.colnames)
combo_y2_axis_error.current() 
combo_y2_axis_error.grid(column=5, row=2, sticky=tk.W)


# select delimiter column

use_limiter = tk.IntVar()
use_limiter.set(0)
chk_limiter = tk.Checkbutton(Good_Graph, text='Use Limiter:', \
                    font=('Arial Bold', 12), onvalue = 1, offvalue = 0, variable=use_limiter)
chk_limiter.grid(column=2, row=4, sticky=tk.E)
combo_limiter = ttk.Combobox(Good_Graph)
combo_limiter['values']= (datatable.colnames)
combo_limiter.current() 
combo_limiter.grid(column=3, row=4, sticky=tk.W)

lbl_limiter_min = tk.Label(Good_Graph, text='Limiter (min, max):', font=('Arial', 12))
lbl_limiter_min.grid(column=4, row=4, sticky=tk.E)
entry_limiter_min = tk.Entry(Good_Graph, width = 9,font=('Arial', 10))
entry_limiter_min.grid(column=5, row=4, sticky=tk.W)
lbl_limiter_range = tk.Label(Good_Graph, text='≤ L ≤', font=('Arial', 12))
lbl_limiter_range.grid (column=5, row=4)
entry_limiter_max = tk.Entry(Good_Graph, width = 9,font=('Arial', 10))
entry_limiter_max.grid(column=5, row=4, sticky=tk.E)


# ******************************************************************************************************
# *************** INITIALIZE DEFAULT PLOT PARAMETERS ***************************************************
# ******************************************************************************************************


# Variables
the_title = 'ALFALFA UAT Science Rocks'
plot_type = 'scatter'
title_size = '18.0'
axis_label_size = '16.0'
figsize_x = '8.00'
figsize_y = '5.00'
frame_linewidth = '1.50'
tick_width= '1.50'
tick_length= '5.00'
tick_label_size = '14.0'
tick_direction = 'in'
minor_tick_length_val = '2.5'
minor_tick_width_val = '1.00'
major_grid_line_width_val = '0.25'
number_minor_x_ticks_val = '5.0'
number_minor_y_ticks_val = '5.0'

# Checkboxes
dont_display_title_val = 0
use_limiter_val = 0
change_title_val = 0
change_x_axis_label_val = 0
change_y_axis_label_val = 0
change_x_min_val = 0
change_x_max_val = 0
change_y_min_val = 0
change_y_max_val = 0
invert_x_axis_val = 0
invert_y_axis_val = 0
bottom_tick_val = 1
left_tick_val = 1
right_tick_val = 1
top_tick_val = 1
include_minor_ticks_val = 0
set_number_minor_ticks_val = 0
include_major_grid_val = 0
dont_display_plot_info_val = 0
dont_display_limiter_info_val = 0
save_graph_Good_Graph_val =1
save_graph_Good_Graph_long_val = 0

# Entry new values
new_title = ' '
new_x_axis_label = ' '
new_y_axis_label = ' '
new_x_min = ' '
new_x_max = ' '
new_y_min = ' '
new_y_max = ' '
delimiter_min = ' '
delimiter_max = ' '


# Read previously saved personal parameter values file here <<<=====

    


# ******************************************************************************************************
# *************** Modify, if desired, title and axis labels ********************************************
# ******************************************************************************************************


# Set Title

lbl_blank_10 = tk.Label(Good_Graph, text=' ',font=('Arial', 10))
lbl_blank_10.grid(column=0, row=10)

lbl_current_title_1 = tk.Label(Good_Graph, text='Current title:',\
                    font=('Arial Bold', 12))
lbl_current_title_1.grid(column=0, row=11, sticky=tk.E)
lbl_current_title_2 = tk.Label(Good_Graph, text=the_title, font=('Arial Bold', 12))
lbl_current_title_2.grid(column=1, row=11, columnspan=2, sticky=tk.W)

dont_display_title = tk.IntVar()
dont_display_title.set(dont_display_title_val)
chk_dont_display_title = tk.Checkbutton(Good_Graph, text='Don\'t display title', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=dont_display_title)
chk_dont_display_title.grid(column=3, row=11, sticky=tk.W)

change_title = tk.IntVar()
change_title.set (change_title_val)
chk_change_title = tk.Checkbutton(Good_Graph, text='Rename title   ', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=change_title)
chk_change_title.grid(column=0, row=12, columnspan=2)
lbl_new_title = tk.Label(Good_Graph, text='New title:',\
                    font=('Arial Bold', 12))
lbl_new_title.grid(column=1, row=12, sticky=tk.E)
entry_new_title = tk.Entry(Good_Graph, width = 40,font=('Arial Bold', 12))
entry_new_title.grid(column=2, row=12, columnspan=2, sticky=tk.W)


# Set x and y axis Labels

change_x_axis_label = tk.IntVar()
change_x_axis_label.set(change_x_axis_label_val)
chk_change_x_axis_label = tk.Checkbutton(Good_Graph, text='Rename x-axis   ', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=change_x_axis_label)
chk_change_x_axis_label.grid(column=0, row=13, columnspan=2)
lbl_new_x_axis_label = tk.Label(Good_Graph, text='New x-axis label:',\
                    font=('Arial Bold', 12))
lbl_new_x_axis_label.grid(column=1, row=13, sticky=tk.E)
entry_new_x_axis_label = tk.Entry(Good_Graph, width = 40,font=('Arial Bold', 12))
entry_new_x_axis_label.grid(column=2, row=13, columnspan=2, sticky=tk.W)

change_y_axis_label = tk.IntVar()
change_y_axis_label.set(change_y_axis_label_val)
chk_change_y_axis_label = tk.Checkbutton(Good_Graph, text='Rename y-axis   ', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=change_y_axis_label)
chk_change_y_axis_label.grid(column=0, row=14, columnspan=2)
lbl_new_y_axis_label = tk.Label(Good_Graph, text='New y-axis label:',\
                    font=('Arial Bold', 12))
lbl_new_y_axis_label.grid(column=1, row=14, sticky=tk.E)
entry_new_y_axis_label = tk.Entry(Good_Graph, width = 40,font=('Arial Bold', 12))
entry_new_y_axis_label.grid(column=2, row=14, columnspan=2, sticky=tk.W)


# ******************************************************************************************************
# *************** Adjust x & y axes: range, inver, linear/log ******************************************
# ******************************************************************************************************

lbl_blank_20 = tk.Label(Good_Graph, text=' ',font=('Arial', 10))
lbl_blank_20.grid(column=0, row=20)

# set linear-log scales
lbl_linear_log_x = tk.Label(Good_Graph, text='x, y-axis:', font=('Arial Bold', 12))
lbl_linear_log_x.grid(column=4, row=20, sticky=tk.E)
var_linear_log_x = tk.StringVar()
var_linear_log_x_values = ('linear', 'log')
spin_linear_log_x = tk.Spinbox(Good_Graph, values=var_linear_log_x_values,\
                     width=9, font=('Arial', 12), textvariable=var_linear_log_x)
spin_linear_log_x.grid(column=5, row=20, sticky=tk.W)

var_linear_log_y = tk.StringVar()
var_linear_log_y_values = ('linear', 'log')
spin_linear_log_y = tk.Spinbox(Good_Graph, values=var_linear_log_y_values,\
                     width=9, font=('Arial', 12), textvariable=var_linear_log_y)
spin_linear_log_y.grid(column=5, row=20, sticky=tk.E)


# CHANGE AXES RANGES

# x-axis
change_x_min = tk.IntVar()
change_x_min.set(change_x_min_val)
chk_change_x_min = tk.Checkbutton(Good_Graph, text='Change xmin:', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=change_x_min)
chk_change_x_min.grid(column=0, row=21, sticky=tk.E)
entry_new_x_min = tk.Entry(Good_Graph, width = 9,font=('Arial', 10))
entry_new_x_min.grid(column=1, row=21, sticky=tk.W)

change_x_max = tk.IntVar()
change_x_max.set(change_x_max_val)
chk_change_x_max = tk.Checkbutton(Good_Graph, text='Change xmax:', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=change_x_max)
chk_change_x_max.grid(column=1, row=21, sticky=tk.E)
entry_new_x_max = tk.Entry(Good_Graph, width = 9,font=('Arial', 10))
entry_new_x_max.grid(column=2, row=21, sticky=tk.W)

# y-axis
change_y_min = tk.IntVar()
change_y_min.set(change_y_min_val)
chk_change_y_min = tk.Checkbutton(Good_Graph, text='Change ymin:', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=change_y_min)
chk_change_y_min.grid(column=2, row=21, sticky=tk.E)
entry_new_y_min = tk.Entry(Good_Graph, width = 9,font=('Arial', 10))
entry_new_y_min.grid(column=3, row=21, sticky=tk.W)

change_y_max = tk.IntVar()
change_y_max.set(change_y_max_val)
chk_change_y_max = tk.Checkbutton(Good_Graph, text='Change ymax:', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=change_y_max)
chk_change_y_max.grid(column=3, row=21, sticky=tk.E)
entry_new_y_max = tk.Entry(Good_Graph, width = 9, font=('Arial', 10))
entry_new_y_max.grid(column=4, row=21, sticky=tk.W)

#invert axes
invert_x_axis = tk.IntVar()
invert_x_axis.set(invert_x_axis_val)
invert_y_axis = tk.IntVar()
invert_y_axis.set(invert_y_axis_val)
chk_invert_x_axis = tk.Checkbutton(Good_Graph, text='Invert x-axis',\
                    font=('Arial', 10), onvalue = 1, offvalue = 0, variable=invert_x_axis)
chk_invert_x_axis.grid(column=5, row=21, sticky=tk.W)
chk_invert_y_axis = tk.Checkbutton(Good_Graph, text='Invert y-axis',\
                    font=('Arial', 10), onvalue = 1, offvalue = 0, variable=invert_y_axis)
chk_invert_y_axis.grid(column=5, row=21, sticky=tk.E)


# ******************************************************************************************************
# *************** Select PLOT-TYPES and Symbol parameters ************************************************
# ******************************************************************************************************

lbl_blank_12 = tk.Label(Good_Graph, text=' ',font=('Arial Bold', 12))
lbl_blank_12.grid(column=0, row=30)

# select plot-types

lbl_plot_type = tk.Label(Good_Graph, text='Plot type (y1,y2):',\
                    font=('Arial Bold', 12))
lbl_plot_type.grid(column=0, row=31, sticky=tk.E)
var_spin_plot_type = tk.StringVar()
var_spin_plot_type_values = ('scatter', 'line','scatter+line')
#var_spin_plot_type_values.set('scatter')
spin_plot_type = tk.Spinbox(Good_Graph, values=var_spin_plot_type_values,\
                     width=9, font=('Arial', 12), textvariable=var_spin_plot_type)
spin_plot_type.grid(column=1,row=31, sticky=tk.W)

var_spin_plot2_type = tk.StringVar()
var_spin_plot2_type_values = ('scatter', 'line','scatter+line')
#var_spin_plot2_type_values.set('scatter')
spin_plot2_type = tk.Spinbox(Good_Graph, values=var_spin_plot2_type_values,\
                     width=9, font=('Arial', 12), textvariable=var_spin_plot2_type)
spin_plot2_type.grid(column=1,row=31, sticky=tk.E)


# *************** Line plot parameters ***********************************

# lineplot transparency

lbl_lineplot_transparency = tk.Label(Good_Graph, text='Line transparency:',\
                    font=('Arial Bold', 12))
lbl_lineplot_transparency.grid(column=4, row=31, sticky=tk.E)
var_lineplot_transparency = tk.StringVar()
var_lineplot_transparency.set(0.7)
spin_lineplot_transparency = tk.Spinbox(Good_Graph, from_=0.2, to=1.0, increment = 0.05,\
                     format='%6.2f', width=5, font=('Arial', 12), textvariable=var_lineplot_transparency)
spin_lineplot_transparency.grid(column=5,row=31, sticky=tk.W)

var_lineplot2_transparency = tk.StringVar()
var_lineplot2_transparency.set(0.7)
spin_lineplot2_transparency = tk.Spinbox(Good_Graph, from_=0.2, to=1.0, increment = 0.05,\
                     format='%6.2f', width=5, font=('Arial', 12), textvariable=var_lineplot2_transparency)
spin_lineplot2_transparency.grid(column=5,row=31)


# lineplot color

lbl_lineplot_line_color = tk.Label(Good_Graph, text='Lineplot line color:',\
                    font=('Arial Bold', 12))
lbl_lineplot_line_color.grid(column=0, row=32, sticky=tk.E)
var_lineplot_line_color = tk.StringVar()
var_lineplot_line_color_values = ('black','grey','lightgrey','maroon','red','orange',\
                'yellow','olive','green','lawngreen','cyan','blue','deepskyblue',\
                'purple','magenta','pink','brown','white')
#var_scatter_color_values.set ('grey')
spin_lineplot_line_color = tk.Spinbox(Good_Graph, values=var_lineplot_line_color_values,\
                     width=9, font=('Arial', 12), textvariable=var_lineplot_line_color)
spin_lineplot_line_color.grid(column=1,row=32, sticky=tk.W)

var_lineplot_line2_color = tk.StringVar()
var_lineplot_line2_color_values = ('black','grey','lightgrey','maroon','red','orange',\
                'yellow','olive','green','lawngreen','cyan','blue','deepskyblue',\
                'purple','magenta','pink','brown','white')
#var_scatter_color_values.set ('black')
spin_lineplot_line2_color = tk.Spinbox(Good_Graph, values=var_lineplot_line2_color_values,\
                     width=9, font=('Arial', 12), textvariable=var_lineplot_line2_color)
spin_lineplot_line2_color.grid(column=1,row=32, sticky=tk.E)


# lineplot marker

lbl_lineplot_line_type = tk.Label(Good_Graph, text='Lineplot line type:',\
                    font=('Arial Bold', 12))
lbl_lineplot_line_type.grid(column=2, row=32, sticky=tk.E)
var_lineplot_line_type = tk.StringVar()
var_lineplot_line_type_values = ('solid', 'dashed', 'dashdot', 'dotted')
#var_lineplot_line_type_values.set ('solid')
spin_lineplot_line_type = tk.Spinbox(Good_Graph, values=var_lineplot_line_type_values,\
                     width=10, font=('Arial', 12), textvariable=var_lineplot_line_type)
spin_lineplot_line_type.grid(column=3,row=32, sticky=tk.W)

var_lineplot_line2_type = tk.StringVar()
var_lineplot_line2_type_values = ('solid', 'dashed', 'dashdot', 'dotted')
#var_lineplot_line_type_values.set ('solid')
spin_lineplot_line2_type = tk.Spinbox(Good_Graph, values=var_lineplot_line2_type_values,\
                     width=10, font=('Arial', 12), textvariable=var_lineplot_line2_type)
spin_lineplot_line2_type.grid(column=3,row=32, sticky=tk.E)


# lineplot markersize

lbl_lineplot_line_width = tk.Label(Good_Graph, text='Lineplot line width:',\
                    font=('Arial Bold', 12))
lbl_lineplot_line_width.grid(column=4, row=32, sticky=tk.E)
var_lineplot_line_width = tk.StringVar()
var_lineplot_line_width.set (1)
spin_lineplot_line_width = tk.Spinbox(Good_Graph, from_=0.5, to=10.0, increment = 0.5,\
                     format='%6.1f', width=5, font=('Arial', 12), textvariable=var_lineplot_line_width)
spin_lineplot_line_width.grid(column=5,row=32, sticky=tk.W)

var_lineplot_line2_width = tk.StringVar()
var_lineplot_line2_width.set (1)
spin_lineplot_line2_width = tk.Spinbox(Good_Graph, from_=0.5, to=10.0, increment = 0.5,\
                     format='%6.1f', width=5, font=('Arial', 12), textvariable=var_lineplot_line2_width)
spin_lineplot_line2_width.grid(column=5,row=32)


# *************** Scattter plot parameters *******************************

# scatterplot color

lbl_scatter_marker_color = tk.Label(Good_Graph, text='Scatter symbol color:',\
                    font=('Arial Bold', 12))
lbl_scatter_marker_color.grid(column=0, row=33, sticky=tk.E)
var_scatter_marker_color = tk.StringVar()
var_scatter_marker_color_values = ('black','grey','lightgrey','maroon','red','orange',\
                'yellow','olive','green','lawngreen','cyan','blue','deepskyblue',\
                'purple','magenta','pink','brown','white')
spin_scatter_marker_color = tk.Spinbox(Good_Graph, values=var_scatter_marker_color_values,\
                     width=9, font=('Arial', 12), textvariable=var_scatter_marker_color)
spin_scatter_marker_color.grid(column=1,row=33, sticky=tk.W)

var_scatter_marker2_color = tk.StringVar()
var_scatter_marker2_color_values = ('black','grey','lightgrey','maroon','red','orange',\
                'yellow','olive','green','lawngreen','cyan','blue','deepskyblue',\
                'purple','magenta','pink','brown','white')
spin_scatter_marker2_color = tk.Spinbox(Good_Graph, values=var_scatter_marker2_color_values,\
                     width=9, font=('Arial', 12), textvariable=var_scatter_marker2_color)
spin_scatter_marker2_color.grid(column=1,row=33,sticky=tk.E)


# scatterplot marker type (symbol)

lbl_scatter_marker_type = tk.Label(Good_Graph, text='Scatterplot symbol:',\
                    font=('Arial Bold', 12))
lbl_scatter_marker_type.grid(column=2, row=33, sticky=tk.E)
var_scatter_marker_type = tk.StringVar()
var_scatter_marker_type_values = ('o','.','s','x','+','v','^','*','d','None')
#var_scatter_marker_type_values = ('point','circle','square','x','plus','triangle_down','triangle_up',\
#                                  'star','thin_diamond')
#var_scatter_marker_type_values.set ('point')
spin_scatter_marker_type = tk.Spinbox(Good_Graph, values=var_scatter_marker_type_values,\
                     width=10, font=('Arial', 12), textvariable=var_scatter_marker_type)
spin_scatter_marker_type.grid(column=3,row=33, sticky=tk.W)
var_scatter_marker2_type = tk.StringVar()
var_scatter_marker2_type_values = ('o','.','s','x','+','v','^','*','d','None')
spin_scatter_marker2_type = tk.Spinbox(Good_Graph, values=var_scatter_marker2_type_values,\
                     width=10, font=('Arial', 12), textvariable=var_scatter_marker2_type)
spin_scatter_marker2_type.grid(column=3,row=33,sticky=tk.E)


# scatterplot markersize (symbol size)

lbl_scatter_marker_size = tk.Label(Good_Graph, text='Scatterplot symbol size:',\
                    font=('Arial Bold', 12))
lbl_scatter_marker_size.grid(column=4, row=33, sticky=tk.E)
var_scatter_marker_size = tk.StringVar()
var_scatter_marker_size.set (5)
spin_scatter_marker_size = tk.Spinbox(Good_Graph, from_=1, to=30, increment = 1.0,\
                     format='%6.1f', width=5, font=('Arial', 12), textvariable=var_scatter_marker_size)
spin_scatter_marker_size.grid(column=5,row=33, sticky=tk.W)

lbl_scatter_marker2_size = tk.Label(Good_Graph, text='Scatterplot symbol size:',\
                    font=('Arial Bold', 12))
lbl_scatter_marker2_size.grid(column=4, row=33, sticky=tk.E)
var_scatter_marker2_size = tk.StringVar()
var_scatter_marker2_size.set (5)
spin_scatter_marker2_size = tk.Spinbox(Good_Graph, from_=1, to=30, increment = 1.0,\
                     format='%6.1f', width=5, font=('Arial', 12), textvariable=var_scatter_marker2_size)
spin_scatter_marker2_size.grid(column=5,row=33)


# *************** Error Bar parameters *************************************

# errorbar color

# y and y2 errorbars

lbl_errorbar_color = tk.Label(Good_Graph, text='Errorbar color(y1,y2):',\
                    font=('Arial Bold', 12))
lbl_errorbar_color.grid(column=0, row=34, sticky=tk.E)
var_y_errorbar_color = tk.StringVar()
var_y_errorbar_color_values = ('black','grey','lightgrey','maroon','red','orange',\
                'yellow','olive','green','lawngreen','cyan','blue','deepskyblue',\
                'purple','magenta','pink','brown','white')
spin_y_errorbar_color = tk.Spinbox(Good_Graph, values=var_y_errorbar_color_values,\
                     width=9, font=('Arial', 12), textvariable=var_y_errorbar_color)
spin_y_errorbar_color.grid(column=1,row=34, sticky=tk.W)
var_y2_errorbar_color = tk.StringVar()
var_y2_errorbar_color_values = ('black','grey','lightgrey','maroon','red','orange',\
                'yellow','olive','green','lawngreen','cyan','blue','deepskyblue',\
                'purple','magenta','pink','brown','white')
spin_y2_errorbar_color = tk.Spinbox(Good_Graph, values=var_y2_errorbar_color_values,\
                     width=9, font=('Arial', 12), textvariable=var_y2_errorbar_color)
spin_y2_errorbar_color.grid(column=1,row=34, sticky=tk.E)

# x errorbar

lbl_errorbar_color = tk.Label(Good_Graph, text='Errorbar color(x):',\
                    font=('Arial Bold', 12))
lbl_errorbar_color.grid(column=2, row=34, sticky=tk.E)

var_x_errorbar_color = tk.StringVar()
var_x_errorbar_color_values = ('black','grey','lightgrey','maroon','red','orange',\
                'yellow','olive','green','lawngreen','cyan','blue','deepskyblue',\
                'purple','magenta','pink','brown','white')
spin_x_errorbar_color = tk.Spinbox(Good_Graph, values=var_x_errorbar_color_values,\
                     width=9, font=('Arial', 12), textvariable=var_x_errorbar_color)
spin_x_errorbar_color.grid(column=3,row=34, sticky=tk.W)

# errorbar width

lbl_errorbar_linewidth = tk.Label(Good_Graph, text='Errorbar line width:',\
                    font=('Arial Bold', 12))
lbl_errorbar_linewidth.grid(column=4, row=34, sticky=tk.E)
var_errorbar_linewidth = tk.StringVar()
var_errorbar_linewidth.set(1.00)
spin_errorbar_linewidth = tk.Spinbox(Good_Graph, from_=0.25, to=5, increment = 0.25, format='%6.2f',\
                     width=5, font=('Arial', 12), textvariable=var_errorbar_linewidth)
spin_errorbar_linewidth.grid(column=5,row=34, sticky=tk.W)


# ******************************************************************************************************
# *************** SET PLOT FRAME PARAMETERS ************************************************************
# ******************************************************************************************************

lbl_blank_30 = tk.Label(Good_Graph, text=' ',font=('Arial Bold', 12))
lbl_blank_30.grid(column=0, row=50)


# Set plot box / frame size ************************

lbl_figsize_x = tk.Label(Good_Graph, text='Plot size (x-axis):',\
                    font=('Arial Bold', 12))
lbl_figsize_x.grid(column=0, row=51, sticky=tk.E)
var_spin_figsize_x = tk.StringVar()
var_spin_figsize_x.set(figsize_x)
spin_figsize_x = tk.Spinbox(Good_Graph, from_=4, to=11, increment = 0.25, format='%6.2f', \
                     width=5, font=('Arial', 12), textvariable=var_spin_figsize_x)
spin_figsize_x.grid(column=1,row=51, sticky=tk.W)

lbl_figsize_y = tk.Label(Good_Graph, text='Plot size (y-axis):',\
                    font=('Arial Bold', 12))
lbl_figsize_y.grid(column=2, row=51, sticky=tk.E)
var_spin_figsize_y = tk.StringVar()
var_spin_figsize_y.set(figsize_y)
spin_figsize_y = tk.Spinbox(Good_Graph, from_=4, to=11, increment = 0.25, format='%6.2f', \
                    width=5, font=('Arial', 12), textvariable=var_spin_figsize_y)
spin_figsize_y.grid(column=3,row=51, sticky=tk.W)


# Set plot frame linewidth **************************

lbl_frame_linewidth = tk.Label(Good_Graph,text='Plot frame line width:', \
                    font=('Arial Bold', 12))
lbl_frame_linewidth.grid(column=4, row=51, sticky=tk.E)
var_spin_frame_linewidth = tk.StringVar()
var_spin_frame_linewidth.set(frame_linewidth)
spin_frame_linewidth = tk.Spinbox(Good_Graph, from_=1, to=4, increment = 0.25, \
                    format='%6.2f', width=5, font=('Arial', 12), textvariable=var_spin_frame_linewidth)
spin_frame_linewidth.grid(column=5,row=51, sticky=tk.W)


# Set title size ************************************

lbl_title_size = tk.Label(Good_Graph, text='Title size:',\
                    font=('Arial Bold', 12))
lbl_title_size.grid(column=0, row=52, sticky=tk.E)
var_spin_title_size = tk.StringVar()
var_spin_title_size.set(title_size)
spin_title_size = tk.Spinbox(Good_Graph, from_=8, to=20, increment = 1.0, \
                    format='%6.1f', width=5, font=('Arial', 12), textvariable=var_spin_title_size)
spin_title_size.grid(column=1,row=52, sticky=tk.W)


# Set axes label size ********************************

lbl_axis_label_size = tk.Label(Good_Graph, text='Axis label size:', \
                    font=('Arial Bold', 12))
lbl_axis_label_size.grid(column=2, row=52, sticky=tk.E)
var_spin_axis_label_size = tk.StringVar()
var_spin_axis_label_size.set(axis_label_size)
spin_axis_label_size = tk.Spinbox(Good_Graph, from_=8, to=20, increment = 1.0, \
                    format='%6.1f', width=5, font=('Arial', 12), textvariable=var_spin_axis_label_size)
spin_axis_label_size.grid(column=3,row=52, sticky=tk.W)


# set tick label size ********************************

lbl_tick_label_size = tk.Label(Good_Graph, text='Axis tick label size:',\
                    font=('Arial Bold', 12))
lbl_tick_label_size.grid(column=4, row=52, sticky=tk.E)
var_spin_tick_label_size = tk.StringVar()
var_spin_tick_label_size.set(tick_label_size)
spin_tick_label_size = tk.Spinbox(Good_Graph, from_=8, to=20, increment = 1.0, \
                    format='%6.1f', width=5, font=('Arial', 12), textvariable=var_spin_tick_label_size)
spin_tick_label_size.grid(column=5,row=52, sticky=tk.W)


# set major tick paramters - length, width, direction ****************

# major tick length
lbl_tick_length = tk.Label(Good_Graph,text='Axis tick length:',font=('Arial Bold',12))
lbl_tick_length.grid(column=0, row=53, sticky=tk.E)
var_spin_tick_length = tk.StringVar()
var_spin_tick_length.set(tick_length)
spin_tick_length = tk.Spinbox(Good_Graph, from_=1, to=12, increment = 0.5, format='%6.2f', \
                     width=5, font=('Arial', 12), textvariable=var_spin_tick_length)
spin_tick_length.grid(column=1, row=53, sticky=tk.W)

# major tick width
lbl_tick_width = tk.Label(Good_Graph, text='Axis tick width:',font=('Arial Bold', 12))
lbl_tick_width.grid(column=2, row=53, sticky=tk.E)
var_spin_tick_width = tk.StringVar()
var_spin_tick_width.set(tick_width)
spin_tick_width = tk.Spinbox(Good_Graph, from_=1, to=2.5, increment = 0.25, format='%6.2f', \
                     width=5, font=('Arial', 12), textvariable=var_spin_tick_width)
spin_tick_width.grid(column=3,row=53, sticky=tk.W)

# major tick direction 
lbl_tick_direction = tk.Label(Good_Graph, text='Axis tick direction:',\
                    font=('Arial Bold', 12))
lbl_tick_direction.grid(column=4, row=53, sticky=tk.E)
var_spin_tick_direction = tk.StringVar()
var_spin_tick_direction_values = ('in', 'out','inout')
#var_spin_tick_direction.set(tick_direction)
spin_tick_direction = tk.Spinbox(Good_Graph, values=var_spin_tick_direction_values,\
                     width=5, font=('Arial', 12), textvariable=var_spin_tick_direction)
spin_tick_direction.grid(column=5,row=53, sticky=tk.W)


# minor ticks or no-minor ticks
include_minor_ticks = tk.IntVar()
include_minor_ticks.set(include_minor_ticks_val)
chk_include_minor_ticks = tk.Checkbutton(Good_Graph, text='Include minor ticks',\
                    font=('Arial', 10), onvalue = 1, offvalue = 0, variable=include_minor_ticks)
chk_include_minor_ticks.grid(column=0, row=54, sticky=tk.W)

# minor tick length
lbl_minor_tick_length = tk.Label(Good_Graph,text='Minor tick length:',font=('Arial Bold',12))
lbl_minor_tick_length.grid(column=1, row=54, sticky=tk.W)
var_spin_minor_tick_length = tk.StringVar()
var_spin_minor_tick_length.set(minor_tick_length_val)
spin_minor_tick_length = tk.Spinbox(Good_Graph, from_=1, to=12, increment = 0.5, format='%6.2f', \
                     width=5, font=('Arial', 12), textvariable=var_spin_minor_tick_length)
spin_minor_tick_length.grid(column=1, row=54, sticky=tk.E)

#minor tick width
lbl_minor_tick_width = tk.Label(Good_Graph, text='Minor tick width:',font=('Arial Bold', 12))
lbl_minor_tick_width.grid(column=2, row=54, sticky=tk.E)
var_spin_minor_tick_width = tk.StringVar()
var_spin_minor_tick_width.set(minor_tick_width_val)
spin_minor_tick_width = tk.Spinbox(Good_Graph, from_=0.25, to=2.5, increment = 0.25, format='%6.2f', \
                     width=5, font=('Arial', 12), textvariable=var_spin_minor_tick_width)
spin_minor_tick_width.grid(column=3,row=54, sticky=tk.W)

# set number of minor ticks
set_number_minor_ticks = tk.IntVar()
set_number_minor_ticks.set(set_number_minor_ticks_val)
chk_set_number_minor_ticks = tk.Checkbutton(Good_Graph, text='Set # of minor',\
                    font=('Arial Bold', 12), onvalue = 1, offvalue = 0, variable=set_number_minor_ticks)
chk_set_number_minor_ticks.grid(column=3, row=54, sticky=tk.E)
lbl_set_number_minor_ticks = tk.Label(Good_Graph, text='ticks (x, y):',font=('Arial Bold', 12))
lbl_set_number_minor_ticks.grid(column=4, row=54, sticky=tk.W)

var_spin_number_minor_x_ticks = tk.StringVar()
var_spin_number_minor_x_ticks.set(number_minor_x_ticks_val)
spin_number_minor_x_ticks = tk.Spinbox(Good_Graph, from_=1, to=12, increment = 1, format='%6.1f', \
                     width=5, font=('Arial', 12), textvariable=var_spin_number_minor_x_ticks)
spin_number_minor_x_ticks.grid(column=4,row=54, sticky=tk.E)

var_spin_number_minor_y_ticks = tk.StringVar()
var_spin_number_minor_y_ticks.set(number_minor_y_ticks_val)
spin_number_minor_y_ticks = tk.Spinbox(Good_Graph, from_=1, to=12, increment = 1, format='%6.1f', \
                     width=5, font=('Arial', 12), textvariable=var_spin_number_minor_y_ticks)
spin_number_minor_y_ticks.grid(column=5,row=54, sticky=tk.W)


# which axes on frame to plot ticks
bottom_tick = tk.IntVar()
bottom_tick.set(bottom_tick_val)
chk_bottom_tick = tk.Checkbutton(Good_Graph, text='bottom ticks',\
                    font=('Arial', 10), onvalue = 1, offvalue = 0, variable=bottom_tick)
chk_bottom_tick.grid(column=5, row=51, sticky=tk.E)

left_tick = tk.IntVar()
left_tick.set(left_tick_val)
chk_left_tick = tk.Checkbutton(Good_Graph, text='left ticks',\
                    font=('Arial', 10), onvalue = 1, offvalue = 0, variable=left_tick)
chk_left_tick.grid(column=5, row=52, sticky=tk.E)

right_tick = tk.IntVar()
right_tick.set(right_tick_val)
chk_right_tick = tk.Checkbutton(Good_Graph, text='right ticks',\
                    font=('Arial', 10), onvalue = 1, offvalue = 0, variable=right_tick)
chk_right_tick.grid(column=5, row=53, sticky=tk.E)

top_tick = tk.IntVar()
top_tick.set(top_tick_val)
chk_top_tick = tk.Checkbutton(Good_Graph, text='top ticks',\
                    font=('Arial', 10), onvalue = 1, offvalue = 0, variable=top_tick)
chk_top_tick.grid(column=5, row=54, sticky=tk.E)


# ******************************************************************************************************
# *************** Grid setup ***************************************************************************
# ******************************************************************************************************

# grid or no-grid ***********
include_major_grid = tk.IntVar()
include_major_grid.set(include_major_grid_val)
chk_include_major_grid = tk.Checkbutton(Good_Graph, text='Include grid',\
                    font=('Arial', 10), onvalue = 1, offvalue = 0, variable=include_major_grid)
chk_include_major_grid.grid(column=0, row=56, sticky=tk.W)

# grid color ****************
lbl_major_grid_color = tk.Label(Good_Graph, text='Grid color:',\
                    font=('Arial Bold', 12))
lbl_major_grid_color.grid(column=1, row=56, sticky=tk.W)
var_major_grid_color = tk.StringVar()
var_major_grid_color_values = ('black','grey','lightgrey','maroon','red','orange',\
                'yellow','olive','green','lawngreen','cyan','blue','deepskyblue',\
                'purple','magenta','pink','brown','white')
spin_major_grid_color = tk.Spinbox(Good_Graph, values=var_major_grid_color_values,\
                     width=9, font=('Arial', 12), textvariable=var_major_grid_color)
spin_major_grid_color.grid(column=1,row=56, sticky=tk.E)

# grid line type *************
lbl_major_grid_line_type = tk.Label(Good_Graph, text='Grid line type:',\
                    font=('Arial Bold', 12))
lbl_major_grid_line_type.grid(column=2, row=56, sticky=tk.E)
var_major_grid_line_type = tk.StringVar()
var_major_grid_line_type_values = ('solid', 'dashed', 'dashdot', 'dotted')
spin_major_grid_line_type = tk.Spinbox(Good_Graph, values=var_major_grid_line_type_values,\
                     width=10, font=('Arial', 12), textvariable=var_major_grid_line_type)
spin_major_grid_line_type.grid(column=3,row=56, sticky=tk.W)

# grid line width *************
lbl_major_grid_line_width = tk.Label(Good_Graph, text='Grid line width:',\
                    font=('Arial Bold', 12))
lbl_major_grid_line_width.grid(column=4, row=56, sticky=tk.E)
var_major_grid_line_width = tk.StringVar()
var_major_grid_line_width.set (major_grid_line_width_val)
spin_major_grid_line_width = tk.Spinbox(Good_Graph, from_=0.25, to=5.0, increment = 0.25,\
                     format='%6.2f', width=5, font=('Arial', 12), textvariable=var_major_grid_line_width)
spin_major_grid_line_width.grid(column=5,row=56, sticky=tk.W)



# ******************************************************************************************************
# *************** Text *********************************************************************************
# ******************************************************************************************************

# plot information text

dont_display_plot_info = tk.IntVar()
dont_display_plot_info.set(dont_display_plot_info_val)
chk_dont_display_plot_info = tk.Checkbutton(Good_Graph, \
                    text='Don\'t display plot information text box', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=dont_display_plot_info)
chk_dont_display_plot_info.grid(column=4, row=82, columnspan=2)


# limiter information

dont_display_limiter_info = tk.IntVar()
dont_display_limiter_info.set(dont_display_limiter_info_val)
chk_dont_display_limiter_info = tk.Checkbutton(Good_Graph, \
                    text='Don\'t display limiter information text box', \
                    font=('Arial', 12), onvalue = 1, offvalue = 0, variable=dont_display_limiter_info)
chk_dont_display_limiter_info.grid(column=4, row=83, columnspan=2)


# ******************************************************************************************************
# *************** SAVE GRAPH ***************************************************************************
# ******************************************************************************************************

lbl_blank_80 = tk.Label(Good_Graph, text=' ',font=('Arial Bold', 12))
lbl_blank_80.grid(column=0, row=80)
lbl_blank_81 = tk.Label(Good_Graph, text=' ',font=('Arial Bold', 12))
lbl_blank_81.grid(column=0, row=81)

# Save graph Good_Graph.jpg -- gets overwritten each time ***************

save_graph_Good_Graph = tk.IntVar(value=1)
save_graph_Good_Graph.set(save_graph_Good_Graph_val)
chk_save_graph_Good_Graph = tk.Checkbutton(Good_Graph, \
                    text='Save graph as \'Good_Graph.jpg\'', \
                    font=('Arial Bold', 12), onvalue = 1, offvalue = 0, variable=save_graph_Good_Graph)
chk_save_graph_Good_Graph.grid(column=0, row=82, columnspan=2)
lbn_save_note_2 = tk.Label(Good_Graph, text='Overwrites existing '\
                    'graph with same filename!',font=('Arial Italic', 12))
lbn_save_note_2.grid(column=0, row=83, columnspan=2)

# Save graph with unique name (includes datafile, x & y axes, date/time) ***************

save_graph_Good_Graph_long = tk.IntVar(value=1)
save_graph_Good_Graph_long.set(save_graph_Good_Graph_long_val)
chk_save_graph_Good_Graph_long = tk.Checkbutton(Good_Graph, \
                    text='Save graph w/ filename, x & y axes, date-time stamp in name', \
                    font=('Arial Bold', 12), onvalue = 1, offvalue = 0, variable=save_graph_Good_Graph_long)
chk_save_graph_Good_Graph_long.grid(column=2, row=82, columnspan=2, sticky=tk.E)
lbn_save_note_3 = tk.Label(Good_Graph, text='Unique filename so never overwritten',\
                    font=('Arial Italic', 12))
lbn_save_note_3.grid(column=2, row=83, columnspan=2)



# ******************************************************************************************************
# *************** CREATE THE GRAPH *********************************************************************
# ******************************************************************************************************

#lbl_blank_90 = tk.Label(Good_Graph, text=' ',font=('Arial Bold', 12))
#lbl_blank_90.grid(column=0, row=90)

def CreatePlot(*args):
    # get arguments from gui box
    the_title = 'ALFALFA UAT Science Rocks' 
        # not sure why need to do this again,  but doesn't work otherwise
    if change_title.get() == 1:
        the_title = entry_new_title.get()
        
    x_axis_data = datatable.colnames[combo_x.current()]
    x_axis_name = datatable.colnames[combo_x.current()]
    if change_x_axis_label.get() == 1:
        x_axis_name = entry_new_x_axis_label.get()
    y_axis_data = datatable.colnames[combo_y.current()]
    y_axis_name = datatable.colnames[combo_y.current()]
    if change_y_axis_label.get() == 1:
        y_axis_name = entry_new_y_axis_label.get()
    if second_y_axis.get() == 1:
        y2_axis_data = datatable.colnames[combo_y2.current()]
        y2_axis_name = datatable.colnames[combo_y2.current()]
    if use_limiter.get() == 1:
        limiter_name = datatable.colnames[combo_limiter.current()]
    
    x_axis = datatable[datatable.colnames[combo_x.current()]]
    y_axis = datatable[datatable.colnames[combo_y.current()]]
    y2_axis = datatable[datatable.colnames[combo_y2.current()]]
    if use_limiter.get() == 1:
        limiter = datatable[datatable.colnames[combo_limiter.current()]]
    
    # set error bars
    if x_axis_error.get() == 1:
        x_error_data = datatable[datatable.colnames[combo_x_axis_error.current()]]
        x_error = x_error_data
    if y_axis_error.get() == 1:
        y_error_data = datatable[datatable.colnames[combo_y_axis_error.current()]]
        y_error = y_error_data
    if y2_axis_error.get() == 1:
        y2_error_data = datatable[datatable.colnames[combo_y2_axis_error.current()]]
        y2_error = y2_error_data
 
    # restrict x and y if delimiter value is out of range
    if use_limiter.get() == 1:
        limiter_min = float(entry_limiter_min.get())
        limiter_max = float(entry_limiter_max.get())
        limiter_info = 'for '+str(limiter_min)+'≤'+limiter_name+'≤'+str(limiter_max)
        x_axis_data_filt = x_axis[(limiter >= limiter_min) & (limiter <= limiter_max)]
        y_axis_data_filt = y_axis[(limiter >= limiter_min) & (limiter <= limiter_max)]
        x_axis = x_axis_data_filt
        y_axis = y_axis_data_filt
        if second_y_axis.get() == 1:
            y2_axis_data_filt = y2_axis[(limiter >= limiter_min) & (limiter <= limiter_max)]
            y2_axis = y2_axis_data_filt
        if x_axis_error.get() == 1:
            x_error_data_filt = x_error_data[(limiter >= limiter_min) & (limiter <= limiter_max)]
            x_error = x_error_data_filt
        if y_axis_error.get() == 1:
            y_error_data_filt = y_error_data[(limiter >= limiter_min) & (limiter <= limiter_max)]
            y_error = y_error_data_filt
        if y2_axis_error.get() == 1:
            y2_error_data_filt = y2_error_data[(limiter >= limiter_min) & (limiter <= limiter_max)]
            y2_error = y2_error_data_filt
    
    title_size = float(spin_title_size.get())
    axis_label_size = float(spin_axis_label_size.get())
    figsize_x = float(spin_figsize_x.get())
    figsize_y = float(spin_figsize_y.get())
    frame_linewidth = float(spin_frame_linewidth.get())
    tick_width = float(spin_tick_width.get())
    tick_length = float(spin_tick_length.get())
    tick_label_size = float(spin_tick_label_size.get())
    tick_direction = spin_tick_direction.get()
    scatter_marker_type = spin_scatter_marker_type.get()
    scatter_marker_size = float(spin_scatter_marker_size.get())
    scatter_marker_color = spin_scatter_marker_color.get()
    lineplot_transparency = float(spin_lineplot_transparency.get())
    lineplot_line_type = spin_lineplot_line_type.get()
    lineplot_line_width = float(spin_lineplot_line_width.get())
    lineplot_line_color = spin_lineplot_line_color.get()
    scatter_marker2_type = spin_scatter_marker2_type.get()
    scatter_marker2_size = float(spin_scatter_marker2_size.get())
    scatter_marker2_color = spin_scatter_marker2_color.get()
    lineplot2_transparency = float(spin_lineplot2_transparency.get())
    lineplot_line2_type = spin_lineplot_line2_type.get()
    lineplot_line2_width = float(spin_lineplot_line2_width.get())
    lineplot_line2_color = spin_lineplot_line2_color.get()
    minor_tick_length = float(spin_minor_tick_length.get())
    minor_tick_width = float(spin_minor_tick_width.get())
    major_grid_color = spin_major_grid_color.get()
    major_grid_line_type = spin_major_grid_line_type.get()
    major_grid_line_width = float(spin_major_grid_line_width.get())
    minor_x_locator = AutoMinorLocator(float(spin_number_minor_x_ticks.get()))
    minor_y_locator = AutoMinorLocator(float(spin_number_minor_y_ticks.get()))
    
    zorder_errorbars = 1   # this puts errorbars in bakground behind data points
    errorbar_linewidth = float(spin_errorbar_linewidth.get())
    
    me = !whoami
    today = datetime.today().date()
    text_info = GGvers + ' ' + str(today) + ' ' + str(me) + '\n' + str(filename)

    plt.rc('axes',linewidth=frame_linewidth)
    
    fig = plt.figure(figsize = (figsize_x,figsize_y))
    ax = fig.add_subplot (1, 1, 1)
    ax.set_xlabel(x_axis_name, fontsize=axis_label_size)
    ax.set_ylabel(y_axis_name, fontsize=axis_label_size)

    #ax.tick_params(bottom = True, left = True, top = True, right = True)
    ax.tick_params(which = 'both', bottom = bottom_tick.get(), left = left_tick.get(), \
                   top = top_tick.get(), right = right_tick.get())
    ax.tick_params(which = 'major', length=tick_length, width=tick_width,direction=tick_direction, \
                   labelsize=tick_label_size)
    ax.tick_params(which = 'minor', length = minor_tick_length, width = minor_tick_width, direction=tick_direction)

    if include_major_grid.get() == 1:
        ax.grid (which = 'major', color = major_grid_color, ls = major_grid_line_type, lw = major_grid_line_width)
    
    if dont_display_title.get() == 0:
        ax.set_title(the_title, fontsize=title_size) 
    
    if dont_display_plot_info.get() == 0:
        plt.figtext(0.70, 0.01, text_info, fontsize=6)
    
    if (dont_display_limiter_info.get() == 0) and (use_limiter.get() == 1):
        plt.figtext(0.08, 0.02, limiter_info, fontsize = 6)
    
    # plot error bars first to keep them from being over the datapoints
    # plot selections for y2-axis
    if second_y_axis.get() == 1:
        if spin_plot2_type.get() == 'scatter':
            if x_axis_error.get() == 1:
                plt.errorbar(x_axis, y2_axis ,xerr=x_error, color=spin_scatter_marker2_color.get(),\
                             linestyle = 'none', ecolor=spin_x_errorbar_color.get(),\
                             elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
            if y2_axis_error.get() == 1:
                plt.errorbar(x_axis, y2_axis ,yerr=y2_error, color=spin_scatter_marker2_color.get(),\
                             linestyle = 'none',ecolor=spin_y2_errorbar_color.get(),\
                             elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
            
        if spin_plot2_type.get() == 'line':
            if x_axis_error.get() == 1:
                plt.errorbar(x_axis, y2_axis ,xerr=x_error, color=spin_lineplot_line2_color.get(),\
                             linestyle = 'none', ecolor=spin_x_errorbar_color.get(),\
                             elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
            if y2_axis_error.get() == 1:
                plt.errorbar(x_axis, y2_axis ,yerr=y2_error, color=spin_lineplot_line2_color.get(),\
                             linestyle = 'none',ecolor=spin_y2_errorbar_color.get(),\
                             elinewidth=errorbar_linewidth, zorder=zorder_errorbars)

        if spin_plot2_type.get() == 'scatter+line':
            if x_axis_error.get() == 1:
                plt.errorbar(x_axis, y2_axis ,xerr=x_error, color=spin_scatter_marker2_color.get(),\
                             linestyle = 'none', ecolor=spin_x_errorbar_color.get(),\
                             elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
            if y_axis_error.get() == 1:
                plt.errorbar(x_axis, y2_axis ,yerr=y2_error, color=spin_scatter_marker2_color.get(),\
                            linestyle = 'none', ecolor=spin_y2_errorbar_color.get(),\
                            elinewidth=errorbar_linewidth, zorder=zorder_errorbars)

    # plot selections for y-axis
    if spin_plot_type.get() == 'scatter':
        if x_axis_error.get() == 1:
            plt.errorbar(x_axis, y_axis ,xerr=x_error, color=spin_scatter_marker_color.get(),\
                         linestyle = 'none', ecolor=spin_x_errorbar_color.get(),\
                         elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
        if y_axis_error.get() == 1:
            plt.errorbar(x_axis, y_axis ,yerr=y_error, color=spin_scatter_marker_color.get(),\
                         linestyle = 'none', ecolor=spin_y_errorbar_color.get(),\
                         elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
            
    if spin_plot_type.get() == 'line':
        if x_axis_error.get() == 1:
            plt.errorbar(x_axis, y_axis ,xerr=x_error, color=spin_lineplot_line_color.get(),\
                         linestyle = 'none', ecolor=spin_x_errorbar_color.get(),\
                         elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
        if y_axis_error.get() == 1:
            plt.errorbar(x_axis, y_axis ,yerr=y_error, color=spin_lineplot_line_color.get(),\
                         linestyle = 'none', ecolor=spin_y_errorbar_color.get(),\
                         elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
       
    if spin_plot_type.get() == 'scatter+line':
        if x_axis_error.get() == 1:
            plt.errorbar(x_axis, y_axis ,xerr=x_error, color=spin_scatter_marker_color.get(),\
                         linestyle = 'none', ecolor=spin_x_errorbar_color.get(),\
                         elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
        if y_axis_error.get() == 1:
            plt.errorbar(x_axis, y_axis ,yerr=y_error, color=spin_scatter_marker_color.get(),\
                         linestyle = 'none', ecolor=spin_y_errorbar_color.get(),\
                         elinewidth=errorbar_linewidth, zorder=zorder_errorbars)
        

    # now, plot the data points
    if second_y_axis.get() == 1:
        if spin_plot2_type.get() == 'scatter':
            plt.scatter(x_axis, y2_axis, marker=spin_scatter_marker2_type.get(),\
                    s = scatter_marker2_size, color=spin_scatter_marker2_color.get())
        if spin_plot2_type.get() == 'line':
            plt.plot(x_axis, y2_axis, linewidth=lineplot_line2_width,\
                     linestyle=spin_lineplot_line2_type.get(), \
                     color = spin_lineplot_line2_color.get())
        if spin_plot2_type.get() == 'scatter+line':
            plt.scatter(x_axis, y2_axis, marker=spin_scatter_marker2_type.get(),\
                     s = scatter_marker2_size, color=spin_scatter_marker2_color.get())
            plt.plot(x_axis, y2_axis, linewidth=lineplot_line2_width,\
                     linestyle=spin_lineplot_line2_type.get(), \
                     color = spin_lineplot_line2_color.get())         
    
    if spin_plot_type.get() == 'scatter':
        plt.scatter(x_axis, y_axis, marker=spin_scatter_marker_type.get(),\
                    s = scatter_marker_size, color=spin_scatter_marker_color.get())
    if spin_plot_type.get() == 'line':
        plt.plot(x_axis, y_axis, linewidth=lineplot_line_width,\
                 linestyle=spin_lineplot_line_type.get(), \
                 color = spin_lineplot_line_color.get())
    if spin_plot_type.get() == 'scatter+line':
        plt.scatter(x_axis, y_axis, marker=spin_scatter_marker_type.get(),\
                    s = scatter_marker_size, color=spin_scatter_marker_color.get())
        plt.plot(x_axis, y_axis, linewidth=lineplot_line_width,\
                 linestyle=spin_lineplot_line_type.get(), \
                 color = spin_lineplot_line_color.get())

    # set linear or logaxes
    if spin_linear_log_x.get() == 'linear': plt.xscale('linear')
    if spin_linear_log_x.get() == 'log': plt.xscale('log')
    if spin_linear_log_y.get() == 'linear': plt.yscale('linear')
    if spin_linear_log_y.get() == 'log': plt.yscale('log')
        
    if include_minor_ticks.get() == 1:
        ax.minorticks_on()
        if set_number_minor_ticks.get() == 1:
            ax.xaxis.set_minor_locator(minor_x_locator)
            ax.yaxis.set_minor_locator(minor_y_locator)
    
    
    if change_x_min.get() == 1:
        plt.xlim (xmin = float(entry_new_x_min.get()))
    if change_x_max.get() == 1:
        plt.xlim (xmax = float(entry_new_x_max.get()))
    if change_y_min.get() == 1:
        plt.ylim (ymin = float(entry_new_y_min.get()))
    if change_y_max.get() == 1:
        plt.ylim (ymax = float(entry_new_y_max.get()))
    if invert_x_axis.get() == 1: 
        ax.invert_xaxis()
    if invert_y_axis.get() == 1: 
        ax.invert_yaxis()
       
        
    # SAVE PLOTS
    
    # this file gets overwritten each time
    if save_graph_Good_Graph.get() == 1:
        plt.savefig('good_graph/Good_Graph.jpg',dpi=300)
        
    # this file is unique name and thus doesn't get overwritten
    if save_graph_Good_Graph_long.get() ==1:
        the_datetime = datetime.today().strftime('%Y-%m-%d_%H%M%S')
        plotfilename = 'good_graph/Good_Graph_('+filename+')_'+\
                y_axis_data+'_vs_'+x_axis_data+'_('+the_datetime+')'+'.jpg'
        plt.savefig(plotfilename,dpi=300)


        
# ******************************************************************************************************
# *************** Action Buttons ***********************************************************************
# ******************************************************************************************************
        
# Read previously saved personal parameter values file
# Save good_Graph parameters in personal default values
def ReadUserParameters(*args):
    #UserParameterFile_input = Table.read ('good_graph_user_parameters.csv')
    Count = 0
    #for char in datatable.colnames:
    #    Count+=1
    #print (UserParameterFile_input)
    
        
# Save good_Graph parameters in personal parameter values file
def SaveUserParameters(*args):
    parameter_file = 'good_graph/Good_Graph_User_Parameters_('+filename+')_'+\
            datatable.colnames[combo_y.current()]+'_vs_'+datatable.colnames[combo_x.current()]+\
            '_('+datetime.today().strftime('%Y-%m-%d_%H%M%S')+').csv'
    UserParameterFile_output = open(parameter_file, 'w')
                                        
    L=[ 'parameter ,',                           'my_value',
        '\ndont_display_title_val , ',           str(dont_display_title.get()),
        '\nuse_limiter_val , ',                  str(use_limiter_val.get()),
        '\nlimiter_min , ',                      entry_limiter_min.get(),
        '\nlimiter_max , ',                      entry_limiter_max.get(),
        '\nchange_title_val , ',                 str(change_title.get()),
        '\nnew_title , ',                        entry_new_title.get(),
        '\nchange_x_axis_label_val , ',          str(change_x_axis_label.get()), 
        '\nx_axis_name , ',                      entry_new_x_axis_label.get(),
        '\nchange_y_axis_label_val , ',          str(change_y_axis_label.get()),
        '\ny_axis_name , ',                      entry_new_y_axis_label.get(),
        '\nlinear_log_x , ',                     spin_linear_log_x.get(),
        '\nlinear_log_y , ',                     spin_linear_log_y.get(),
        '\nchange_x_min_val , ',                 str(change_x_min.get()), 
        '\nnew_x_min , ',                        entry_new_x_min.get(),
        '\nchange_x_max_val , ',                 str(change_x_max.get()),
        '\nnew_x_max , ',                        entry_new_x_max.get(),
        '\nchange_y_min_val , ',                 str(change_y_min.get()), 
        '\nnew_y_min , ',                        entry_new_y_min.get(),
        '\nchange_y_max_val , ',                 str(change_y_max.get()),
        '\nnew_y_max , ',                        entry_new_y_max.get(),
        '\ninvert_x_axis , ',                    str(invert_x_axis.get()),
        '\ninvert_y_axis , ',                    str(invert_y_axis.get()),
        '\nplot_type , ',                        spin_plot_type.get(),
        '\nplot2_type , ',                       spin_plot2_type.get(),
        '\nlineplot_transparency , ',            spin_lineplot_transparency.get(),
        '\nlineplot2_transparency , ',           spin_lineplot2_transparency.get(),
        '\nlineplot_line_color , ',              spin_lineplot_line_color.get(),
        '\nlineplot_line2_color , ',             spin_lineplot_line2_color.get(),
        '\nlineplot_line_type , ',               spin_lineplot_line_type.get(),
        '\nlineplot_line2_type , ',              spin_lineplot_line2_type.get(),
        '\nlineplot_line_width , ',              spin_lineplot_line_width.get(),
        '\nlineplot_line2_width , ',             spin_lineplot_line2_width.get(),
        '\nscatter_marker_color , ',             spin_scatter_marker_color.get(),
        '\nscatter_marker2_color , ',            spin_scatter_marker2_color.get(),
        '\nscatter_marker_type , ',              spin_scatter_marker_type.get(),
        '\nscatter_marker2_type , ',             spin_scatter_marker2_type.get(),
        '\nscatter_marker_size , ',              spin_scatter_marker_size.get(),
        '\nscatter_marker2_size , ',             spin_scatter_marker2_size.get(),
        '\ny_errorbar_color , ',                 spin_y_errorbar_color.get(),
        '\ny2_errorbar_color , ',                spin_y2_errorbar_color.get(),
        '\nx_errorbar_color , ',                 spin_x_errorbar_color.get(),
        '\nerrorbar_linewidth, ',                spin_errorbar_linewidth.get(),
        '\nfigsize_x , ',                        spin_figsize_x.get(),
        '\nfigsize_y , ',                        spin_figsize_y.get(),
        '\nframe_linewidth , ',                  spin_frame_linewidth.get(),
        '\ntitle_size , ',                       spin_title_size.get(),
        '\naxis_label_size , ',                  spin_axis_label_size.get(),
        '\ntick_label_size , ',                  spin_tick_label_size.get(),
        '\ntick_length , ',                      spin_tick_length.get(),
        '\ntick_width , ',                       spin_tick_width.get(),
        '\ntick_direction , ',                   spin_tick_direction.get(),
        '\ndont_display_plot_info_val , ',       str(dont_display_plot_info.get()),
        '\ndont_display_limiter_info_val , ',    str(dont_display_limiter_info.get()),
        '\nsave_graph_Good_Graph_val , ',        str(save_graph_Good_Graph.get()), 
        '\nsave_graph_Good_Graph_long_val , ',   str(save_graph_Good_Graph_long.get())]
    UserParameterFile_output.writelines(L)  
    UserParameterFile_output.close
# add dont_use_y2_as_delimieter, log/lin    
# grid info
#ticks top, left, ...
#minor ticks

# ******************************************************************************************************
# *************** Action Buttons ***********************************************************************
# ******************************************************************************************************

# ***** MAKE GRAPH ********************

btn_plot_it = tk.Button(Good_Graph, text='Create & Save New Plot', font=('Arial Bold', 14),\
                  command=CreatePlot)
btn_plot_it.config( height = 2, width = 25 )
btn_plot_it.grid(column=1, row=91, columnspan=2)
lbn_save_note_1 = tk.Label(Good_Graph, text='Note: To save graphs, folder \'good_graph\' '\
                         'must exist in program folder',font=('Arial Italic', 10))
lbn_save_note_1.grid(column=1, row=93, columnspan=2)


# ***** READ USER PARAMETERS *********

#btn_read_parameters = tk.Button(Good_Graph, text='(Read My G_G\nParameters)', \
#                  command=ReadUserParameters)
btn_read_parameters = tk.Button(Good_Graph, text='(Function\ncoming soon)',font=('Arial', 12))

btn_read_parameters.config(height = 2, width = 12)
btn_read_parameters.grid(column=5, row=91, sticky=tk.W)


# ***** SAVE USER PARAMETERS ********

btn_save_parameters = tk.Button(Good_Graph, text='Save My G_G\nParameters', font=('Arial', 12), \
                  command=SaveUserParameters)
btn_save_parameters.config( height = 2, width = 12)
btn_save_parameters.grid(column=5, row=93, sticky=tk.W)


Good_Graph.mainloop()

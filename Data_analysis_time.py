import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import pygal
import numpy as np
# from IPython.display import SVG

ROOT_PATH = os.path.join(os.getcwd(), 'data')
if not os.path.isdir(ROOT_PATH):
    os.mkdir(ROOT_PATH)

# Read in data top keyword counts
data = dict()
data_names = []
for i in range(1985, 2015, 5):
    with open(ROOT_PATH + "/mostcommon_" + str(i) + "_" + str(i + 4) + 
              ".txt", "r") as data_file:
        data[str(i) + "_" + str(i + 4)] = json.load(data_file)
        data_names.append(str(i) + "_" + str(i + 4)) 

# Merge dicts into dataframe
df = pd.DataFrame()
for i in data_names:
    if df.empty:
        df = pd.DataFrame(data[i].values(), index=data[i].keys(), columns=[str(i)])
    else:
        df = pd.merge(df, pd.DataFrame(data[i].values(), index=data[i].keys(), columns=[str(i)]), 
                      left_index=True, right_index=True, how='outer').fillna(0)

# Compute period evolution scores
for i in range(0, len(data_names) - 1):
    ratio = df[data_names[i + 1]] / df[data_names[i]]
    df[str(data_names[i + 1] + '/' + data_names[i])] = ratio 

sc_df = df.fillna(1).replace('%','',regex=True).astype('float')

# Change default font
custom_style = pygal.style.Style(
    background='white',
    plot_background='white',
    font_family='Lato')

# First lost, not coming back
sort_data = sc_df.sort_values(by="1990_1994/1985_1989",ascending=False)
data = sort_data.loc[(sc_df["1990_1994/1985_1989"] <= 0.8) &
                     (sc_df["1995_1999/1990_1994"] <= 0.8) &
                     (sc_df["2000_2004/1995_1999"] <= 1.2) & 
                     (sc_df["2000_2004/1995_1999"] >= 0.8) & 
                     (sc_df["2005_2009/2000_2004"] <= 1.2) & 
                     (sc_df["2005_2009/2000_2004"] >= 0.8) & 
                     (sc_df["2010_2014/2005_2009"] <= 1.2) &
                     (sc_df["2010_2014/2005_2009"] >= 0.8), data_names][:12]

line_chart = pygal.Line(logarithmic=False, legend_at_bottom=True, 
                        style=custom_style, y_title='# Normalized published articles')
line_chart.title = 'Old loss in published papers keywords'
line_chart.x_labels = list(data.keys())
for row in data.iterrows():
    line_chart.add(str(row[0]), list(row[1]))
line_chart.render_to_file(ROOT_PATH + '/old_loss.svg')
#SVG(filename=ROOT_PATH + '/old_loss.svg')


# Last increase
sort_data = sc_df.sort_values(by="2010_2014/2005_2009",ascending=False)
data = sort_data.loc[(sc_df["1990_1994/1985_1989"] >= 0.8) &
                     (sc_df["1990_1994/1985_1989"] <= 1.2) &
                     (sc_df["1995_1999/1990_1994"] >= 0.8) &
                     (sc_df["1995_1999/1990_1994"] <= 1.2) &
                     (sc_df["2000_2004/1995_1999"] <= 1.2) &
                     (sc_df["2000_2004/1995_1999"] >= 0.8) &
                     (sc_df["2005_2009/2000_2004"] <= 1.2) & 
                     (sc_df["2005_2009/2000_2004"] >= 0.8) & 
                     (sc_df["2010_2014/2005_2009"] >= 1.4), data_names][:12]


line_chart = pygal.Line(logarithmic=False, legend_at_bottom=True, 
                        style=custom_style, y_title='# Normalized published articles')
line_chart.title = 'Recent increase in published papers keywords'
line_chart.x_labels = list(data.keys())
for row in data.iterrows():
    line_chart.add(str(row[0]), list(row[1]))
line_chart.render_to_file(ROOT_PATH + '/recent_increase.svg')
#SVG(filename=ROOT_PATH + '/recent_increase.svg')


# Steady growth
sort_data = sc_df.sort_values(by="2005_2009/2000_2004",ascending=False)
data = sort_data.loc[(sc_df["1990_1994/1985_1989"] >= 0.8) &
                     (sc_df["1990_1994/1985_1989"] <= 1.2) &
                     (sc_df["1995_1999/1990_1994"] >= 0.8) &
                     (sc_df["1995_1999/1990_1994"] <= 1.2) &
                     (sc_df["2000_2004/1995_1999"] <= 1.2) &
                     (sc_df["2000_2004/1995_1999"] >= 0.8) &
                     (sc_df["2005_2009/2000_2004"] >= 1.2) &  
                     (sc_df["2010_2014/2005_2009"] >= 0.8), data_names][:12]


line_chart = pygal.Line(logarithmic=False, legend_at_bottom=True, 
                        style=custom_style, y_title='# Normalized published articles')
line_chart.title = 'Steady interest in published papers keywords'
line_chart.x_labels = list(data.keys())
for row in data.iterrows():
    line_chart.add(str(row[0]), list(row[1]))
line_chart.render_to_file(ROOT_PATH + '/steady_interest.svg')
#SVG(filename=ROOT_PATH + '/steady_interest.svg')


# Moment of glory
data = sc_df.sort_values(by="1995_1999/1990_1994",ascending=False)
data = sort_data.loc[(sc_df["1990_1994/1985_1989"] >= 0.8) &
                     (sc_df["1990_1994/1985_1989"] <= 1.2) &
                     (sc_df["1995_1999/1990_1994"] >= 1.2) &
                     (sc_df["2000_2004/1995_1999"] <= 0.8) &
                     (sc_df["2005_2009/2000_2004"] <= 1.2) &
                     (sc_df["2005_2009/2000_2004"] >= 0.8) &
                     (sc_df["2010_2014/2005_2009"] >= 0.8) &
                     (sc_df["2010_2014/2005_2009"] <= 1.2), data_names][:12]


line_chart = pygal.Line(logarithmic=False, legend_at_bottom=True, 
                        style=custom_style, y_title='# Normalized published articles')
line_chart.title = 'Temporary interest in published papers keywords'
line_chart.x_labels = list(data.keys())
for row in data.iterrows():
    line_chart.add(str(row[0]), list(row[1]))
line_chart.render_to_file(ROOT_PATH + '/moment_glory.svg')
#SVG(filename=ROOT_PATH + '/moment_glory.svg')

#Focused targets
data = sc_df[[0, 1, 2, 3, 4, 5]].ix[['Host-Pathogen Interactions', 
                                     'Listeria monocytogenes', 
                                     'Staphylococcus aureus', 
                                     'RNA, Bacterial', 
                                     'Microbiota', 
                                     'Transcriptome']]
line_chart = pygal.StackedLine(fill=True, legend_at_bottom=True, 
                               style=custom_style, y_title='# Normalized published articles', 
                               truncate_legend=-1)
line_chart.title = 'Evolution in time of selected topics'
line_chart.x_labels = list(data.keys())
for row in data.iterrows():
    line_chart.add(str(row[0]), list(row[1]), show_dots=False)
line_chart.render_to_file(ROOT_PATH + '/Topics_Line_2010_2014.svg')
#SVG(filename=ROOT_PATH + '/Topics_Line_2010_2014.svg')

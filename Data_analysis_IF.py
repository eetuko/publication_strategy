import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import pygal
import numpy as np

ROOT_PATH = os.path.join(os.getcwd(), 'data')
if not os.path.isdir(ROOT_PATH):
    os.mkdir(ROOT_PATH)


# Read in data top keyword counts
data = dict()
data_names = []
for i in range(1985, 2015, 5):
    for low, high in [(0, 5), (5, 15), (15, 100)]:
        with open(ROOT_PATH + "/mostcommon_" + str(i) + "_" + str(i + 4) + '_IF_' + 
                  str(low) + '_' + str(high) + ".txt", "r") as data_file:
            data[str(i) + "_" + str(i + 4) + '_IF_' + str(low) + '_' + str(high)] = json.load(data_file)
            data_names.append(str(i) + "_" + str(i + 4) + '_IF_' + str(low) + '_' + str(high)) 

# Merge dicts into dataframe
df = pd.DataFrame()
for i in data_names:
    if df.empty:
        df = pd.DataFrame(data[i].values(), index=data[i].keys(), columns=[str(i)])
    else:
        df = pd.merge(df, pd.DataFrame(data[i].values(), index=data[i].keys(), columns=[str(i)]), 
                      left_index=True, right_index=True, how='outer').fillna(0)

sc_df = df.replace('%','',regex=True).astype('float')

# Change default font
custom_style = pygal.style.Style(
    background='white',
    plot_background='white',
    font_family='Lato')

# if random subsampling done with following :
# data = sc_df[[15, 16, 17]].take(np.random.permutation(len(sc_df[[15, 16, 17]]))[:500])
data = sc_df[[15, 16, 17]]
line_chart = pygal.Line(show_legend=False, legend_at_bottom=True, 
                        style=custom_style, y_title='# Normalized published articles')
line_chart.title = 'Influence of IF on 2010-2014'
line_chart.x_labels = list(x.lstrip('2010_2014_') for x in data.keys())
for row in data.iterrows():
    line_chart.add(str(row[0]), list(row[1]))
line_chart.render_to_file(ROOT_PATH + '/IF_2010_2014.svg')
#SVG(filename=ROOT_PATH + '/IF_2010_2014.svg')


data = sc_df[[12, 13, 14]]
line_chart = pygal.Line(show_legend=False, legend_at_bottom=True, 
                        style=custom_style, y_title='# Normalized published articles')
line_chart.title = 'Influence of IF on 2005-2009'
line_chart.x_labels = list(x.lstrip('2005_2009_') for x in data.keys())
for row in data.iterrows():
    line_chart.add(str(row[0]), list(row[1]))
line_chart.render_to_file(ROOT_PATH + '/IF_2005_2009.svg')
#SVG(filename=ROOT_PATH + '/IF_2005_2009.svg')

# Specific topics
data = sc_df[[15, 16, 17]].ix[['Host-Pathogen Interactions', 
                               'Listeria monocytogenes', 
                               'Staphylococcus aureus', 
                               'RNA, Bacterial', 
                               'Microbiota', 
                               'Transcriptome']]
bar_chart = pygal.Bar(truncate_legend=-1, legend_at_bottom=True, style=custom_style)
bar_chart.title = 'Selected topics'
bar_chart.x_labels = list(x.lstrip('2010_2014') for x in data.keys())
for row in data.iterrows():
    bar_chart.add(str(row[0]), list(row[1]))
bar_chart.render_to_file(ROOT_PATH + '/Topics_Bar_IF_2010_2014.svg')
#SVG(filename=ROOT_PATH + '/Topics_Bar_IF_2010_2014.svg')
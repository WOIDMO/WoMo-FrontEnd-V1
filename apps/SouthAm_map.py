# MIT-License
#
# Copyright 2020 World Infectious Disease Monitoring Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
# South America Maps
#

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from appfw import app
#Load the data
data_SAM = pd.read_csv("./data/CL_stats.csv")

#Add state abbreviations
ddfm = data_SAM.copy() #!!!!!!!!Make an actual copy
ddfm.drop(ddfm[ddfm.jurisdiction == 'Chile-North'].index, inplace=True)
ddfm.drop(ddfm[ddfm.jurisdiction == 'Chile-Central'].index, inplace=True)
ddfm.drop(ddfm[ddfm.jurisdiction == 'Chile-South'].index, inplace=True)
#ddfm.drop(ddfm[ddfm.jurisdiction == 'New York City'].index, inplace=True)


#print(ddfm)

#Generate date slider list
dates = data_SAM.date.unique()
date_options = {}
weeks=0
import datetime
for date_item in dates:
    date_item = datetime.datetime.strptime(date_item, "%Y-%m-%d").date()
    if (weeks == 0):
        date_options[weeks] = date_item.strftime("%b %d")
    else:
        date_options[weeks] = date_item.strftime("%b %d")
    weeks = weeks + 1

#Pick a default date
inprogress = data_SAM['date'][data_SAM.index[-3]]
first_date = data_SAM['date'][data_SAM.index[0]]
last_date = data_SAM['date'][data_SAM.index[-1]]

#Set up the charts
import plotly.express as px
import plotly.graph_objects as go

#figSAM = go.figSAMure() # or any Plotly Express function e.g. px.bar(...)
figSAM = px.choropleth()
bar1SAM = px.bar()
bar2SAM = px.bar()

colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"
] # or px.colors.sequential.Plasma

#Style the charts
plotcfg = {'displayModeBar': False}
#figSAM1.update_xaxes(rangeslider_visible=True)
figSAM.update_layout(height=500, margin=dict(l=0, r=0, b=0, t=0, pad=0), coloraxis_colorbar=dict(title="Z-score"), plot_bgcolor='rgb(255,255,255)')

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

layout = html.Div([
    dcc.Graph(id='map-SAM', figure=figSAM, config=plotcfg),
    dcc.Slider(
        id='date-slider',
        min=0,
        max=weeks-1,
        step=None,
        marks=date_options,
        value=weeks-3),
    html.Div([html.P("2020")],
             style={'color': '#666',
                    'padding-left': '4px',
                    'margin-top': '-10px',
                    'text-align': 'left',
                    'fontSize': '12px',
                    'backgroundColor': '#fffff'}),
    html.Div(id='slider-output-container-SAM'),
    dcc.Graph(id='graph4-SAM', figure=bar1SAM, config=plotcfg),
    dcc.Graph(id='graph5-SAM', figure=bar2SAM, config=plotcfg)
])

#@app.callback(
#    dash.dependencies.Output('slider-output-container', 'children'),
#    [dash.dependencies.Input('date-slider', 'value')])
#def update_output(value):
#    selected_date = dates[value]
#    return 'You have selected "{}"'.format(selected_date)

@app.callback(
    dash.dependencies.Output(component_id='map-SAM', component_property='figure'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_df(value):
    selected_date = dates[value]
    ddfmp = ddfm[ddfm['date'] == selected_date]
    figSAM = px.choropleth(locations=ddfmp['jurisdiction'], locationmode="country names", color=ddfmp['s_z'], scope="south america",
                        color_continuous_scale=colorscale, range_color=(0, 15),
                        labels={'color': 'Z-score', 'locations': 'State'})
    figSAM.update_layout(height=500, margin=dict(l=0, r=0, b=0, t=0, pad=0), coloraxis_colorbar=dict(title="Z-score"), plot_bgcolor='rgb(255,255,255)', geo = dict(showlakes=True))
    return figSAM

@app.callback(
    dash.dependencies.Output(component_id='graph4-SAM', component_property='figure'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_df(value):
    selected_date = dates[value]
    ddf = data_SAM[data_SAM['date'] == selected_date]
    ddfz = ddf.sort_values(by=['s_z'], ascending=False)
    bar1SAM = px.bar(ddfz, x='jurisdiction', y='s_z', labels={'s_z': 'Z-score', 'jurisdiction': 'State'})
    bar1SAM.update_layout(barmode='group', xaxis_tickangle=-45, height=300, margin=dict(l=0, r=0, b=0, t=0, pad=0),
                       xaxis_title="",
                       yaxis_title="Z-score", legend_title_text='Data')
    return bar1SAM

@app.callback(
    dash.dependencies.Output(component_id='graph5-SAM', component_property='figure'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_df(value):
    selected_date = dates[value]
    ddf = data_SAM[data_SAM['date'] == selected_date]
    ddfc = ddf.sort_values(by=['cum_excess_std0'], ascending=False)
    ddfc.drop(ddfc[ddfc.jurisdiction == 'United States'].index, inplace=True)
    bar2SAM = px.bar(ddfc, x='jurisdiction', y='cum_excess_std0',
                  labels={'cum_excess': 'Cumulated Excess Mortality', 'jurisdiction': 'State'})
    bar2SAM.update_layout(barmode='group', xaxis_tickangle=-45, height=300, margin=dict(l=0, r=0, b=0, t=0, pad=0),
                       xaxis_title="",
                       yaxis_title="Cumulated Excess Mortality", legend_title_text='Data')
    return bar2SAM


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
# South America Charts
#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from appfw import app

#Load the data
data_SAM = pd.read_csv("./data/CL_stats.csv")

#Generate the states dropdown list
states = data_SAM.jurisdiction.unique()
drop_options = []
for state in states:
    drop_options.append(dict(label=state, value=state))

#In progress dates
first_date = data_SAM['date'][data_SAM.index[0]]
inprogress_start = data_SAM['date'][data_SAM.index[-3]]
inprogress_end = data_SAM['date'][data_SAM.index[-1]]

#Set up the charts
import plotly.express as px
#fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
fig1SAM = px.line()
fig2SAM = px.line()
fig3SAM = px.line()

#Style the charts
plotcfg = {'displayModeBar': False}
#fig1SAM.update_xaxes(rangeslider_visible=True)

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

layout = html.Div([
        html.P([
        html.Label("Choose a dataset"),

        dcc.Dropdown(
        id='state-dropdown',
        options=drop_options,
        value='Chile')],
            style = {'width': '200px',
                    'fontSize' : '12px',
                    'padding-left' : '50px',
                    'display': 'inline-block'}),
    dcc.Graph(id='graph1-SAM', figure=fig1SAM, config=plotcfg),
    dcc.Graph(id='graph2-SAM', figure=fig2SAM,config=plotcfg),
    dcc.Graph(id='graph3-SAM', figure=fig3SAM,config=plotcfg),
    html.Div(id='dd-output-container-SAM'),
    html.Div([html.P("woidmo.org")],
                     style = {'padding-right' : '10px' ,
                              'margin-top' : '-10px',
                              'text-align' : 'right',
                              'fontSize' : '12px',
                              'backgroundColor' : '#fffff'})
])

#@app.callback(
#    dash.dependencies.Output('dd-output-container', 'children'),
#    [dash.dependencies.Input('state-dropdown', 'value')])
#def update_output(value):
#    ddf=data_SAM[data_SAM['jurisdiction'] == format(value)]
#    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output(component_id='graph1-SAM', component_property='figure'),
    [dash.dependencies.Input('state-dropdown', 'value')])
def update_df(value):
    ddf=data_SAM[data_SAM['jurisdiction'] == format(value)]
    fig1SAM = px.line(ddf, x="date", y="natural_cause", color="jurisdiction", line_group="jurisdiction", labels={'natural_cause':'Mortality/Week', 'jurisdiction':'State'})
    fig1SAM.add_scatter(x=ddf["date"], y=ddf["s_mean"], mode='lines', name="Baseline", line_color='rgba(0,200,0,0.3)')
    fig1SAM.add_scatter(x=ddf["date"], y=ddf["s_mean"] - ddf["s_std"], mode='lines', showlegend=False,line_color='rgba(0,200,0,0.15)', fill = 'tonexty', fillcolor='rgba(0,200,0,0.1)' )
    fig1SAM.add_scatter(x=ddf["date"], y=ddf["s_mean"] + ddf["s_std"], mode='lines', showlegend=False,line_color='rgba(0,200,0,0.15)', fill = 'tonexty', fillcolor='rgba(0,200,0,0.1)' )
    fig1SAM.update_layout(autosize=True, height=250, margin=dict(l=0, r=0, b=0, t=0, pad=0), xaxis_title="",
                       yaxis_title="Mortality / Week", legend_title_text='Data', xaxis= {'tick0': first_date , 'dtick': 86400000*7})
    fig1SAM.update_layout(
        shapes=[
            # 1st highlight during Feb 4 - Feb 6
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=inprogress_start,
                y0=0,
                x1=inprogress_end,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0,
            )])
    return fig1SAM

@app.callback(
    dash.dependencies.Output(component_id='graph2-SAM', component_property='figure'),
    [dash.dependencies.Input('state-dropdown', 'value')])
def update_df(value):
    ddf=data_SAM[data_SAM['jurisdiction'] == format(value)]
    fig2SAM = px.line(ddf, x="date", y="cum_excess_std0", color="jurisdiction", line_group="jurisdiction", labels={'cum_excess':'Cumulated Excess Mortality', 'jurisdiction':'State'})
    fig2SAM.add_scatter(x=ddf["date"], y=ddf["cum_excess_std1"], mode='lines', name="1 std Excess", line_color='rgba(0,200,0,1)')
    fig2SAM.add_scatter(x=ddf["date"], y=ddf["cum_excess_std2"], mode='lines', name="2 std Excess", line_color='rgba(200,0,0,1)')
    fig2SAM.update_layout(autosize=True, height=250, margin=dict(l=0, r=0, b=0, t=0, pad=0), xaxis_title="",
                       yaxis_title="Cumulated Excess Mortality", legend_title_text='Data', xaxis= {'tick0': first_date , 'dtick': 86400000*7})
    fig2SAM.update_layout(
        shapes=[
            # 1st highlight during Feb 4 - Feb 6
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=inprogress_start,
                y0=0,
                x1=inprogress_end,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0,
            )])
    return fig2SAM

@app.callback(
    dash.dependencies.Output(component_id='graph3-SAM', component_property='figure'),
    [dash.dependencies.Input('state-dropdown', 'value')])
def update_df(value):
    ddf=data_SAM[data_SAM['jurisdiction'] == format(value)]
    fig3SAM = px.line(ddf, x="date", y="s_z", color="jurisdiction", line_group="jurisdiction", labels={'s_z':'Z-score', 'jurisdiction':'State'})
    fig3SAM.update_layout(autosize=True, height=250, margin=dict(l=0, r=0, b=0, t=0, pad=0), xaxis_title="",
                       yaxis_title="Z-score", legend_title_text='Data', xaxis= {'tick0': first_date , 'dtick': 86400000*7})
    fig3SAM.update_layout(
        shapes=[
            # 1st highlight during Feb 4 - Feb 6
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=inprogress_start,
                y0=0,
                x1=inprogress_end,
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0,
            )])
    return fig3SAM
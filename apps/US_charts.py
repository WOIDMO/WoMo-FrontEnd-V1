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
# USA Charts
#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from appfw import app

#Load the data
data_US = pd.read_csv("./data/US_stats.csv")

#Generate the states dropdown list
states = data_US.jurisdiction.unique()
drop_options = []
for state in states:
    drop_options.append(dict(label=state, value=state))

#In progress dates
first_date = data_US['date'][data_US.index[0]]
inprogress_start = data_US['date'][data_US.index[-3]]
inprogress_end = data_US['date'][data_US.index[-1]]

#Set up the charts
import plotly.express as px
#fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
fig1 = px.line()
fig2 = px.line()
fig3 = px.line()

#Style the charts
plotcfg = {'displayModeBar': False}
#fig1.update_xaxes(rangeslider_visible=True)

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
        value='United States')],
            style = {'width': '200px',
                    'fontSize' : '12px',
                    'padding-left' : '50px',
                    'display': 'inline-block'}),
    dcc.Graph(id='graph1', figure=fig1, config=plotcfg),
    dcc.Graph(id='graph2', figure=fig2,config=plotcfg),
    dcc.Graph(id='graph3', figure=fig3,config=plotcfg),
    html.Div(id='dd-output-container'),
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
#    ddf=data_US[data_US['jurisdiction'] == format(value)]
#    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output(component_id='graph1', component_property='figure'),
    [dash.dependencies.Input('state-dropdown', 'value')])
def update_df(value):
    ddf=data_US[data_US['jurisdiction'] == format(value)]
    fig1 = px.line(ddf, x="date", y="natural_cause", color="jurisdiction", line_group="jurisdiction", labels={'natural_cause':'Mortality/Week', 'jurisdiction':'State'})
    fig1.add_scatter(x=ddf["date"], y=ddf["s_mean"], mode='lines', name="Baseline", line_color='rgba(0,200,0,0.3)')
    fig1.add_scatter(x=ddf["date"], y=ddf["s_mean"] - ddf["s_std"], mode='lines', showlegend=False,line_color='rgba(0,200,0,0.15)', fill = 'tonexty', fillcolor='rgba(0,200,0,0.1)' )
    fig1.add_scatter(x=ddf["date"], y=ddf["s_mean"] + ddf["s_std"], mode='lines', showlegend=False,line_color='rgba(0,200,0,0.15)', fill = 'tonexty', fillcolor='rgba(0,200,0,0.1)' )
    fig1.update_layout(autosize=True, height=250, margin=dict(l=0, r=0, b=0, t=0, pad=0), xaxis_title="",
                       yaxis_title="Mortality / Week", legend_title_text='Data', xaxis= {'tick0': first_date , 'dtick': 86400000*7})
    fig1.update_layout(
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
    return fig1

@app.callback(
    dash.dependencies.Output(component_id='graph2', component_property='figure'),
    [dash.dependencies.Input('state-dropdown', 'value')])
def update_df(value):
    ddf=data_US[data_US['jurisdiction'] == format(value)]
    fig2 = px.line(ddf, x="date", y="cum_excess_std0", color="jurisdiction", line_group="jurisdiction", labels={'cum_excess':'Cumulated Excess Mortality', 'jurisdiction':'State'})
    fig2.add_scatter(x=ddf["date"], y=ddf["cum_excess_std1"], mode='lines', name="1 std Excess", line_color='rgba(0,200,0,1)')
    fig2.add_scatter(x=ddf["date"], y=ddf["cum_excess_std2"], mode='lines', name="2 std Excess", line_color='rgba(200,0,0,1)')
    fig2.update_layout(autosize=True, height=250, margin=dict(l=0, r=0, b=0, t=0, pad=0), xaxis_title="",
                       yaxis_title="Cumulated Excess Mortality", legend_title_text='Data', xaxis= {'tick0': first_date , 'dtick': 86400000*7})
    fig2.update_layout(
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
    return fig2

@app.callback(
    dash.dependencies.Output(component_id='graph3', component_property='figure'),
    [dash.dependencies.Input('state-dropdown', 'value')])
def update_df(value):
    ddf=data_US[data_US['jurisdiction'] == format(value)]
    fig3 = px.line(ddf, x="date", y="s_z", color="jurisdiction", line_group="jurisdiction", labels={'s_z':'Z-score', 'jurisdiction':'State'})
    fig3.update_layout(autosize=True, height=250, margin=dict(l=0, r=0, b=0, t=0, pad=0), xaxis_title="",
                       yaxis_title="Z-score", legend_title_text='Data', xaxis= {'tick0': first_date , 'dtick': 86400000*7})
    fig3.update_layout(
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
    return fig3
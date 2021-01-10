#
# USA Maps
#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from appfw import app
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'New York City': 'NYC',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))
#code=us_state_abbrev['Wisconsin']
#print(code)

#Load the data
data_US = pd.read_csv("./data/US_stats.csv")

#Add state abbreviations
ddfm = data_US.copy() #!!!!!!!!Make an actual copy
ddfm.drop(ddfm[ddfm.jurisdiction == 'United States'].index, inplace=True)
#ddfm.drop(ddfm[ddfm.jurisdiction == 'New York City'].index, inplace=True)
#ddfm.drop(ddfm[ddfm.s_z < 1].index, inplace=True)
ddfm['state_abr'] = ''
for ind in ddfm.index:
    #print(data_US.jurisdiction[ind])
    abr = us_state_abbrev[ddfm.jurisdiction[ind]]
    ddfm.loc[ind, 'state_abr'] = abr

#print(ddfm)

#Generate date slider list
dates = data_US.date.unique()
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
inprogress = data_US['date'][data_US.index[-3]]
first_date = data_US['date'][data_US.index[0]]
last_date = data_US['date'][data_US.index[-1]]

#Set up the charts
import plotly.express as px
import plotly.graph_objects as go

#fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
fig = px.choropleth()
bar1 = px.bar()
bar2 = px.bar()

colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"
] # or px.colors.sequential.Plasma

#Style the charts
plotcfg = {'displayModeBar': False}
#fig1.update_xaxes(rangeslider_visible=True)
fig.update_layout(height=500, margin=dict(l=0, r=0, b=0, t=0, pad=0), coloraxis_colorbar=dict(title="Z-score"), plot_bgcolor='rgb(255,255,255)')

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}
style_slider = {'writing-mode': 'vertical-rl','text-orientation': 'use-glyph-orientation','white-space': 'nowrap'}
slider_dates = {}
for i, date in date_options.items():
    slider_dates[i] = {'label':date, 'style':style_slider}

layout = html.Div([
    dcc.Graph(id='map', figure=fig, config=plotcfg),
    dcc.Slider(
        id='date-slider',
        min=0,
        max=weeks-1,
        step=None,
        marks=slider_dates,
        value=weeks-3),
    html.Div([html.P("2020")],
             style={'color': '#666',
                    'padding-left': '4px',
                    'margin-top': '-10px',
                    'text-align': 'left',
                    'fontSize': '12px',
                    'backgroundColor': '#fffff'}),
    html.Div(id='slider-output-container'),
    dcc.Graph(id='graph4', figure=bar1, config=plotcfg),
    dcc.Graph(id='graph5', figure=bar2, config=plotcfg)
])

#@app.callback(
#    dash.dependencies.Output('slider-output-container', 'children'),
#    [dash.dependencies.Input('date-slider', 'value')])
#def update_output(value):
#    selected_date = dates[value]
#    return 'You have selected "{}"'.format(selected_date)

@app.callback(
    dash.dependencies.Output(component_id='map', component_property='figure'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_df(value):
    selected_date = dates[value]
    ddfmp = ddfm[ddfm['date'] == selected_date]
    fig = px.choropleth(locations=ddfmp['state_abr'], locationmode="USA-states", color=ddfmp['s_z'], scope="usa",
                        color_continuous_scale=colorscale, range_color=(0, 15),
                        labels={'color': 'Z-score', 'locations': 'State'})
    fig.update_layout(height=500, margin=dict(l=0, r=0, b=0, t=0, pad=0), coloraxis_colorbar=dict(title="Z-score"), plot_bgcolor='rgb(255,255,255)', geo = dict(showlakes=True))
    return fig

@app.callback(
    dash.dependencies.Output(component_id='graph4', component_property='figure'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_df(value):
    selected_date = dates[value]
    ddf = data_US[data_US['date'] == selected_date]
    ddfz = ddf.sort_values(by=['s_z'], ascending=False)
    bar1 = px.bar(ddfz, x='jurisdiction', y='s_z', labels={'s_z': 'Z-score', 'jurisdiction': 'State'})
    bar1.update_layout(barmode='group', xaxis_tickangle=-45, height=300, margin=dict(l=0, r=0, b=0, t=0, pad=0),
                       xaxis_title="",
                       yaxis_title="Z-score", legend_title_text='Data')
    return bar1

@app.callback(
    dash.dependencies.Output(component_id='graph5', component_property='figure'),
    [dash.dependencies.Input('date-slider', 'value')])
def update_df(value):
    selected_date = dates[value]
    ddf = data_US[data_US['date'] == selected_date]
    ddfc = ddf.sort_values(by=['cum_excess_std0'], ascending=False)
    ddfc.drop(ddfc[ddfc.jurisdiction == 'United States'].index, inplace=True)
    bar2 = px.bar(ddfc, x='jurisdiction', y='cum_excess_std0',
                  labels={'cum_excess': 'Cumulated Excess Mortality', 'jurisdiction': 'State'})
    bar2.update_layout(barmode='group', xaxis_tickangle=-45, height=300, margin=dict(l=0, r=0, b=0, t=0, pad=0),
                       xaxis_title="",
                       yaxis_title="Cumulated Excess Mortality", legend_title_text='Data')
    return bar2


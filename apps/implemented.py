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
# Implemented countries
#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from appfw import app

import plotly.express as px
import numpy as np

#Load the country datafile
df = pd.read_csv("./data/country_list.csv")
df = df.replace(np.nan, '', regex=True)
#print(df)

colorscale = ["#f7fbff", #No data
              "#00BFFF", #Pending
              "#08306b", #Implemented
              "#B0E0E6", #Limited data
              ]
plotcfg = {'displayModeBar': False}
colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

fig = px.choropleth(df, locations="iso_alpha",
                    color="Status", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_discrete_sequence=colorscale,
                    scope='world',
                    #projection='natural earth',
                    )
fig.update_layout(height=300, margin=dict(l=0, r=0, b=0, t=0, pad=0), coloraxis_colorbar=dict(title="Status"), plot_bgcolor='rgb(255,255,255)', geo = dict(showlakes=True))
fig.update_traces(marker_line_width=0)

#app = dash.Dash()
layout = html.Div([
    html.H3('Implemented countries'),
    dcc.Graph(id='map1', figure=fig, config=plotcfg)
])

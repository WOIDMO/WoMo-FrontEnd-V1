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


import os

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from appfw import app

from apps import implemented, US_charts, US_map, SouthAm_charts ,SouthAm_map, Europe_charts, Europe_map

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/implemented':
        return implemented.layout
    #USA
    elif pathname == '/apps/US_map':
        return US_map.layout
    elif pathname == '/apps/US_charts':
        return US_charts.layout
    #South America
    elif pathname == '/apps/SouthAm_map':
        return SouthAm_map.layout
    elif pathname == '/apps/SouthAm_charts':
        return SouthAm_charts.layout
        # Europe
    elif pathname == '/apps/Europe_map':
        return Europe_map.layout
    elif pathname == '/apps/Europe_charts':
        return Europe_charts.layout
    #Not found
    else:
        return '404'

if __name__ == '__main__':
    #app.run_server(debug=False, host= 0.0.0.0, port=8050, use_reloader=False)
    app.run_server(debug=True)

#https://dash.plotly.com/deployment
#https://www.phillipsj.net/posts/deploying-dash-to-google-app-engine/
#
# Deploy
#heroku login
#git status
#git add .
#git commit -m 'added implemented title'
#git push heroku master
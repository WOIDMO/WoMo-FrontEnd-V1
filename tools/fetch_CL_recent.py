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
#Fetch South America data
#Chile https://estadisticas.sed.srcei.cl/defcom
#05-0",{startdate:e,enddate:t})}
#Ecuador https://www.registrocivil.gob.ec/cifras/
import pandas as pd

#Function to return dates for week of the year
from datetime import date, timedelta
import datetime
import time
import requests

def get_start_end_dates(year, week):
    d = date(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)

def fetch_chile_deaths(start_date, end_date):
    # Import Chile data
    url = 'https://codigo.registrocivil.cl/api/estdefuncion/ltAllComunas/'
    headers = {'Content-type': 'application/json'}
    r = requests.post(url=url, json={'startdate': str(start_date), 'enddate': str(end_date)}, headers=headers)
    #print(r.status_code)
    data = r.json()
    df = pd.DataFrame.from_dict(data)
    #print(df)
    total_deaths = df['total'].sum()
    north_deaths = df[df['zona'] == 'Norte'].sum()['total']
    central_deaths = df[df['zona'] == 'Central'].sum()['total']
    south_deaths = df[df['zona'] == 'Sur'].sum()['total']
    #print(total_deaths)
    return total_deaths, north_deaths, central_deaths, south_deaths

today = datetime.date.today()
year = 2020
current_week = (today - date(year, 1, 1)).days/7
output = pd.DataFrame()
week = 0
while (week <= current_week):
    start_date, end_date = get_start_end_dates(year, week)
    total_deaths, north_deaths, central_deaths, south_deaths = fetch_chile_deaths(start_date, end_date)
    
    print('Year: %d, Week: %d, Start date: %s, End date: %s' % (int(year), int(week), str(start_date), str(end_date)))
    print('Total deaths: %d, North: %d, Central: %d, South: %d' % (int(total_deaths), int(north_deaths), int(central_deaths), int(south_deaths)))
    
    jurisdiction, deaths = ['Chile', 'Chile-North', 'Chile-Central', 'Chile-South'], [total_deaths, north_deaths, central_deaths, south_deaths]
    for j, d in zip(jurisdiction, deaths):
        output = output.append({'date': end_date,
                        'year': end_date.year,
                        'week': week % 52,
                        'jurisdiction': j,
                        'natural_cause': d}, ignore_index=True)
    week += 1

output['year'] = output['year'].astype(int)
output['week'] = output['week'].astype(int)
output['natural_cause'] = output['natural_cause'].astype(int)
output.to_csv("../data/CL_2020.csv", index=False)
print(output)

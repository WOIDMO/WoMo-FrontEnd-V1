#
#EUROSTAT historic processing
#
import pandas as pd
from datetime import date, timedelta
import datetime

#Dictionaries and stuff
ccodes = ['AT', 'BE', 'BG', 'CH', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'HU', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'ME', 'NO', 'PT', 'RS', 'SE', 'SI', 'SK', 'UK', ]
ccodes_trans = {
    'AT': 'Austria',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CH': 'Switzerland ',
    'CZ': 'Czechia',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'ES': 'Spain',
    'FI': 'Finland ',
    'FR': 'France',
    'HU': 'Hungary',
    'IS': 'Iceland',
    'IT': 'Italy',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'ME': 'Montenegro ',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'PT': 'Portugal',
    'RS': 'Serbia',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'UK': 'United Kingdom',
}

def get_start_end_dates(year, week):
    d = date(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)

#Load the trimmed Eurostat file
eurostat_df = pd.read_csv("../data/EUROSTAT_trimmed.csv")

start_year = 2010
end_year = 2019
weeks = 52

output = pd.DataFrame()
totalrows = eurostat_df.shape[0] - 1
current_year = start_year
row = 0
#Iterate over the dataframe to reformat to the standard import format
while (row <= totalrows):
    while (current_year <= end_year):
        current_week = 1
        while(current_week <= weeks):
            col = str(current_year)+"W"+str('{:02}'.format(current_week))
            start_date, end_date = get_start_end_dates(current_year, current_week) #Find start and end date for this week
            #Process the dataframe here
            ccode = eurostat_df.at[row, 'geo']      #Get the corresponding country name fron the abr
            country = ccodes_trans[ccode]
            mortality = eurostat_df.at[row, col]    #Get the mortality from the dataframe
            #print(row, col, end_date, current_year, current_week, country, mortality)
            row_dict = {'date': end_date, 'year': current_year,'week': current_week, 'jurisdiction': country, 'natural_cause': mortality}
            print(row_dict)
            output = output.append(row_dict, ignore_index=True)
            current_week += 1
        print("NEXT YEAR")
        current_year += 1
        current_week = 1
    print("NEXT ROW")
    current_week = 1
    current_year = start_year
    row += 1
    print("NEXT COUNTRY")

output.to_csv (r'../data/EUROSTAT_historic.csv', header=True, index=False)
#country = ccodes_trans['AT']
#eurostat_df.at[0,'geo']
#eurostat_df.at[0,'2020W19']
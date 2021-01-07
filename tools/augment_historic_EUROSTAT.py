#
#Augment EUROSTAT historic stats with data from mortality.org
#
import pandas as pd
from datetime import date, timedelta
import datetime
import numpy as np

#Dictionaries and stuff
ccodes = ['AT', 'BE', 'BG', 'CH', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'HU', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'ME', 'NO', 'PT', 'RS', 'SE', 'SI', 'SK', 'UK', ]
ccodes_trans = {
    'AUT': 'Austria',
    'BEL': 'Belgium',
    'BGR': 'Bulgaria',
    'CH': 'Switzerland ',
    'CZE': 'Czechia',
    'DEUTNP': 'Germany',
    'DNK': 'Denmark',
    'EST': 'Estonia',
    'ESP': 'Spain',
    'FIN': 'Finland ',
    'FRATNP': 'France',
    'HUN': 'Hungary',
    'ISL': 'Iceland',
    'ITA': 'Italy',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LUX': 'Luxembourg',
    'LV': 'Latvia',
    'ME': 'Montenegro ',
    'NLD': 'Netherlands',
    'NOR': 'Norway',
    'PRT': 'Portugal',
    'RS': 'Serbia',
    'SWE': 'Sweden',
    'SI': 'Slovenia',
    'SVK': 'Slovakia',
    'GBRTENW': 'England',
    'GBR_SCO': 'Scotland',
    'USA': 'United States'
}

def get_start_end_dates(year, week):
    d = date(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt, d + dlt + timedelta(days=6)

#Vars
start_year = 2010
end_year = 2019
weeks = 52

#Load the historic Eurostat file
eurostat_historic_df = pd.read_csv("../data/EUROSTAT_historic.csv")

#Load the mortality.org file and clean up, Drop the US and everything below 2010
mort_org_df = pd.read_csv("../data/historic-augment/stmf.csv")
mort_org_df.drop(mort_org_df[mort_org_df.CountryCode == 'USA'].index, inplace=True)
mort_org_df.drop(mort_org_df[mort_org_df.Sex == 'f'].index, inplace=True)
mort_org_df.drop(mort_org_df[mort_org_df.Sex == 'm'].index, inplace=True)
mort_org_df.drop(mort_org_df[mort_org_df.Year < start_year].index, inplace=True)
mort_org_df.drop(mort_org_df[mort_org_df.Year > end_year].index, inplace=True)
mort_org_df.reset_index(drop=True, inplace=True)

#Translate the country codes to actual names
totalrows = mort_org_df.shape[0] - 1
row = 0
while (row <= totalrows):
    # Process the dataframe here
    ccode = mort_org_df.at[row, 'CountryCode']  # Get the corresponding country name from the abr
    country = ccodes_trans[ccode]
    #print(country)
    mort_org_df.loc[row,'jurisdiction'] = country
    row +=1

#
# Update United Kingdom, needs combination of Scotland and England

#Combine England and Scotland into United Kingdom
df_scotland = mort_org_df[mort_org_df.jurisdiction == 'Scotland']
df_scotland.reset_index(drop=True, inplace=True)
df_england = mort_org_df[mort_org_df.jurisdiction == 'England']
df_england.reset_index(drop=True, inplace=True)

df_england['natural_cause'] = df_england['DTotal'] + df_scotland['DTotal']
#Add the two entities and append as United Kingdom
print('Processing UK ---------------------')
totalrows = df_england.shape[0] - 1
row = 0
jurisdiction = 'United Kingdom'
while (row <= totalrows):
    row_year = df_england['Year'][row]
    row_week = df_england['Week'][row]
    condition = ((eurostat_historic_df.jurisdiction == jurisdiction) &
              (eurostat_historic_df.year == row_year) &
              (eurostat_historic_df.week == row_week) &
              (eurostat_historic_df.natural_cause > 0)
              )
    if (condition.any() == False):
        query = "jurisdiction == '" + jurisdiction + "' & year == " + str(row_year) + " & week == " + str(row_week)
        index_EU = eurostat_historic_df.query(query).index[0]
        print("INSERT " + str(row_year) +" "+ str(row_week) +" "+ str(condition.any()) +" "+ str(index_EU))
        eurostat_historic_df['natural_cause'][index_EU] = df_england['natural_cause'][row]
    row += 1


#
#Update all data from mort_org

#Drop eveything related to UK in mort_org
mort_org_df.drop(mort_org_df[mort_org_df.CountryCode == 'GBRTENW'].index, inplace=True)
mort_org_df.drop(mort_org_df[mort_org_df.CountryCode == 'GBR_SCO'].index, inplace=True)
mort_org_df.reset_index(drop=True, inplace=True)

print('Processing EU -------------------------')

for index, row in mort_org_df.iterrows():
    print(row['jurisdiction'])
    jurisdiction = row['jurisdiction']
    row_year = row['Year']
    row_week = row['Week']
    row_natural_cause = row['DTotal']
    condition = ((eurostat_historic_df.jurisdiction == jurisdiction) &
                 (eurostat_historic_df.year == row_year) &
                 (eurostat_historic_df.week == row_week) &
                 (eurostat_historic_df.natural_cause > 0)
                 )
    if (condition.any() == False):
        query = "jurisdiction == '" + jurisdiction + "' & year == " + str(row_year) + " & week == " + str(row_week)
        index_EU = eurostat_historic_df.query(query).index[0]
        print("INSERT " + str(row_year) + " " + str(row_week) + " " + str(condition.any()) + " " + str(index_EU))
        eurostat_historic_df['natural_cause'][index_EU] = row_natural_cause

eurostat_historic_df.to_csv (r'../data/EUROSTAT_historic.csv', header=True, index=False)
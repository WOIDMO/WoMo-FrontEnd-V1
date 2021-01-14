#
#EUROSTAT import
#

# https://ec.europa.eu/eurostat/cache/metadata/en/demomwk_esms.htm
# https://ec.europa.eu/eurostat/web/products-datasets/-/demo_r_mweek3

import eurostat

#Import the data from Eurostat
eurost_df = eurostat.get_data_df('demo_r_mweek3', flags=False)
#Rename column 'geo\time' to 'geo'
eurost_df.rename(columns={r'geo\time': 'geo'}, inplace=True)
#Select for totals sex and age groups
trimmed_df = eurost_df[(eurost_df['sex'] == "T") & (eurost_df['age'] == "TOTAL")]
#Trim to the country totals data
ccodes = ['AT', 'BE', 'BG', 'CH', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'HU', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'ME', 'NL', 'NO', 'PT', 'RS', 'SE', 'SI', 'SK', 'UK', ]
countries_df = trimmed_df[trimmed_df['geo'].isin(ccodes)]

#Output downloaded data
eurost_df.to_csv (r'../data/EUROSTAT_full.csv', header=True, index=False)
countries_df.to_csv (r'../data/EUROSTAT_trimmed.csv', header=True, index=False)

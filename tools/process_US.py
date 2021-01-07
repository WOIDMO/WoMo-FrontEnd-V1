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

# Load the Pandas libraries with alias 'pd'
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns

#
# Concat the df's and rename the columns in the historic data to match the 2019 format
dfs = []

data_old1 = pd.read_csv("../data/2014w1-2018w52-1.csv")
data_old1.rename(columns={'weekendingdate':'week_ending_date',
                          'allcause':'all_cause',
                          'naturalcause':'natural_cause'}, inplace=True)
dfs.append(data_old1)

data_old2 = pd.read_csv("../data/2014w1-2018w52-2.csv")
data_old2.rename(columns={'weekendingdate':'week_ending_date',
                          'allcause':'all_cause',
                          'naturalcause':'natural_cause'}, inplace=True)
dfs.append(data_old2)

data_new = pd.read_csv("../data/2019w1-2020w20.csv")
dfs.append(data_new)

data_all = pd.concat(dfs, ignore_index=True)

#
#Clean up the years in new and historic data
data_new.drop(data_new[data_new.mmwryear == 2019].index, inplace=True) #Remove the last year from new data
data_all.drop(data_all[data_all.mmwryear == 2020].index, inplace=True) #Remove the current year in historic data

#
#Convert the year/week columns to something pandas can deal with
data_new['formatted_date'] = data_new.mmwryear * 1000 + data_new.mmwrweek * 10 + 0
data_new['date'] = pd.to_datetime(data_new['formatted_date'], format='%Y%W%w')
data_all['formatted_date'] = data_all.mmwryear * 1000 + data_all.mmwrweek * 10 + 0
data_all['date'] = pd.to_datetime(data_all['formatted_date'], format='%Y%W%w')
#all_data.head()
#print(all_data[all_data.jurisdiction_of_occurrence.eq('Alabama')])


#
#Process the stats for each state
dfs_stats = []
states = data_new.jurisdiction_of_occurrence.unique()
for state in states:
    df_new_state = data_new[data_new.jurisdiction_of_occurrence.eq(state)] #Extract data for this state from new
    df_all_state = data_all[data_all.jurisdiction_of_occurrence.eq(state)] #Extract data for this state from historic

    #
    #Generate the stats from the historic data and merge with the new data
    df_stats = pd.DataFrame()
    df_new_state.set_index('mmwrweek', inplace=True) #Create an index based on the current year
    df_stats['date'] = df_new_state['date']
    df_stats['week'] = df_stats.index
    df_stats['jurisdiction'] = state
    df_stats['natural_cause'] = df_new_state['natural_cause']
    df_stats['s_min'] = df_all_state.groupby('mmwrweek')['natural_cause'].min()
    df_stats['s_mean'] = df_all_state.groupby('mmwrweek')['natural_cause'].mean()
    df_stats['s_max'] = df_all_state.groupby('mmwrweek')['natural_cause'].max()
    df_stats['s_std'] = df_all_state.groupby('mmwrweek')['natural_cause'].std()
    # Excess +-
    df_stats['excess'] = df_stats['natural_cause'] - df_stats['s_mean']
    # std0
    df_stats['excess_std0'] = df_stats['natural_cause'] - df_stats['s_mean']
    df_stats['excess_std0'] = df_stats['excess_std0'].clip(lower=0)
    df_stats['cum_excess_std0'] = df_stats['excess_std0'].cumsum()
    # std1
    df_stats['excess_std1'] = df_stats['natural_cause'] - df_stats['s_mean'] - df_stats['s_std']
    df_stats['excess_std1'] = df_stats['excess_std1'].clip(lower=0)
    df_stats['cum_excess_std1'] = df_stats['excess_std1'].cumsum()
    # std2
    df_stats['excess_std2'] = df_stats['natural_cause'] - df_stats['s_mean'] - df_stats['s_std'] - df_stats['s_std']
    df_stats['excess_std2'] = df_stats['excess_std2'].clip(lower=0)
    df_stats['cum_excess_std2'] = df_stats['excess_std2'].cumsum()

    df_stats['s_z'] = df_stats['excess'] / df_stats['s_std']

    dfs_stats.append(df_stats)
    #End of states for loop

#
#Combine all the stats
stats_all = pd.concat(dfs_stats, ignore_index=True)

#Export to CSV
stats_all.to_csv (r'../data/US_stats.csv', header=True, index=False)


#plt.plot(df_all_tmp.mmwrweek, df_all_tmp.all_cause,linewidth=0.5)
#plt.plot(df_new_tmp.mmwrweek, df_new_tmp.all_cause,linewidth=0.5)
#plt.plot(df_stats, linewidth=0.5)
#plt.plot(df_stats.date, df_stats.natural_cause, linewidth=0.5)
#plt.plot(df_stats.date, df_stats.s_mean, linewidth=0.5)
#plt.plot(df_stats.date, df_stats.s_mean-df_stats.s_std, linewidth=0.5)
#plt.plot(df_stats.date, df_stats.s_mean+df_stats.s_std, linewidth=0.5)

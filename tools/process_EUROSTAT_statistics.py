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
# Import (and Concat the df's)
data_all = pd.read_csv("../data/EUROSTAT_historic.csv", index_col="date")
data_all['date_col'] = data_all.index #Make things easy
data_new = pd.read_csv("../data/EUROSTAT_2020.csv", index_col="date")
data_new['date_col'] = data_new.index #Make things easy

#all_data.head()
#print(all_data[all_data.jurisdiction_of_occurrence.eq('Alabama')])


#
#Process the stats for each jurisdiction
dfs_stats = []
states = data_new.jurisdiction.unique()
for state in states:
    df_new_state = data_new[data_new.jurisdiction.eq(state)] #Extract data for this state from new
    df_all_state = data_all[data_all.jurisdiction.eq(state)] #Extract data for this state from historic

    print(df_new_state)
    #
    #Generate the stats from the historic data and merge with the new data
    df_stats = pd.DataFrame()
    df_new_state.set_index('week', inplace=True) #Create an index based on the current year
    df_stats['date'] = df_new_state['date_col']
    df_stats['week'] = df_stats.index
    df_stats['jurisdiction'] = state
    df_stats['natural_cause'] = df_new_state['natural_cause']
    df_stats['s_min'] = df_all_state.groupby('week')['natural_cause'].min()
    df_stats['s_mean'] = df_all_state.groupby('week')['natural_cause'].mean()
    df_stats['s_max'] = df_all_state.groupby('week')['natural_cause'].max()
    df_stats['s_std'] = df_all_state.groupby('week')['natural_cause'].std()
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
stats_all.to_csv (r'../data/EUROSTAT_stats.csv', header=True, index=False)


#plt.plot(df_all_tmp.mmwrweek, df_all_tmp.all_cause,linewidth=0.5)
#plt.plot(df_new_tmp.mmwrweek, df_new_tmp.all_cause,linewidth=0.5)
#plt.plot(df_stats, linewidth=0.5)
#plt.plot(df_stats.date, df_stats.natural_cause, linewidth=0.5)
#plt.plot(df_stats.date, df_stats.s_mean, linewidth=0.5)
#plt.plot(df_stats.date, df_stats.s_mean-df_stats.s_std, linewidth=0.5)
#plt.plot(df_stats.date, df_stats.s_mean+df_stats.s_std, linewidth=0.5)

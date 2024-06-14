# requirement 1
# perform basic analysis on IPL

import feather
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow
import warnings
from warnings import filterwarnings
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, plot , iplot
from collections import Counter


deliver_data=pd.read_csv(r"C:\Users\902568\PycharmProjects\DataTransformation\IPL_Data_Analysis\5-IPL data Analysis/IPL Ball-by-Ball 2008-2020.csv")

match_data=pd.read_csv(r"C:\Users\902568\PycharmProjects\DataTransformation\IPL_Data_Analysis\5-IPL data Analysis/IPL Matches 2008-2020.csv")

print(deliver_data.columns)
print(match_data.columns)

# Requiremnet 1
# find the IPL team who won maximux toss
# first Find how many matches has been played
print(match_data.shape)
print(type(match_data.shape))
# print 1st value of tuple
print(match_data.shape[0])

# and unique cities

print(match_data['venue'].unique())
print(match_data['city'].unique())

# unique team
print(match_data['team1'].unique())
# find toss winner team and it's count
print(match_data['toss_winner'].value_counts())

# 1st team won maximum toss
print("Maximum toss_winner Team is =",match_data['toss_winner'].value_counts().index[0])

# Requirement 2
#Particluar batsman analysis

# Virat kohali's run contribution
# eg.
# 1's=200
# 2's=190
# 3's=98
# 4's=80
# 6's=90
# create pie or donut chart

print("batsman",deliver_data['batsman'].unique())

filter=deliver_data['batsman']=='V Kohli'

# dataframe will have batsman only virat kohli
print(deliver_data[filter])
df_vkohli=deliver_data[filter]
print(df_vkohli.columns)
# how v kohli used dismiss a lot
print(df_vkohli['dismissal_kind'].value_counts())
# what type of runs bastman makes
print(df_vkohli['batsman_runs'].unique())
# count of runs

filter1=df_vkohli['batsman_runs']==1
print("count of 1's=",len(df_vkohli[filter1]))
filter2=df_vkohli['batsman_runs']==2
print("count of 2's=",len(df_vkohli[filter2]))
filter3=df_vkohli['batsman_runs']==3
print("count of 3's=",len(df_vkohli[filter3]))
filter4=df_vkohli['batsman_runs']==4
print("count of 4's=",len(df_vkohli[filter4]))
filter6=df_vkohli['batsman_runs']==6
print("count of 6's=",len(df_vkohli[filter6]))
values=[1919,346,13,504,202]
labels=[1,2,3,4,6]

trace=go.Pie(labels=labels, values=values,hole=0.3)
data = [trace]
fig=go.Figure(data=data)
fig.show()


# def funcount(x):
#     a=[1,2,3,4,6]
#     for i in a:
#         return len((df_vkohli[df_vkohli['batsman_runs']==i]))
# df_vkohli['batsman_runs'].apply(funcount(1))

# print("count of runs",df_vkohli['batman_runs'].value_counts())

# print(deliver_data[])

# requirement 3
# Analysis Toss descision accross the season of IPLS
# Data in form of
# eg season(i.e year) toss_Descision count
print(match_data.columns)

print(match_data['date'])

# chnage datatype object to datetime
match_data['Season']=pd.to_datetime(match_data['date']).dt.year
print(match_data.groupby(['Season','toss_decision']).size())
print(type(match_data.groupby(['Season','toss_decision']).size()))
# to print the plot convert the series to df
season_toss_count_df=match_data.groupby(['Season','toss_decision']).size().reset_index().rename(columns={0:'count'})
print("season_toss_count_df",season_toss_count_df)

plt.figure(figsize=(10,6))
sns.boxplot(x='Season',y='count',hue='toss_decision',data=season_toss_count_df)
plt.show()
# Requirement 4
#Annalysising whether wining toss implies to winning games or not !
# data required
# Win toss win game
# Yes=212
# No =120

print(match_data[['team1','team2','toss_winner','winner']])
# if 'toss_winner'=='winner'--> yes else -->no
match_data['toss_win_the_game']=np.where(match_data['toss_winner']==match_data['winner'],'Yes','No')
print(match_data['toss_win_the_game'])
print(match_data['toss_win_the_game'].value_counts())

print("index=",match_data['toss_win_the_game'].value_counts().index)
print("values=",match_data['toss_win_the_game'].value_counts().values)
index=match_data['toss_win_the_game'].value_counts().index
values=match_data['toss_win_the_game'].value_counts().values

trace=go.Pie(labels=labels, values=values,hole=0.3)
data = [trace]
fig=go.Figure(data=data)
fig.show()
print()

# Requirement 5
# Analysing which team won the tournament the most?

print(match_data.columns)
print(match_data['Season'].unique())
df_2018=match_data[match_data['Season']==2018]
print(df_2018['winner'].tail(1).values[0])
#
winner_team={}
for year in sorted(match_data['Season'].unique()):
    current_year_df = match_data[match_data['Season'] == year]
    print(current_year_df['winner'].tail(1).values[0])
    winner_team[year]=current_year_df['winner'].tail(1).values[0]
print("winner_team",winner_team)


Counter(winner_team.values())
print(Counter(winner_team.values()))

# Requirement 6
# Comparitive Analysis of the team
# which team has most number of wins
print(match_data['team1'].value_counts() + match_data['team2'].value_counts())
match_played=match_data['team1'].value_counts() + match_data['team2'].value_counts()
matches_played_df=match_played.to_frame().reset_index()
print("matches_played_df",matches_played_df)
matches_played_df.columns=['team_name','Matches_played']
print(match_data['winner'].value_counts())
wins=pd.DataFrame(match_data['winner'].value_counts()).reset_index()
wins.columns=['team_name','wins']
print(wins)
played_df=matches_played_df.merge(wins, how='left', on='team_name')
print(played_df)

# print plot
# trace1=go.Bar(
#     x=played_df['team_name'], y=played_df['Matches_played'],name='Total_Matches'
# )
#
# trace2=go.Bar(
#     x=played_df['team_name'], y=played_df['wins'],name='Total_Matches'
# )
#
# data=[trace1,trace2]
# iplot(data)
# plt.show()
plt.figure(figsize=(10,6))
sns.boxplot(x='Matches_played',y='wins',hue='team_name',data=played_df)
plt.show()







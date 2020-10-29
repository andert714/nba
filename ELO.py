import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from meta import *

df = pd.read_csv('data/schedules/2019.csv', parse_dates = ['Date'])
df['game_id'] = np.arange(0, len(df))
df = df[['game_id', 'Visitor/Neutral', 'Visitor Points', 'Home/Neutral', 'Home Points']]
df['Visitor/Neutral'] = df['Visitor/Neutral'].replace(nba_team_names, nba_teams)
df['Home/Neutral'] = df['Home/Neutral'].replace(nba_team_names, nba_teams)

df_long = df[['game_id', 'Visitor/Neutral', 'Home/Neutral']]
df_long = df_long.melt(id_vars='game_id', var_name='home', value_name='team')
df_long['home'] = np.array(df_long['home'] == 'Home/Neutral', 'int64')

df_long['pts'] = df['Visitor Points'].append(df['Home Points']).values
df_long = df_long.sort_values('game_id')

print(df_long.groupby('team')[['pts']].ewm(alpha = 0.05))
print(df_long.groupby('team')['pts'].expanding(window=3).mean())
print(df_long.query('team == "ATL"'))

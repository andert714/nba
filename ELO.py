import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from meta import *

df = pd.read_csv('data/schedules/2019.csv', parse_dates = ['Date'])
df['game_id'] = np.arange(0, len(df))
df['margin'] = df['Home Points'] - df['Visitor Points']
df['home'] = df['Home/Neutral']
df['away'] = df['Visitor/Neutral']

df_long = df[['game_id', 'home', 'away', 'margin']]
df_long = df.melt(id_vars = ['game_id', 'margin'], value_vars = ['home', 'away'],
                  var_name='home', value_name = 'team')
df_long = df_long.sort_values('game_id')
df_long['home'] = np.array(df_long['home'] == 'home', 'int64')
df_long['team'] = df_long['team'].replace(nba_team_names, nba_teams)
df_long['margin'] = df_long['margin']*(2*df_long['home'] - 1)
df_long['margin'] = df_long.groupby('team')['margin'].transform(lambda x: x.ewm(alpha=0.05).mean().shift(1))
df_long['margin'] = df_long.groupby('game_id')['margin'].agg(lambda x: x.iloc[0] - x.iloc[1])


uta_ids = df_long.query('team == "UTA"')['game_id']
df_long.query('game_id in @uta_ids').tail(20)
df_long.columns

w_margin_diff = df_long.pivot(index = 'game_id', columns = 'home', values = 'margin')[1].to_numpy()
y = np.array(df['margin'] > 0, 'int64')

# Find correlation between difference in weighted margin of victory and win indicator

# Draw a scatterplot of difference in weighted margin of victory against win indicator with smooth curve

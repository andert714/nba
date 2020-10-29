import pandas as pd
import numpy as np
import seaborn as sns

def to_seconds(ms):
    min, sec = ms.split(':')
    return int(min) + int(sec)/60

df = pd.read_csv('data/box_scores/2019.csv')
df = df.query('MP not in ["Did Not Play", "Did Not Dress", "Not With Team"]')
# df['MP'] = df['MP'].replace(to_replace=["Did Not Play", "Did Not Dress", "Not With Team"], value='0:00')
df['MP'] = df['MP'].transform(lambda x: to_seconds(x))



team_abb = 'HOU'
player_name = 'James Harden'


player = df.query('PLAYER == @player_name')
team = df.query('TEAM == @team_abb').mean()
lg = df.mean()

# League: AST, FG, FT, PTS, FGA, FTA, ORB, TOV, TRB, PF, Pace
# Team: AST, FG, Pace
# Player: MP, 3P, AST, FG, FT, TOV, FGA, FTA, TRB, ORB, STL, BLK, PF
# Pace: 48 * ((Tm Poss + Opp Poss) / (2 * (Tm MP / 5)))



48 * ((Tm Poss + Opp Poss) / (2 * (Tm MP / 5)))

def get_PER(MP, )

factor = (2 / 3) - (0.5 * (lg.AST / lg.FG)) / (2 * (lg.FG / lg.FT))
VOP = lg.PTS / (lg.FGA - lg.ORB + lg.TOV + 0.44 * lg.FTA)
DRB_perc = (lg.TRB - lg.ORB) / lg.TRB

uPER = (1 / player['MP']) * np.sum([ player['3P'],
 (2/3) * player['AST'],
 (2 - factor * (team.AST / team.FG)) * player['FG'],
 (player['FT'] *0.5 * (1 + (1 - (team.AST / team.FG)) + (2/3) * (team.AST / team.FG))),
 -VOP * player['TOV'],
 -VOP * DRB_perc * (player['FGA'] - player['FG']),
 -VOP * 0.44 * (0.44 + (0.56 * DRB_perc)) * (player['FTA'] - player['FT']),
 VOP * (1 - DRB_perc) * (player['TRB'] - player['ORB']),
 VOP * DRB_perc * player['ORB'],
 VOP * player['STL'],
 VOP * DRB_perc * player['BLK'],
 -player['PF'] * ((lg.FT / lg.PF) - 0.44 * (lg.FTA / lg.PF) * VOP) ])

pace_adj = 100/97.9

aPER = pace_adj*uPER


aPER * (15/ lg_aPER)
'''

========== PER ==========
uPER = (1 / MP) *
     [ 3P
     + (2/3) * AST
     + (2 - factor * (team_AST / team_FG)) * FG
     + (FT *0.5 * (1 + (1 - (team_AST / team_FG)) + (2/3) * (team_AST / team_FG)))
     - VOP * TOV
     - VOP * DRB% * (FGA - FG)
     - VOP * 0.44 * (0.44 + (0.56 * DRB%)) * (FTA - FT)
     + VOP * (1 - DRB%) * (TRB - ORB)
     + VOP * DRB% * ORB
     + VOP * STL
     + VOP * DRB% * BLK
     - PF * ((lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP) ]

factor = (2 / 3) - (0.5 * (lg_AST / lg_FG)) / (2 * (lg_FG / lg_FT))
VOP    = lg_PTS / (lg_FGA - lg_ORB + lg_TOV + 0.44 * lg_FTA)
DRB%   = (lg_TRB - lg_ORB) / lg_TRB

pace adjustment = lg_Pace / team_Pace

aPER = (pace adjustment) * uPER
PER = aPER * (15 / lg_aPER)
'''

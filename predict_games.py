import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import web_scraping
import meta
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LogisticRegression

# Scrape data from basketball-reference.com
# for year in range(2015, 2020):
#    filepath = 'data/schedules/{}.csv'.format(year)
#    schedule = web_scraping.scrape_schedule(year)
#    schedule.to_csv(filepath)

def clean_schedule(df, year):
    df['season'] = year
    df['game_id'] = np.arange(0, len(df))
    df['margin'] = df['Home Points'] - df['Visitor Points']
    df = df.rename(columns={'Home/Neutral': 'home', 'Visitor/Neutral': 'away'})
    df = df[['season', 'game_id', 'home', 'away', 'margin']]
    df = df.melt(id_vars = ['season', 'game_id', 'margin'], value_vars = ['home', 'away'], var_name='home', value_name = 'team')
    df = df.sort_values('game_id')
    df['home'] = np.array(df['home'] == 'home', 'int64')
    df['team'] = df['team'].replace(meta.nba_team_names, meta.nba_teams)

    return df

# Combine data from 2014 to 2019
df = pd.DataFrame()
for year in range(2015, 2020):
    filepath = 'data/schedules/{}.csv'.format(year)
    schedule = pd.read_csv(filepath)
    schedule = clean_schedule(schedule, year)
    df = df.append(schedule)

def get_features(df, alpha):
    # Create y-vector of home margins
    df = df.copy()
    y = np.array(df.query('home == 1')['margin'] > 0, 'int64')

    # Create exponentially weighted margins grouped by team
    df['margin'] = df['margin']*(2*df['home'] - 1)
    df['margin'] = df.groupby('team')['margin'].transform(lambda x: x.ewm(alpha=alpha).mean().shift(1))
    df = df.pivot(index=['season','game_id'], columns='home', values=['margin','team'])

    # Create X matrix (column of difference in exponentially weighted margins)
    X = np.array(df['margin'][1] - df['margin'][0], 'float64').reshape(-1,1)

    # Take out first 100 games
    X = X[100:]
    y = y[100:]
    return X, y

# Model specification
# X = [1 (home) | (home exponentially weighted margin - away exponentially weighted margin)_i]
# y = [margin_i]

# Cross validation for tuning alpha parameter
alphas = np.linspace(1e-5, 0.2, 100)
scores = np.zeros(len(alphas))

for i in range(len(alphas)):
    X, y = get_features(df, alphas[i])
    X = X[:-1000]
    y = y[:-1000]
    cv = TimeSeriesSplit()
    cv_scores = []
    for train_index, test_index in cv.split(X):
        X_train = X[train_index]
        y_train = y[train_index]
        X_test = X[test_index]
        y_test = y[test_index]
        m = LogisticRegression(penalty='none').fit(X_train, y_train)
        cv_scores.append(m.score(X_test, y_test))

    scores[i] = np.mean(cv_scores)

plt.plot(alphas, scores)
plt.title('5 fold cross validation accuracy for differing alphas')
plt.xlabel('Alpha')
plt.ylabel('Accuracy')

best_alpha = alphas[np.argmax(scores)]
X, y = get_features(df, best_alpha)
X_train = X[:-1000]
X_test = X[-1000:]
y_train = y[:-1000]
y_test = y[-1000:]
m = LogisticRegression(penalty='none').fit(X_train, y_train)
m.score(X_test, y_test)

from pandas import DataFrame, concat, to_datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

def scrape_schedule(year):
    def scrape_month(month, year):
        url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html'.format(year, month)
        html = urlopen(url)
        soup = BeautifulSoup(html, features = 'html.parser')

        table = soup('table')[0]
        headers = [i['aria-label'] for i in table('th', {'scope': 'col'})][1:]
        index = [i.getText() for i in table('th', {'scope': 'row'})]
        body = [[i.getText() for i in row('td')] for row in table('tr')][1:]
        if month == 'april':
            playoff_index = body.index([])
            body = body[:playoff_index]
            index = index[:playoff_index]
        return DataFrame(data = body, index = index, columns = headers)

    schedule = []
    for month in ['october', 'november', 'december', 'january', 'february', 'march', 'april']:
        schedule.append(scrape_month(month, year))

    schedule = concat(schedule)
    schedule = schedule.reset_index().rename(columns={'index': 'Date'})
    return schedule

def scrape_box_score(date, home_abb, away_abb):
    def scrape_table(table_soup):
        header = [i.text for i in table_soup('th', scope='col')][1:]
        index = [i.text for i in table_soup('tbody')[0]('th', scope='row')]
        body = [[i.text for i in row('td')] for row in table_soup('tbody')[0]('tr', lambda x: x != 'thead')]
        df = DataFrame(body, index=index, columns = header)
        return df

    url = 'https://www.basketball-reference.com/boxscores/{}0{}.html'.format(date, home_abb)
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')

    home_table = scrape_table(soup('table', id='box-{}-game-basic'.format(home_abb))[0])
    away_table = scrape_table(soup('table', id='box-{}-game-basic'.format(away_abb))[0])

    home_table['TEAM'] = home_abb
    away_table['TEAM'] = away_abb

    box_score = concat([home_table, away_table])
    box_score = box_score.reset_index().rename(columns={'index': 'PLAYER'})
    return box_score

def concat_box_scores(year):
    schedule_df = scrape_year(year)
    schedule_df['Date'] = to_datetime(schedule_df['Date'])
    dates = schedule_df['Date'].dt.strftime('%Y%m%d')
    home_abbs = schedule_df['Home/Neutral'].replace(dict(zip(meta.nba_team_names, meta.nba_teams)))
    away_abbs = schedule_df['Visitor/Neutral'].replace(dict(zip(meta.nba_team_names, meta.nba_teams)))

    box_scores = []
    for date, home_abb, away_abb in zip(dates, home_abbs, away_abbs):
        box_score = scrape_box_score(date, home_abb, away_abb)
        box_score['GAME_ID'] = len(box_scores)
        print(len(box_scores))
        box_scores.append(box_score)

    box_scores = concat(box_scores)
    return box_scores

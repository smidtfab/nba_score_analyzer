import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import numpy as np
import sys


class BoxScoreTraditionalV2Scraper():
    endpoint = 'boxscoretraditionalv2'
    expected_data = {'PlayerStats': ['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_ID', 'PLAYER_NAME', 'START_POSITION', 'COMMENT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS'], 'TeamStarterBenchStats': ['GAME_ID', 'TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'STARTERS_BENCH', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS'], 'TeamStats': ['GAME_ID', 'TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']}

    nba_response = None
    data_sets = None
    player_stats = None
    team_stats = None
    headers = None
    base_url = ""

    def __init__(self,
                base_url,
                game_id = None,
                end_period=None,
                end_range=None,
                range_type=None,
                start_period=None,
                start_range=None,
                proxy=None,
                headers=None,
                timeout=30,
                get_request=True):
        self.proxy = proxy
        self.base_url = base_url
        if headers is not None:
            self.headers = headers
        else:
            self.headers = {
            "Host": "stats.nba.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-NewRelic-ID": "VQECWF5UChAHUlNTBwgBVw==",
            "x-nba-stats-origin": "stats",
            "x-nba-stats-token": "true"
            }
        self.timeout = timeout
    
    def get_request(self, params):
        response = requests.get(url=self.base_url, params=params, headers=self.headers, verify=False, timeout=self.timeout)
        # custom return dictionary, TODO: modify
        cust_game = {
            'response_url': response.url,
            'status': response.status_code,
            'content': response.json()
        }
        return cust_game
        
    def load_response(self, scraper_response):
        # get all games for given day
        games = scraper_response['content']['resultSets'][1]
        
        # get headers
        headers = games['headers']

        # get rows --> the games (2 rows per game with same gameid)
        rows = games['rowSet']
        print(rows)

        dictionary = dict(zip(headers, rows[0]))
        print(dictionary)

        # create df from response
        df = pd.DataFrame(np.array(rows), columns=headers)
        
        return df

    def write_games(self, filename, df):
        df.to_csv(filename, mode='a', header=False)

def main():
    date = sys.argv[1] # get date format --> "02/27/2020"
    print("Scraping games on {}".format(date)) 

    parameters = {
        "DayOffset": "0",
        "LeagueID": "00",
        "gameDate": date
    }

    scraper = BoxScoreTraditionalV2Scraper(base_url = 'https://stats.nba.com/stats/scoreboardV2')
    scraper_response = scraper.get_request(params=parameters)
    response_df = scraper.load_response(scraper_response)
    print(response_df)

if __name__ == '__main__':
    main()
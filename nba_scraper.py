import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import numpy as np
import sys
import datetime

from games_db import GamesDB

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

        # create df from response
        if len(rows) > 0:
            df = pd.DataFrame(np.array(rows), columns=headers)
        else:
            df = None
        return df

    def write_games(self, filename, df):
        df.to_csv(filename, mode='a', header=False)

def build_date_range(start_date_str, end_date_str):
    # convert start and end date to datetime and calculate delta
    start_date = datetime.datetime.strptime(start_date_str, '%m/%d/%Y')
    end_date = datetime.datetime.strptime(end_date_str, '%m/%d/%Y')
    delta = end_date - start_date

    # difference has to be greater zero
    assert delta.days > 0, "Invalid input of dates"

    dates = []

    for i in range(delta.days + 1):
        date_time = start_date + datetime.timedelta(days=i)

        # convert date_time back to string
        date_str = date_time.strftime('%m/%d/%Y')

        # add to list
        dates.append(date_str)

    # list has to have elements
    assert len(dates) != 0, "List is empty."

    return dates

def scrape_date_range(dates):
    # class to access mongo data base
    gamesDB = GamesDB()

    # scraper class to retrieve game data
    scraper = BoxScoreTraditionalV2Scraper(base_url = 'https://stats.nba.com/stats/scoreboardV2')

    # use date range provided by build_date_range 
    for date in dates:
        # define parameter dictionary to use for request
        parameters = {
            "DayOffset": "0",
            "LeagueID": "00",
            "gameDate": date
        }

        # send request
        scraper_response = scraper.get_request(params=parameters)
        response_df = scraper.load_response(scraper_response)
        print(response_df)

        # convert data frame to dictionary and save to mongodb
        if (response_df is not None and not response_df['PTS'].isnull().values.any()):
            # if scraping returned games for that day save them
            gamesDB.update_games(response_df.to_dict('records'))
        elif response_df['PTS'].isnull().values.any():
            # if any game is not played on that day stop scraping
            break

    #gamesDB.retrieve_all()

    #gamesDB.games_db.remove( { 'PTS': None } )

def main():
    # Initialize empty list to be filled with dates to scrape
    dates = []

    # check if second param (the end date) was passed
    if len(sys.argv) > 2:
        # two dates passed
        start_date_str = sys.argv[1] # get date format --> "02/27/2020"
        end_date_str = sys.argv[2] # get date format --> "02/27/2020"
        print("Scraping games from {} until {}".format(start_date_str, end_date_str)) 
        
        # fill dates array dates
        dates = build_date_range(start_date_str, end_date_str)
    else:
        # only one date passed
        start_date_str = sys.argv[1] # get date format --> "02/27/2020"
        print("Scraping games on {}".format(start_date_str)) 

        # fill dates with the only date
        dates.append(start_date_str)

    # scrape the data for given range and store in db
    scrape_date_range(dates)


if __name__ == '__main__':
    main()
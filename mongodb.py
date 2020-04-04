import pymongo
from pymongo import MongoClient
from nba_scraper import BoxScoreTraditionalV2Scraper

class GamesDB():

    client = MongoClient()
    db = client.pymongo_games

    games_db = db.games

    def insert_game(self, game):
        game_id = GamesDB.games_db.insert_one(game).inserted_id
        game_id
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    def insert_multiple(self, games):
        result = GamesDB.games_db.insert_many(games)
        print(result.inserted_ids)

    def retrieve_all(self):
        for game in GamesDB.games_db.find():
            print(game)

    #post = games.find_one({'author': 'Scott'})
    #print(post)

gamesDB = GamesDB()

parameters = {
        "DayOffset": "0",
        "LeagueID": "00",
        "gameDate": "02/27/2020"
    }

scraper = BoxScoreTraditionalV2Scraper(base_url = 'https://stats.nba.com/stats/scoreboardV2')
scraper_response = scraper.get_request(params=parameters)
response_df = scraper.load_response(scraper_response)
print(response_df)

# convert data frame to dictionary and save to mongodb
gamesDB.insert_multiple(response_df.to_dict('records'))

gamesDB.retrieve_all()
import pymongo
from pymongo import MongoClient
from pymongo import UpdateOne
import pandas as pd

class GamesDB():

    client = MongoClient()
    db = client.pymongo_games # test collection
    #db = client.pymongo_games_clean # clean db

    games_db = db.games

    def insert_game(self, game):
        game_id = GamesDB.games_db.insert_one(game).inserted_id
        game_id

    def update_games(self, games):
        for game in games:  
            print(game['GAME_ID'])

            result  = GamesDB.games_db.update(
                {
                    "GAME_ID" : game["GAME_ID"],
                    "TEAM_ID" : game["TEAM_ID"]
                }, # Query parameter
                game, # Replacement document
                True # Upsert option --> Insert if query not matched, otherwise update
            )
            print(result)

    def insert_multiple(self, games):
        result = GamesDB.games_db.insert_many(games)
        print(result.inserted_ids)

    def retrieve_all(self):
        games = []
        for game in GamesDB.games_db.find():
            #print(game)
            games.append(game)
        return GamesDB.games_db.find()

    def remove_all(self):
        GamesDB.games_db.remove()

    def convert_to_df(self, list_of_dic):
        return pd.DataFrame(list_of_dic)
import pymongo
from pymongo import MongoClient
from pymongo import UpdateOne

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
                    "TEAM_CITY_NAME" : game["TEAM_CITY_NAME"]
                }, # Query parameter
                game, # Replacement document
                True # Upsert option --> Insert if query not matched, otherwise update
            )
            print(result)

    def insert_multiple(self, games):
        result = GamesDB.games_db.insert_many(games)
        print(result.inserted_ids)

    def retrieve_all(self):
        for game in GamesDB.games_db.find():
            print(game)

    def remove_all(self):
        GamesDB.games_db.remove()
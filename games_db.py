import pymongo
from pymongo import MongoClient

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
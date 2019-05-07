from flask import Flask, request
from flask_restful import Resource, Api
import json

application = Flask(__name__)
api = Api(application)

class Player:
    def __init__(self, alias, balance, hand, wager, move_status, win_status):
        self.alias = alias
        self.balance = balance
        self.hand = hand
        self.wager = wager
        self.move_status = move_status
        self.win_status = win_status

class game:
    def __init__(self):
        self.playersList = [Player(None, None, None, None, None, None) for i in range (5)]
        self.dealer = Player("Dealer", None, None, None, None, None)
        self.gameState = "awaitingWagers"

    def getGameStatusJson(self):
        gameStatus = {
            "gameState" : 
        }




class HelloWorld(Resource):
    def get(self):
        return {'about' : 'Hello World!'}

api.add_resource(HelloWorld, '/')

class GameEnter(Resource):
    def get(self, alias, balance):
        print("Alias: ", alias, " Balance: ", balance)
        handle_newUser(alias)

        #Begin new client thread
        
        return "Alias: " + alias + " Balance: " + str(balance)

api.add_resource(GameEnter, '/GE/<string:alias>/<int:balance>')

def handle_newUser(alias):







if __name__ == '__main__':
    application.run(debug=True)
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
        self.score = None #TODO: calculate score from hand

class _game:
    def __init__(self):
        self.playersList = [Player(None, None, None, None, None, None) for i in range (5)]
        self.dealer = Player("Dealer", None, None, None, None, None)
        self.gameState = "awaitingWagers"

    def getGameStatusJson(self):
        gameStatus = {
            "gameState" : self.gameState,
            "dealer" : {
                "hand" : self.dealer.hand,
                "score" : self.dealer.score,
                "winStatus" : self.dealer.win_status
            },
            "players" : {
                "player1" : {
                    "alias" : self.playersList[0].alias,
                    "balance" : self.playersList[0].balance,
                    "hand" : self.playersList[0].hand,
                    "score" : self.playersList[0].score,
                    "wager" : self.playersList[0].wager,
                    "moveStatus" : self.playersList[0].move_status,
                    "winStatus" : self.playersList[0].win_status
                },
                "player2" : {
                    "alias" : self.playersList[1].alias,
                    "balance" : self.playersList[1].balance,
                    "hand" : self.playersList[1].hand,
                    "score" : self.playersList[1].score,
                    "wager" : self.playersList[1].wager,
                    "moveStatus" : self.playersList[1].move_status,
                    "winStatus" : self.playersList[1].win_status
                },
                "player3" : {
                    "alias" : self.playersList[2].alias,
                    "balance" : self.playersList[2].balance,
                    "hand" : self.playersList[2].hand,
                    "score" : self.playersList[2].score,
                    "wager" : self.playersList[2].wager,
                    "moveStatus" : self.playersList[2].move_status,
                    "winStatus" : self.playersList[2].win_status
                },
                "player4" : {
                    "alias" : self.playersList[3].alias,
                    "balance" : self.playersList[3].balance,
                    "hand" : self.playersList[3].hand,
                    "score" : self.playersList[3].score,
                    "wager" : self.playersList[3].wager,
                    "moveStatus" : self.playersList[3].move_status,
                    "winStatus" : self.playersList[3].win_status
                },
                "player5" : {
                    "alias" : self.playersList[4].alias,
                    "balance" : self.playersList[4].balance,
                    "hand" : self.playersList[4].hand,
                    "score" : self.playersList[4].score,
                    "wager" : self.playersList[4].wager,
                    "moveStatus" : self.playersList[4].move_status,
                    "winStatus" : self.playersList[4].win_status
                }
            }
        }
        return json.dumps(gameStatus)

game = _game()



class HelloWorld(Resource):
    def get(self):
        return {'about' : 'Hello World!'}

api.add_resource(HelloWorld, '/')

class GameEnter(Resource):
    def get(self, alias):
        print("Alias: ", alias,)
        handle_newUser(alias)

        #Begin new client thread
        
        return "Alias: " + alias)

api.add_resource(GameEnter, '/GE/<string:alias>')


def handle_newUser(alias):
    #TODO: Handle new user
    return None

class GameStatus(Resource):
    def get(self):
        print("GameStatus Requested\n")
        return game.getGameStatusJson()

api.add_resource(GameStatus, '/status')

    global game

    for i in range(5):
        if game.playersList[i].alias == None:
            game.playersList[i].alias = alias
            game.playersList[i].balance = 100
            return jsonify({'seatNo': i})

def quit_game(seatNo):

    global game


    game.playersList[seatNo].alias = None
    game.playersList[seatNo].balance = None

    #edit game status json










if __name__ == '__main__':
    application.run(debug=True)
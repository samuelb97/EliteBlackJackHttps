from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import json
import os
import random

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
        
        return "Alias: " + alias

api.add_resource(GameEnter, '/GE/<string:alias>')


def handle_newUser(alias):
    #TODO: Handle new user
    global game

    for i in range(5):
        if game.playersList[i].alias == None:
            game.playersList[i].alias = alias
            game.playersList[i].balance = 100
            return jsonify({'seatNo': i})
        
    return None

class GameStatus(Resource):
    def get(self):
        global game
        print("GameStatus Requested\n")
        return game.getGameStatusJson()

api.add_resource(GameStatus, '/status')

class Wager(Resource):
    def post(self):
        global game
        print("Wager Post\n")
        req = request.get_json(force=True)
        wager = req["wager"]
        seatNo = req["seatNo"]  
        game.playersList[seatNo - 1].wager = wager
        #TODO: Check if all players have wagered then change game Status

api.add_resource(Wager, '/WA') 

class quit_game(Resource):
    def post(self):
        global game
        print("Quit Game Post\n")
        req = request.get_json(force=True)
        seatNo = req["seatNo"]
        game.playersList[seatNo - 1] = Player(None, None, None, None, None, None)

api.add_resource(quit_game, '/QG')

class Action(Resource):
    def post(self):
        global game
        print("Action request\n")
        
        req = get_json(force=True)
        handle_action(req)


        return None

api.add_resource(Action, '/AC')

def handle_action(req):
    global deck
    global game
    seatNo = req['seatNo']
    seatNo -= 1
    game.playersList[seatNo].move_status = req['action']
    #insert logic for move

    if(game.playersList[seatNo].move_status == "HT"):
        hit(game.playersList[seatNo].hand)

        # msg = "GU:" + str(game.dealer.hand[0])      
        # for i in range(5):
        #     if(game.playersList[i].hand == None):
        #         msg = msg + ":--"
        #     else:
        #         msg = msg + ":"
        #         for card in game.playersList[i].hand:
        #             msg = msg + str(card)
        # broadcast(bytes(":" + msg, "utf8"))                       #send game update message

    elif(game.playersList[seatNo].move_status == "DD"):
        wager_int = int(game.playersList[seatNo].wager) 
        wager_int *= 2
        game.playersList[seatNo].wager = str(wager_int)
        hit(game.playersList[seatNo].hand)
        game.playersList[seatNo].move_status = "ST"

        # msg = "GU:" + str(game.dealer.hand[0])
        # for i in range(5):
        #     if(game.playersList[i].hand == None):
        #         msg = msg + ":--"
        #     else:
        #         msg = msg + ":"
        #         for card in game.playersList[i].hand:
        #             msg = msg + str(card)
        # broadcast(bytes(":" + msg, "utf8"))                       #send game update message

    if(game.playersList[seatNo].move_status == "ST"):

        done_with_hand = "YES"
        for i in range(5):
            if(game.playersList[i].alias != None):
                if(game.playersList[i].move_status != "ST"):
                    done_with_hand = "NO"
        if(done_with_hand != "NO"):
            # msg = "DU:"
            while total(game.dealer.hand) < 17:
                hit(game.dealer.hand)
                # for card in game.dealer.hand:
                #     msg = msg + str(card)
                # broadcast(bytes(":" + msg, "utf8"))
            game.dealer.move_status = "ST"

        while True:  #holds player after ST, waits for other players and dealer
            if(game.dealer.move_status == "ST"): #check for win/loss
                game.playersList[seatNo].win_status = score(game.dealer.hand, game.playersList[seatNo].hand)
                game.playersList[seatNo].move_status = "Done"
                break
        
        game_status = "Over"
        for i in range(5):
            if(game.playersList[i].move_status != "Done"):
                if(game.playersList[i].alias != None):
                    game_status = "Going"

        if(game_status == "Over"):
            msg = "GE"
            game.dealer.score = total(game.dealer.hand)
            # msg = msg + ":" + str(game.dealer.score)
            # for i in range(5):
            #     if(game.playersList[i].alias != None):
            #         msg = msg + ":" + str(game.playersList[i].win_status)  
            #     else:
            #         msg = msg + ":"
            # broadcast(bytes(":" + msg, "utf8"))     #send Game End W/L message to clients
            
            for i in range(5):              #updating player balances
                if(game.playersList[i].alias != None):
                    if(game.playersList[i].win_status == "W"):
                        balance_update = int(game.playersList[i].wager)
                        balance = int(game.playersList[i].balance)
                        balance += balance_update
                        game.playersList[i].balance = str(balance)

                    elif(game.playersList[i].win_status == "L"):
                        balance_update = int(game.playersList[i].wager)
                        balance = int(game.playersList[i].balance)
                        balance -= balance_update
                        game.playersList[i].balance = str(balance)

                game.playersList[i].hand = None             #reset player values for new game
                game.playersList[i].wager = None
                game.playersList[i].win_status = None
                game.playersList[i].move_status = None

            game.dealer.hand = []
            game.dealer.move_status = None
            deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4







def deal(deck):											#BTS
    hand = []
    for i in range(2):
	    random.shuffle(deck)
	    card = deck.pop()
	    if card == 11:card = "J"
	    if card == 12:card = "Q"
	    if card == 13:card = "K"
	    if card == 14:card = "A"
	    if card == 10:card = "T"
	    hand.append(card)
    return hand

def total(hand):
    total = 0
    for card in hand:
	    if card == "T" or card == "J" or card == "Q" or card == "K":
	        total+= 10
	    elif card == "A":
	        if total >= 11: total+= 1
	        else: total+= 11
	    else:
	        total += card
    return total

def hit(hand):
	card = deck.pop()
	if card == 11:card = "J"
	if card == 12:card = "Q"
	if card == 13:card = "K"
	if card == 14:card = "A"
	if card == 10:card = "T"
	hand.append(card)
	return hand

def score(dealer_hand, player_hand):
    if total(player_hand) == total(dealer_hand):
        return "P"
    elif total(player_hand) == 21:
        return "W"  
    elif total(dealer_hand) == 21:
        return "L"
    elif total(player_hand) > 21:
        return "L"
    elif total(dealer_hand) > 21:
        return "W"
    elif total(player_hand) < total(dealer_hand):
        return "L"
    elif total(player_hand) > total(dealer_hand):
        return "W"

deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4








if __name__ == '__main__':
    application.run(debug=True)
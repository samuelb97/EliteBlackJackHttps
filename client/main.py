from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, IPPROTO_IP, IP_MULTICAST_LOOP, SOL_IP, IP_MULTICAST_IF, IP_ADD_MEMBERSHIP, IP_MULTICAST_TTL, inet_aton, gethostbyname
from threading import Thread
import datetime
import random
import os
import requests
import json
from gameWin import *

def total(hand):
    total = 0
    for card in hand:
        if card == "T" or card == "J" or card == "Q" or card == "K":
	        total+= 10
        elif card == "A":
	        if total >= 11: total+= 1
	        else: total+= 11
        else:
            print("Total, Card: %i" %int(card))
            total += int(card)
    return total

class receiveQueue:
    def __init__(self):
        self.dealerQ = []
        self.p1Q = []
        self.p2Q = []
        self.p3Q = []
        self.p4Q = []
        self.p5Q = []
        self.score = 0
        self.dealerCtr = 2
        self.p1Ctr = 3
        self.p2Ctr = 3
        self.p3Ctr = 3
        self.p4Ctr = 3
        self.p5Ctr = 3
        self.end = False
        self.dealerEndTotal = 0
        self.GS = False
        self.p1result = ""
        self.p2result = ""
        self.p3result = ""
        self.p4result = ""
        self.p5result = ""
        self.yourResult = ""

recQ = receiveQueue()
seatNo = ""

def randomSuit():
    x = random.randint(1,4)
    if x == 1:
        suit = "S" 
    elif x == 2:
        suit = "C"
    elif x == 3:
        suit = "D"
    else:
        suit = "H"
    return suit

def updateUI():
    global recQ
    global GU_hand_counter
    global seatNo

    data = requests.get(url = URL + "status").json()
    data = json.loads(data)

    gameState = data["gameState"]

    if(gameState == "awaitingWagers"):
        #TODO: Reset UI if second game
        print("awaitingWagers")

    if(gameState == "awaitingTurns"):
        #TODO: Show cards executed
        print("awaitingTurns")


    if(gameState == "complete"):
        #TODO: dealer cards

    #player1 = data['players']['player1']

def receive():
    global client_recv_socket
    global recQ
    global GU_hand_counter
    global seatNo
    x = 2
    #Handles receiving of messages.
    while True:
        _data, addr = client_recv_socket.recvfrom(BUFSIZ)
        print("Recieved in Thread: %s" %_data)
        _data = _data.decode("utf8")
        data = _data.split(":")
        code = data[1]
        if code == "GS":    #Game Start
            print("Game Start")
            temp = data[2]
            recQ.dealerQ.append("B")
            recQ.dealerQ.append(temp[0])
            temp = data[3]
            if(temp != "--"):
                for card in temp:
                    recQ.p1Q.append(card)
            temp = data[4]
            if(temp != "--"):
                for card in temp:
                    recQ.p2Q.append(card)
            temp = data[5]
            if(temp != "--"):
                for card in temp:
                    recQ.p3Q.append(card)
            temp = data[6]
            if(temp != "--"):
                for card in temp:
                    recQ.p4Q.append(card)
            temp = data[7]
            if(temp != "--"):
                for card in temp:
                    recQ.p5Q.append(card)

            recQ.score = total(data[3 + int(seatNo)])  
            recQ.GS = True      

        elif code == "GU":    #Game Update
            print("Game Update")
            temp = data[3]
            if(temp != "--" and recQ.p1Ctr == len(temp)):
                recQ.p1Q.append(temp[recQ.p1Ctr - 1])
                recQ.p1Ctr += 1
            temp = data[4]
            if(temp != "--" and recQ.p2Ctr == len(temp)):
                recQ.p2Q.append(temp[recQ.p2Ctr - 1])
                recQ.p2Ctr += 1
            temp = data[5]
            if(temp != "--" and recQ.p3Ctr == len(temp)):
                recQ.p3Q.append(temp[recQ.p3Ctr - 1])
                recQ.p3Ctr += 1
            temp = data[6]
            if(temp != "--" and recQ.p4Ctr == len(temp)):
                recQ.p4Q.append(temp[recQ.p4Ctr - 1])
                recQ.p4Ctr += 1
            temp = data[7]
            if(temp != "--" and recQ.p5Ctr == len(temp)):
                recQ.p5Q.append(temp[recQ.p5Ctr - 1])
                recQ.p5Ctr += 1
            #set score queue
            if(len(data[3 + int(seatNo)]) > x):
                recQ.score = total(data[3 + int(seatNo)])
                x += 1
            
        elif code == "GE":    #Game End
            recQ.end = True
            recQ.dealerEndTotal = data[2]
            recQ.p1result = data[3]
            recQ.p2result = data[4]
            recQ.p3result = data[5]
            recQ.p4result = data[6]
            recQ.p5result = data[7]
            recQ.yourResult = data[3 + int(seatNo)]

        elif code == "DU":
            temp = data[2]
            recQ.dealerQ.append(temp[recQ.dealerCtr])
            recQ.dealerCtr += 1

# def send(msg):  # event is passed by binders.
#         #Handles sending of messages.
#         print("msg: %s" % msg)

#         global client_socket

#         client_socket.send(bytes(msg, "utf8"))


if __name__ == "__main__":
    alias = input("Please Enter Your Name: ")
    balance = 100
    wager = 0
    winnings = 0
    URL = "http://127.0.0.1:5000/"

    seatNo = requests.get(url = URL + "GE/" + alias)


    
    print("Seat Number: %s" %seatNo)


    win = GraphWin("Blackjack", 700, 900)
    win.setCoords(0, 200, 415, 0)
    win.setBackground("grey")
        
    game = gameWin(win)
    game.balance_view.updateText(str(balance))


    if seatNo == "0":
        game.p1.updateBG()
        game.p1.updateText(alias)

    elif seatNo == "1":
        game.p2.updateBG()
        game.p2.updateText(alias)

    elif seatNo == "2":
        game.p3.updateBG()
        game.p3.updateText(alias)

    elif seatNo == "3":
        game.p4.updateBG()
        game.p4.updateText(alias)

    elif seatNo == "4":
        game.p5.updateBG()
        game.p5.updateText(alias)

    
    p = win.getMouse()
    
    while True:
        if recQ.GS:
            game.enableGameButtons()
            recQ.GS = False

        if recQ.score != 0 :
            game.score_view.updateText(recQ.score)
            recQ.score = 0

        if recQ.end:
            dealerTotal = Text(Point(208, 20), str(recQ.dealerEndTotal))
            dealerTotal.setTextColor("red")
            dealerTotal.setSize(14)
            dealerTotal.draw(win)

            game.p1.addResult(win, recQ.p1result)
            game.p2.addResult(win, recQ.p2result)
            game.p3.addResult(win, recQ.p3result)
            game.p4.addResult(win, recQ.p4result)
            game.p5.addResult(win, recQ.p5result)

            if recQ.yourResult == "W":
                print("W")
                balance = balance + (wager * 2)
                winnings += wager
                wager = 0
                game.wager_view.updateText(str(wager))
                game.winnings_view.updateText(str(winnings))
                game.balance_view.updateText(str(balance))

            elif recQ.yourResult == "L":
                winnings -= wager
                wager = 0
                game.wager_view.updateText(str(wager))
                game.winnings_view.updateText(str(winnings))

            else:
                balance = balance + wager
                wager = 0
                game.wager_view.updateText(str(wager))
                game.balance_view.updateText(str(balance))


            game.enableWagers()

        while len(recQ.dealerQ) != 0:
            print("Dealer Q Not Empty")
            temp = recQ.dealerQ.pop()
            if temp == "B":
                game.dealerTotalCards = addDealerCard(win, "purple_back", game.dealerTotalCards)
            elif temp == "T":
                game.dealerTotalCards = addDealerCard(win, "10" + randomSuit(), game.dealerTotalCards)
            else:
                game.dealerTotalCards = addDealerCard(win, str(temp) + randomSuit(), game.dealerTotalCards)

        while len(recQ.p1Q) != 0:
            print("p1 Q Not Empty")
            temp = recQ.p1Q.pop()
            if temp == "T":
                game.p1TotalCards = addCard(win, game.p1, "10" + randomSuit(), game.p1TotalCards)     
            else:
                game.p1TotalCards = addCard(win, game.p1, str(temp) + randomSuit(), game.p1TotalCards)
                
            print("p1 TotalCards: %s" %game.p1TotalCards)

        while len(recQ.p2Q) != 0:
            print("p2 Q Not Empty")
            temp = recQ.p2Q.pop()
            if temp == "T":
                game.p2TotalCards = addCard(win, game.p2, "10" + randomSuit(), game.p2TotalCards)
            else:
                game.p2TotalCards = addCard(win, game.p2, str(temp) + randomSuit(), game.p2TotalCards)

        while len(recQ.p3Q) != 0:
            print("p3 Q Not Empty")
            temp = recQ.p3Q.pop()
            if temp == "T":
                game.p3TotalCards = addCard(win, game.p3, "10" + randomSuit(), game.p3TotalCards)
            else:
                game.p3TotalCards = addCard(win, game.p3, str(temp) + randomSuit(), game.p3TotalCards)

        while len(recQ.p4Q) != 0:
            print("p4 Q Not Empty")
            temp = recQ.p4Q.pop()
            if temp == "T":
                game.p4TotalCards = addCard(win, game.p4, "10" + randomSuit(), game.p4TotalCards)
            else:
                game.p4TotalCards = addCard(win, game.p4, str(temp) + randomSuit(), game.p4TotalCards)

        while len(recQ.p5Q) != 0:
            print("p1 Q Not Empty")
            temp = recQ.p5Q.pop()
            if temp == "T":
                game.p5TotalCards = addCard(win, game.p5, "10" + randomSuit(), game.p5TotalCards)
            else:
                game.p5TotalCards = addCard(win, game.p5, str(temp) + randomSuit(), game.p5TotalCards)

        win.update_idletasks()

        p = win.getMouse()
        if game.wager5_Button.clicked(p):
            requests.post(url = URL + "WA", json = {"wager" : 5, "seatNo" : seatNo})
            balance -= 5
            wager = 5
            game.wager_view.updateText(str(wager))
            game.balance_view.updateText(str(balance))
            game.disableWagers()

        if game.wager10_Button.clicked(p):
            requests.post(url = URL + "WA", json = {"wager" : 10, "seatNo" : seatNo})
            balance -= 10
            wager = 10
            game.wager_view.updateText(str(wager))
            game.balance_view.updateText(str(balance))
            game.disableWagers()

        if game.wager20_Button.clicked(p):
            requests.post(url = URL + "WA", json = {"wager" : 20, "seatNo" : seatNo})
            balance -= 20
            wager = 20
            game.wager_view.updateText(str(wager))
            game.balance_view.updateText(str(balance))
            game.disableWagers()

        if game.wager50_Button.clicked(p):
            requests.post(url = URL + "WA", json = {"wager" : 50, "seatNo" : seatNo})
            balance -= 50
            wager = 50
            game.wager_view.updateText(str(wager))
            game.balance_view.updateText(str(balance))
            game.disableWagers()

        if game.hit_Button.clicked(p):
            requests.post(url = URL + "AC", json = {"seatNo" : seatNo, "action" : "HT"} )
            game.enableGameButtons()


        if game.stay_Button.clicked(p):
            requests.post(url = URL + "AC", json = {"seatNo" : seatNo, "action" : "ST"} )
            game.disableGameButtons()

        if game.double_Button.clicked(p):
            requests.post(url = URL + "AC", json = {"seatNo" : seatNo, "action" : "DD"} )
            game.disableGameButtons()
            balance -= wager
            wager = wager * 2
            game.balance_view.updateText(str(balance))
            game.wager_view.updateText(str(wager))
            
        
        

        #game.wager_view.updateText(value)


    #Quit Game Message




    

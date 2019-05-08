from graphics import *
from Button import *
from Model import *
from Hand import *
import time

class gameWin():
    def __init__(self, win):
        #win: 400x600
        #Set Variables For the Game
        center = Point(250,110)
        self.score = 0
        self.winnings = 0
        self.balance = 0
        self.wager = 0

        self.p1Alias = ""
        self.p2Alias = ""
        self.p3Alias = ""
        self.p4Alias = ""
        self.p5Alias = ""

        self.dealerTotalCards = 0
        self.p1TotalCards = 0
        self.p2TotalCards = 0
        self.p3TotalCards = 0
        self.p4TotalCards = 0
        self.p5TotalCards = 0

        _table = "client/images/table.png"
        table = Image(Point(205,40), _table)
        table.draw(win)

        self.p1 = player(win, Point(357, 30), "Empty")
        self.p2 = player(win, Point(300, 65), "Empty")  
        self.p3 = player(win, Point(181, 78), "Empty")
        self.p4 = player(win, Point(72, 65), "Empty")
        self.p5 = player(win, Point(18, 30), "Empty")

        self.p1Hand = Hand()
        self.p2Hand = Hand()
        self.p3Hand = Hand()
        self.p4Hand = Hand()
        self.p5Hand = Hand()

        self.wager_view = Scorebox(win, Point(60,118),"Wager:",self.wager)  
        self.balance_view = Scorebox(win, Point(215,118),"Balance:",self.balance)
        self.winnings_view = Scorebox(win, Point(370,118),"Winnings:",self.winnings)
        self.score_view = Scorebox(win, Point(215,126),"Score:",self.score)

        self.wager5_Button = Button(win, Point(20,126), 20, 10,10,"5", True)
        self.wager10_Button = Button(win, Point(40,126), 20, 10,10,"10", True)
        self.wager20_Button = Button(win, Point(60,126), 20, 10,10,"20", True)
        self.wager50_Button = Button(win, Point(80,126), 20, 10,10,"50", True)
        self.hit_Button = Button(win, Point(50,110),60,10,10,"Hit", False)
        self.stay_Button = Button(win, Point(360,110),60,10,10,"Stay", False)
        self.double_Button = Button(win, Point(205,110), 60, 10,10,"Double", False)
        self.quit_Button = Button(win, Point(360,126), 60, 10,10,"Quit", True)
        self.buttons = [self.hit_Button, self.stay_Button, self.double_Button, self.quit_Button]

    def disableWagers(self):
        self.wager5_Button.deactivate()
        self.wager10_Button.deactivate()
        self.wager20_Button.deactivate()
        self.wager50_Button.deactivate()

    def enableWagers(self):
        self.wager5_Button.activate()
        self.wager10_Button.activate()
        self.wager20_Button.activate()
        self.wager50_Button.activate()

    def enableGameButtons(self):
        self.hit_Button.activate()
        self.stay_Button.activate()
        self.double_Button.activate()

    def disableGameButtons(self):
        self.hit_Button.deactivate()
        self.stay_Button.deactivate()
        self.double_Button.deactivate()


def addCard(win, _player, value, totalCards):
    location = Point(_player.center.getX() - 5 + (totalCards * 10), _player.center.getY() + 20)
    totalCards += 1
    card = Card(win, value, location)
    return totalCards

def addDealerCard(win, value, totalCards):
    location = Point(180 + (totalCards * 10), 10)
    totalCards += 1
    card = Card(win, value, location)
    return totalCards








        

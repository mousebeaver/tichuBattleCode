import tplayer as tplayer0
import tplayer as tplayer1
import tplayer as tplayer2
import tplayer as tplayer3
import numpy as np

#IDs of other players in relation to player with ID i
def partnerID(i):
    return (i+2)%4

def leftID(i):
    return (i+3)%4

def rightID(i):
    return (i+1)%4

#the gameclass itself
class gameMaster:
    def __init__(self, moveDuration): #How long should the cards be displayed in seconds?
        self.moveDuration = moveDuration
        self.pointsA = 0 #points of the teams
        self.pointsB = 0

    def theGame(self): #game loop
        while self.pointsA < 1000 and self.pointsB < 1000:
            self.startRound() #Play a single round
            self.playRound

    def playRound(self): #actually do a round
        pass


    def startRound(self):
        #generate card stack
        self.cardStack = [(j, i) for j in range(13) for i in range(4)] + [(j, 4) for j in range(4)]
        
        #distribute 8 cards to every player
        self.cardHands = [[], [], [], []]
        for i in range(4):
            for _ in range(8):
                nextCard = self.cardStack[np.random.randint(0, len(self.cardStack))]
                self.cardStack.remove(nextCard)
                self.cardHands[i].append(nextCard)
        self.players = [tplayer0.Tplayer(self.cardHands[0], [0, 3, 2, 1]),
                        tplayer1.Tplayer(self.cardHands[1], [1, 0, 3, 2]),
                        tplayer2.Tplayer(self.cardHands[2], [2, 1, 0, 3]),
                        tplayer3.Tplayer(self.cardHands[3], [3, 2, 1, 0])]
        
        #ask for great Tichu (and show the results to others)
        self.greatTichu = []
        for p in self.players:
            self.greatTichu.append(p.greatTichu())
        self.players[0].seeGreatTichu([self.greatTichu[3], self.greatTichu[2], self.greatTichu[1]])
        self.players[1].seeGreatTichu([self.greatTichu[0], self.greatTichu[3], self.greatTichu[2]])
        self.players[2].seeGreatTichu([self.greatTichu[1], self.greatTichu[0], self.greatTichu[3]])
        self.players[3].seeGreatTichu([self.greatTichu[2], self.greatTichu[1], self.greatTichu[0]])

        #prepare for storing the claims of Small Tichu
        self.smallTichu = [False, False, False, False]
        self.playedAlready = [False, False, False, False] #Is the small Tichu now impossible?

        #distribute the remaining cards (6 per player)
        for i in range(4):
            additionalCards = []
            for _ in range(6):
                nextCard = self.cardStack[np.random.randint(0, len(self.cardStack))]
                self.cardStack.remove(nextCard)
                additionalCards.append(nextCard)
            self.cardHands[i] += additionalCards

        #Storage for cards that are not in the game any more
        self.spentCards = []

        #Storage for the wish:
        self.wish = None

        #Make the Schupfing-Process
        schupfStorage = [[None for _ in range(3)] for _ in range(4)]
        for i in range(4):
            schupfAway = self.players[i].schupf()
            schupfStorage[leftID(i)][2] = schupfAway[0]
            schupfStorage[partnerID(i)][1] = schupfAway[1]
            schupfStorage[rightID(i)][0] = schupfAway[2]
        for i in range(4):
            self.players[i].getSchupf(schupfStorage[i])

        #Who's turn is it
        self.turn = 0
        while not (4, 1) in self.cardHands[self.turn]:
            self.turn += 1
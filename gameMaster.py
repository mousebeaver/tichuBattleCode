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

def pointValue(cardList): #returns accumulated value of a list of cards
    output = 0
    for c in cardList:
        if c.first == 5: #the card is a 5
            output += 5
        elif c.first == 10 or c.first == 13: #the card is a 10 or a king
            output += 10
        elif c == (2, 4): #the card is the dragon
            output += 25
        elif c == (3, 4): #the card is the phoenix
            output -= 25
    return output


#the gameclass itself
class gameMaster:
    def __init__(self, moveDuration): #How long should the cards be displayed in seconds?
        self.moveDuration = moveDuration
        self.pointsA = 0 #points of the teams (0, 2)
        self.pointsB = 0 #player(1, 3)
        self.controlCardStack = [(j, i) for j in range(13) for i in range(4)] + [(j, 4) for j in range(4)] #the whole set of cards

    def theGame(self): #game loop
        while self.pointsA < 1000 and self.pointsB < 1000:
            #Play a single round
            self.startRound()
            self.playRound()

    def playRound(self): #actually do a round
        while (not (len(self.cardHands[0]) == 0 and len(self.cardHands[2]) == 0)) and (not (len(self.cardHands[1]) == 0 and len(self.cardHands[3]) == 0)) and self.legalRound:
            #ask for a turn
            turn = self.player[self.turn] #The turn the player actually does            

            #check whether the turn is illegal...
            #...based on claiming a small Tichu
            if turn[len(turn)-2] == True and (self.smallTichu[self.turn] or self.playedAlready[self.turn] or self.greatTichu[self.turn]): 
                self.handleIllegalPlays(self.turn)
                break

            #...based on making an illegal wish
            w = turn(len(turn)-1)
            if turn[len(turn)-1] != None and (self.wish != None or turn[0] != (1, 4) or len(turn) != 3 or (not w in self.controlCardStack) or w.second == 4): 
                self.handleIllegalPlays(self.turn)
                break

            #...based on playing illegal cards
            for c in turn[:len(turn)-2]:
                if (not c in self.controlCardStack) or (c in self.spentCards):
                    self.handleIllegalPlays(self.turn)
                    break


            #set wish/Tichu/alreadyPlayed/knockCounter/spentCards/hands of players
            if turn[len(turn)-2] == True: 
                self.smallTichu[self.player[self.turn]] = True #The player claimed a small Tichu

            if turn[len(turn)-1] != None: 
                self.wish = turn[len(turn)-1] #There is a wish

            if len(turn) > 2:
                self.playedAlready[self.turn] = True
                for c in turn[:len(turn)-2]:
                    self.spentCards.append(c)
                    self.players[self.turn].remove(c)
            else:
                self.knockCounter += 1

            #did the player finish?
            if len(self.players[self.turn]) == 0:
                self.finished[self.turn] = len(self.spentCards)
            
            #inform the others about the turn
            for i in range(1, 4):
                self.players[(self.turn+i)%4].seeTurn(turn, self.turn)

            noBombCounter = 0 #How many players have chosen not to put down a bomb
            while noBombCounter < 4 and self.legalRound:
                #Ask everyone for a bomb:

                for i in range(4):
                    b = self.players[i].bomb()
                    
                    #Check small Tichu (and legality):
                    if b[len(b)-1]:
                        if self.playedAlready[i]:
                            self.handleIllegalPlays(i)
                        else:
                            self.smallTichu[i] = True
                    
                    #set spentCards:
                    for c in turn[:len(turn)-1]:
                        self.spentCards.append(c)
                        self.players[i].remove(c)

                    #handle bomb (if put down)
                    if len(b) > 1:
                        self.alreadyPlayed[i] = True
                        noBombCounter = 0
                        self.knockCounter = 3 #No not-bomb is possible any more
                        #show the bomb to everyone:
                        for j in range(1, 4):
                            self.players[(i+j)%4].showBomb(b, i)


            #handle the case that everyone knocked:
            if self.knockCounter == 3:
                self.playerPoints[self.turn] += pointValue(self.currentTrick)
                self.currentTrick = []
                self.stackTop = []
                self.knockCounter = 0

            #set the player who can make the next turn
            self.turn = (self.turn+1)%4
            while len(self.cardHands[self.turn]) == 0:
                self.turn = (self.turn+1)%4

        if(self.legalRound):
            #Award points after a round that has finished legally
            first = 0 #Who finished first?
            for i in range(1, 4):
                if self.finished[first] == None or (self.finished[i] != None and self.finished[i] < self.finished[first]):
                    first = i

            #Double win?
            if len(self.cardHands[0]) > 0 and len(self.cardHands[2]) > 0:
                self.pointsB += 200
            elif len(self.cardHands[1]) > 0 and len(self.cardHands[3]) > 0:
                self.pointsA += 200
            else: #No double win                    
                last = 0 #Who has not finished
                while len(self.cardHands[last]) > 0:
                    last += 1

                #Give away won tricks:
                self.playerPoints[first] += self.playerPoints[last]
                self.playerPoints[last] = 0

                #Give away handcards:
                if last == 0 or last == 2:
                    self.playerPoints[1] += pointValue[self.cardHands[last]]
                else:
                    self.playerPoints[0] += pointValue[self.cardHands[last]]

                #Add up points:
                self.playerPoints[0] += self.playerPoints[2]
                self.playerPoints[1] += self.playerPoints[3] 
                self.pointsA += self.playerPoints[0]
                self.pointsB += self.playerPoints[1]

            #Process Tichus:
            for i in [0, 2]:
                if self.smallTichu[i]:
                    if i == first:
                        self.pointsA += 100
                    else:
                        self.pointsA -= 100
                if self.greatTichu[i]:
                    if i == first:
                        self.pointsA += 200
                    else:
                        self.pointsA -= 200
            for i in [1, 3]:
                if self.smallTichu[i]:
                    if i == first:
                        self.pointsB += 100
                    else:
                        self.pointsB -= 100
                if self.greatTichu[i]:
                    if i == first:
                        self.pointsB += 200
                    else:
                        self.pointsB -= 200
    
    def handleIllegalPlays(self, playerID): #If the player does an illegal move, 200 points are deducted and 200 are awarded to the other team
        self.legalRound = False
        if playerID == 0 or playerID == 2:
            self.A -= 200
            self.B += 200
        else:
            self.B -= 200
            self.A += 200

    def startRound(self):
        #generate card stack
        self.cardStack = self.controlCardStack

        #Has no rule been violated?
        self.legalRound = True

        #current Trick
        self.currentTrick = [] #List of cards in the current trick
        self.stackTop = [] #Combination on the top of the stack

        #points of the players
        self.playerPoints = [0, 0, 0, 0] #Number of points, every player has already aquired
        
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

        #Storage for how many players have knocked (in a row)
        self.knockCounter = 0

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

        #Who finished when?
        self.finished = [None, None, None, None] #After how many cards (totally played) did the player finish?
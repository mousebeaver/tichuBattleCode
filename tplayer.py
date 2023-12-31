"""
Cards are represented by pairs of integers:
-the first integer is the value. For special cards:  0->Hound, 1->One, 2->Dragon , 3->Phoenix, else 2-14
-the second integer is the color (0-3 for normal colours, 4 for special cards)
"""

from tichuCards import *

class Tplayer:
    def __init__(self, firstEight, ids): #ids is list of player ids: [self, left, partner, right]
        self.cards = firstEight #List of the card currently in the hand of the player
        self.ids = ids #ids of the other players
        self.upperTrick = [] #Trick on the top
        self.knockCounter = 0 #Count of players who have knocked after last card
        self.wish = None #Card that was wished by the one
        pass
    
    def greatTichu(self): #great Tichu after first eight cards?
        return False

    def seeGreatTichu(self, bets): #list of booleans: who of the others bet a great Tichu? [left, partner, right]
        pass

    def fillCards(self, lastSix): #Gives the next six cards after possible greatTichu
        self.cards += lastSix
        self.cards = sorted(self.cards)
        pass

    def schupf(self): #returns tuple of 3 cards: left, partner, right
        output = [self.cards[0], self.cards[len(self.cards)-1], self.cards[1]]
        for i in output:
            self.cards.remove(i)
        self.cards = sorted(self.cards)
        return output

    def getSchupf(self, cards): #receives three cards: from left, from partner, from right
        self.cards += cards
        self.cards = sorted(self.cards)
        pass

    def seeTurn(self, turn, player): #receives the turn of an opponent and index of player who made the turn
        if len(turn) == 2: #the player knocked
            self.knockCounter += 1
            if(self.knockCounter == 3):
                self.upperTrick = []
                self.knockCounter = 0
        else:
            self.upperTrick = turn[:len(turn)-2]
        
        if (0,4) in turn: #There was a hound
            self.upperTrick = []
            self.knockCounter = 0

        if turn[len(turn)-1] != None: #the player has a wish:
            self.wish = turn[len(turn)-1]
        pass 

    def turn(self): #returns (empty) list of cards to be put down, second-last element is boolean: small Tichu?, last element: integer of card as wish
        output = []
        if self.upperTrick == [] and len(self.cards) > 0:
            output.append(self.cards[0]) #The player can put down a card
            self.cards.remove(output[0])
            self.knockCounter = 0
        else:
            self.knockCounter += 1 #The player "knocks" if he is already finished!!!
            if(self.knockCounter == 3):
                self.upperTrick = []
                self.knockCounter = 0
        self.upperTrick = []
        output.append(False)
        output.append(None)
        return output

    def bomb(self): #returns (empty) list of bomb to be put down, last element is boolean for small Tichu
        return [False]
    
    def showBomb(self, bomb, player): #receives the bomb as list (last element is boolean for small Tichu) and the id of the player who put it down
        self.knockCounter = 0
        self.upperTrick = bomb
        pass

    def getToPlay(self, id): #The player with the given ID receives the right to play (at an empty stack of cards)
        self.knockCounter = 0
        self.upperTrick = []

    def donateDragon(self): #Return the id the dragon should be donated to?
        return self.ids[0]
    
    def seeDonation(self, id): #Gets the id of the player the dragon is donated to
        pass

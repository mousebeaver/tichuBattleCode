#This file is meant to contain some useful functionality concerning Tichu cards and their combinations
#It is used by the gameMaster-Class and the dumb sample player, but it does not have to be used by the player

def pointValue(cardList): #returns accumulated value of a list of cards
    output = 0
    for c in cardList:
        if c[0] == 5: #the card is a 5
            output += 5
        elif c[0] == 10 or c[0] == 13: #the card is a 10 or a king
            output += 10
        elif c == (2, 4): #the card is the dragon
            output += 25
        elif c == (3, 4): #the card is the phoenix
            output -= 25
    return output


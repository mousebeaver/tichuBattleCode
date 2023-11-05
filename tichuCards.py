#This file is meant to contain some useful functionality concerning Tichu cards and their combinations
#It is used by the gameMaster-Class and the dumb sample player, but it does not have to be used by the player

phoenix = (3, 4)
dragon = (2, 4)
one = (1, 4)
hound = (0, 4)

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

def identifyCombination(cardList, prevCardList):
    """
    returns the type of the combination in cardList as one of the following values:
    - "singleCard"
    - "triple"
    - "fullHouse"
    - "straight"
    - "pairStraight (a pair is a pairStraight of length 1)"
    - "fourBomb"
    - "straightBomb"
    - None

    prevCardList is the trick the current CardList is put one (important for single card phoenix)

    this value is combined with its height to form a tuple
    - singleCard => value of the card (1000 for dragon)
    - fullHouse => value of the tripel
    - anything else => lowest card in the cardList
    - None => No tuple made

    in the case of (pair-)straights (or straightBombs), their length is the third element of the tupel
    in the case of pairStreets, this is the number of pairs!
    """

    cardList.sort()

    if len(cardList) == 1:
        #A single card
        if cardList[0] == dragon:
            #the dragon
            return ("singleCard", 1000)
        elif cardList[0] == phoenix:
            #the phoenix
            value = 1.5
            if prevCardList != []:
                value = prevCardList[0][0]+0.5 #We assume that this list does not contain the dragon
            return ("singleCard", value)
        else:
            #some other single Card
            return ("singleCard", cardList[0][0])
    
    if len(cardList) == 3:
        #Maybe a triple
        if cardList[0] == phoenix:
            #The first card is the phoenix -> swap to another position
            tmp = cardList[1]
            cardList[1] = cardList[0]
            cardList[0] = tmp
        if (cardList[1] == phoenix or cardList[1][0] == cardList[0][0]) and (cardList[2] == phoenix or cardList[2][0] == cardList[0][0]):
            return ("triple", cardList[0][0])
        
    if len(cardList) == 5:
        #Maybe a fullHouse
        if phoenix in cardList:
            cardList.erase(phoenix)
            if cardList[0][0] == cardList[1][0] and cardList[2][0] == cardList[3][0]:
                cardList.append(phoenix)
                return ("fullHouse", cardList[3][0])
            cardList.append(phoenix)
        elif cardList[0][0] == cardList[1][0] and cardList[0][0] == cardList[2][0] and cardList[3][0] == cardList[4][0]:
            return ("fullHouse", cardList[0][0])
        elif cardList[0][0] == cardList[1][0] and cardList[3][0] == cardList[2][0] and cardList[2][0] == cardList[4][0]:
            return ("fullHouse", cardList[4][0])
        
    if len(cardList) >= 5:
        #Maybe a straigt
        pcounter = 0
        if phoenix in cardList:
            cardList.erase(phoenix)
            pcounter += 1
        straight = True
        for i in range(1, len(cardList)):
            if cardList[i][0] == cardList[i-1][0]+2 and pcounter > 0:
                pcounter -= 1
            elif cardList[i][0] != cardList[i-1][0]+1:
                straight = False
                break
        cardList.append(phoenix)
        if straight:
            return ("straight", cardList[0][0])



    if len(cardList) >= 2 and len(cardList)%2 == 0:
        #Maybe a pairStraight
        pass

    if len(cardList) == 4:
        #Maybe a FourBomb
        if (not phoenix in cardList) and (not dragon in cardList) and (not hound in cardList) and (not one in cardList):
            if cardList[0][0] == cardList[1][0] and cardList[0][0] == cardList[2][0] and cardList[0][0] == cardList[3][0]:
                return ("fourBomb", cardList[0][0]) 

    if len(cardList) >= 5:
        #Maybe a StraightBomb
        if (not phoenix in cardList) and (not dragon in cardList) and (not hound in cardList) and (not one in cardList):
            straight = True
            for i in range(1, len(cardList)):
                if cardList[i][0] != cardList[i-1][0]+1:
                    straight = False
                    break
            if straight:
                return ("streetBomb", cardList[0][0])

    return None

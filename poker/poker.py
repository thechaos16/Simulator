import os,sys
import random
import deck, checker

# dictionaries
score = {1:'Royal Straight Flush', 2:'Straight flush', 3:'Four cards', 4:'Full house', 5:'Flush', 6:'Straight', 7:'Triple', 8:'Two pairs', 9:'One pair', 10:'None'}
dealing = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
dealing2 = {1:'Spade',2:'Diamond',3:'Heart',4:'Club'}

# class of board
class board:
	def __init__(self,nop):
		self.nop = nop

# play Holdem (input: number of players)
def holdem(n):
    # define deck
    dk = deck.deck(1)
    dk.setdeck()

    # define table
    p = [deck.player('table',0)]
    for i in range(n):
        p.append(deck.player(str(i+1),100))

    # deal 2 cards to each
    for i in range(1,len(p)):
        p[i].take(dk.deal())
        p[i].take(dk.deal())

    # bet
    ##

    # deal 2 cards to table
    p[0].take(dk.deal())
    p[0].take(dk.deal())

    # show table cards
    print 'table cards'
    p[0].showcards()

    # bet
    ##

    # deal 3 more cards to table
    p[0].take(dk.deal())
    p[0].take(dk.deal())
    p[0].take(dk.deal())

    # show table cards
    print 'table cards'
    p[0].showcards()
    print ''
    # bet
    ##

    # check
    # get best cards of each
    best = []
    for i in range(1,len(p)):
        if p[i].status==1:
            continue
        temp = p[0].getcards()
        for j in range(len(temp)):
            p[i].take(temp[j])
        best.append([checker.extract(p[i].getcards(),5),i])
    # check the winner
    win = [0]
    for i in range(1,len(best)):
        fight = checker.compete([best[win[0]][0],best[i][0]])
        if fight==2:
            win = [i]
        elif fight==1:
            win.append(i)
    # show result
    for i in range(len(best)):
        p[best[i][1]].showcards()
        print p[best[i][1]].name+': '+score[checker.order(best[i][0])]
        for j in range(len(best[i][0])):
            print best[i][0][j]
        print ''
    print 'The winner is '
    for i in range(len(win)):
        print p[best[win[i]][1]].name

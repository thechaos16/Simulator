import os,sys
import random
import deck

# dictionaries
score = {'2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'J' : 10, 'Q' : 10, 'K' : 10, 'A1' : 1, 'A2' : 11}
dealing = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
dealing2 = {1:'Spade',2:'Diamond',3:'Heart',4:'Club'}

# return value of card
def card(a, b):
    if a=='A':
        if b==1:
            return score['A1']
        else:
            return score['A2']
    else:
        return score[a]

# dealer's strategy (a : sum of previous cards, b : new card tag(str))
def dealer(a, b):
    p1 = a+card(b,1)
    p2 = a+card(b,2)
    if b=='A':
        if p2<=21:
            if p2>=17:
                return 'S'
            else:
                return 'H'
        else:
            if p1>=17:
                return 'S'
            else:
                return 'H'
    else:
        if p1>=17:
            return 'S'
        else:
            return 'H'

# dealer's strategy (a : cards dealer got) -> soft 17
def dealer2(a):
    dcards = a.getcards()
    tempval = a.value()
    if tempval>=17:
        return 'S'
    ch = 0
    for i in range(len(dcards)):
        if dcards[i][1] == 'A':
            ch += 1
    if ch==0:
        return 'H'
    else:
        if tempval+10>=17 and tempval+10<=21:
            a.setvalue2(tempval+10)
            #print a.value()
            return 'S'
        else:
            return 'H'

# play game (card deck, delaer, players, betting money)
def run(dd,d,p,b):
    # set the game
    #dd = deck()
    #dd.setdeck()
    ter = 0
    
    # first two rounds
    r = 1
    d.setvalue()
    for i in range(len(p)):
        p[i].setvalue()
    while(1):
        if r>2:
            break
        if r==2:
            temp = d.value()
            d.take(dd.deal())
            # dealer's next move
            #dnm = dealer(temp,d.getlastcard())
            d.setvalue()
            dnm = dealer2(d)
        else:
            d.take(dd.deal())
            #d.take(['Club','A'])
        for i in range(len(p)):
            p[i].take(dd.deal())
            p[i].setvalue()
        #nm = dealer2(p[0])
        r=r+1

    # black jack!
    if d.value()==21 or p[0].value()==21:
        ter = 1

    # additional rounds
    # double checker
    isdouble = 0
    while(ter==0):
        #show both cards
        d.showcards(1)
        for i in range(len(p)):
            print ""
            p[i].showcards(0)

        # determine next moves
        nm = raw_input("Your moves?")
        if nm=='H':
            p[0].nextmove(dd.deal())
            p[0].setvalue()
            #nm = dealer2(p[0])
            '''if dnm=='H':
                temp2 = dd.deal()
                #dnm = dealer(d.value(),temp2[1])
                d.take(temp2)
                d.setvalue()
                dnm = dealer2(d)'''
            if p[0].value()>21 or d.value()>21:
                break
        # when player stay
        elif nm=='S':
            while(dnm=='H'):
                temp2 = dd.deal()
                #dnm = dealer(d.value(),temp2[1])
                d.take(temp2)
                d.setvalue()
                dnm = dealer2(d)
            break
        # when player double
        else:
            isdouble = 1
            p[0].nextmove(dd.deal())
            p[0].setvalue()
            if p[0].value()>21:
                break
            while(dnm=='H'):
                temp2 = dd.deal()
                d.take(temp2)
                d.setvalue()
                dnm = dealer2(d)
            break

    d.showcards(0)
    for i in range(len(p)):
        print ""
        p[i].showcards(0)
    print "Dealer got " + str(d.value()) + ", and you got " + str(p[0].value()) + "."
    if p[0].value()>21:
        print "Dealer win!"
        p[0].setmoney(-b)
        if isdouble==1:
            p[0].setmoney-(b)
    elif d.value()>21:
        print "You win!"
        p[0].setmoney(b)
        if isdouble==1:
            p[0].setmoney(b)
    else:
        if d.value()>p[0].value():
            print "Dealer win!"
            p[0].setmoney(-b)
            if isdouble==1:
                p[0].setmoney(-b)
        elif d.value()==p[0].value():
            print "Draw!"
        else:
            print "You win!"
            p[0].setmoney(b)
            if isdouble==1:
                p[0].setmoney(b)
    for i in range(len(p)):
        p[i].clearcards()
    d.clearcards()


# blackjack simulator    
def simulator():
    # number of deck
    nod = 5
    dd = deck.deck(nod)
    dd.setdeck()
    # players
    d = deck.player("Dealer",0)
    p = [deck.player("Player 1",10)]

    # play game
    while(1):
        print p[0].name + ' has ' +str(p[0].getmoney())
        bet = raw_input("betting money?")
        if int(bet)>p[0].getmoney():
            print p[0].name + ' does not have enough money!'
            continue
        run(dd,d,p,int(bet))
        kk = raw_input("more game?")
        if kk=='N':
            break
        if p[0].getmoney()<=0:
            print p[0].name + ' has been bankrupted!'
            break


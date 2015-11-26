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

# play game (card deck, delaer, players, betting money, database for AI, number of deck)
def run(dd,d,p,b,dbres,nod):
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
        nm = dealer2(p[0])
        r=r+1

    # black jack!
    if d.value()==21 or p[0].value()==21:
        ter = 1

    # number of round (for preventing double)
    ro = 0
    # double checker
    isdouble = 0
    # additional rounds
    while(ter==0):
        #show both cards
        #d.showcards(1)
        #for i in range(len(p)):
            #print ""
            #p[i].showcards(0)

        # determine next moves automatically
        sit = [d.getcards()[1],p[0].getcards(),p[0].value()]
        #nm = raw_input("Your moves?")
        # aritificial intelligence
        if ro==0:
            nm = AI(sit,dbres)
            #print nm
        else:
            nm = dealer2(p[0])
        # when player hit
        if nm=='H':
            p[0].nextmove(dd.deal())
            p[0].setvalue()
            if p[0].value()>21:
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
        ro+=1

   # print ""
   # d.showcards(0)
    #for i in range(len(p)):
        #print ""
        #p[i].showcards(0)
   # print "Dealer got " + str(d.value()) + ", and you got " + str(p[0].value()) + "."
    if p[0].value()>21:
        #print "Dealer win!"
        p[0].setmoney(-b)
        if isdouble==1:
            p[0].setmoney(-b)
    elif d.value()>21:
        #print "You win!"
        p[0].setmoney(b)
        if isdouble==1:
            p[0].setmoney(b)
    else:
        if d.value()>p[0].value():
            #print "Dealer win!"
            p[0].setmoney(-b)
            if isdouble==1:
                p[0].setmoney(-b)
        #elif d.value()==p[0].value():
            #print ""
            #print "Draw!"
        else:
            #print "You win!"
            p[0].setmoney(b)
            if isdouble==1:
                p[0].setmoney(b)
    for i in range(len(p)):
        p[i].clearcards()
    d.clearcards()

# artificial intelligence (naive version)
def AI(sit,dbres):
    res = ['H','S','D']
    dvalue = sit[0][1]
    if dvalue=='A':
        dvalue = 1
    if dvalue=='J' or dvalue=='Q' or dvalue=='K':
        dvalue = 10
    pvalue = sit[2]
    #print dvalue, pvalue
    # check if player has Ace
    temp = 0
    for i in range(len(sit[1])):
        if sit[1][i][1]=='A':
            temp = 1
    for i in range(len(dbres)):
        if int(dvalue)==int(dbres[i][0]):
            if temp==0:
                if 'A' not in dbres[i][1]:
                    if int(dbres[i][1])==int(pvalue):
                        return res[int(dbres[i][2])]
            else:
                if 'A' in dbres[i][1]:
                    if int(dbres[i][1][0:len(dbres[i][1])-1])==int(pvalue):
                        return res[int(dbres[i][2])]

# read database (select strategy with biggest winning probability)
def db(nod):
    f = file(str(nod)+'db.txt','r')
    data = []
    for line in f:
        if line[0]=='d':
            continue
        l = line.split('\t')
        temp = 0.0
        tempind = 0
        for i in range(2,5):
            if float(l[i])>temp:
                tempind = i-2
                temp = float(l[i])
        temp2 = [l[0],l[1],tempind]
        data.append(temp2)        
    return data

# read raw DB
def dbraw(nod):
    f = file(str(nod)+'db.txt','r')
    data = []
    for line in f:
        if line[0]=='d':
            continue
        l = line.split('\t')
        temp = [l[0],l[1]]
        check = 0
        for i in range(5,8):
            l[i] = l[i].strip('\n')
            l[i] = l[i].strip('[')
            l[i] = l[i].strip(']')
            temp2 = l[i].split(', ')
            for j in range(len(temp2)):
                check+=int(temp2[j])
            temp.append(temp2[0])
        temp.append(str(check/3))
        data.append(temp)
    return data

# blackjack simulator    
def simulator(a,nod):
    # number of deck
    nod = 5
    dd = deck.deck(nod)
    dd.setdeck()
    # players
    smoney = 10
    d = deck.player("Dealer",0)
    p = [deck.player("Player 1",smoney)]

    # load database
    dbres = db(nod)

    # auto betting
    bet = 1

    # result
    res = 0

    # play game
    while(1):
        #print p[0].name+' has '+str(p[0].getmoney())
        run(dd,d,p,bet,dbres,nod)
        #k = raw_input("asdf?")
        if p[0].getmoney()<=0:
            #print p[0].name + ' has been bankrupted!'
            break
        elif float(p[0].getmoney())>float(smoney)*a:
            #print p[0].name + 'has won!'
            res = 1
            break

    return res

# full result (n: # of trial, a: target, nod: number of deck)
def itisim(n,a,nod):
    res = 0
    for i in range(n):
        temp = simulator(a,nod)
        res+=temp
    # number of winning trial
    return res

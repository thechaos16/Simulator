import os,sys
import random

# card class
class cards:
    def __init__(self):
        ran1 = random.randint(1,10)
        self.num = ran1
    def getcard(self):
        return self.num

# deck class
class deck:
    def __init__(self,p):
        self.p = p
        self.dlist = []
        self.checker = 0
    def setdeck(self):
        for i in range(1,11):
            self.dlist.append([i,self.p])
    def getdeck(self):
        return self.dlist
    def deal(self):
        dcard = cards()
        dealed = dcard.getcard()
        if [dealed,0] in self.dlist:
            #print "it has been dealed"
            return self.deal()
        else:
            #print "The card " + dealed[1] + " " + dealed[0]+" has been dealed"
            for i in range(self.p+1):
                if [dealed,i] in self.dlist:
                    self.dlist[self.dlist.index([dealed,i])] = [dealed,i-1]
                    break
            return dealed
    def lid(self):
        res = []
        for i in range(len(self.dlist)):
            for j in range(self.dlist[i][1]):
                res.append(self.dlist[i][0])
        return res

# player class
class player:
    def __init__(self,a,m):
        self.name = a
        self.card = 0
        self.money = m
        self.status = 0
    def take(self,l):
        self.card = l
    def setmoney(self,m):
        self.money+=m
    def showcards(self):
        print self.card
    def getcards(self):
        return self.card
    def getmoney(self):
        return self.money
    def clearcards(self):
        self.card = 0
    def move(self,m,b):
        # if player folds, status becomes 1
        self.status = m
        if self.status==0:
            self.bet(b)
    def bet(self,m):
        self.money-=m
    def getstatus(self):
        return self.status
    def getname(self):
        return self.name

# conditional probability (p(a|d), a: my card, d: deck)
def cardprob(d):
    l = []
    remain = d.lid()
    for i in range(10):
        l.append(round(float(remain.count(i+1))/float(len(remain)),3))
    return l

# winning probability (d: deck in table, c: opponent's card)
def winp(d,c):
    remain = d.lid()
    if remain==0:
        return -1
    check = 0
    tie = 0
    for i in range(len(remain)):
        if c>remain[i]:
            check+=1
        elif c==remain[i]:
            tie+=1
    return 1-round((float(check)/float(len(remain)-tie)),3)

# predict my card (need to be improved)
def mcard(d,m):
    l = []
    prior = cardprob(d)
    for i in range(10):
        # opponent's winning probability based on my cards (unknown)
        temp = winp(d,i+1)
        # opponent folds
        if m==0:
            l.append(round(2*prior[i]*(1-temp),3))
        # opponent bets
        else:
            l.append(round(2*prior[i]*temp,3))
    return l

# function based budget (player, opponent, move of opponent) 
def budget(p,o,m):
    bp = p.getmoney()
    bo = o.getmoney()
    fun = bp*bo*m
    return 0

# select my move (d: deck, m: opponent's move, c: opponent's card)
def mmove(d,m,c):
    l = mcard(d,m)
    res = 0.0
    for i in range(10):
        if i+1-c<0:
            res-=l[i]
        elif i+1-c>0:
            res+=l[i]
    return res

# play
def indian():
    p = []
    for i in range(2):
        p.append(player('player'+str(i+1),10))

    # set deck
    nod = 2
    dd = deck(nod)
    dd.setdeck()

    # play
    while 1:
        # termination
        if len(dd.lid())==0:
            print 'all cards have been dealed'
            if p[0].getmoney()>p[1].getmoney():
                print p[0].getname() + ' wins!'
            elif p[0].getmoney()<p[1].getmoney():
                print p[1].getname() + ' wins!'
            else:
                print 'tie!'
        if p[0].getmoney()<=0:
            print p[0].getname() + ' has been bankrupted'
            print p[1].getname() + ' wins!'
        if p[1].getmoney()<=0:
            print p[1].getname() + ' has been bankrupted'
            print p[0].getname() + ' wins!'
        # deal
        p[0].take(dd.deal())
        p[1].take(dd.deal())

        # bet
        checker = 0
        cb = [0,0]
        while 1:
            print 'current betting is ' + str(cb[(checker+1)%2])
            print 'you got $'+str(p[checker%2].getmoney())
            bb = raw_input('betting?')
            if bb=='0':
                p[checker%2].move(1,0)
                break
            else:
                while 1:
                    if cb[checker%2]+int(bb)<cb[(checker+1)%2]:
                        print 'you should bet at least '+str(cb[(checker+1)%2]-cb[checker%2])
                        bb = raw_input('betting?')
                    else:
                        break
                p[checker%2].move(0,int(bb))
                cb[checker%2]+=int(bb)
                if cb[checker%2]==cb[(checker+1)%2]:
                    break
            checker+=1

        # check
        p[0].showcards()
        p[1].showcards()

        # if someone folds
        if p[1].getstatus()==1:
            p[0].setmoney(cb[0]+cb[1])
            if p[1].getcards()==10:
                p[1].bet(10)
                p[0].setmoney(10)
            print p[0].getname() + ' wins!'
            continue
        if p[0].getstatus()==1:
            p[1].setmoney(cb[0]+cb[1])
            if p[0].getcards()==10:
                p[0].bet(10)
                p[1].setmoney(10)
            print p[1].getname() + ' wins!'
            continue

        
        if p[0].getcards()>p[1].getcards():
            p[0].setmoney(cb[0]+cb[1])
            print p[0].getname() + ' wins!'
        elif p[0].getcards()<p[1].getcards():
            p[1].setmoney(cb[0]+cb[1])
            print p[1].getname() + ' wins!'
        else:
            p[0].setmoney(cb[0])
            p[1].setmoney(cb[1])
            print 'Tie!'
        

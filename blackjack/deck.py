import os,sys
import random

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

# card class
class cards:
    def getcard(self):
        ran1 = random.randint(1,13)
        ran2 = random.randint(1,4)
        num = dealing[ran1]
        pat = dealing2[ran2]
        return [num,pat]

# deck class
class deck:
    def __init__(self,p):
        self.p = p
        self.dlist = []
        self.checker = 0
    def setdeck(self):
        for i in range(1,5):
            for j in range(1,14):
                # p cards in the deck
                # p : number of deck
                self.dlist.append([dealing2[i],dealing[j],self.p])
    def getdeck(self):
        return self.dlist
    def deal(self):
        if self.checker<52*self.p:
            dcard = cards()
            dealed = dcard.getcard()
            if [dealed[1],dealed[0],0] in self.dlist:
                #print "it has been dealed"
                return self.deal()
            else:
                #print "The card " + dealed[1] + " " + dealed[0]+" has been dealed"
                for i in range(self.p+1):
                    if [dealed[1],dealed[0],i] in self.dlist:
                        self.dlist[self.dlist.index([dealed[1],dealed[0],i])] = [dealed[1],dealed[0],i-1]
                        break
                self.checker = self.checker+1
                return [dealed[1],dealed[0]]
        # refresh the deck
        else:
            self.dlist = []
            self.setdeck()
            self.checker=0
            return self.deal()
    def removefromdeck(self,a):
        if [a[0],a[1],1] in self.dlist:
            self.dlist[self.dlist.index([a[0],a[1],1])] = [a[0],a[1],0];
    def addtodeck(self,a):
        for i in range(self.p+1):
            if [a[0],a[1],i] in self.dlist:
                self.dlist[self.dlist.index([a[0],a[1],i])] = [dealed[1],dealed[0],i+1]
                break

# player class
class player:
    def __init__(self,a,m):
        self.name = a
        self.clist = []
        self.money = m
    def take(self,l):
        self.clist.append(l)
    def setvalue(self):
        self.val = 0
        ck = 0
        for i in range(len(self.clist)):
            if self.clist[i][1] == 'A':
                ck=1
            self.val+=card(self.clist[i][1],1)
        if ck==1:
            if self.val+10<=21:
                self.val+=10
    def setvalue2(self,a):
        self.val = a
    def setmoney(self,m):
        self.money+=m
    def value(self):
        return self.val
    def showcards(self,t):
        for i in range(t,len(self.clist)):
            print self.clist[i]
    def nextmove(self,c):
        self.take(c)
    def getlastcard(self):
        return self.clist[len(self.clist)-1][1]
    def getcards(self):
        return self.clist
    def getmoney(self):
        return self.money
    def clearcards(self):
        self.clist = []

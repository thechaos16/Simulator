# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 19:37:58 2016

@author: thech
"""

import os,sys
import numpy.random as random

# dictionaries
score = {1:'Royal Straight Flush', 2:'Straight flush', 3:'Four cards', 4:'Full house', 5:'Flush', 6:'Straight', 7:'Triple', 8:'Two pairs', 9:'One pair', 10:'None'}
dealing = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
dealing2 = {1:'Spade',2:'Diamond',3:'Heart',4:'Club'}

# card class
class Cards:
    def __init__(self):
        ran1 = random.randint(1,13)
        ran2 = random.randint(1,4)
        self.number = dealing[ran1]
        self.pattern = dealing2[ran2]
    def get_cards(self):
        return [self.number,self.pattern]

# deck class
class Deck:
    def __init__(self,player):
        self.player = player
        self.deck_list = []
        self.checker = 0
    def setdeck(self):
        for i in range(1,5):
            for j in range(1,14):
                self.dlist.append([dealing2[i],dealing[j],self.p])
    def getdeck(self):
        return self.dlist
    def deal(self):
        if self.checker<52:
            dcard = Cards()
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
    def removefromdeck(self,a):
        if [a[0],a[1],1] in self.dlist:
            self.dlist[self.dlist.index([a[0],a[1],1])] = [a[0],a[1],0];
    def noc(self):
        cnt = 0
        for i in range(len(self.dlist)):
            cnt+=self.dlist[i][2]
        return cnt
    def reset(self):
        for i in range(len(self.dlist)):
            self.dlist[i][2] = 1

# player class
class player:
    def __init__(self,a,m):
        self.name = a
        self.clist = []
        self.money = m
        self.status = 0
    def take(self,l):
        self.clist.append(l)
    def setmoney(self,m):
        self.money+=m
    def showcards(self):
        for i in range(len(self.clist)):
            print self.clist[i]
    def getlastcard(self):
        return self.clist[len(self.clist)-1][1]
    def getcards(self):
        return self.clist
    def getmoney(self):
        return self.money
    def clearcards(self):
        self.clist = []
    def move(self,m):
        # if player folds, status becomes 1
        self.status = m
    def getstatus(self):
        return self.status

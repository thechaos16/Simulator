# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:03:46 2016

@author: thech
"""
import numpy as np

# card class
class Cards:
    def __init__(self):
        random_number = np.random.randint(1,10)
        self.num = random_number
    def get_card(self):
        return self.num

# deck class
class Deck:
    def __init__(self,number_of_player):
        self.number_of_player = number_of_player
        self.deck_list = []
        self.checker = 0
    def set_deck(self):
        for i in range(1,11):
            self.deck_list.append([i,self.number_of_player])
    def get_deck(self):
        return self.deck_list
    def deal(self):
        card_from_deck = Cards()
        dealed_card = card_from_deck.getcard()
        if [dealed_card,0] in self.deck_list:
            #print "it has been dealed_card"
            return self.deal()
        else:
            #print "The card " + dealed_card[1] + " " + dealed_card[0]+" has been dealed_card"
            for i in range(self.p+1):
                if [dealed_card,i] in self.deck_list:
                    self.deck_list[self.deck_list.index([dealed_card,i])] = [dealed_card,i-1]
                    break
            return dealed_card
    def deck_result(self):
        res = []
        for i in range(len(self.deck_list)):
            for j in range(self.deck_list[i][1]):
                res.append(self.deck_list[i][0])
        return res

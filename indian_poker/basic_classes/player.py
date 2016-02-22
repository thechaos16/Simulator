# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:12:31 2016

@author: thech
"""
# player class
class Player:
    def __init__(self,name,money,strategy = '1'):
        self.name = name
        self.card = 0
        self.money = money
        self.status = 0
        self.strategy = strategy
    def take(self,l):
        self.card = l
    def set_money(self,m):
        self.money+=m
    def show_cards(self):
        print(self.card)
    def get_cards(self):
        return self.card
    def fold(self):
        self.card = -1
    def get_money(self):
        return self.money
    def clear_cards(self):
        self.card = 0
    def move(self,player_move,bet):
        # if player folds, status becomes 1
        self.status = player_move
        if not self.status:
            self.bet(bet)
    def bet(self,money):
        self.money-=money
    def get_status(self):
        return self.status
    def get_name(self):
        return self.name
        
    def next_move(self,opp_num,betting_odd):
        ## filled in after ai is developed
        pass
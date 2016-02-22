# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:16:01 2016

@author: thech
"""

import sys
try:
    import basic_classes.deck as deck
except ImportError:
    sys.path.append('../')
import basic_classes.player as player

class Game:
    def __init__(self,money=10):
        self.deck = deck.Deck(2)
        self.deck.set_deck()
        self.player1 = player.Player('player1',money)
        self.player2 = player.Player('player2',money)
        
    def deal(self):
        card = self.deck.deal()
        return card
    
    def poker_play(self):
        while True:
            ## terminal conditions
            cur_deck = self.deck.deck_result()
            if cur_deck==0:
                # self.deck.set_deck()
                break
            ## bankrupt
            if self.player1.get_money()<0:
                print(self.player1.get_name() + ' has been bankrupt!')
                break            
            if self.player2.get_money()<0:
                print(self.player2.get_name() + ' has been bankrupt!')
                break
            
            ## deal card
            self.player1.take(self.deck.deal())
            self.player2.take(self.deck.deal())
            
            ## bet
            checker = 0
            betting_odd = [0,0]
            ## will be replaced by AI
            while True:
                ## until betting is done by either call or fold
                break
        
            ## result handler
            if self.player1.get_cards() > self.player2.get_cards():
                self.player1.set_money(betting_odd[1])
                self.player2.set_money(-betting_odd[1])
            elif self.player2.get_cards() > self.player1.get_cards():
                self.player2.set_money(betting_odd[0])
                self.player1.set_money(-betting_odd[0])           
            
        ## final
        if self.player1.get_money()>self.player2.getmoney():
            print(self.player1.get_name() + ' wins!')            
        elif self.player2.get_money()>self.player1.getmoney():
            print(self.player2.get_name() + ' wins!')
        else:
            print('Tie!')
        
    
if __name__=='__main__':
    game = Game()
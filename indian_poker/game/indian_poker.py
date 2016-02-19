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
        self.player1 = player.Player('player1',money)
        self.player2 = player.Player('player2',money)
        
    def deal(self):
        pass
    
    
if __name__=='__main__':
    game = Game()
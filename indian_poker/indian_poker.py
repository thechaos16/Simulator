# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 23:44:57 2016

@author: thech
"""

import basic_classes.deck as deck
import basic_classes.player as player

class Game():
    def __init__(self,player1,player2):
        self.deck = deck.Deck(2)
        self.player1 = player.Player(player1['name'],player1['money'])
        self.player2 = player.Player(player1['name'],player1['money'])
        
    def game_play(self):
        while True:
            ## if the deck is empty, refill it
            if len(self.deck.deck_result())==0:
                self.refill_deck()
            
            ## termination condition
            if self.player1.get_money()<=0:
                print(self.player1.get_name() + ' has been bankrupt!')
                break
            if self.player2.get_money()<=0:
                print(self.player2.get_name() + ' has been bankrupt!')
                break
            
            ## deal cards
            self.player1.take(self.deck.deal())
            self.player2.take(self.deck.deal())
            
            ## bet
            cur_bet = 0
            sum_bet = 0
            winning_player = None
            while True:
                p1_bet = self.bet(cur_bet,self.player1,self.player2.show_cards())
                if p1_bet==-1:
                    winning_player = self.player2
                sum_bet+=p1_bet
                self.player1.set_money(-p1_bet)
                if p1_bet==cur_bet:
                    if cur_bet!=0:
                        break
                cur_bet = max(p1_bet,cur_bet)
                p2_bet = self.bet(cur_bet,self.player2,self.player1.show_cards())
                if p2_bet==-1:
                    winning_player = self.player1
                self.player2.set_money(-p2_bet)
                sum_bet+=p2_bet
                if p2_bet==cur_bet:
                    break
                cur_bet = max(p2_bet,cur_bet)

            ## check
            if not isinstance(winning_player,player.Player):
                ## show cards
                self.player1.show_cards()
                self.player2.show_cards()
                if self.player1.get_cards()>self.player2.get_cards():
                    print(self.player1.get_name()+ ' won!')
                    self.player1.set_money(sum_bet)
                elif self.player1.get_cards()==self.player2.get_cards():
                    print('Tie!')
                    self.player1.set_money(sum_bet/2)
                    self.player2.set_money(sum_bet/2)
                else:
                    print(self.player2.get_name()+ ' won!')
                    self.player2.set_money(sum_bet)
            else:
                print(winning_player.get_name() + ' won!')
                winning_player.set_money(sum_bet)
            
    
    ## TODO: this should be improved or clarified
    def bet(self,cur_bet,player,opponent_card):
        while True:
            try:
                bet = int(input('betting?'))
            except ValueError:
                print('You should put number!')
            ## fold
            ## TODO: make better rule for fold
            if bet==-1:
                break
            if bet>player.get_money():
                print('Error! you cannot bet more than you have')
            else:
                if bet<cur_bet:
                    print('Error! you should bet more than current bet!')
                else:
                    break
        return bet
    
    def refill_deck(self):
        self.deck.set_deck()
        
if __name__=='__main__':
    game_board = Game({'name':'p1','money':10},{'name':'p2','money':10})
    game_board.game_play()
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:30:59 2016

@author: thech
"""

def decision_maker(cur_deck,opponent_card):
    pass

# conditional probability (p(a|d), a: my card, d: deck)
# output is list of pmf
def my_card_pmf(deck):
    card_pmf = []
    remain = deck.deck_result()
    for i in range(10):
        card_pmf.append(round(float(remain.count(i+1))/float(len(remain)),3))
    return card_pmf

# winning probability
# win/(entire-tie)
def winning_probability(deck,opponent_card):
    remain = deck.deck_result()
    if remain==0:
        return -1
    check = 0
    tie = 0
    for i in range(len(remain)):
        if opponent_card>remain[i]:
            check+=1
        elif opponent_card==remain[i]:
            tie+=1
    return 1-round((float(check)/float(len(remain)-tie)),3)

# predict my card (need to be improved)
def my_card_prediction(deck,opponent_move):
    card_pmf = []
    prior = my_card_pmf(deck)
    for i in range(10):
        # opponent's winning probability based on my cards (unknown)
        temp = winning_probability(deck,i+1)
        # opponent folds
        if opponent_move==0:
            card_pmf.append(round(2*prior[i]*(1-temp),3))
        # opponent bets
        else:
            card_pmf.append(round(2*prior[i]*temp,3))
    return card_pmf

# select my move (d: deck, m: opponent's move, c: opponent's card)
def mmove(d,m,c):
    l = my_card_prediction(d,m)
    res = 0.0
    for i in range(10):
        if i+1-c<0:
            res-=l[i]
        elif i+1-c>0:
            res+=l[i]
    return res
    

if __name__=='__main__':
    pass
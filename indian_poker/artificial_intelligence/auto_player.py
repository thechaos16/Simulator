# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:30:59 2016

@author: thech
"""


# conditional probability (p(a|d), a: my card, d: deck)
def my_card_pdf(deck):
    card_pdf = []
    remain = deck.deck_result()
    for i in range(10):
        card_pdf.append(round(float(remain.count(i+1))/float(len(remain)),3))
    return card_pdf

# winning probability (d: deck in table, c: opponent's card)
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
    card_pdf = []
    prior = my_card_pdf(deck)
    for i in range(10):
        # opponent's winning probability based on my cards (unknown)
        temp = winning_probability(deck,i+1)
        # opponent folds
        if opponent_move==0:
            card_pdf.append(round(2*prior[i]*(1-temp),3))
        # opponent bets
        else:
            card_pdf.append(round(2*prior[i]*temp,3))
    return card_pdf

# function based budget (player, opponent, move of opponent) 
def budget(p,o,m):
    bp = p.getmoney()
    bo = o.getmoney()
    fun = bp*bo*m
    return 0

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
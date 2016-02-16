# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 00:38:41 2016

@author: thech
"""

try:
    import blackjack_util.deck as deck
except ImportError:
    import os,sys
    cur_dir = os.getcwd()
    sys.path.append(os.path.join(cur_dir,'../'))
    import blackjack_util.deck as deck

# dealer's strategy (a : sum of previous cards, b : new card tag(str))
def dealer_hard_strategy(sum_of_previous_cards,new_card):
    score_1 = sum_of_previous_cards+deck.card(new_card,1)
    score_2 = sum_of_previous_cards+deck.card(new_card,2)
    if new_card=='A':
        if score_2<=21:
            if score_2>=17:
                return 'S'
            else:
                return 'H'
        else:
            if score_1>=17:
                return 'S'
            else:
                return 'H'
    else:
        if score_1>=17:
            return 'S'
        else:
            return 'H'

# dealer's strategy (a : cards dealer got) -> soft 17
def dealer_soft_strategy(dealr_instance):
    dealer_card = dealr_instance.get_cards()
    dealer_value = dealr_instance.get_value()
    if dealer_value>=17:
        return 'S'
    ch = 0
    for i in range(len(dealer_card)):
        if dealer_card[i][1] == 'A':
            ch += 1
    if ch==0:
        return 'H'
    else:
        if dealer_value+10>=17 and dealer_value+10<=21:
            dealr_instance.set_value_by_assign(dealer_value+10)
            #print a.value()
            return 'S'
        else:
            return 'H'
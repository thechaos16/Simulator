try:
    import blackjack_util.deck as deck
except ImportError:
    import os,sys
    cur_dir = os.getcwd()
    sys.path.append(os.path.join(cur_dir,'../'))
    import blackjack_util.deck as deck
import blackjack_util.dealer_strategy as ds

# play game (card deck, delaer, players, betting money)
def run(deck_in_table,dealer,player,b):
    ter = 0
    # first two rounds
    r = 1
    dealer.set_value_by_computing()
    for i in range(len(player)):
        player[i].set_value_by_computing()
    while(True):
        if r>2:
            break
        if r==2:
            temp = dealer.get_value()
            dealer.take(deck_in_table.deal())
            # dealer's next move
            #dealer_next_move = dealer(temp,d.getlastcard())
            dealer.set_value_by_computing()
            dealer_next_move = ds.dealer_soft_strategy(dealer)
        else:
            dealer.take(deck_in_table.deal())
            #d.take(['Club','A'])
        for i in range(len(player)):
            player[i].take(deck_in_table.deal())
            player[i].set_value_by_computing()
        #next_move = dealer2(p[0])
        r=r+1

    # black jack!
    if dealer.get_value()==21 or player[0].get_value()==21:
        ter = 1

    # adeck_in_tableitional rounds
    # double checker
    is_double = 0
    while(ter==0):
        #show both cards
        dealer.show_cards(1)
        for i in range(len(player)):
            print("")
            player[i].show_cards(0)

        # determine next moves
        next_move = input("Your moves?")
        if next_move=='H':
            player[0].next_move(deck_in_table.deal())
            player[0].set_value_by_computing()
            #next_move = dealer2(p[0])
            '''if dealer_next_move=='H':
                temp2 = deck_in_table.deal()
                #dealer_next_move = dealer(d.value(),temp2[1])
                d.take(temp2)
                d.set_value_by_computing()
                dealer_next_move = dealer2(d)'''
            if player[0].get_value()>21 or dealer.get_value()>21:
                break
        # when player stay
        elif next_move=='S':
            while(dealer_next_move=='H'):
                temp2 = deck_in_table.deal()
                #dealer_next_move = dealer(d.value(),temp2[1])
                dealer.take(temp2)
                dealer.set_value_by_computing()
                dealer_next_move = ds.dealer_soft_strategy(dealer)
            break
        # when player double
        else:
            is_double = 1
            player[0].next_move(deck_in_table.deal())
            player[0].set_value_by_computing()
            if player[0].get_value()>21:
                break
            while(dealer_next_move=='H'):
                temp2 = deck_in_table.deal()
                dealer.take(temp2)
                dealer.set_value_by_computing()
                dealer_next_move = ds.dealer_soft_strategy(dealer)
            break

    dealer.show_cards(0)
    for i in range(len(player)):
        print("")
        player[i].show_cards(0)
    print("Dealer got " + str(dealer.get_value()) + ", and you got " + str(player[0].get_value()) + ".")
    if player[0].get_value()>21:
        print("Dealer win!")
        player[0].add_money(-b)
        if is_double==1:
            player[0].add_money(-b)
    elif dealer.get_value()>21:
        print("You win!")
        player[0].add_money(b)
        if is_double==1:
            player[0].add_money(b)
    else:
        if dealer.get_value()>player[0].get_value():
            print("Dealer win!")
            player[0].add_money(-b)
            if is_double==1:
                player[0].add_money(-b)
        elif dealer.get_value()==player[0].get_value():
            print("Draw!")
        else:
            print("You win!")
            player[0].add_money(b)
            if is_double==1:
                player[0].add_money(b)
    for i in range(len(player)):
        player[i].clear_cards()
    dealer.clear_cards()


# blackjack simulator
## for now, only one player acceptable
def simulator():
    # number of deck
    number_of_deck = 5
    deck_in_table = deck.Deck(number_of_deck)
    deck_in_table.set_deck()
    # players
    dealer = deck.Player("Dealer",0)
    player = [deck.Player("Player 1",10)]

    # play game
    while(True):
        print(player[0].name + ' has ' +str(player[0].get_money()))
        bet = input("betting money?")
        try:
            betting_integer = int(bet)
        except ValueError:
            raise ValueError('input should be an integer!')
        if betting_integer>player[0].get_money():
            print(player[0].name + ' does not have enough money!')
            continue
        run(deck_in_table,dealer,player,betting_integer)
        continue_input = input("more game?")
        if continue_input.lower()=='n':
            break
        if player[0].get_money()<=0:
            print(player[0].name + ' has been bankrupted!')
            break
        
if __name__=='__main__':
    simulator()


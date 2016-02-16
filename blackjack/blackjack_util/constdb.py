import os,sys
try:
    import blackjack_util.deck as deck
except ImportError:
    cur_dir = os.getcwd()
    sys.path.append(os.path.join(cur_dir,'../'))
    import blackjack_util.deck as deck
import blackjack_util.dealer_strategy as ds

# experiment (d1 : dealer's first card, p1/p2 : player's first/second card, pm : player's move, number_of_deck: number of deck)
# strategies: Hit ('H'), Stay ('S'), Double ('D')
def experi(d1,p1,p2,pm,number_of_deck):
    deck_on_table = deck.Deck(number_of_deck)
    deck_on_table.set_deck()
    dealer = deck.Player("Dealer",0)
    player = deck.Player("Player 1",100)

    # previous setting
    dealer.take(d1)
    player.take(p1)
    player.take(p2)
    deck_on_table.remove_from_deck(d1)
    deck_on_table.remove_from_deck(p1)
    deck_on_table.remove_from_deck(p2)

    # deal new card to dealer
    dealer.take(deck_on_table.deal())
    dealer.set_value_by_computing()
    player.set_value_by_computing()
    dealer_next_move = ds.dealer_soft_strategy(dealer)

    # run
    if pm=='H':
        # player has soft 17 strategy
        kk = 'H'
        while(kk=='H'):
            player.take(deck_on_table.deal())
            player.set_value_by_computing()
            kk = ds.dealer_soft_strategy(player)
    # double
    if pm=='D':
        player.take(deck_on_table.deal())
        player.set_value_by_computing()
        
    while(dealer_next_move=='H'):
        temp2 = deck_on_table.deal()
        dealer.take(temp2)
        dealer.set_value_by_computing()
        dealer_next_move = ds.dealer_soft_strategy(dealer)

    # determine winner
    if player.get_value()>21:
        #print "Dealer win!"
        return 2
    elif dealer.get_value()>21:
        #print "You win!"
        return 0
    else:
        if dealer.get_value()>player.get_value():
            #print "Dealer win!"
            return 2
        elif dealer.get_value()==player.get_value():
            #print "Draw!"
            return 1
        else:
            #print "You win!"
            return 0

def iterative_experiment(a,b,number_of_deck):
    res = [0,0,0]
    for i in range(b):
        temp = experi(a[0],a[1],a[2],a[3],number_of_deck)
        res[temp]+=1
    return res

# convert quiz into actual cards
# assumption: no A for player
def converter(dealer,player):
    if dealer==1:
        dealer_card = ['Heart','A']
    else:
        dealer_card = ['Heart',str(dealer)]
    player_card = []
    for i in range(2,int(player/2)+1):
        if i>10 or player-i>10:
            continue
        temp = []
        temp.append(['Spade',str(i)])
        temp.append(['Spade',str(player-i)])
        player_card.append(temp)
    return [dealer_card,player_card]

# assumption: A for player
def convertera(dealer,player):
    if dealer==1:
        dealer_card = ['Heart','A']
    else:
        dealer_card = ['Heart',str(dealer)]
    player_card = []
    if player<=11:
        temp = []
        temp.append(['Spade','A'])
        if player==2:
            temp.append(['Spade','A'])
        else:
            temp.append(['Spade',str(player-1)])
    else:
        temp = []
        temp.append(['Spade','A'])
        if player==12:
            temp.append(['Spade','A'])
        else:
            temp.append(['Spade',str(player-11)])
    player_card.append(temp)
    return [dealer_card,player_card]

# run experiment (a: dealer upcard, b: sum of player's cards, c: existence of A, number_of_deck: number of decks)
def run_experiment(a,b,c,number_of_deck):
    # test size
    size = 1000
    # result (# of player's win, # of draw, # of dealer's win for hit, stay and double)
    res = [[0,0,0],[0,0,0],[0,0,0]]
    # sample
    if c==0:
        sample = converter(a,b)
    # sample with A for player
    else:
        sample = convertera(a,b)
    for i in range(len(sample[1])):
        temph = iterative_experiment([sample[0],sample[1][i][0],sample[1][i][1],'H'],size,number_of_deck)
        temps = iterative_experiment([sample[0],sample[1][i][0],sample[1][i][1],'S'],size,number_of_deck)
        tempd = iterative_experiment([sample[0],sample[1][i][0],sample[1][i][1],'D'],size,number_of_deck)
        res[0][0]+=temph[0]
        res[0][1]+=temph[1]
        res[0][2]+=temph[2]
        res[1][0]+=temps[0]
        res[1][1]+=temps[1]
        res[1][2]+=temps[2]
        res[2][0]+=tempd[0]
        res[2][1]+=tempd[1]
        res[2][2]+=tempd[2]

        if sample[0][1]=='10':
            for j in range(3):
                res[0][0]+=temph[0]
                res[0][1]+=temph[1]
                res[0][2]+=temph[2]
                res[1][0]+=temps[0]
                res[1][1]+=temps[1]
                res[1][2]+=temps[2]
                res[2][0]+=tempd[0]
                res[2][1]+=tempd[1]
                res[2][2]+=tempd[2]

        if sample[1][i][1][1]=='10':
            for j in range(3):
                res[0][0]+=temph[0]
                res[0][1]+=temph[1]
                res[0][2]+=temph[2]
                res[1][0]+=temps[0]
                res[1][1]+=temps[1]
                res[1][2]+=temps[2]
                res[2][0]+=tempd[0]
                res[2][1]+=tempd[1]
                res[2][2]+=tempd[2]

    return res


# write database
def experiment_result(number_of_deck):
    data = []
    for i in range(1,11):
        for j in range(2,21):
            if j!=2 and j!=3:
                res = run_experiment(i,j,0,number_of_deck)
                data.append([i,j,res])
            res = run_experiment(i,j,1,number_of_deck)
            data.append([i,str(j)+'A',res])
    return data

# txt file
def result_in_text(number_of_deck,text_file = 'db.txt',db_dir = None):
    if db_dir is None:
        cur_dir = os.getcwd()
        db_dir = os.path.join(os.path.split(cur_dir)[0],'db_result')
    data = experiment_result(number_of_deck)
    f = open(os.path.join(db_dir,str(number_of_deck)+'_'+text_file),'w')
    f.write('dealer\tplayer\thit\tstay\tdouble\thit\tstay\tdouble\n')
    for i in range(len(data)):
        f.write(str(data[i][0]))
        f.write('\t')
        f.write(str(data[i][1]))
        f.write('\t')
        f.write(str(round(float(data[i][2][0][0])/float(sum(data[i][2][0])),3)))
        f.write('\t')
        f.write(str(round(float(data[i][2][1][0])/float(sum(data[i][2][1])),3)))
        f.write('\t')
        f.write(str(round(float(data[i][2][2][0])/float(sum(data[i][2][2])),3)))
        f.write('\t')
        f.write(str(data[i][2][0]))
        f.write('\t')
        f.write(str(data[i][2][1]))
        f.write('\t')
        f.write(str(data[i][2][2]))
        f.write('\n')
    f.close()


if __name__=='__main__':
    data = experiment_result(1)
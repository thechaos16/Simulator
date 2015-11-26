import os,sys
import random
import deck

# dictionaries
score = {'2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'J' : 10, 'Q' : 10, 'K' : 10, 'A1' : 1, 'A2' : 11}
dealing = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
dealing2 = {1:'Spade',2:'Diamond',3:'Heart',4:'Club'}

# return value of card
def card(a, b):
    if a=='A':
        if b==1:
            return score['A1']
        else:
            return score['A2']
    else:
        return score[a]

# dealer's strategy (a : sum of previous cards, b : new card tag(str))
def dealer(a, b):
    p1 = a+card(b,1)
    p2 = a+card(b,2)
    if b=='A':
        if p2<=21:
            if p2>=17:
                return 'S'
            else:
                return 'H'
        else:
            if p1>=17:
                return 'S'
            else:
                return 'H'
    else:
        if p1>=17:
            return 'S'
        else:
            return 'H'

# dealer's strategy (a : cards dealer got) -> soft 17
def dealer2(a):
    dcards = a.getcards()
    tempval = a.value()
    if tempval>=17:
        return 'S'
    ch = 0
    for i in range(len(dcards)):
        if dcards[i][1] == 'A':
            ch += 1
    if ch==0:
        return 'H'
    else:
        if tempval+10>=17 and tempval+10<=21:
            a.setvalue2(tempval+10)
            #print a.value()
            return 'S'
        else:
            return 'H'

# experiment (d1 : dealer's first card, p1/p2 : player's first/second card, pm : player's move, nod: number of deck)
# strategies: Hit ('H'), Stay ('S'), Double ('D')
def experi(d1,p1,p2,pm,nod):
    dd = deck.deck(nod)
    dd.setdeck()
    d = deck.player("Dealer",0)
    p = deck.player("Player 1",100)

    # previous setting
    d.take(d1)
    p.take(p1)
    p.take(p2)
    dd.removefromdeck(d1)
    dd.removefromdeck(p1)
    dd.removefromdeck(p2)

    # deal new card to dealer
    d.take(dd.deal())
    d.setvalue()
    p.setvalue()
    dnm = dealer2(d)

    # run
    if pm=='H':
        # player has soft 17 strategy
        kk = 'H'
        while(kk=='H'):
            p.take(dd.deal())
            p.setvalue()
            kk = dealer2(p)
    # double
    if pm=='D':
        p.take(dd.deal())
        p.setvalue()
        
    while(dnm=='H'):
        temp2 = dd.deal()
        d.take(temp2)
        d.setvalue()
        dnm = dealer2(d)
        
    #d.showcards(0)
    #print '\n'
    #p.showcards(0)

    # determine winner
    #print "Dealer got " + str(d.value()) + ", and you got " + str(p.value()) + "."
    if p.value()>21:
        #print "Dealer win!"
        return 2
    elif d.value()>21:
        #print "You win!"
        return 0
    else:
        if d.value()>p.value():
            #print "Dealer win!"
            return 2
        elif d.value()==p.value():
            #print "Draw!"
            return 1
        else:
            #print "You win!"
            return 0

def iterexperi(a,b,nod):
    res = [0,0,0]
    for i in range(b):
        temp = experi(a[0],a[1],a[2],a[3],nod)
        res[temp]+=1
    return res

# convert quiz into actual cards
# assumption: no A for player
def converter(dealer,player):
    if dealer==1:
        dcard = ['Heart','A']
    else:
        dcard = ['Heart',str(dealer)]
    pcard = []
    for i in range(2,player/2+1):
        if i>10 or player-i>10:
            continue
        temp = []
        temp.append(['Spade',str(i)])
        temp.append(['Spade',str(player-i)])
        pcard.append(temp)
    return [dcard,pcard]

# assumption: A for player
def convertera(dealer,player):
    if dealer==1:
        dcard = ['Heart','A']
    else:
        dcard = ['Heart',str(dealer)]
    pcard = []
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
    pcard.append(temp)
    return [dcard,pcard]

# run experiment (a: dealer upcard, b: sum of player's cards, c: existence of A, nod: number of decks)
def runexp(a,b,c,nod):
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
        temph = iterexperi([sample[0],sample[1][i][0],sample[1][i][1],'H'],size,nod)
        temps = iterexperi([sample[0],sample[1][i][0],sample[1][i][1],'S'],size,nod)
        tempd = iterexperi([sample[0],sample[1][i][0],sample[1][i][1],'D'],size,nod)
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
def expres(nod):
    data = []
    for i in range(1,11):
        for j in range(2,21):
            if j!=2 and j!=3:
                res = runexp(i,j,0,nod)
                data.append([i,j,res])
            res = runexp(i,j,1,nod)
            data.append([i,str(j)+'A',res])
    return data

# txt file
def dbtxt(nod):
    data = expres(nod)
    f = file(str(nod)+'db.txt','w')
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

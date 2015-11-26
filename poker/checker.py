import os,sys
import random
import deck

# dictionaries
score = {1:'Royal Straight Flush', 2:'Straight flush', 3:'Four cards', 4:'Full house', 5:'Flush', 6:'Straight', 7:'Triple', 8:'Two pairs', 9:'One pair', 10:'None'}
dealing = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
dealing2 = {1:'Spade',2:'Diamond',3:'Heart',4:'Club'}

# determine if cards set is flush (0: flush, 1: not)
def isflush(card):
    check = 0
    pat = ''
    for i in range(len(card)):
        if pat=='':
            pat = card[i][0]
        else:
            if card[i][0]!=pat:
                check=1
                break
    return check

# determine if cards set is straight (0: straight, 1: not, 2: royal straight)
def isstraight(card):
    check = 0
    arr = []
    for i in range(len(card)):
        if card[i][1]>'0' and card[i][1]<='9':
            arr.append(int(card[i][1]))
        else:
            if card[i][1]=='A':
                arr.append(1)
            elif card[i][1]=='J':
                arr.append(11)
            elif card[i][1]=='Q':
                arr.append(12)
            elif card[i][1]=='K':
                arr.append(13)
    arr.sort()
    for i in range(len(arr)-1):
        if arr[i+1]-arr[i]!=1:
            check=1
            break
    if check==1:
        if arr == [1,10,11,12,13]:
            check=2
    return check

# determine if there is order (0: none, 1: four cards, 2: full house, 3: triple, 4: two pairs, 5: one pair)
def isorder(card):
    arr = []
    noarr = []
    for i in range(len(card)):
        if card[i][1] not in arr:
            arr.append(card[i][1])
            noarr.append(1)
        else:
            noarr[arr.index(card[i][1])]+=1

    # four cards
    if 4 in noarr:
        return 1
    # full house
    if 3 in noarr and 2 in noarr:
        return 2
    # triple
    if 3 in noarr:
        return 3
    # two pairs
    if 2 in noarr and len(noarr)==3:
        return 4
    # one pair
    if 2 in noarr:
        return 5
    # none
    return 0

# define order of cards set
def order(card):
    # exception
    if len(card)!=5:
        print "error!"
        return -1
    # Royal straight flush
    if isflush(card)==0 and isstraight(card)==2:
        return 1
    # Straight flush
    elif isflush(card)==0 and isstraight(card)==0:
        return 2
    # Four cards
    elif isorder(card)==1:
        return 3
    # Full house
    elif isorder(card)==2:
        return 4
    # Flush
    elif isflush(card)==0:
        return 5
    # Straight
    elif isstraight(card)==0:
        return 6
    # Triple
    elif isorder(card)==3:
        return 7
    # Two pairs
    elif isorder(card)==4:
        return 8
    # One pair
    elif isorder(card)==5:
        return 9
    # None
    else:
        return 10


# return sorted array
def sortcard(card):
    arr = []
    for i in range(len(card)):
        if card[i][1]>'0' and card[i][1]<='9':
            arr.append(int(card[i][1]))
        else:
            if card[i][1]=='A':
                arr.append(14)
            elif card[i][1]=='J':
                arr.append(11)
            elif card[i][1]=='Q':
                arr.append(12)
            elif card[i][1]=='K':
                arr.append(13)
    arr.sort()
    return arr

# return most member of list
def pop(li):
    mem = []
    nom = []
    # buffer
    nom2 = []
    for i in range(len(li)):
        if li[i] not in mem:
            mem.append(li[i])
            nom.append(1)
            nom2.append(1)
        else:
            nom[mem.index(li[i])]+=1
            nom2[mem.index(li[i])]+=1
    nom2.sort(reverse=True)
    res = []
    if nom2==[4,1] or nom2==[3,2]:
        for i in range(len(nom2)):
            res.append(mem[nom.index(nom2[i])])
    elif nom2==[3,1,1] or nom2==[2,1,1,1]:
        res.append(mem[nom.index(nom2[0])])
        kk = []
        for i in range(len(mem)):
            if mem[i] in res:
                continue
            kk.append(mem[i])
        kk.sort(reverse=True)
        for i in range(len(kk)):
            res.append(kk[i])
    else:
        kk = []
        temp = 0
        for i in range(len(mem)):
            if nom[i]==2:
                kk.append(mem[i])
            else:
                temp = i
        kk.sort(reverse=True)
        for i in range(len(kk)):
            res.append(kk[i])
        res.append(mem[temp])
    return res

# compare two card deck (0: first man win, 1: tie, 2: second man win)
def compete(p):
    #p = [players[0].getcards(),players[1].getcards()]
    o = []
    # get order of each cards
    for i in range(len(p)):
        o.append(order(p[i]))

    #print 'Player 1: '+score[o[0]]
    #print 'Player 2: '+score[o[1]]
    # competition
    if o[0]<o[1]:
        #print 'Player 1 wins!'
        return 0
    elif o[0]>o[1]:
        #print 'Player 2 wins!'
        return 2
    else:
        sortp = [sortcard(p[0]), sortcard(p[1])]
        # Royal Straight Flush
        if o[0]==1:
            #print 'Tie!'
            return 1
        # Straight
        elif o[0]==2 or o[0]==6:
            if sortp[0][4]>sortp[1][4]:
                #print 'Player 1 wins!'
                return 0
            elif sortp[0][4]<sortp[1][4]:
                #print 'Player 2 wins!'
                return 2
            else:
                #print 'Tie!'
                return 1
        # Flush or none
        elif o[0]==3 or o[0]==10:
            check = 0
            for i in range(len(sortp[0])):
                if sortp[0][4-i]>sortp[1][4-i]:
                    #print 'Player 1 wins!'
                    check=1
                    return 0
                elif sortp[0][4-i]<sortp[1][4-i]:
                    #print 'Player 2 wins!'
                    check=1
                    return 2
            if check==0:
                #print 'Tie!'
                return 1
        # Others
        else:
            popp = [pop(sortp[0]),pop(sortp[1])]
            check = 0
            for i in range(len(popp[0])):
                if popp[0][i]>popp[1][i]:
                    #print 'Player 1 wins!'
                    check=1
                    return 0
                elif popp[0][i]<popp[1][i]:
                    #print 'Player 2 wins!'
                    check=1
                    return 2
            if check==0:
                #print 'Tie!'
                return 1

# return combination (0~n-1)
def comb(n,r):
    res = []
    check = 0
    if r==0:
        return [[]]
    elif r==n:
        return [range(n)]
    else:
        if r>n/2:
            r = n-r
            check = 1
        kk = comb(n,r-1)
        for i in range(len(kk)):
            for j in range(n):
                if j not in kk[i]:
                    temp = kk[i]+[j]
                    temp.sort()
                    if check==0:
                        if temp not in res:
                            res.append(temp)
                    else:
                        temp2 = range(n)
                        for k in range(len(temp)):
                            temp2.remove(temp[k])
                        if temp2 not in res:
                            res.append(temp2)
    return res

# extract best 5-draw among 7 cards
def extract(card,n):
    li = comb(len(card),n)
    #initialization
    best = []
    for i in range(len(li[0])):
        best.append(card[li[0][i]])
    for i in range(1,len(li)):
        temp = []
        for j in range(len(li[i])):
            temp.append(card[li[i][j]])
        res = compete([best,temp])
        if res==2:
            for j in range(len(best)):
                best[j] = temp[j]
    return best


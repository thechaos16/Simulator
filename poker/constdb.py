import os,sys
import random
import deck, checker

# dictionaries
score = {1:'Royal Straight Flush', 2:'Straight flush', 3:'Four cards', 4:'Full house', 5:'Flush', 6:'Straight', 7:'Triple', 8:'Two pairs', 9:'One pair', 10:'None'}
dealing = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
dealing2 = {1:'Spade',2:'Diamond',3:'Heart',4:'Club'}


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

# possibile card set for given deck
def cpair(dk,n):
    # remained deck
    rdeck = dk.getdeck()
    # combination (52C2)
    c = comb(52,n)
    # checker
    check = 0
    res = []
    for i in range(len(c)):
        tempres = []
        check=0
        for j in range(len(c[i])):
            if rdeck[c[i][j]][2]==1:
                check+=1
                tempres.append(rdeck[c[i][0]][0:2])
        if check==n:
            res.append(tempres)
    return res

# winning probability estimator (return: win, draw, lose)
def wp(table,p1,dk):
    clist = cpair(dk,2)
    # best five for player
    temp = p1.getcards()
    temp2 = table.getcards()
    for i in range(len(temp)):
        temp2.append(temp[i])
    best = checker.extract(temp2,5)

    # compete to possible opponent cards
    cnt = 0
    # number of draw
    nod = 0
    for i in range(len(clist)):
        temp = clist[i]
        temp2 = table.getcards()
        for j in range(len(temp)):
            temp2.append(temp[j])
        oppbest = checker.extract(temp2,5)
        fight = checker.compete([best,oppbest])
        if fight==0:
            cnt+=1
        elif fight==1:
            nod+=1
    return [cnt,nod,len(clist)-cnt-nod]

# simulator
def constdb():    
    # define deck
    dk = deck.deck(1)
    dk.setdeck()

    # define table & player
    p = [deck.player('table',0)]
    p.append(deck.player('player',100))

    # all possible card set for table
    tclist = cpair(dk,5)

    # file
    f = file('holdem_db.txt','w')
    f.write('tcard1\ttcard2\ttcard3\ttcard4\ttcard5\tpcard1\tpcard2\twin\tdraw\tlose\n')
    f.close()

    # run
'''    for i in range(len(tclist)):
        dk.reset()
        for j in range(len(tclist[i])):
            dk.removefromdeck(tclist[i][j])
            p[0].take(tclist[i][j])
            #write data
            f.write(tclist[i][j][0]+' '+tclist[i][j][1]+'\t')
        # all possible pair for player
        plist = cpair(dk,2)
        for j in range(len(plist)):
            dk.removefromdeck(plist[j][0])
            dk.removefromdeck(plist[j][1])
            p[1].take(plist[j][0])
            p[1].take(plist[j][1])
            #write data
            f.write(plist[j][0][0]+' '+plist[j][0][1]+'\t')
            f.write(plist[j][1][0]+' '+plist[j][1][1]+'\t')
            # winning probability result
            res = wp(p[0],p[1],dk)
            #write data
            f.write(str(res[0])+'\t'+str(res[1])+'\t'+str(res[2])+'\n')

    f.close()'''

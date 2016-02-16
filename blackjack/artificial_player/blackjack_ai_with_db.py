import os,sys
try:
    import blackjack_util.deck as deck
except ImportError:
    cur_dir = os.getcwd()
    sys.path.append(os.path.join(cur_dir,'../'))
    import blackjack_util.deck as deck
import blackjack_util.dealer_strategy as ds
import simulator.blackjack as bj

class BlackjackAIWithDB:
    def __init__(self,db_dir):
        pass
# artificial intelligence (naive version)
def AI(sit,dbres):
    res = ['H','S','D']
    dvalue = sit[0][1]
    if dvalue=='A':
        dvalue = 1
    if dvalue=='J' or dvalue=='Q' or dvalue=='K':
        dvalue = 10
    pvalue = sit[2]
    #print dvalue, pvalue
    # check if player has Ace
    temp = 0
    for i in range(len(sit[1])):
        if sit[1][i][1]=='A':
            temp = 1
    for i in range(len(dbres)):
        if int(dvalue)==int(dbres[i][0]):
            if temp==0:
                if 'A' not in dbres[i][1]:
                    if int(dbres[i][1])==int(pvalue):
                        return res[int(dbres[i][2])]
            else:
                if 'A' in dbres[i][1]:
                    if int(dbres[i][1][0:len(dbres[i][1])-1])==int(pvalue):
                        return res[int(dbres[i][2])]

# read database (select strategy with biggest winning probability)
def db(nod):
    f = open(str(nod)+'db.txt','r')
    data = []
    for line in f:
        if line[0]=='d':
            continue
        l = line.split('\t')
        temp = 0.0
        tempind = 0
        for i in range(2,5):
            if float(l[i])>temp:
                tempind = i-2
                temp = float(l[i])
        temp2 = [l[0],l[1],tempind]
        data.append(temp2)        
    return data

# read raw DB
def dbraw(nod):
    f = open(str(nod)+'db.txt','r')
    data = []
    for line in f:
        if line[0]=='d':
            continue
        l = line.split('\t')
        temp = [l[0],l[1]]
        check = 0
        for i in range(5,8):
            l[i] = l[i].strip('\n')
            l[i] = l[i].strip('[')
            l[i] = l[i].strip(']')
            temp2 = l[i].split(', ')
            for j in range(len(temp2)):
                check+=int(temp2[j])
            temp.append(temp2[0])
        temp.append(str(check/3))
        data.append(temp)
    return data
    
# full result (n: # of trial, a: target, nod: number of deck)
def itisim(n,a,nod):
    res = 0
    for i in range(n):
        temp = simulator(a,nod)
        res+=temp
    # number of winning trial
    return res


## sample run
if __name__=='__main__':
    pass
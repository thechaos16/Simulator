import numpy.random as random

# dictionaries
score = {'2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'J' : 10, 'Q' : 10, 'K' : 10, 'A1' : 1, 'A2' : 11}
dealing = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
dealing2 = {1:'Spade',2:'Diamond',3:'Heart',4:'Club'}

# return value of card
def card(key, only_for_ace):
    if key=='A':
        if only_for_ace==1:
            return score['A1']
        else:
            return score['A2']
    else:
        return score[key]

# card class
class Cards:
    def __init__(self):
        pass

    def get_specific_card(self,number,pattern):
        return [dealing[number],dealing2[pattern]]
    
    # get random cards
    def get_random_card(self):
        random_for_number = random.randint(1,13)
        random_for_pattern = random.randint(1,4)
        num = dealing[random_for_number]
        pattern = dealing2[random_for_pattern]
        return [num,pattern]

# deck class
class Deck:
    def __init__(self,number_of_deck):
        self.number_of_deck = number_of_deck
        self.cards_in_deck = []
        self.checker = 0
    def set_deck(self):
        for i in range(1,5):
            for j in range(1,14):
                # p cards in the deck
                # p : number of deck
                self.cards_in_deck.append([dealing2[i],dealing[j],self.number_of_deck])
    def get_deck(self):
        return self.cards_in_deck
    def deal(self):
        if self.checker<52*self.number_of_deck:
            dealed_card = Cards()
            dealed = dealed_card.get_random_card()
            if [dealed[1],dealed[0],0] in self.cards_in_deck:
                #print "it has been dealed"
                return self.deal()
            else:
                #print "The card " + dealed[1] + " " + dealed[0]+" has been dealed"
                for i in range(self.number_of_deck+1):
                    if [dealed[1],dealed[0],i] in self.cards_in_deck:
                        self.cards_in_deck[self.cards_in_deck.index([dealed[1],dealed[0],i])] = [dealed[1],dealed[0],i-1]
                        break
                self.checker = self.checker+1
                return [dealed[1],dealed[0]]
        # refresh the deck
        else:
            self.cards_in_deck = []
            self.set_deck()
            self.checker=0
            return self.deal()
    def remove_from_deck(self,card_info):
        [card_num,card_pattern] = card_info
        if [card_num,card_pattern,1] in self.cards_in_deck:
            self.cards_in_deck[self.cards_in_deck.index([card_num,card_pattern,1])] = [card_num,card_pattern,0];
    ##???????
    def add_to_deck(self,card_info):
        [card_num,card_pattern] = card_info
        for i in range(self.number_of_deck+1):
            if [card_num,card_pattern,i] in self.cards_in_deck:
                self.cards_in_deck[self.cards_in_deck.index([card_num,card_pattern,i])] = [dealed[1],dealed[0],i+1]
                break

# player class
class Player:
    def __init__(self,name,money):
        self.name = name
        self.card_list = []
        self.money = money
    def take(self,l):
        self.card_list.append(l)
    def set_value_by_computing(self):
        self.val = 0
        is_ace = False
        for i in range(len(self.card_list)):
            if self.card_list[i][1] == 'A':
                is_ace=True
            self.val+=card(self.card_list[i][1],1)
        if is_ace:
            if self.val+10<=21:
                self.val+=10
    def set_value_by_assign(self,value_input):
        self.val = value_input
    def add_money(self,income):
        self.money+=income
    def get_value(self):
        return self.val
    def show_cards(self,t):
        for i in range(t,len(self.card_list)):
            print(self.card_list[i])
    def next_move(self,new_card):
        self.take(new_card)
    def get_last_card(self):
        return self.card_list[len(self.card_list)-1][1]
    def get_cards(self):
        return self.card_list
    def get_money(self):
        return self.money
    def clear_cards(self):
        self.card_list = []

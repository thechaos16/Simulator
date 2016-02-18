import os,sys
try:
    import blackjack_util.deck as deck
except ImportError:
    cur_dir = os.getcwd()
    sys.path.append(os.path.join(cur_dir,'../'))
    import blackjack_util.deck as deck
import blackjack_util.dealer_strategy as ds
import simulator.blackjack as bj
import numpy as np

class BlackjackAIWithDB:
    def __init__(self,db_dir,money_at_first=100):
        ## check validity
        if not os.path.isdir(db_dir):
            raise FileNotFoundError(db_dir + ' does not exist!')
        self.db_dir = db_dir
        ## initialize
        self.initialize(money_at_first)
        
    def initialize(self,money_at_first):
        self.cur_condition = None
        self.money = money_at_first
        self.database = {}
        self.read_database()
    
    ## curr_cards format: {player:['S5','C3'],dealer:['S10']}    
    def play_blackjack(self,curr_cards):
        key = self.get_db_key_from_cards(curr_cards)
        cur_probability = self.database[1][key]
        print(cur_probability)
        
    
    ## percentage based
    def read_database(self):
        db_files = os.listdir(self.db_dir)
        for file in db_files:
            cur_number_of_deck = int(file.split('db')[0])
            temp_data = {}
            temp_file = open(os.path.join(self.db_dir,file))
            ## header parser
            header = temp_file.readline().strip('\n').split('\t')
            for line in temp_file:
                line_list = line.split('\t')
                line_data = {}
                for i in range(2,5):
                    line_data[header[i]] = line_list[i]
                temp_data[','.join(line_list[:2])] = line_data  
            temp_file.close()
            self.database[cur_number_of_deck] = temp_data
        
    def get_database(self):
        return self.database
        
    def get_db_key_from_cards(self,curr_cards):
        dealer_card = curr_cards['dealer']
        player_cards = curr_cards['player']
        dealer_number = int(dealer_card[0][1:]) if dealer_card[0][1]!='A' else 1
        is_ace = False
        player_number = 0
        for card in player_cards:
            if card[1]=='A':
                player_number+=1
                is_ace = True
            else:
                player_number+=int(card[1])
        key = str(dealer_number)+','+str(player_number)
        if is_ace:
            key+='A'
        return key

## sample run
if __name__=='__main__':
    ai_instance = BlackjackAIWithDB('../db_result')
from cards import Card, GroupOfCards, Deck, Hand



class HandAnalyzer:
    def __init__(self, hand):
        self.hand = hand
         #should already be sorted but will sort again just in case
        #self.hand.sort_cards()
        #must be 14 to account for A being 1
        self.count_list = [0] * 14
        self.unique_card_dict = {}
        self.hand_type = 0

    def analyze(self):
        is_flush = self.check_hand()
        num_unique = len(self.unique_card_dict)

        if not is_flush:
            if num_unique == 2:
                if self.check_matches(4):
                    self.hand_type = 7
                else:
                    self.hand_type = 6
            if num_unique == 3:
                if self.check_matches(3):
                    self.hand_type = 3
                else:
                    self.hand_type = 2
            elif num_unique == 4:
                if self.check_pair_rank():
                    self.hand_type = 1

        if num_unique == 5:
            is_straight = self.check_straight()
            if is_straight == 0 and is_flush:
                self.hand_type = 8
            elif is_straight == 1 and is_flush:
                self.hand_type = 9
            elif is_straight == 0 or is_straight == 1:
                self.hand_type = 4
            elif is_flush:
                self.hand_type = 5


    def check_hand(self):
        is_flush = True
        suit = self.hand.get_cards()[0].get_suit()
        for c in self.hand.get_cards():
            self.count_list[c.get_num()] += 1
            self.unique_card_dict[c.get_num()] = self.count_list[c.get_num()]
            if c.get_suit() != suit:
                is_flush = False

        return is_flush

    def check_matches(self, matches):
        found = False
        for x in self.unique_card_dict:
            if self.unique_card_dict[x] == matches:
                found = True
        return found

    #will return 0 for normal straight, 1 for royal straight, -1 for none
    #NEED TO FIX
    def check_straight(self):
        diff = self.hand.get_cards()[4].get_num() - self.hand.get_cards()[0].get_num()
        if diff == 4:
            return 0
        elif diff == 12:
            if self.hand.get_cards()[1].get_num() == 10:
                return 1
        return -1

    def check_pair_rank(self):
        i = 0
        found = False
        while i < len(self.count_list) and not found:
            if self.count_list[i] == 2:
                found = True
            i += 1

        return i == 2 or i >= 12



    def get_hand_type(self):
        return self.hand_type
    #def print_hand_type(self):
        #print(hand_dict[self.hand_type])




"""Spring 2020 Physics 77 Group 8 Final Project, Basic strategy player"""
""" This py file simulates the behavior of a basic strategy player"""

"""Spring 2020 Physics 77 Group 8 Final Project, Blackjack"""
import math
import Player
import numpy as np
import Deck


# continue_hardpoint_hit = np.array([[1,1,1,1,1,1,1,1,1,1],
# [1,1,1,1,1,1,1,1,1,1],
# [1,1,1,1,1,1,1,1,1,1],
# [1,1,1,1,1,1,1,1,1,1],
# [1,1,2,2,2,1,1,1,1,1],
# [2,2,2,2,2,1,1,1,1,1],
# [2,2,2,2,2,1,1,1,1,1],
# [2,2,2,2,2,1,1,1,1,1],
# [2,2,2,2,2,1,1,1,1,1],
# [2,2,2,2,2,2,2,2,2,2]])

# continue_softpoint_hit = np.array([[1,1,1,1,1,1,1,1,1,1],  #13 soft point
# [1,1,1,1,1,1,1,1,1,1],
# [1,1,1,1,1,1,1,1,1,1],
# [1,1,1,1,1,1,1,1,1,1],
# [1,1,1,1,1,1,1,1,1,1],
# [2,2,2,2,2,2,2,1,1,1],
# [2,2,2,2,2,2,2,2,2,2]]) #19 soft point


class player:

    def __init__(self, money):
        # 1/hit, 2/stand 3/double 4/split Those three matrixes has all the strategi
        # column : dealer's hand        2 3 4 5 6 7 8 9 T A
        # if H-L index is above that number, hit, otherwise stand, -999 == must hit, 999 == must stand
        self.hardpoint_strategy = np.array(
            [[999, 999, 999, 999, 999, 999, 999, 999, 999, 999],  # 9 hard point
             [999, 999, 999, 999, 999, 999, 999, 999, 999, 999],  # 10 hard point
             [999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
             [14, 6, 2, -1, 0, 999, 999, 999, 999, 999],
             [1, -2, -5, -9, -8, 50, 999, 999, 999, 999],
             [-5, -8, -13, -17, -17, 20, 38, -999, -999, -999],
             [-12, -17, -21, -26, -28, 13, 15, 12, 8, 16],
             [-21, -25, -30, -34, -35, 10, 11, 6, 0, 14],
             [-999, -999, -999, -999, -999, -999, -999, -999, -999, -15],
             [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999]  # 18 hard point
             ])
        # if H-L index is above that number, hit, otherwise stand, -999 == must hit, 999 == must stand
        self.softpoint_strategy = np.array(
            [[999, 999, 999, 999, 999, 999, 999, 999, 999, 999],  # 9 hard point
             [999, 999, 999, 999, 999, 999, 999, 999, 999, 999],  # 10 hard point
             [999, 999, 999, 999, 999, 999, 999, 999, 999, -999],
             [14, 6, 2, -1, 0, 999, 999, 999, 999, 999],
             [1, -2, -5, -9, -8, 50, 999, 999, 999, 999],
             [-5, -8, -13, -17, -17, 20, 38, -999, -999, -999],
             [-12, -17, -21, -26, -28, 13, 15, 12, 8, 16],
             [-21, -25, -30, -34, -35, 10, 11, 6, 0, 14],
             [999, 999, 999, 999, 999, 29, 999, 999, 999, 999],  # 17 hard point
             [-999, -999, -999, -999, -999, -999, -999, 999, 12, -6]  # 18 hard point
             ])  # always stand above 19
        # if H-L index is above that number, split, otherwise not split, -999 == must split, 999 == must stand
        self.split_strategy = np.array([[-9, -15, -22, -30, -999, -999, 999, 999, 999, 999],  # 2-2 pair
                                        [-21, -34, -999, -999, -999, -999, 6, 999, 999, 999],
                                        [999, 18, 8, 0, 5, 999, 999, 999, 999, 999],
                                        [999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
                                        [0, -3, -8, -13, -16, -8, 999, 999, 999, 999],
                                        [-22, -29, -35, -999, -999, -999, -999, 999, 999, 999],
                                        [-999, -999, -999, -999, -999, -999, -999, -999, 24, -18],
                                        [-3, -8, -10, -15, -14, 8, -16, -22, 999, 10],
                                        [25, 17, 10, 6, 7, 19, 999, 999, 999, 999],  # T-T pair
                                        [-999, -999, -999, -999, -999, -33, -24, -22, -20, -17]])  # A-A pair
        self.hardpoint_double = np.array([
            [999, 999, 999, 999, 999, 999, 999, 999, 999, 999],  # 4 hard points never double
            [999, 999, 999, 20, 26, 999, 999, 999, 999, 999],  # 5 hard points
            [999, 999, 27, 18, 24, 999, 999, 999, 999, 999],
            [999, 45, 21, 14, 17, 999, 999, 999, 999, 999],
            [999, 22, 11, 5, 5, 22, 999, 999, 999, 999],
            [3, 0, -5, -10, -12, 4, 14, 999, 999, 999],
            [-15, -17, -21, -24, -26, -17, -9, -3, 7, 6],
            [-23, -26, -29, -33, -35, -26, -16, -10, -9, -3]  # 11 hard points , never double above 12
        ])

        self.softpoint_double = np.array([
            [999, 10, 2, -19, -13, 999, 999, 999, 999, 999],  # A-2
            [999, 11, -3, -13, -19, 999, 999, 999, 999, 999],  # A-3
            [999, 19, -7, -16, -23, 999, 999, 999, 999, 999],
            [999, 21, -6, -16, -32, 999, 999, 999, 999, 999],
            [1, -6, -14, -28, -30, 999, 999, 999, 999, 999],
            # A-6 versus dealer's 2 is a special case, only db when index b/w 1-10
            [999, -2, -15, -18, -23, 999, 999, 999, 999, 999],
            [999, 9, 5, 1, 0, 999, 999, 999, 999, 999],
            [999, 20, 12, 8, 8, 999, 999, 999, 999, 999]  # A-9 case.
        ])

        self.starting_fund = money
        self.hand = []
        self.split_hand = []
        self.money = money
        self.dealer = False
        self.split = False
        self.bet = 0
        self.split_bet = 0
        self.insured = False
        self.double_hand = False
        self.double_split_hand = False
        self.is_stand = False
        self.is_split_stand = False
        self.is_hit = True
        self.is_split_hit = True
        self.turns = 0
        self.card_points = 0
        self.high_low_index = 0

    def player_decide_split(self, player, dealer):
        """
        This function tells the AI to split or not.
        """
        # special cases
        if player.sum_hand == 16 and dealer.hand[0].value == 10:
            if player.high_low_index < 24:
                action = 4
                return action
            else:
                intent = player.player_decide_double(player, dealer)
                return intent
        if player.sum_hand == 6 and dealer.hand[0].value == 8:
            if player.high_low_index < -2 or player.high_low_index > 6:
                action = 4
                return action
            else:
                intent = player.player_decide_double(player, dealer)
                return intent
        # general cases
        if player.high_low_index > self.split_strategy[player.hand[0].value - 2, dealer.hand[0].value - 2]:
            action = '4'  # split
            return action
        # if decide not split, then consider double
        else:
            intent = player.player_decide_double(player, dealer)
            return intent
    def player_decide_double(self, player, dealer):
        '''
        This function tells whether player should double
        '''
        if not self.softness():
            if player.sum_hand() <= 11:
                if self.high_low_index > self.hardpoint_double[player.sum_hand() - 4, dealer.hand[0].value - 2]:
                    action = '3'
                    return action
                else:
                    # if player not double, then decide whether to hit
                    intent = player.player_decide_hit(player, dealer)
                    return intent
            else:
                intent = player.player_decide_hit(player, dealer)
                return intent
        else:
            if player.sum_hand() <= 21:
                if player.sum_hand() == 17:
                    if 1 < player.high_low_index < 10: # THe special case
                        action = '3'
                        return action
                    else:
                        intent = player.player_decide_hit(player, dealer)
                        return intent
                if self.high_low_index > self.softpoint_double[player.sum_hand() - 13, dealer.hand[0].value - 2]:
                    action = '3'
                    return action
                else:
                    # if player not double, then decide whether to hit
                    intent = player.player_decide_hit(player, dealer)
                    return intent
            else:
                intent = player.player_decide_hit(player, dealer)
                return intent

    def player_decide_split_double(self, player, dealer):
        '''
        This function allow the player to decide the split hand.
        :param player:
        :param dealer:
        :return:
        '''
        if self.split_softness():
            if player.sum_split_hand() <= 11:
                if self.high_low_index > self.hardpoint_double[player.sum_split_hand() - 4, dealer.hand[0].value - 2]:
                    action = '3'
                    return action
                else:
                    # if player not double, then decide whether to hit
                    intent = player.player_decide_split_hit(player, dealer)
                    return intent
            else:
                intent = player.player_decide_split_hit(player, dealer)
                return intent
        else:
            if player.sum_split_hand() <= 21:
                if player.sum_split_hand() == 17:
                    if 1 < player.high_low_index < 10: # THe special case
                        action = '3'
                        return action
                    else:
                        intent = player.player_decide_hit(player, dealer)
                        return intent
                if self.high_low_index > self.softpoint_double[player.sum_split_hand() - 13, dealer.hand[0].value - 2]:
                    action = '3'
                    return action
                else:
                    # if player not double, then decide whether to hit
                    intent = player.player_decide_split_hit(player, dealer)
                    return intent
            else:
                intent = player.player_decide_split_hit(player, dealer)
                return intent

    def player_decide_hit(self, player, dealer):
        """
        This function tells the AI when to hit
        """
        if not player.softness():  # hard point
            if player.sum_hand() <= 8:
                action = '1'  # always hit
                return action
            elif 8 < player.sum_hand() <= 18:
                if self.high_low_index <= self.hardpoint_strategy[player.sum_hand() - 9, dealer.hand[0].value - 2]:
                    action = '1'
                    return action
                else:
                    action = '2'
                    return action
            else:
                action = '2'  # always stand
                return action
        else:  # soft point
            if player.sum_hand() >= 19:
                action = '2'  # always hit
                return action
            elif player.sum_hand() >= 9 and player.sum_hand() <= 18:
                if self.high_low_index <= self.softpoint_strategy[player.sum_hand() - 9, dealer.hand[0].value - 2]:
                    action = '1'
                    return action
                else:
                    action = '2'
                    return action
            else:
                return '2'

    def player_decide_split_hit(self, player, dealer):
        """
        This function tells the AI when to hit
        """
        if not player.split_softness():  # hard point
            if player.sum_split_hand() <= 8:
                action = '1'  # always hit
                return action
            elif 8 < player.sum_split_hand() <= 18:
                if self.high_low_index <= self.hardpoint_strategy[player.sum_split_hand() - 9, dealer.hand[0].value - 2]:
                    action = '1'
                    return action
                else:
                    action = '2'
                    return action
            else:
                action = '2'  # always stand
                return action
        else:  # soft point
            if player.sum_split_hand() >= 19:
                action = '2'  # always hit
                return action
            elif 9 <= player.sum_split_hand() <= 18:
                if self.high_low_index <= self.softpoint_strategy[player.sum_split_hand() - 9, dealer.hand[0].value - 2]:
                    action = '1'
                    return action
                else:
                    action = '2'
                    return action
            else:
                return '2'

    def is_insurance(self,player):
        """
        This function tells a BSP should never pay insurance! That is the rule!
        """
        if player.high_low_index > 8:
            return "Yes"
        return "No"

    def bet_amount(self):
        """
        This function sets the bet amount each round
        """
        return 2

    def take_out(self, amount):
        """
             amount -- an integer.
             This function takes a certain amount of money out of a player's fund.
             """
        self.money -= amount

    def take_in(self, amount):
        """
         amount -- an integer
         This function gives a certain amount of money to a player.
         """
        self.money += amount

    def print_hand(self):
        """
         This function prints the hand.
         """
        if not self.dealer:
            new_str = "You have a "
        else:
            new_str = "The dealer has a "
        if len(self.hand) == 0:
            new_str = 'You do not have any card.'
        elif len(self.hand) == 1:
            new_str = new_str + str(self.hand[0])
        else:
            new_str = new_str + str(self.hand[0])
            for i in range(1, len(self.hand) - 1):
                new_str = new_str + ', '
                new_str = new_str + str(self.hand[i])
            new_str = new_str + " and a " + str(self.hand[-1])  # The last card

        print(new_str)
        points = self.sum_hand()
        if not self.dealer:
            if points == 21 and len(self.hand) != 2:
                new_str = "Awesome! You have 21 points!"
            else:
                new_str = "You have " + str(points) + " points"
        else:
            new_str = "The dealer has " + str(points) + " points."
        contains_Ace = False
        for card in self.hand:
            if card.face == 'A':
                contains_Ace = True
        if contains_Ace:
            if self.softness():
                new_str = new_str + " And this hand is soft."
            else:
                new_str = new_str + " And this hand is hard."
        print(new_str)

    def softness(self):
        """
         This function takes in a hand and returns True if it is soft, and False
         if it is hard.
         Soft is defined as having at least one card with value 11.
         """
        soft = False
        for card in self.hand:
            if card.value == 11:
                soft = True
        return soft

    def split_softness(self):
        """
         This function takes in a hand and returns True if it is soft, and False
         if it is hard.
         Soft is defined as having at least one card with value 11.
         """
        split_soft = False
        for card in self.split_hand:
            if card.value == 11:
                split_soft = True
        return split_soft

    def print_split_hand(self):
        """
         This function prints the split hand.
         """
        new_str = "You have a "
        if len(self.split_hand) == 0:
            new_str = 'As for the split hand, You do not have any card.'
        elif len(self.split_hand) == 1:
            new_str = new_str + str(self.split_hand[0])
        else:
            new_str = new_str + str(self.split_hand[0])
            for i in range(1, len(self.split_hand) - 1):
                new_str = new_str + ', '
                new_str = new_str + str(self.split_hand[i])
            new_str = new_str + " and a " + str(self.split_hand[-1])  # The last card

        print(new_str)
        points = self.sum_split_hand()
        if self.dealer == False:
            if points == 21 and len(self.hand) != 2:
                new_str = "Awesome! You have 21 points!"
            else:
                new_str = "You have " + str(points) + " points"
        contains_Ace = False
        for card in self.split_hand:
            if card.face == 'A':
                contains_Ace = True
        if contains_Ace:
            if self.split_softness():
                new_str = new_str + " And this hand is soft."
            else:
                new_str = new_str + " And this hand is hard."
        print(new_str)

    def sum_hand(self):
        """
         This function calculates the value of the hand.
         """
        sum = 0
        for card in self.hand:
            sum += card.value
        if sum > 21:
            for card in self.hand:
                if card.value == 11:
                    card.value = 1
                    sum -= 10
        return sum

    def sum_split_hand(self):
        """
         This function calculates the value fo the split sum_hand
         """
        sum_split = 0
        for card in self.split_hand:
            sum_split += card.value
        if sum_split > 21:
            for card in self.split_hand:
                if card.value == 11:
                    card.value = 1
                    sum_split -= 10
        return sum_split

    def busted(self):
        """
         This function determines if the player has busted.
         """
        if self.sum_hand() > 21:
            return True
        return False

    def busted_split_hand(self):
        """
         This function determines if the player's split hand has busted.
         """
        if self.sum_split_hand() > 21:
            return True
        elif self.split_hand == []:
            return True
        # for the convenience of the line 105, because if a player has no second hand,
        # I assume the player lose this hand, without bet.
        return False

    def hit(self, deck):
        """
         This function adds the first card of a deck to a player's hand.
         """
        hit_card = deck.draw()
        self.hand.append(hit_card)
        return hit_card

    def split_hit(self, deck):
        """
         This function adds the first card of a deck to a player's hand.
         """
        hit_split_card = deck.draw()
        self.split_hand.append(hit_split_card)
        return hit_split_card

    def keep_playing(self):
        """
        This function tells when to stop playing
        """
        self.turns = self.turns + 1
        if self.turns > 1000:
            return False
        else:
            return True

    def counting_cards(self,card,deck,player):
        """
        This function allows the player to counting cards
        low point cards are 2,3,4,5,6,7  (+1)
        high point cards are 9, T, A   (-1)
        mid point cards are 8 and 9   (0)
        """
        # counting cards basically counts the cards on the table
        card_num = len(deck.cards)
        if card.face in ['2', '3', '4', '5', '6']:
            player.card_points += 1
        elif card.face in ['10', 'J', 'Q', 'K','A']:
            player.card_points -= 1
        else:
            pass
        player.high_low_index = 100 * player.card_points / card_num
        return player.high_low_index

    def play_bet(self):
        """
        This function tells the AI player the bet amount
        based on the H-L index
        """
        if self.high_low_index <= 3:
            bet = 2
        elif 3 < self.high_low_index <= 5:
            bet = 4
        elif 5 < self.high_low_index <= 7:
            bet = 6
        elif 7 < self.high_low_index <= 9:
            bet = 8
        else:
            bet = 10
            # Do not be to high! Otherwise the casino supervisor will detect that!
        print("The initial bet is ${}".format(bet))
        return bet

    def clear_hand(self):
        """
         This function clears the player's hand.
         """
        """
         I put the original hand and split hand here together.
         I do not know how to type Italic letters here.
         """
        self.bet = 0
        self.split_bet = 0
        self.split = False
        self.insured = False
        self.hand = []
        self.split_hand = []
        self.double_hand = False
        self.double_split_hand = False
        self.is_stand = False
        self.is_split_stand = False
        self.is_hit = False
        self.is_split_hit = False


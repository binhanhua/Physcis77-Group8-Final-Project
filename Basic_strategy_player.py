"""Spring 2020 Physics 77 Group 8 Final Project, Basic strategy player"""
""" This py file simulates the behavior of a basic strategy player"""

"""Spring 2020 Physics 77 Group 8 Final Project, Blackjack"""
import math
import Player
import numpy as np

#continue_hardpoint_hit = np.array([[1,1,1,1,1,1,1,1,1,1],
                                   #[1,1,1,1,1,1,1,1,1,1],
                                   #[1,1,1,1,1,1,1,1,1,1],
                                   #[1,1,1,1,1,1,1,1,1,1],
                                   #[1,1,2,2,2,1,1,1,1,1],
                                   #[2,2,2,2,2,1,1,1,1,1],
                                   #[2,2,2,2,2,1,1,1,1,1],
                                   #[2,2,2,2,2,1,1,1,1,1],
                                   #[2,2,2,2,2,1,1,1,1,1],
                                   #[2,2,2,2,2,2,2,2,2,2]])

#continue_softpoint_hit = np.array([[1,1,1,1,1,1,1,1,1,1],  #13 soft point
                                   #[1,1,1,1,1,1,1,1,1,1],
                                   #[1,1,1,1,1,1,1,1,1,1],
                                   #[1,1,1,1,1,1,1,1,1,1],
                                   #[1,1,1,1,1,1,1,1,1,1],
                                   #[2,2,2,2,2,2,2,1,1,1],
                                   #[2,2,2,2,2,2,2,2,2,2]]) #19 soft point




class player:

    def __init__(self,money):
        # 1/hit, 2/stand 3/double 4/split Those three matrixes has all the strategi
        # column : dealer's hand        2 3 4 5 6 7 8 9 T A                        

        self.hardpoint_strategy = np.array([[1,1,1,1,1,1,1,1,1,1],  #4-8 hard point
                                       [1,3,3,3,3,1,1,1,1,1],  # 9 hard point
                                       [3,3,3,3,3,3,3,3,1,1],
                                       [1,1,2,2,2,1,1,1,1,1],
                                       [2,2,2,2,2,1,1,1,1,1],
                                       [2,2,2,2,2,1,1,1,1,1],
                                       [2,2,2,2,2,1,1,1,1,1],
                                       [2,2,2,2,2,1,1,1,1,1],
                                       [2,2,2,2,2,2,2,2,2,2]]) #17+ hard point

        self.softpoint_strategy = np.array([[1,1,1,3,3,1,1,1,1,1],  #13 soft point
                                       [1,1,1,3,3,1,1,1,1,1],
                                       [1,1,3,3,3,1,1,1,1,1],
                                       [1,1,3,3,3,1,1,1,1,1],
                                       [1,3,3,3,3,1,1,1,1,1],
                                       [2,3,3,3,3,2,2,1,1,1],
                                       [2,2,2,2,2,2,2,2,2,2]]) #19 soft point

        self.split_strategy = np.array([[4,4,4,4,4,4,1,1,1,1],  # 2-2 pair
                                   [4,4,4,4,4,4,1,1,1,1],
                                   [1,1,1,4,4,1,1,1,1,1],
                                   [4,4,4,4,4,1,1,1,1,1],
                                   [4,4,4,4,4,4,1,1,1,1],
                                   [4,4,4,4,4,4,4,4,4,4],
                                   [4,4,4,4,4,4,4,4,4,4],
                                   [4,4,4,4,4,2,4,4,2,2],
                                   [2,2,2,2,2,2,2,2,2,2], # T-T pair
                                   [4,4,4,4,4,4,4,4,4,4]]) # A-A pair



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

    def player_decide_split(self, player, dealer):
        """
        This function tells the AI to split or not.
        """

        if player.hand[0].face == player.hand[1].face:
            action = self.split_strategy[player.hand[0].value-2,dealer.hand[0].value-2]
            action = str(action)
            return action

    def player_decide_hit(self,player,dealer):
        """
        This function tells the AI when to hit
        """
        if not player.softness(): # hard point
            if player.sum_hand() <= 8:
                action = '1' #always hit
                return action
            elif player.sum_hand() > 8 and player.sum_hand() <= 16:
                action = str(self.hardpoint_strategy[player.sum_hand() - 8,dealer.hand[0].value-2])
                return action
            else:
                action = '2' # always stand
                return action
        else: # soft point
            if player.sum_hand() >= 19 :
                action = '2' #always hit
                return action
            elif player.sum_hand() >= 13 and player.sum_hand() <= 18:
                action = str(self.softpoint_strategy[player.sum_hand() - 13,dealer.hand[0].value-2])
                return action


    def player_decide_split_hit(self,player,dealer):
        """
        This function tells the AI when to hit the split hand
        """
        if not player.split_softness(): # hard point
            if player.sum_split_hand() <= 8:
                action = '1' #always hit
                return action
            elif player.sum_split_hand() > 8 and player.sum_split_hand() <= 16:
                action = str(self.hardpoint_strategy[player.sum_split_hand() - 8,dealer.hand[0].value-2])
                return action
            else:
                action = '2' # always stand
                return action
        else: # soft point
            if player.sum_split_hand() >= 19 :
                action = '2' #always hit
                return action
            elif player.sum_split_hand() >= 13 and player.sum_split_hand() <= 18:
                action = str(self.softpoint_strategy[player.sum_split_hand() - 13,dealer.hand[0].value-2])
                return action

    def is_insurance(self):
        """
        This function tells a BSP should never pay insurance! That is the rule!
        """
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
         if self.dealer == False:
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
             new_str = new_str + " and a " + str(self.hand[-1]) #The last card

         print(new_str)
         points = self.sum_hand()
         if self.dealer == False:
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
             new_str = new_str + " and a " + str(self.split_hand[-1]) #The last card

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


    def split_hit(self, deck):
         """
         This function adds the first card of a deck to a player's hand.
         """
         hit_split_card = deck.draw()
         self.split_hand.append(hit_split_card)


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




















































































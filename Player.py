"""Spring 2020 Physics 77 Group 8 Final Project, Blackjack"""
import math
import Deck

class Player:
    """This class creates a player that can enter the game."""

    def __init__(self, money, dealer=False):
        """
        money -- an integer; This is the money this player will start the game with.
        dealer -- a boolean value; This is the indicate if the player is a dealer.
        If the player is a dealer, we assume that the dealer has infinite amount of money.
        """
        self.starting_fund = money
        self.hand = []
        self.split_hand = []
        self.money = money
        self.dealer = dealer
        self.split = False
        self.bet = 0
        self.insured = False
        if self.dealer:
            self.money = math.inf

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
        elif self.dealer == True:
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


    def print_split_hand(self):
        """
        This function prints the hand.
        """
        new_str = "As for the split hand,\nYou have a "
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
        sum = 0
        for card in self.split_hand:
            sum += card.value
        if sum > 21:
            for card in self.hand:
                if card.value == 11:
                    card.value = 1
                    sum -= 10
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
        self.split = False
        self.insured = False
        self.hand = []
        self.split_hand = []

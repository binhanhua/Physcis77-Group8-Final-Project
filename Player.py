"""Spring 2020 Physics 77 Group 8 Final Project, Blackjack"""
import math

class Player(object):
    """This class creates a player that can enter the game."""

    def __init__(self, money, dealer=False):
        """
        money -- an integer; This is the money this player will start the game with.
        dealer -- a boolean value; This is the indicate if the player is a dealer.
        If the player is a dealer, we assume that the dealer has infinite amount of money.
        """
        self.money = money
        self.dealer = dealer
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

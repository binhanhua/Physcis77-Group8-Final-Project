"""Spring 2020 Physics 77 Group 8 Final Project, Blackjack"""

import random

class Card:
    """A single card in a deck"""

    def __init__(self, suit, face):
        """
        Creates a card.
        suit -- a string; 'Spades', 'Hearts', 'Diamonds', or 'Clubs'.
        face -- a string that describes what's shown on the card.
        """
        self.suit = suit
        self.face = face
        if face in ['J', 'Q', 'K']:
            self.value = 10
        elif face == 'A':
            self.value = 11
        else:
            self.value = int(self.face)

    def __str__(self):
        return self.face + " of " + self.suit


class Deck:
    """An entire deck excluding jokers"""

    def __init__(self):
        """
        Create a deck of cards excluding the two jokers.
        """
        self.cards = []
        for suit in ('Spades', 'Hearts', 'Diamonds', 'Clubs'):
            self.cards.append(Card(suit, 'A'))
            for i in range(2, 11):
                self.cards.append(Card(suit, str(i)))
            for face in ('J', 'Q', 'K'):
                self.cards.append(Card(suit, face))


class PlayDeck:
    """An playing deck that is created depending on the number of decks players choose to use"""

    def __init__(self, num):
        """
        num -- a integer; tells how many decks of cards we would use.
        """
        self.cards = []
        for i in range(num):
            self.cards.extend(Deck().cards)

    def draw(self):
        """
        This function removes and returns the first card of the entire deck.
        """
        return self.cards.pop(0)

    def shuffle(self):
        """
        This function shuffles the entire playing deck.
        """
        random.shuffle(self.cards)

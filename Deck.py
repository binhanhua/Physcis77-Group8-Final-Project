"""Spring 2020 Physics 77 Group 8 Final Project, Blackjack"""

import random

class Card(object):
    """A single card in a deck"""

    def __init__(self, suit, face):
        """
        Creates a card.
        suit -- a string; 'Spades', 'Hearts', 'Diamonds', or 'Clubs'.
        face -- a string that describes what's shown on the card.
        """
        self.suit = suit
        self.face = face
        if face == 'Jack' or face == 'Quenn' or face == 'King':
            self.value = 10
        if face == 'Ace':
            self.value = 11
        else:
            self.value = int(self.face)


class Deck(object):
    """An entire deck excluding jokers"""

    def __init__(self):
        """
        Create a deck of cards excluding the two jokers.
        """
        self.deck = []
        for suit in ('Spades', 'Hearts', 'Diamonds', 'Clubs'):
            self.deck.append(Card(suit, 'Ace'))
            for i in range(2, 11):
                self.deck.append(Card(suit, str(i)))
            for face in ('Jack', 'Queen', 'King'):
                self.deck.append(Card(suit, face))


class PlayDeck(object):
    """An playing deck that is created depending on the number of decks players choose to use"""

    def __init__(self, num):
        """
        num -- a integer; tells how many decks of cards we would use.
        """
        self.deck = []
        for i in range(num):
            self.deck.extend(Deck().deck)

    def draw(self):
        """
        This function removes and returns the first card of the entire deck.
        """
        return self.deck.pop(0)

    def shuffle(self):
        """
        This function shuffles the entire playing deck.
        """
        random.shuffle(self.deck)

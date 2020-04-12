"""Spring 2020 Physics 77 Final Project Blackjack"""

import Deck
import Player

MIN_BET = 2
MAX_BET = 200
##############
###Gameplay###
##############
def play():
    """
    I want this function to determine what kind of rules/settings that the player
    wants to play in. From here, we can implement all kinds of different rules.
    For now, I am only creating the most basic difference. I am using the most
    general blackjack rule for the two_decks and four_decks functions
    """
    #Asking for the number of decks the player wants to start with
    deck_num = input('How many decks do you want to play with?\nA. 2 decks\nB. 4 decks\n')

    if deck_num in ['A', 'a']:
        #Asking for the desired starting fund
        money = input('How much money do you want to start with?\nA. 200 dollars\nB. 400 dollars\n')
        if money in ['A', 'a']:
            two_decks(200)
        if money in ['B', 'b']:
            two_decks(400)
        if money not in ['A', 'a', 'B', 'b']:
            print("That's not a choice!")
            play()

    if deck_num in ['B', 'b']:
        #Asking for the desired starting fund
        money = input('How much money do you want to start with?\nA. 200 dollars\nB. 400 dollars\n')
        print(money)
        if money in ['A', 'a']:
            four_decks(200)
        if money in ['B', 'b']:
            four_decks(400)
        if money not in ['A', 'a', 'B', 'b']:
            print("That's not a choice!")
            play()

    #For some reason using else here will run the following code regardless.
    #That's why I used a if ... not in ... to stop this from happening.
    if deck_num not in ['A', 'a', 'B', 'b']:
        print("That's not a choice!")
        play()

def two_decks(num):
    deck = Deck.PlayDeck(2)
    player = Player.Player(num)
    dealer = Player.Player(num, True)
    deck.shuffle()
    print(deck.cards[0].value)


def four_decks(num):
    deck = PlayDeck(4)
    player = Player(num)
    dealer = Player(num, True)
    deck.shuffle()
    print(deck.cards[0].value)

##########
###Main###
##########
name = input("Welcome! What's your name? ")
intent = input("Hello, " + name + "! Do you want to play Blackjack? (Y/N) ")
if intent in ['yes', 'Yes', 'y', 'Y']:
    play()
else:
    print("Oh, that's ok. Come back next time!")

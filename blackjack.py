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
    start_turn(player, dealer, deck)

def four_decks(num):
    deck = PlayDeck(4)
    player = Player(num)
    dealer = Player(num, True)
    deck.shuffle()
    start_turn(player, dealer, deck)

def start_turn(player, dealer, deck):
    """
    This function plays a complete turn of Blackjack
    """
    #If the player runs out of money, the program ends.
    if player.money <= 0:
        print("Sorry " + name + ", you are broke and can no longer play.")
        conclude(player)
        exit()

    bet = bet_amount(player)
    #The player and the dealer take out the same amount of bet.
    player.take_out(bet)
    dealer.take_out(bet)
    print("Burn a card")
    deck.draw()
    print("Dealing the cards")
    player.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
    player.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
    print("The dealer has one card hidden and a " + str(dealer.hand[1]))
    player.print_hand()

    #Player's turn.
    hit(player, deck)

    #Dealer's turn.
    if player.busted():
        print("The dealer wins")
    else:
        print("Onto the dealer now.")
        while dealer.sum_hand() < 17:
            print("The dealer decides to hit.")
            dealer.hit(deck)
            dealer.print_hand()
            if dealer.busted():
                print("The dealer busted. You won this hand!")
                player.money += 2 * bet
                break
            if dealer.sum_hand() >= 17:
                print('The dealer decides to stand.')
                break
        if dealer.busted():
            pass
        else:
            announce(player, dealer, bet)
    print("You now have {} dollars".format(player.money))

    #Ask the player if they want to keep playing
    keep_playing = input('Do you want to keep playing? (Y/N) ')
    if keep_playing in ['yes', 'Yes', 'y', 'Y']:
        player.clear_hand()
        dealer.clear_hand()
        start_turn(player, dealer, deck)
    else:
        conclude(player)
        exit()


def conclude(player):
    """
    This comes at the end of each game and serves as a conclusion of one session.
    """
    print("Thanks for playing!")
    new_str = "You started with " + str(player.starting_fund) + " dollars"
    if player.money == player.starting_fund:
        new_str += " and didn't lose anything. Good job!"
    if player.money < player.starting_fund:
        new_str += " and lost "+ str(player.starting_fund - player.money) + " dollars. Better luck next time."
    if player.money > player.starting_fund:
        new_str += " and won " + str(player.starting_fund - player.money) + " dollars. You're awesome."
    print(new_str)



def announce(player, dealer, bet):
    """
    This function is called at the end of each term where no one has busted.
    This announces who won the turn and adds the money proportionally.
    """
    player_score = player.sum_hand()
    dealer_score = dealer.sum_hand()
    print("The player has a score of {}".format(player_score))
    print("The dealer has a score of {}".format(dealer_score))
    if player_score == dealer_score:
        print("It's a draw!")
        player.money += bet
        dealer.money += bet
    elif player_score > dealer_score:
        print("You won!")
        player.money += 2 * bet
    else:
        print("Dealer wins.")


def hit(player, deck):
    """
    This function utilizes the already implemented hit function in the Player class
    and continues to ask the player until they choose to stop hitting.
    """
    answer = input('Do you want to hit? (Y/N) ')
    if answer in ['yes', 'Yes', 'y', 'Y']:
        hit_card = deck.cards[0]
        print("Your new card is " + str(hit_card))
        player.hit(deck)
        player.print_hand()
        if player.busted():
            print("Sorry, you busted")
        else:
            hit(player, deck)
    else:
        pass


def bet_amount(player):
    """
    This functions determine the amount of bet the player wants to bet and
    account for false inputs
    """
    bet = input("How much do you want to bet? ")
    while not is_int(bet):
        print("The bet must be an integer")
        bet = input("How much do you want to bet? ")
    bet = int(bet)

    #After legal input of bet, determine if the amount of bet is within limits
    #use recursion to force a bet within limit.
    if bet > player.money or bet < MIN_BET or bet > MAX_BET:
        if bet > player.money:
            print('You do not have enough money.')
        elif bet < MIN_BET:
            print('You must bet more.')
        elif bet > MAX_BET:
            print('You must bet less')
        bet = bet_amount(player)

    return bet



def is_int(s):
    """
    This function determines if a string is the string of an integer.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


##########
###Main###
##########
name = input("Welcome! What's your name? ")
intent = input("Hello, " + name + "! Do you want to play Blackjack? (Y/N) ")
if intent in ['yes', 'Yes', 'y', 'Y']:
    play()
else:
    print("Oh, that's ok. Come back next time!")

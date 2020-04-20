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
        if money in ['A', 'a']:
            four_decks(200)
        if money in ['B', 'b']:
            four_decks(400)
        if money not in ['A', 'a', 'B', 'b']:
            print("That's not a choice!")
            play()

    if deck_num not in ['A', 'a', 'B', 'b']:
        print("That's not a choice!")
        play()


def two_decks(num):
    """
    As the name suggests, this function starts the game with two decks of cards.
    """
    deck = Deck.PlayDeck(2)
    player = Player.Player(num)
    dealer = Player.Player(num, True)
    deck.shuffle()
    start_turn(player, dealer, deck)


def four_decks(num):
    """
    As the name suggests, this function starts the game with four decks of cards.
    """
    deck = Deck.PlayDeck(4)
    player = Player.Player(num)
    dealer = Player.Player(num, True)
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

    if len(deck.cards) < 0.25 * 52 * deck.num_of_deck:
        deck.reshuffle()
        print("Plastic card hit. Deck reshuffled.")

    #First deal with the initial bets
    player.bet = bet_amount(player)
    player.take_out(player.bet)

    #Dealing the initial cards
    print("Burn a card")
    deck.draw()
    print("Dealing the cards")
    player.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
    player.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
    print("The dealer has one card hidden and a " + str(dealer.hand[1]))
    player.print_hand()

    #First check everything related to naturals and insurance.
    #natural blackjack for the player

    if dealer.hand[1].value == 11:
        print("The dealer has an Ace faced up.")
        pay_insurance(player)

    if player.sum_hand() == 21:
        print("You hit a natural blackjack!")
        if dealer.sum_hand() < 21:
            dealer.print_hand()
            print("The dealer does not have a blackjack, You won!")
            player.take_in(2.5 * player.bet)
            print("Unfortunately, you cannot get your insurance back")
        elif dealer.sum_hand() == 21:
            dealer.print_hand()
            print("The dealer also has a natural blackjack. It's a tie.")
            player.take_in(player.bet)
            if player.insured:
                print("And you get some insurance money back.")
                player.take_in(1.5 * player.bet)
        else:
            pass

    elif dealer.sum_hand() == 21:
        print("The dealer's hidden card is" + str(dealer.hand[0]))
        print("Oh no, the dealer has a natural blackjack. You lost this turn.")
        if player.insured:
            print("At least you get some insurance money back.")
            player.take_in(1.5 * player.bet)
    # In the following cases, no one has a blackjack.
    else:
        if player.insured:
            print("The dealer does not have a blackjack, game continue.")
        player_turn(player, deck)
        dealer_turn(player, dealer, deck)


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


def pay_insurance(player):
    insurance = 0.5 * player.bet
    intent = input("Do you want to pay $" + str(insurance) + " insurance?(Y/N) ")
    if intent in ['yes', 'Yes', 'y', 'Y']:
        player.take_out(insurance)
        player.insured = True
    else:
        print("You decided not to pay insurance.")


def player_turn(player, deck):
    """
    This function simulates the player's turn
    """
    double_bet(player)
    hit(player, deck)


def double_bet(player):
    """
    This function asks if the player wants to double their bet
    """
    intent = input("Do you want to double your bet? (Y/N) ")
    if intent in ['Yes', 'yes', 'Y', 'y']:
        if player.money < player.bet:
            print("You don't have enough money to double!")
        else:
            player.take_out(player.bet)
            player.bet *= 2
            print("You have doubled your bet. Your bet now is ${}.".format(player.bet))
    else:
        print("You decided not to double.")


def dealer_turn(player, dealer, deck):
    """
    This function simulates the dealer's turn
    """
    # If player busted both hands, then declare the result.
    if player.busted() and player.busted_split_hand():
        print("The dealer wins")
    else:
        print("Onto the dealer now.")
        dealer.print_hand()
        while dealer.sum_hand() < 17:
            print("The dealer decides to hit.")
            dealer.hit(deck)
            dealer.print_hand()
            #When dealer busted, do separately.
            if dealer.busted():
                print("The dealer busted.")
                if player.split:
                    if not player.busted() and not player.busted_split_hand():
                        print("The player won both of the hands")
                        player.money += 4 * player.bet
                    elif player.busted() and not player.busted_split_hand():
                        print("The player won the second hand!")
                        player.money += 2 * player.bet
                    elif not player.busted() and player.busted_split_hand():
                        print("The player won the first hand!")
                        player.money += 2 * player.bet
                else:
                    print("You won this game!")
                    player.money += 2 * player.bet
                break
            if dealer.sum_hand() >= 17:
                print('The dealer decides to stand.')
                break
        if dealer.busted():
            pass
        else:
            announce(player, dealer)


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
        new_str += " and won " + str(player.money - player.starting_fund) + " dollars. You're awesome."
    print(new_str)


def announce(player, dealer):
    """
    This function is called at the end of each term where no one has busted.
    This announces who won the turn and adds the money proportionally.
    """
    # Perhaps it makes nonsense to announce a busted score
    player_score = player.sum_hand()
    if player.split:
        player_split_score = player.sum_split_hand()
    dealer_score = dealer.sum_hand()
    if not player.busted():
        print("The player has a score of {}".format(player_score))
    if player.split:

        if not player.busted_split_hand():
            print("The player split hand has a score of {}".format(player_split_score))
    print("The dealer has a score of {}".format(dealer_score))

    # Here we need to announce separately according to player.split
    if not player.split:
        if player_score == dealer_score:
            print("It's a draw!")
            player.take_in(player.bet)
        elif player_score > dealer_score:
            print("You won!")
            player.take_in(2 * player.bet)
        else:
            print("Dealer wins.")

    else:
        if player_score == dealer_score:
            print("The first hand is a draw!")
            player.take_in(player.bet)
        elif not player.busted() and player_score > dealer_score:
            print("You won the first hand!")
            player.take_in(2 * player.bet)
        else:
            print("Dealer wins the first hand.")

        if player_split_score == dealer_score:
            print("The second hand is a draw!")
            player.take_in(player.bet)
        elif not player.busted_split_hand() and player_split_score > dealer_score:
            print("You won the second hand!")
            player.take_in(2 * player.bet)
        else:
            print("Dealer wins the second hand.")



def hit(player, deck):
    """
    This function utilizes the already implemented hit function in the Player class
    and continues to ask the player until they choose to stop hitting.
    """
    #Ask if the player wants to split here
    if player.hand[0].face == player.hand[1].face:
        split(player, deck)

    if player.split:
        answer = input('Do you want to hit the first hand? (Y/N) ')
        while answer in ['yes', 'Yes', 'y', 'Y']:
            hit_card = deck.cards[0]
            print("Your new card for the first hand is " + str(hit_card))
            player.hit(deck)
            player.print_hand()
            if player.sum_hand() == 21:
                print("Awesome, you made a 21!")
                break
            if player.busted():
                print("Sorry, you busted your first hand")
                break
            answer = input('Do you want to hit the first hand? (Y/N) ')

        print("Onto the second hand now.")

        answer = input('Do you want to hit your second hand? (Y/N) ')
        while answer in ['yes', 'Yes', 'y', 'Y']:
            hit_card = deck.cards[0]
            print("Your new card for the second hand is " + str(hit_card))
            player.split_hit(deck)
            player.print_split_hand()
            if player.sum_split_hand() == 21:
                print("Awesome, you made a 21!")
                break
            if player.busted_split_hand():
                print("Sorry, you busted the second hand")
                break
            answer = input('Do you want to hit the second hand? (Y/N) ')


    else:
        answer = input('Do you want to hit? (Y/N) ')
        while answer in ['yes', 'Yes', 'y', 'Y']:
            hit_card = deck.cards[0]
            print("Your new card is " + str(hit_card))
            player.hit(deck)
            player.print_hand()
            if player.sum_hand() == 21:
                print("Awesome, you made a 21!")
                break
            if player.busted():
                print("Sorry, you busted")
                break
            answer = input('Do you want to hit? (Y/N) ')


def split(player, deck):
    """
    This function asks if the player wants to split the hand and modify the corresponding
    variables in the player's instance.
    """
    intent = input("Do you want to split the cards?")
    if intent in ["Yes", "yes", "Y", "y"]:
        if player.money < player.bet:
            print("Sorry, you don't have enough money to split.")
            pass
        else:
            print("You decided to split")
            #Modify the instance variable
            player.split = True
            if player.hand[0].face == "A":
                # Earlier sum_hand function changes the value of the Ace. Here I change
                # it back when the player wants to split.
                player.hand[0].value = 11
                player.hand[1].value = 11
            #increase the player's bet.
            player.take_out(player.bet)
            #modify the hands
            player.split_hand.append(player.hand.pop(1))
            player.hand.append(deck.draw())
            player.split_hand.append(deck.draw())
            print("In your first hand:")
            player.print_hand()
            print("In your second hand:")
            player.print_split_hand()
    else:
        print("You decided not to split.")


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

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
    # Asking for the number of decks the player wants to start with
    deck_num = input('How many decks do you want to play with?\nA. 2 decks\nB. 4 decks\n')

    if deck_num in ['A', 'a']:
        # Asking for the desired starting fund
        money = input('How much money do you want to start with?\nA. 200 dollars\nB. 400 dollars\n')
        if money in ['A', 'a']:
            two_decks(200)
        if money in ['B', 'b']:
            two_decks(400)
        if money not in ['A', 'a', 'B', 'b']:
            print("That's not a choice!")
            play()

    if deck_num in ['B', 'b']:
        # Asking for the desired starting fund
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
    # If the player runs out of money, the program ends.
    if player.money <= 0:
        print("Sorry " + name + ", you are broke and can no longer play.")
        conclude(player)
        exit()

    if len(deck.cards) < 0.25 * 52 * deck.num_of_deck:
        deck.reshuffle()
        print("Plastic card hit. Deck reshuffled.")

    # First deal with the initial bets
    player.bet = bet_amount(player)
    player.take_out(player.bet)

    # Dealing the initial cards
    print("Burn a card")
    deck.draw()
    print("Dealing the cards")
    player.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
    player.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
    print("The dealer has one card hidden and a " + str(dealer.hand[1]))
    player.print_hand()

    # First check everything related to naturals and insurance.
    # natural blackjack for the player

    if dealer.hand[1].value == 11:
        print("The dealer has an Ace faced up.")
        pay_insurance(player)

    if player.sum_hand() == 21:
        print("You hit a natural blackjack!")
        if dealer.sum_hand() < 21:
            dealer.print_hand()
            print("The dealer does not have a blackjack, You won!")
            player.take_in(2.5 * player.bet)
            if player.insured:
                print("Unfortunately, you cannot get your insurance back")
            print_money(player, dealer, deck)
        elif dealer.sum_hand() == 21:
            dealer.print_hand()
            print("The dealer also has a natural blackjack. It's a tie.")
            player.take_in(player.bet)
            if player.insured:
                print("And you get some insurance money back.")
                player.take_in(1.5 * player.bet)
            print_money(player, dealer, deck)
        else:
            pass

    else:
        if player.insured:
            print("The dealer does not have a blackjack, game continue.")
        player_turn(player, dealer, deck)


def print_money(player, dealer, deck):
    """
    Name says it all! It prints the money of the player, and asks the intention for the next round
    """
    print("You now have {} dollars".format(player.money))

    # Ask the player if they want to keep playing
    keep_playing = input('Do you want to keep playing? (Y/N) ')
    if keep_playing in ['yes', 'Yes', 'y', 'Y']:
        player.clear_hand()
        dealer.clear_hand()
        start_turn(player, dealer, deck)
    else:
        conclude(player)
        exit()


def pay_insurance(player):
    """
    This function pays insurance, only when the player is insured and the dealer has a BJ.
    """
    insurance = 0.5 * player.bet
    intent = input("Do you want to pay $" + str(insurance) + " insurance?(Y/N) ")
    if intent in ['yes', 'Yes', 'y', 'Y']:
        player.take_out(insurance)
        player.insured = True
    else:
        print("You decided not to pay insurance.")


def player_turn(player, dealer, deck):
    """
    This function simulates the player's turn
    """
    if not player.split:
        if player.hand[0].face != player.hand[1].face:
            print("Do you want to hit, stand or double?")
            intent = input("Press 1 to hit, 2 to stand, 3 to double")
            if intent == '4':
                print('That is not a choice!')
                player_turn(player,dealer,deck)
        else:
            print("Do you want to hit, stand, double or split?")
            intent = input("Press 1 to hit, 2 to stand, 3 to double, 4 to split")

        if intent == '1':
            hit(player, dealer, deck)
        elif intent == '2':
            stand(player, dealer, deck)
        elif intent == '3':
            double(player, dealer, deck)
        elif intent == '4':
            split(player, dealer, deck)
        else:
            print("That is not a choice!")
            player_turn(player, dealer, deck)
    else:
        player_first_hand(player, dealer, deck)


def player_first_hand(player, dealer, deck):
    """
    This is how the player deal with the first hand when split.
    """
    print("On to the first hand now")
    if player.sum_hand() == 21:
        print("Congratulations!")
        player_second_hand(player, dealer, deck)
    else:
        print("Do you want to hit, stand or double?")
        intent = input("Press 1 to hit, 2 to stand, 3 to double")
        if intent == '3':
            player.double_hand = True
            double(player, dealer, deck)
        elif intent == '1':
            player.is_hit = True
            hit(player, dealer, deck)
        elif intent == '2':
            player.is_stand = True
            stand(player, dealer, deck)
        else:
            print("That is not a choice!")
            player_first_hand(player, dealer, deck)


def player_second_hand(player, dealer, deck):
    """
    This is how the player deal with the first hand when split.
    """
    print("On to the second hand now")
    print("Do you want to hit, stand or double?")
    intent = input("Press 1 to hit, 2 to stand, 3 to double")
    if intent == '3':
        player.double_split_hand = True
        double(player, dealer, deck)
    elif intent == '1':
        player.is_split_hit = True
        hit(player, dealer, deck)
    elif intent == '2':
        player.is_split_stand = True
        stand(player, dealer, deck)
    else:
        print("That is not a choice!")
        player_second_hand(player, dealer, deck)


def double(player, dealer, deck):
    """
    This function give the player one card and declare the result if he decided to double.
    """
    if not player.split:
        if player.money < player.bet:
            print("You don't have enough money to double!")
            player_turn(player, dealer, deck)
        else:
            print("You have decided to double")
            player.take_out(player.bet)
            player.bet *= 2
            print("You have doubled your bet. Your bet now is ${}.".format(player.bet))
            hit_card = deck.cards[0]
            print("Your new card is " + str(hit_card))
            player.hit(deck)
            player.print_hand()
            if player.busted():
                print("Sorry, you busted")
            else:
                dealer_turn(player, dealer, deck)
    else:
        if player.double_hand:
            print("You have decided to double your first hand")
            player.take_out(player.bet)
            player.bet *= 2
            print("You have doubled your first hand bet. Your bet now is ${}.".format(player.bet))
            hit_card = deck.cards[0]
            print("Your new card is " + str(hit_card))
            player.hit(deck)
            player.print_hand()
            player.double_hand = False
            if player.busted():
                print("Sorry, you busted")
                player_second_hand(player, dealer, deck)
            else:
                # After doubling the first hand, then go to the second hand
                player_second_hand(player, dealer, deck)
        elif player.double_split_hand:
            print("You have decided to double your split hand")
            player.take_out(player.split_bet)
            player.split_bet *= 2
            print("You have doubled your split hand bet. Your bet now is ${}.".format(player.split_bet))
            hit_card = deck.cards[0]
            print("Your new card is " + str(hit_card))
            player.split_hit(deck)
            player.print_split_hand()
            player.double_split_hand = False
            if player.busted_split_hand():
                print("Sorry, you busted")
                dealer_turn(player, dealer, deck)
            else:
                dealer_turn(player, dealer, deck)


def stand(player, dealer, deck):
    '''
    This function activates when the player want to stand
    '''
    # Here I don't classify split or not. If not split, and the player choose to stand
    # This turn automatically goes to the dealer, if split and stand the first hand
    # Then hit function will guide to the second, if stand on the second, then dealer's turn.
    if not player.split:
        print("You decided to stand")
        dealer_turn(player, dealer, deck)
    elif player.is_stand:
        player.is_stand = False
        print("You decided to stand the first hand")
        player_second_hand(player, dealer, deck)
    elif player.is_split_stand:
        player.is_split_stand = False
        print("You decided to stand the second hand")
        dealer_turn(player, dealer, deck)
    else:
        pass


def dealer_turn(player, dealer, deck):
    """
    This function simulates the dealer's turn
    """
    if dealer.sum_hand() == 21:
        print("The dealer's hidden card is " + str(dealer.hand[0]))
        print("Oh no, the dealer has a natural blackjack. You lost this turn.")
        if player.insured:
            print("At least you get some insurance money back.")
            player.take_in(1.5 * player.bet)
        print_money(player, dealer, deck)
    # In the following cases, no one has a blackjack.

    # If player busted both hands, then declare the result.
    if player.busted() and player.busted_split_hand():
        print("The dealer wins")
        print_money(player, dealer, deck)
    else:
        print("Onto the dealer now.")
        dealer.print_hand()
        while dealer.sum_hand() < 17:
            print("The dealer decides to hit.")
            dealer.hit(deck)
            dealer.print_hand()
            # When dealer busted, do separately.
            if dealer.busted():
                print("The dealer busted.")
                if player.split:
                    if not player.busted() and not player.busted_split_hand():
                        print("The player won both of the hands")
                        player.money += 2 * player.bet + 2 * player.split_bet
                        print_money(player, dealer, deck)
                    elif player.busted() and not player.busted_split_hand():
                        print("The player won the second hand!")
                        player.money += 2 * player.split_bet
                        print_money(player, dealer, deck)
                    elif not player.busted() and player.busted_split_hand():
                        print("The player won the first hand!")
                        player.money += 2 * player.bet
                        print_money(player, dealer, deck)
                else:
                    print("You won this game!")
                    player.money += 2 * player.bet
                    print_money(player, dealer, deck)
                break
            if dealer.sum_hand() >= 17:
                print('The dealer decides to stand.')
                break
        if dealer.busted():
            pass
        else:
            announce(player, dealer, deck)


def conclude(player):
    """
    This comes at the end of each game and serves as a conclusion of one session.
    """
    print("Thanks for playing!")
    new_str = "You started with " + str(player.starting_fund) + " dollars"
    if player.money == player.starting_fund:
        new_str += " and didn't lose anything. Good job!"
    if player.money < player.starting_fund:
        new_str += " and lost " + str(player.starting_fund - player.money) + " dollars. Better luck next time."
    if player.money > player.starting_fund:
        new_str += " and won " + str(player.money - player.starting_fund) + " dollars. You're awesome."
    print(new_str)


def announce(player, dealer, deck):
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
        if player.split:
            print("The player's first hand has a score of {}".format(player_score))
        else:
            print("The player's hand has a score of {}".format(player_score))
    if player.split:
        if not player.busted_split_hand():
            print("The player split hand has a score of {}".format(player_split_score))
    print("The dealer has a score of {}".format(dealer_score))

    # Here we need to announce separately according to player.split
    if not player.split:
        if player_score == dealer_score:
            print("It's a draw!")
            player.take_in(player.bet)
        elif player_score > dealer_score and not player.busted():
            print("You won!")
            player.take_in(2 * player.bet)
        else:
            print("Dealer wins.")
        print_money(player, dealer, deck)

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
            player.take_in(2 * player.split_bet)
        else:
            print("Dealer wins the second hand.")
        print_money(player, dealer, deck)


def hit(player, dealer, deck):
    """
    This function utilizes the already implemented hit function in the Player class
    and continues to ask the player until they choose to stop hitting.
    """
    if player.split:
        if player.is_hit:
            answer = '1'
            player.is_hit = False
            while answer == '1':
                hit_card = deck.cards[0]
                print("Your new card for the first hand is " + str(hit_card))
                player.hit(deck)
                player.print_hand()
                if player.sum_hand() == 21:
                    # we do not need to print the exclamation, because it is inside the player function
                    break
                if player.busted():
                    print("Sorry, you busted your first hand")
                    # break the while loop and go to the second
                    break
                answer = input('Press 1 to hit, press any other keys to stand')
            player_second_hand(player, dealer, deck)

        if player.is_split_hit:
            print("Onto the second hand now.")
            answer = '1'
            player.is_split_hit = False
            while answer == '1':
                hit_card = deck.cards[0]
                print("Your new card for the second hand is " + str(hit_card))
                player.split_hit(deck)
                player.print_split_hand()
                if player.sum_split_hand() == 21:
                    dealer_turn(player, dealer, deck)
                if player.busted_split_hand():
                    print("Sorry, you busted the second hand")
                    dealer_turn(player, dealer, deck)
                answer = input('Press 1 to hit, press any other key to stand')
            dealer_turn(player, dealer, deck)


    else:
        answer = '1'
        while answer == '1':
            hit_card = deck.cards[0]
            print("Your new card is " + str(hit_card))
            player.hit(deck)
            player.print_hand()
            if player.sum_hand() == 21:
                # if the player hits 21, Turn to the dealer.
                dealer_turn(player, dealer, deck)
            if player.busted():
                print("Sorry, you busted")
                break
            answer = input('Press 1 to hit, press 2 to stand.')
        dealer_turn(player, dealer, deck)


def split(player, dealer, deck):
    """
    This function asks if the player wants to split the hand and modify the corresponding
    variables in the player's instance.
    """
    if player.money < player.bet:
        print("Sorry, you don't have enough money to split.")
        player_turn(player, dealer, deck)

    print("You decided to split")
    player.split = True
    player.split_bet = player.bet
    if player.hand[0].face == "A":
        # Earlier sum_hand function changes the value of the Ace. Here I change
        # it back when the player wants to split.
        player.hand[0].value = 11
        player.hand[1].value = 11
    # increase the player's bet.
    player.take_out(player.split_bet)
    # modify the hands
    player.split_hand.append(player.hand.pop(1))
    player.hand.append(deck.draw())
    player.split_hand.append(deck.draw())
    print("In your first hand:")
    player.print_hand()
    print("In your second hand:")
    player.print_split_hand()
    player_turn(player, dealer, deck)


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

    # After legal input of bet, determine if the amount of bet is within limits
    # use recursion to force a bet within limit.
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

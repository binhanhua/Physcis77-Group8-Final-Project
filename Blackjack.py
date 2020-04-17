"""Spring 2020 Physics 77 Final Project Blackjack"""

import Deck
import Player


MIN_BET = 2
MAX_BET = 200
game_deck = 0
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
    global game_deck
    #Asking for the number of decks the player wants to start with
    deck_num = input('How many decks do you want to play with?\nA. 2 decks\nB. 4 decks\n')
    if deck_num in ['A', 'a']:
        game_deck = 2
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
        game_deck = 4
        #Asking for the desired starting fund
        money = input('How much money do you want to start with?\nA. 200 dollars\nB. 400 dollars\n')
        if money in ['A', 'a']:
            four_decks(200)
        if money in ['B', 'b']:
            four_decks(400)
        if money not in ['A', 'a', 'B', 'b']:
            print("That's not a choice!")
            play()

        #This is used to declare the number of decks used in this game.

    #For some reason using else here will run the following code regardless.
    #That's why I used a if ... not in ... to stop this from happening.

    if deck_num not in ['A', 'a', 'B', 'b']:
        print("That's not a choice!")
        play()


def two_decks(num):
    deck = Deck.PlayDeck(2)
    player = Player.Player(num)
    dealer = Player.Player(num, True)
    # dealer is a class of player
    deck.shuffle()
    start_turn(player, dealer, deck, game_deck)

def four_decks(num):
    deck = Deck.PlayDeck(4)
    player = Player.Player(num)
    dealer = Player.Player(num, True)
    deck.shuffle()
    start_turn(player, dealer, deck,game_deck)


def start_turn(player, dealer, deck, game_deck):
    """
    This function plays a complete turn of Blackjack
    """
    #If the player runs out of money, the program ends.
    if player.money <= 0:
        print("Sorry " + name + ", you are broke and can no longer play.")
        conclude(player)
        exit()
    # Reshuffle when 75% of cards are used.
    # May differ in casinos on this issue.
    if len(deck.cards) < 0.25 * 52 * game_deck:
        deck = Deck.PlayDeck(game_deck)
        deck.shuffle()
        # In real casino games, dealer inserts a plastic card
        # To indicate him to shuffle after the round when the card appeared.
        print("Plastic card appeared, Reshuffle the deck")


    bet = bet_amount(player)
    #The player and the dealer take out the same amount of bet.
    player.take_out(bet)
    print("Dealing the cards")
    player.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
    player.hand.append(deck.draw())
    dealer.hand.append(deck.draw())
    print("The dealer has one card hidden and a " + str(dealer.hand[1]))
    player.print_hand()

    #check the dealer's open card and insurance
    is_insurance = False
    is_pay_insurance = False
    insurance_bet = 0
    if dealer.hand[1].face == 'A':
        is_insurance, is_pay_insurance, insurance_bet = insurance(bet,dealer,player)

    #Player's turn.
    if player.sum_hand() == 21:
        print("Congratulations! You hit a blackjack.")
        player.money += 2.5 * bet
    else:
        bet = double(player,bet)
        sp = False
        if player.hand[0].face == player.hand[1].face:
            sp=split(player, bet, deck, sp)
        hit(player, deck, sp)

        #Dealer's turn.\\

        if player.busted() and player.busted_split_hand():
            print("The dealer has a "+str(dealer.hand[0])+" and a "+str(dealer.hand[1]))
            print("The dealer's hidden card is " + str(dealer.hand[0]))
            print("The dealer wins")
            if is_insurance:
                pay_insurance(is_pay_insurance, insurance_bet,player)
        else:
            print("Onto the dealer now.")
            # If dealer on or exceeds 17, then stand.
            print("The dealer has a "+str(dealer.hand[0])+" and a "+str(dealer.hand[1]))
            pay_insurance(is_pay_insurance, insurance_bet,player)
            if dealer.sum_hand() >= 17:
                if dealer.sum_hand() == 21 and not is_pay_insurance:
                    print("The dealer hits a Blackjack!")
            else:
                pass


            while dealer.sum_hand() < 17:
                print("The dealer decides to hit.")
                dealer.hit(deck)
                dealer.print_hand()
                if dealer.busted():
                    print("The dealer busted. You won this hand!")
                    player.money = player_money(player, bet, sp)
                    break
                if dealer.sum_hand() >= 17:
                    print('The dealer decides to stand.')
                    break #break out the while loop
            if dealer.busted():
                pass
            else:
                announce(player, dealer, bet,sp)
    print("You now have {} dollars".format(player.money))
    sp = False
    #Ask the player if they want to keep playing
    keep_playing = input('Do you want to keep playing? (Y/N) ')
    if keep_playing in ['yes', 'Yes', 'y', 'Y']:
        player.clear_hand()
        dealer.clear_hand()
        start_turn(player, dealer, deck, game_deck)
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
        new_str += " and won " + str(player.money - player.starting_fund) + " dollars. You're awesome."
    print(new_str)



def announce(player, dealer, bet, sp):
    """
    This function is called at the end of each term where no one has busted.
    This announces who won the turn and adds the money proportionally.
    """
    """
    If the player decided to split, this compare the points when every one has the hand that not busted,
    This announces who won the turn and adds the money proportionally.
    """
    player_score = player.sum_hand()
    dealer_score = dealer.sum_hand()
    print("The player has a score of {}".format(player_score))
    if sp:
        player_split_score = player.sum_split_hand()
        print("The player split hand has a score of {}".format(player_split_score))
    if dealer_score != 21:
        print("The dealer has a score of {}".format(dealer_score))
    if not sp:
        if player_score == dealer_score:
            print("PUSH")
            player.money += bet
            dealer.money += bet
        elif player_score > dealer_score:
            print("You won!")
            player.money += 2 * bet
        else:
            print("Dealer wins.")
    if sp:
        if player_score == dealer_score and not player.busted():
            print("First hand: PUSH")
            player.money += bet
            dealer.money += bet
        elif player_score > dealer_score and not player.busted():
            print("You won the first hand!")
            player.money += 2 * bet
        else:
            print("The dealer won the first hand")

        if player_split_score == dealer_score and not player.busted_split_hand():
            print("Second hand: PUSH")
            player.money += bet
            dealer.money += bet
        elif player_split_score > dealer_score and not player.busted_split_hand():
            print("You won the second hand!")
            player.money += 2 * bet
        else:
            print("The dealer won the second hand")


def hit(player, deck, sp):
    """
    This function utilizes the already implemented hit function in the Player class
    and continues to ask the player until they choose to stop hitting.
    """
    if not sp:
        answer = input('Do you want to hit? (Y/N) ')
        if answer in ['yes', 'Yes', 'y', 'Y']:
            hit_card = deck.cards[0]
            print("Your new card is " + str(hit_card))
            player.hit(deck)
            player.print_hand()
            sum = player.sum_hand()
            print("You now have {} points".format(sum))
            if sum == 21:
                print("Awesome! You made a 21!")
                pass
            elif player.busted():
                print("Sorry, you busted")
            else:
                hit(player, deck, sp)
        else:
            pass
    else:
        hit_first_hand = True
        while hit_first_hand:
            answer1 = input("Do you want to hit your first hand? (Y/N)")
            if answer1 in ['yes', 'Yes', 'y', 'Y']:
                hit_card1 = deck.cards[0]
                print("Your new card for the first hand is " + str(hit_card1))
                player.hit(deck)
                player.print_hand()
                sum1 = player.sum_hand()
                print("You now have {} points".format(sum1))
                if sum1 == 21:
                    print("Awesome! You made a 21!")
                    hit_first_hand = False
                    break
                elif player.busted():
                    print("Sorry, you busted")
                    hit_first_hand = False
                    break
            else:
                break

            if not hit_first_hand:
                break

        hit_second_hand = True
        while hit_second_hand:
            answer2 = input("Do you want to hit your second hand? (Y/N)")
            if answer2 in ['yes','Yes','y','Y']:
                hit_card2 = deck.cards[0]
                print("Your new card for the second hand is " + str(hit_card2))
                player.split_hit(deck)
                player.print_split_hand()
                sum2 = player.sum_split_hand()
                print("You now have {} points".format(sum2))
                if sum2 == 21:
                    print("Awesome! You made a 21!")
                    hit_second_hand = False
                    break
                elif player.busted_split_hand():
                    print("Sorry, you busted")
                    hit_second_hand = False
                    break
            else:
                break

            if not hit_second_hand:
                break



def double(player, bet):
    """
    This function allows the player to seek some wild fun:
    Double their bet!
    Notice that player should be a param.
    """
    is_double = input("Do you want to double your bet? (Y/N)")
    if is_double in ['Yes','yes','Y','y']:
        if player.money < bet:
            print("You do not have enough money to double!")
        else:
            print("You decided to double, the bet is now ${}".format(2*bet))
            player.take_out(bet)
            bet = 2 * bet
    else:
        print("You decided not to double.")
    return bet

def split(player, bet, deck, sp):
    """
    This function allows the player to split the cards
    A powerful weapon to win more money!
    """
    is_split = input("Do you want to split your cards? (Y/N)")
    if is_split in ["Yes","yes","Y","y"]:
        if player.money < bet:
            print("You do not have enough money to split!")
        else:
            sp = True
            print("You have decided to split")
            player.split_hand.append(player.hand.pop())
            player.take_out(bet)
            player.hand.append(deck.draw())
            player.split_hand.append(deck.draw())
            print("In the first hand")
            player.print_hand()
            player.print_split_hand()
    else:
        print("You decided not to split")
    return sp

def player_money(player,bet,sp):
    """
    This function is used to calculate the money when the dealer busts
    Split is taken into consideration
    """
    if sp == False:
        player.money += 2 * bet
    elif sp == True:
        if not player.busted():
            if not player.busted_split_hand():
                player.money += 4 * bet
            else:
                player.money += 2 * bet
        else:
            if not player.busted_split_hand():
                player.money += 2 * bet
    return player.money


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
        #This is simply an iteration for the player to enter a rational number
    print("Bet accepted")
    print("The bet for this round is ${}".format(bet))
    return bet

def insurance(bet,dealer,player):
    """
    This function allow player to pay insurance when the dealer has an A face up
    """
    insurance = input("Dealer's Ace face up, do you want to pay insurance ${}? （Y/N) ".format(bet/2))
    if insurance in ["Yes","yes","y",'Y']:
        insurance_bet = bet/2
        player.take_out(insurance_bet)
        is_insurance = True
        print("You decided to pay insurance")
        if dealer.hand[0].value == 10:
            is_pay_insurance = True
        else:
            is_pay_insurance = False
    else:
        is_insurance = False
        is_pay_insurance = False
        insurance_bet = 0
        pass
    return is_insurance, is_pay_insurance, insurance_bet

def pay_insurance(is_pay_insurance, insurance_bet,player):
    """
    This function returns the profit of insurance proportionally
    """
    if is_pay_insurance:
        print("The dealer has a Blackjack, insurance paid 2 to 1")
        player.take_in(3*insurance_bet)
    else:
        pass



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
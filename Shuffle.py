import random
import time


chip = 2500
# shuffle cards
def shuffle_cards(num_of_deck):
    cardfaces = []
    suits = ["Hearts","Diamond","Clubs","Spades"]
    royals = ["J","Q","K","A"]
    deck = []


    for i in range(2,11):
        cardfaces.append(str(i))

    for j in range(4):
        cardfaces.append(royals[j])
    for n in range(num_of_deck):
        for k in range(4):
            for l in range(13):
                card = (cardfaces[l] + " of " +suits[k])
                deck.append(card)
    random.shuffle(deck)

    return deck

def calculate_points(cardlist)


#Game starts
Game_result = "win"
player = input("Player name:")
print("Hey! "+player+"\nWelcome to Blackjack! ")
num_of_deck = int(input("Number of decks:"))
print("You now have ${}".format(chip))
bet = int(input("How much do you want to try?"))
while bet>chip:
    print("Sorry, you do not have enough money!")
    bet = int(input("How much do you want to try?"))

time.sleep(1)
print("Bet accepted!")
print("The bet for this game is ${}".format(bet))


cards = shuffle_cards(num_of_deck)
print("Your cards:",cards[0])
time.sleep(0.3)
print("The dealer's cards:",cards[1])
time.sleep(0.3)
print("Your cards:\n",cards[0]+'\n '+cards[2])
time.sleep(0.3)
print("The dealer's cards:\n",cards[1],"\n","***")



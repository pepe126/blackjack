import random
from colorama import Fore

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
         'Ten', 'Jack', 'Queen', 'King', 'Ace')

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 1}

twentyOne = 21


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck:
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                carta = Card(rank, suit)
                self.cards.append(carta)
        random.shuffle(self.cards)

    def deal(self):
        popped = self.cards.pop()
        return popped


class Field:
    def __init__(self):
        self.bet = 0
        self.dealerField = []
        self.playerField = []
        self.dealerPoints = 0
        self.playerPoints = 0

    def playerTake(self, dealedCard):
        self.playerField.append(dealedCard)

    def dealerTake(self, dealedCard):
        self.dealerField.append(dealedCard)

    def dealerCalcPoints(self):
        points = 0
        for card in self.dealerField:
            points = points + card.value
        return points

    def playerCalcPoints(self):
        points = 0
        for card in self.playerField:
            points = points + card.value
        return points


class Chip:
    def __init__(self, balance):
        self.balance = balance

    def bet(self):
        pass

    def __str__(self):
        return "Player balance is {}".format(self.balance)


def checkStillUnder(total):
    if total > twentyOne:
        print("{}You went over 21{}".format(Fore.RED, '\x1b[0m'))
        return False
    else:
        print("{}Yor are still under 21{}".format(Fore.GREEN, '\x1b[0m'))
        return True


print("WELCOME TO BLACKJACK V 0.1")
print("In blackjack the objective is to get as close as possible to 21")
print("without going over it. You can either hit and draw a card from")
print("the deck or stay and keep your cards. All the figures has a value")
print("of 10 and the Ace has a value of 1.")
print("HAVE FUN!\n")
print("---------------------------------------------------------------")


gameOver = False
mazzo = Deck()
game = Field()
while True:
    try:
        balance = int(input("How many {}$$${} you'll deposit? ".format(
                      Fore.GREEN, '\x1b[0m')))
    except ValueError:
        print("Insert a Number")
        continue
    else:
        break

eMoney = Chip(balance)

while gameOver is False:
    print("Dealing cards")
    for x in range(2):
        game.playerTake(mazzo.deal())
    for x in range(2):
        game.dealerTake(mazzo.deal())
    print("\n{}Dealer Cards are:{}\n".format(Fore.YELLOW, '\x1b[0m'))
    print(game.dealerField[0])
    print("{}COVERED{}\n".format(Fore.RED, '\x1b[0m'))
    print("{}Your Cards are:{}\n".format(Fore.YELLOW, '\x1b[0m'))
    for card in game.playerField:
        print(card)
    betted = False
    while betted is False:
        while True:
            try:
                bet = int(input("\nHow much do you want to bet? "))
            except ValueError:
                print("Enter a number")
                continue
            else:
                break
        if bet > eMoney.balance:
            print("You don't have enough money")
        elif bet == 0:
            print("Not enough")
        else:
            betted = True
    eMoney.balance = eMoney.balance - bet
    playerTurn = True
    while playerTurn:
        print("\nWhat do you want to do?")
        while True:
            try:
                decision = str(input("Enter 'hit' or 'stay': "))
            except ValueError:
                print("Enter a string")
                continue
            else:
                break
        decision = decision.upper()
        if decision == "HIT":
            game.playerTake(mazzo.deal())
            print("{}Your Cards are:{}\n".format(Fore.YELLOW, '\x1b[0m'))
            for card in game.playerField:
                print(card)
            playerP = game.playerCalcPoints()
            playerTurn = checkStillUnder(playerP)
        elif decision == "STAY":
            playerTurn = False
        else:
            print("Enter right option")
    print("\n{}DEALER REVEAL HIS COVERED CARD{}\n\nDealer Cards are:\n"
          .format(Fore.MAGENTA, '\x1b[0m'))
    for card in game.dealerField:
        print(card)
    dealerLosing = game.dealerCalcPoints() <= game.playerCalcPoints()
    if game.playerCalcPoints() > twentyOne:
        dealerLosing = False
    while dealerLosing:
        print("\nDealer will HIT")
        game.dealerTake(mazzo.deal())
        print("{}Dealer Cards are:{}\n".format(Fore.YELLOW, '\x1b[0m'))
        for card in game.dealerField:
            print(card)
        dealerLosing = game.dealerCalcPoints() <= game.playerCalcPoints()
    if game.dealerCalcPoints() <= twentyOne:
        print("\n{}Dealer won the round and took the chips{}".format(Fore.RED,
              '\x1b[0m'))
        bet = 0
        print("\nNext Turn!\n")
    else:
        print("\n{}Dealer lost going over 21!{}".format(Fore.GREEN, '\x1b[0m'))
        print("{}Dealer Cards are:{}\n".format(Fore.YELLOW, '\x1b[0m'))
        for card in game.dealerField:
            print(card)
        print("\n{}Your cards are:{}\n".format(Fore.YELLOW, '\x1b[0m'))
        for card in game.playerField:
            print(card)
        eMoney.balance = eMoney.balance + (bet*2)
        bet = 0
    game.dealerField.clear()
    game.playerField.clear()
    if eMoney.balance < 1:
        print("{}You have no money left, YOU LOST{}".format(Fore.RED,
              '\x1b[0m'))
        gameOver = True

    elif not mazzo.cards:
        mazzo = None
        mazzo = Deck()
        print("\n...Restarting deck...\n")
    else:
        print("\nYour Balance is: {}".format(eMoney.balance))
        while True:
            try:
                doesPlayer = str(input("\nDo you want to continue?(y/n) "))
            except ValueError:
                print("Enter a string")
                continue
            else:
                break
        if doesPlayer.upper() == "N":
            gameOver = True
            print("You are leaving the table with: {}".format(eMoney.balance))
        else:
            print("The game will continue\n")

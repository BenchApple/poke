# Benjamin Chappell
# This file just stores the cards class, it's very basic
# 0-12 represents the ace through king of spades, 13-25 ace through king of diamonds
# 26-38 ace through king of clubs, 39-51 ace through king of hearts

from random import shuffle
from cards import Cards

# This class stores the deck
class Deck:
    def __init__(self) -> None:
        self.cards = [i for i in range(0, 52)]
        shuffle(self.cards)

        self.pos = 0 # Tracks where in the cards list we are

    def shuffle_deck(self):
        shuffle(self.cards)

    def get_next_card(self):
        self.pos += 1
        return self.cards[self.pos - 1]
    
    def reset(self):
        shuffle(self.cards)
        self.pos = 0
    
    # Prints a hand, where a hand is a list of cards
    def print_hand(self, hand):
        s = ""
        for card in hand:
            s = s + "\n" + str(Cards(card).name)

        print(s)
        print()

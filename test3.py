# Benjamin Chappell

# Testing the paly of the game

from hand_checker import *
from deck import Deck
from player import Player
from cards import Cards
from hands import Hand, HandClass
import sys

d = Deck()

worst_hand = [1, 15, 3, 17, 6]

h = five_card_checker(worst_hand)
d.print_hand(worst_hand)
print(h)
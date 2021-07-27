# Benjamin Chappell
# This one is to test the comparator

from hand_checker import *
from deck import Deck
from player import Player
from cards import Cards
from hands import Hand, HandClass
import sys
from random import randint

quads = [0, 13, 26, 39, 1]
boat = [0, 13, 26, 1, 14]
sflush = [0, 1, 2, 3, 4]
broad = [9, 10, 11, 12, 0]
two_pair = [0, 13, 1, 14, 2]
two_pair2 = [12, 25, 0, 13, 4]
two_pair3 = [1, 14, 2, 15, 3, 4]
s = [0, 13, 26, 1, 2]
flush = [1, 2, 4, 6, 8]
pair = [1, 14, 0, 2, 51]
high = [1, 15, 17, 51, 49]
straight = [0, 14, 28, 42, 4]

d = Deck()

test_hand = [d.get_next_card() for i in range(0, 7)]
print(test_hand)
d.print_hand(test_hand)

b = get_top_hand(test_hand)
print(b)

sample = [17, 40, 49, 36, 12, 51, 31]
d.print_hand(sample)
b = get_top_hand(sample)
print(b)

# Benjamin Chappell
# Testing of classes

from hand_checker import *
from deck import Deck
from player import Player
from cards import Cards
from hands import Hand, HandClass
import sys

d = Deck()

hand1 = []
hand2 = []

quads = [0, 13, 26, 39, 1]
boat = [0, 13, 26, 1, 14]
sflush = [0, 1, 2, 3, 4]
broad = [9, 10, 11, 12, 0]
two_pair = [0, 13, 1, 14, 2]
two_pair = [12, 25, 0, 0, 4]
s = [0, 13, 26, 1, 2]
flush = [1, 2, 4, 6, 8]
pair = [1, 14, 0, 2, 51]
high = [1, 15, 17, 51, 49]
straight = [0, 14, 28, 42, 4]

d.print_hand(quads)
print(five_card_checker(quads))
d.print_hand(boat)
print(five_card_checker(boat))
d.print_hand(sflush)
print(five_card_checker(sflush))
d.print_hand(broad)
print(five_card_checker(broad))
d.print_hand(two_pair)
print(five_card_checker(two_pair))
d.print_hand(s)
print(five_card_checker(s))
d.print_hand(flush)
print(five_card_checker(flush))
d.print_hand(pair)
print(five_card_checker(pair))
d.print_hand(high)
print(five_card_checker(high))
d.print_hand(straight)
print(five_card_checker(straight))

quad = 0
sflush = 0
rflush = 0
boat = 0
set = 0
tpair = 0
pair = 0
straight = 0
flush = 0
high = 0

for i in range(0, 1000000):
    hand1 = []
    d.reset()
    for i in range(0, 5):
        hand1.append(d.get_next_card())
    h = five_card_checker(hand1)
    if h.type == HandClass.SFLUSH:
        sflush += 1
    elif h.type == HandClass.QUADS:
        quad += 1
    elif h.type == HandClass.RFLUSH:
        rflush += 1
    elif h.type == HandClass.BOAT:
        boat += 1
    elif h.type == HandClass.SET:
        set += 1
    elif h.type == HandClass.TWO_PAIR:
        tpair += 1
    elif h.type == HandClass.PAIR:
        pair += 1
    elif h.type == HandClass.STRAIGHT:
        straight += 1
    elif h.type == HandClass.FLUSH:
        flush += 1
    else:
        high += 1
    
print("Royal Flush")
print(rflush)
print("SFlush")
print(sflush)
print("Quads")
print(quad)
print("Boat")
print(boat)
print("Flush")
print(flush)
print("Straigth")
print(straight)
print("Set")
print(set)
print("2 pair")
print(tpair)
print("pair")
print(pair)
print("High")
print(high)

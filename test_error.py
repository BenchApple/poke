# Benjamin Chappell

from hand_checker import *
from deck import Deck
from player import Player
from cards import Cards
from hands import Hand, HandClass
import sys

hand1 = [Cards.SIX_CLUBS.value, Cards.TWO_HEARTS.value, Cards.JACK_HEARTS.value, \
         Cards.TWO_SPADES.value, Cards.NINE_SPADES.value, Cards.FOUR_DIAMONDS.value, \
         Cards.KING_SPADES.value]
hand2 = [Cards.SIX_CLUBS.value, Cards.TWO_HEARTS.value, Cards.JACK_HEARTS.value, \
         Cards.TWO_SPADES.value, Cards.NINE_SPADES.value, Cards.FIVE_HEARTS.value, \
         Cards.TEN_HEARTS.value]
shithand = [1, 15, 3, 17, 6]

h1 = hand_checker(hand1)
h2 = hand_checker(hand2)
sh = five_card_checker(shithand)

print(h1)
print(h2)
print(sh)

print(h1.compare(h2))
print(h1.compare(sh))
print(h2.compare(sh))
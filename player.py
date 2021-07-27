# Benjamin Chappell
# This file contains the player for the poker game

class Player:
    def __init__(self, stack, position) -> None:
        self.stack = stack # starting stack
        self.position = position # starting position
        # For position, 0 means small blind, 1 means big blind, max is button

        self.cards = [-1, -1] # Stores the 2 cards for the current player

    def get_stack(self): return self.stack
    def set_stack(self, stack): self.stack = stack

    def get_position(self): return self.position
    def update_position(self, max_pos): self.position = (self.position + 1) % max_pos

    def set_first_card(self, card):
        self.cards[0] = card

    def set_second_card(self, card):
        self.cards[1] = card

    stack = property(get_stack, set_stack)
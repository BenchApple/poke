# Benjamin Chappell
# This file contains the player for the poker game

from action import Action

class Player:
    def __init__(self, stack, position) -> None:
        self._stack = stack # starting stack
        self.position = position # starting position
        # For position, 0 means small blind, 1 means big blind, max is button

        self.cards = [-1, -1] # Stores the 2 cards for the current player

        self.total_in = 0 # Represents the amount this player has put into the pot
        self.current_bet = 0 # Represents the most recent bet of this player
        self.folded = False
        self.called = False
        self.raised = False

        self.actions = [] # Stores all the actions taken this round

    # Resets the player for the next round
    def reset(self):
        self.cards = [-1, -1]
        self.current_bet = 0
        self.total_in = 0
        self.actions = []
        self.folded = False
        self.called = False
        self.raised = False
    
    # Called between streets
    def soft_reset(self):
        self.current_bet = 0
        self.called = False
        self.raised = False
    
    def fold(self):
        self.folded = True
    def get_folded(self):
        return self.folded
    
    def call(self):
        self.called = True
    def get_called(self):
        return self.called
    
    def do_raise(self):
        self.raised = True
    def get_raised(self):
        return self.raised

    # Adds money into the pot and subtracts from stack
    # If blind is true it doesn't count as the most recent bet
    def bet(self, amount):
        self._stack -= amount
        self.total_in += amount
        self.current_bet += amount
        
        return amount

    # To be used for payouts
    def get_money(self, amount):
        self._stack += amount
    
    # Returns whether or not the balance is negative
    def is_out(self):
        return self._stack > 0

    # Returns info on the player such as stack size, position, money in, current bet
    def get_info(self):
        # Returns in the following order
        # position, stack, total_in, current bet, folded, actions
        return (self.position, self.stack, self.total_in, self.current_bet, self.folded, [str(a) for a in self.actions])
    
    def add_action(self, action):
        self.actions.append(action)

    def get_stack(self): return self._stack
    def set_stack(self, stack): self._stack = stack

    def get_position(self): return self.position
    def update_position(self, max_pos): self.position = (self.position - 1) % max_pos

    def set_first_card(self, card):
        self.cards[0] = card

    def set_second_card(self, card):
        self.cards[1] = card

    # Takes a list of legal actions
    def get_input(self, legal_actions, call_amount):
        print("Legal Actions are " + str(legal_actions))
        print("Your position is: " + str(self.position))
        print("Your stack is " + str(self._stack))
        print("You have %f in the pot and %f to call" % (self.total_in, call_amount - self.current_bet))
        action = -1

        while action not in legal_actions:
            action = int(input("What move would you like (fold-0, check-1, call-2, raise-3, shove-4): "))

        amount = -1
        if action == 3:
            amount = self.stack + 1
            while amount > self._stack or amount <= call_amount:
                amount = float(input("How much would you like to raise to? "))

        self.add_action(Action(action, amount=amount))
        return self.actions[-1]


    stack = property(get_stack, set_stack)
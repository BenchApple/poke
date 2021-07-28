# Benjamin Chappell
# Class used to classify all the actions one can take in poker

from enum import Enum, auto

class ActionTypes(Enum):
    FOLD = 0
    CHECK = auto()
    CALL = auto()
    RAISE = auto()
    shove = auto()

class Action:
    # Move is an enum value designating fold, check, call, raise, shove
    # amount is equal to the amount raising or shoving
    def __init__(self, move, amount=-1) -> None:
        self.move = move
        self.amount = amount

    def __str__(self) -> str:
        return "Move: %s; Amount: %d" % (ActionTypes(self.move).name, self.amount)
        
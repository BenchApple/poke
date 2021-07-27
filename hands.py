# Benjamin Chappell
# Hand value storage

from enum import Enum
from rank import Rank

class HandClass(Enum):
    HIGH = 0
    PAIR = 1
    TWO_PAIR = 2
    SET = 3
    STRAIGHT = 4
    FLUSH = 5
    BOAT = 6
    QUADS = 7
    SFLUSH = 8
    RFLUSH = 9

class Hand:
    def __init__(self, type, rank, rank2=False) -> None:
        self.type = type
        self.rank = rank
        self.rank2 = rank2

        if self.rank == 0:
            self.rank += 13

        for i in range(0, len(rank2)):
            if rank2[i] == 0:
                rank2[i] += 13
    
    def __str__(self) -> str:
        s = "Class: %s; Rank: %s; Secondary Rank: " % (self.type, Rank(self.rank%13).name)
        for i in range(0, len(self.rank2)):
            s = s + Rank(self.rank2[i]%13).name + ", "
        
        return s

    # Compares 2 hand objects
    # if hand1 is greater than hand2, return True, hand2 greater than hand1 return False
    # If the two hands are equal, return -1
    def compare(self, hand2):
        if self.type.value != hand2.type.value:
            return self.type.value > hand2.type.value
        else:
            if self.rank != hand2.rank:
                return self.rank > hand2.rank
            for i in range(0, len(self.rank2)):
                if self.rank2[i] != hand2.rank2[i]:
                    return self.rank2 > hand2.rank2
            return -1
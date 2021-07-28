# Benjamin Chappell
# This file recognizes hands

from hands import Hand, HandClass

# Takes a list of 7 cards and returns its hand
def hand_checker(cards):
    assert(len(cards) == 7)

    return get_top_hand(cards)

def get_top_hand(cards):
    if len(cards) > 5:
        hands = []
        for i in range(0, len(cards)):
            hand = cards.copy()
            hand.pop(i)
            # Recursively find the top hand out of these six cards
            hands.append(get_top_hand(hand))
        
        # Now that we have all of the hands from this set of cards, 
        # compare them to find the best
        top_hand = hands[0]
        for hand in hands:
            # Since our comparator returns true if hand is better than top_hand
            if hand.compare(top_hand):
                top_hand = hand
        
        # Now return the top hand
        return top_hand
    # Base case, just call the 5 card checker
    else:
        return five_card_checker(cards)

# Version of the card checker that only checks for 5 cards
def five_card_checker(cards):
    assert(len(cards) == 5)

    # Stores the histogram of ranks in the hand
    # 0 is ace, 12 is king
    ranks = [0 for i in range(0, 13)]

    for card in cards:
        ranks[card % 13] += 1

    ranks_o = ranks.copy()
    histo = ranks.copy()
    histo.sort(reverse=True)

    cards.sort()

    c = HandClass.HIGH
    r = -1
    r2 = []
    if histo[0] == 4:
        c = HandClass.QUADS
        # Set the ranks
        r = ranks.index(4)
        r2.append(ranks.index(1))
    elif histo[0] == 3:
        if histo[1] == 2:
            c = HandClass.BOAT
            # Set the ranks properly
            r = ranks.index(3)
            r2.append(ranks.index(2))
        else:
            c = HandClass.SET
            r = ranks.index(3)
            # This is how we get the ranks for a set
            r2.insert(0, ranks.index(1))
            ranks.remove(1)
            r2.insert(0, ranks.index(1) + 1)
    elif histo[0] == 2:
        if histo[1] == 2:
            # Get the ranks for this 
            second_pair = ranks.index(2)

            if second_pair == 0:
                r = second_pair
                ranks.remove(2)
                r2.insert(0, ranks.index(2) + 1)
                r2.append(ranks.index(1) + 1)
            else:
                r2.insert(0, second_pair)
                ranks.remove(2)
                r = ranks.index(2) + 1
                ranks.insert(second_pair, 2)
                r2.append(ranks.index(1))
            c = HandClass.TWO_PAIR
        else:
            c = HandClass.PAIR

            r = ranks.index(2)
            kicker = ranks.index(1)
            r2.append(kicker)
            ranks.remove(1)
            if kicker == 0:
                r2.insert(1, ranks.index(1) + 1)
                ranks.remove(1)
                r2.insert(1, ranks.index(1) + 2)
            else:
                r2.insert(0, ranks.index(1) + 1)
                ranks.remove(1)
                r2.insert(0, ranks.index(1) + 2)

    # Check for a flush only if we haven't found anything else
    if c == HandClass.HIGH:
        suit = cards[0] // 13
        is_flush = True

        for card in cards:
            if card // 13 != suit:
                is_flush = False
                break
        
        if is_flush:
            c = HandClass.FLUSH
            if cards[0] % 13 == 0:
                r = 0
            else:
                r = cards[4] % 13
    
    # Check for a straight, and by extension a straight flush
    # Since we now have a copied version of ranks, use that
    ranks = ranks_o.copy()
    if c == HandClass.HIGH or c == HandClass.FLUSH:
        # Make the cards easier to work with for straights
        cards = [cards[i] % 13 for i in range(0, len(cards))]
        cards.sort()
        is_straight = True

        start = ranks.index(1)
        if ranks[start] == ranks[start+1] == ranks[start+2] == ranks[start+3] == ranks[start+4] == 1:

            is_straight = True
        else:
            is_straight = False

        # manually check for a braodway
        if cards[0] == 0 and cards[1] == 9 and \
            cards[2] == 10 and cards[3] == 11 and \
            cards[4] == 12:
            is_straight = True

        if is_straight:
            if c == HandClass.FLUSH:
                c = HandClass.SFLUSH
            else:
                c = HandClass.STRAIGHT
            
            # If it's a wheel then we wnat the 5 to be the high
            if ranks[0] == 1 and not ranks[4] == 1:
            #if cards[0] % 13 == 0 and cards[4] % 13 != 4:
                r = 0
            else:
                r = cards[4]
    
    # If we're still high then we need to set r
    if c == HandClass.HIGH:
        for i in range(0, 4):
            r2.insert(0, ranks.index(1) + i)
            ranks.remove(1)
        r = ranks.index(1) + 4

    # Check to see if we have a royal flush
    if r == 0 and c == HandClass.SFLUSH:
        c = HandClass.RFLUSH

    hand = Hand(c, r, rank2=r2)
    return hand
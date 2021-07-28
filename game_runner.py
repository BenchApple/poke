# Benjamin Chappell
# Methods made to run the game

from types import LambdaType
from cards import Cards
from deck import Deck
from hand_checker import *
from hands import HandClass, Hand
from player import Player
from rank import Rank
from action import Action

def main():
    # This is in number of big blinds
    # This means small blind is always .5 and bb is always 1
    starting_stack = 20
    max_players = 8
    players = [] # Keeps track of all of the players
    sb_pos = 1 # Keeps track of the position of the small blind

    hands = 25 # the total amount of hands to be played
    cur_hand = 0

    d = Deck()

    # Create all of the players
    for i in range(0, max_players):
        players.append(Player(starting_stack, i))

    while cur_hand < hands:
        play_one_hand(players, max_players, d, sb_pos)

        d.shuffle_deck()
        sb_pos = (sb_pos + 1) % max_players
        cur_hand += 1

def play_one_hand(players, max_players, d, sb_pos):
        d.shuffle_deck()
        board = [] # Stores the table cards
        players_in_hand = max_players

        # pre-flop
        for p in players:
            p.set_first_card(d.get_next_card())
        for p in players:
            p.set_second_card(d.get_next_card())
        
        # Now get actions from all players
        pot = 0
        # Get the blinds in play
        pot += players[sb_pos%max_players].bet(0.5)
        pot += players[(sb_pos+1)%max_players].bet(1)

        call_amount = 1
        prev_amount_in = 0 # The amount a player must have put in to stay in this hand
        last_player = 2 + max_players
        cur_player = 2
        default_legal_moves = [0, 2, 3, 4]
        while True:
            # Beause for some reason updating the while condition breaks it
            if reached_end_of_street(cur_player, last_player):
                break
            print(cur_player, last_player)
            legal_moves = default_legal_moves.copy()
            p = players[(sb_pos+cur_player) % max_players]

            # Check to see if this player is the only one in the hand
            if players_in_hand == 1:
                break # if this is the only player left, return
            elif p.current_bet == call_amount:
                legal_moves = [1, 3, 4]

            # Limit legal moves if certain conditions are met
            if p.get_folded():
                cur_player += 1
                continue # move onto the next player
            if p.get_called() or p.get_raised():
                legal_moves = [0, 2]

            d.print_hand(p.cards)
            print("Player %d" % ((sb_pos + cur_player) % max_players))
            print("Call amount is " + str(call_amount))
            action = p.get_input(legal_moves, call_amount)

            if action.move == 0:
                p.fold()
                players_in_hand -= 1
            elif action.move == 1:
                pass # Nothing happens if you check
            elif action.move == 2:
                p.call()
                pot += call_amount - p.current_bet
                p.bet(call_amount - p.current_bet)
            elif action.move == 3: # Raising
                p.do_raise()
                pot += p.bet(action.amount)
                call_amount = action.amount
                last_player = cur_player + max_players
            elif action.move == 4:
                p.do_raise()
                call_amount = p.bet(p.get_stack)
                pot += call_amount
                last_player = cur_player + max_players
            
            cur_player += 1
        
        if players_in_hand == 1:
            pay_out_if_one_player(players, pot)
            end_hand(players, max_players)
            return
        else:
            print("Pot is: %f" % pot)
        
        # Soft reset the status of each of the players
        player_status_between_hands(players)
        input()

        # Flop
        print("TO THE FLOP")
        # Lay out the board
        d.get_next_card() # Burn one card
        for i in range(0, 3):
            board.append(d.get_next_card())
        
        pot, players_in_hand, call_amount = run_post_flop_rounds(players, pot, call_amount, sb_pos, max_players, board, players_in_hand, d)
        
        if players_in_hand == 1:
            pay_out_if_one_player(players, pot)
            end_hand(players, max_players)
            return
        else:
            print("Pot is: %f" % pot)
        
        # Soft reset the status of each of the players
        player_status_between_hands(players)
        input()

        # Turn
        print("TO THE TURN")
        # Lay out the board
        d.get_next_card() # Burn one card
        board.append(d.get_next_card())

        pot, players_in_hand, call_amount = run_post_flop_rounds(players, pot, call_amount, sb_pos, max_players, board, players_in_hand, d)

        if players_in_hand == 1:
            pay_out_if_one_player(players, pot)
            end_hand(players, max_players)
            return
        else:
            print("Pot is: %f" % pot)
        
        # Soft reset the status of each of the players
        player_status_between_hands(players)
        input()

        # River
        print("TO THE RIVER")
        d.get_next_card() # Burn one card
        board.append(d.get_next_card())

        pot, players_in_hand, call_amount = run_post_flop_rounds(players, pot, call_amount, sb_pos, max_players, board, players_in_hand, d)

        if players_in_hand == 1:
            pay_out_if_one_player(players, pot)
            end_hand(players, max_players)
            return
        else:
            print("Pot is: %f" % pot)
        
        # Soft reset the status of each of the players
        player_status_between_hands(players)
        input()

        # Showdown
        print("To the Showdown!")
        # If we've gotten to this point we know go from player to player and find their best hand and compare them
        worst_hand = [1, 15, 3, 16, 5] # This is the worst 5 card hand in poker

        # Store the best hand object we find and the player it's associated with
        best_player = -1
        best_hand = five_card_checker(worst_hand)
        tied_list = [] # Stores the players that are tied
        tied_hands = []

        for i in range(0, len(players)):
            p = players[i]

            if not p.get_folded(): # make sure the player hasn't folded
                # Combine to form a 7 card hand
                cards = p.cards + board
                hand = hand_checker(cards)
                print(hand)

                # Compare this hand with the best hand so far
                comparison = hand.compare(best_hand) # If hand is better than best hand this will be True
                if comparison:
                    # If this hand is the best hand, set that to be so
                    best_hand = hand
                    best_player = i
                elif comparison == -1:
                    # This means the two hands are tied
                    if best_player not in tied_list:
                        tied_list.append(best_player)
                        tied_hands.append(best_hand)

                    tied_list.append(i)
                    tied_hands.append(i)
        
        if best_player > -1:
            # Pay out to the player with the best hand
            print("Player %d has won the pot with the following hand" % best_player)
            print(best_hand)
            players[best_player].get_money(pot)
            pot = 0
        elif len(tied_list) > 0:
            if tied_list[0] == -1:
                tied_list.remove(-1) # If for whatever reason the tied list is in here, remove it from the list
            
            for i in tied_list: # Iterate through the tied list and pay split pot to each
                print("Player %d wins part of the split pot with the following hand" % i)
                print(best_hand)
                players[i].get_money(pot / len(tied_list))
            pot = 0
        
        end_hand(players, max_players)
        
def end_hand(players, max_players):
    print("END OF HAND")
    for p in players:
        print(p.get_info())
        p.update_position(max_players)
        p.reset()

# Runs all post flop rounds since they all run the same, returns a tuple of (pot, players_in_hand)
def run_post_flop_rounds(players, pot, prev_amount_in, sb_pos, max_players, board, players_in_hand, d):
    cur_player = 0
    last_player = max_players
    call_amount = 0
    default_legal_moves = [1, 3, 4] # Cannot fold if there are no bets
    while cur_player < last_player:
        legal_moves = default_legal_moves.copy()
        p = players[(sb_pos+cur_player) % max_players]

        # Check to see if this player is the only one in the hand
        if players_in_hand == 1:
            break # if this is the only player left, return
        elif p.current_bet == call_amount:
            legal_moves = [1, 3, 4]

        # Limit legal moves if certain conditions are met
        if p.get_folded():
            cur_player += 1
            continue # move onto the next player
        if p.get_called() or p.get_raised():
            legal_moves = [0, 2]

        print("Board Cards")
        d.print_hand(board)
        print("Player Cards")
        d.print_hand(p.cards)
        print("Player %d" % ((sb_pos + cur_player) % max_players))
        print("Call amount is " + str(call_amount))
        action = p.get_input(legal_moves, call_amount)

        if action.move == 0:
            p.fold()
            players_in_hand -= 1
        elif action.move == 1:
            pass # Nothing happens if you check
        elif action.move == 2:
            p.call()
            call_deficit = call_amount - p.current_bet
            pot += call_deficit
            # Bet the call amount minus whatever's in plus what you put in on previous streets
            p.bet(call_deficit) 
        elif action.move == 3: # Raising
            p.do_raise()
            pot += p.bet(action.amount)
            call_amount = action.amount
            last_player = cur_player + max_players
            default_legal_moves = [0, 2, 3, 4]
        elif action.move == 4:
            p.do_raise()
            call_amount = p.bet(p.get_stack)
            pot += call_amount
            last_player = cur_player + max_players
            default_legal_moves = [0, 2, 3, 4] # Adjust the legal moves now that there's a bet
        cur_player += 1
    
    return (pot, players_in_hand, call_amount)

def reached_end_of_street(cur_player, last_player):
    return cur_player == last_player

def pay_out_if_one_player(players, pot):
    # Check to see for the one player still in the hand and pay out
    for p in players:
        if not p.get_folded():
            p.get_money(pot)
            print("Player has won the hand")
    pot = 0

def player_status_between_hands(players):
    for i in range(0, len(players)):
        p = players[i]
        if p.get_folded():
            print("Player " + str(i) + " has folded. They have a stack of " + str(p.get_stack()))
        else:
            print("Player " + str(i) + " is in for " + str(p.total_in) + ". They have a stack of " + str(p.get_stack()))
        p.soft_reset()

if __name__ == "__main__":
    main()
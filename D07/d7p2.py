"""
This module solves Part Two of Day 7's problem of the Advent of Code challenge.
We use the same hand type representation as in Part One, but we add a bunch of annoying
special cases to handle all the ways different Jack wildcards could improve a hand.
"""
# --- Part Two ---
# To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are
# jokers - wildcards that can act like whatever card would make the hand the strongest type
# possible.
#
# To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards
# stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.
#
# J cards can pretend to be whatever card is best for the purpose of determining hand type; for
# example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between
# two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is
# weaker than QQQQ2 because J is weaker than Q.
#
# Now, the above example goes very differently:
#
# 32T3K 765 T55J5 684 KK677 28 KTJJT 220 QQQJA 483 32T3K is still the only one pair; it doesn't
# contain any jokers, so its strength doesn't increase. KK677 is now the only two pair, making it
# the second-weakest hand. T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3,
# QQQJA gets rank 4, and KTJJT gets rank 5. With the new joker rule, the total winnings in this
# example are 5905.
#
# Using the new joker rule, find the rank of every hand in your set. What are the new total
# winnings?
#
# Answer for sample input: 6440
# Answer for input: 250757288

FILENAME = 'input.txt'

def hand_parser(file_name) -> list(tuple()):
    """
    Parses a Camel Cards file into a list
    Each list member is a tuple that consists of the hand and the bid value
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            cards_data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    
    # Use list comprehension to read each line of the file and create a tuple
    # for each hand and bid
    return [tuple(line.split()) for line in cards_data]

def is_five_of_a_kind(hand) -> bool:
    """
    Checks if a hand is a five of a kind
    """
    # Ways to make five of a kind:
    # - Natural five of a kind
    # - Four of a kind and a wild Jack
    # - Three of a kind and two wild Jacks
    # - Two of a kind and three wild Jacks
    return all(c == hand[0] for c in hand) or \
           (any(hand.count(c) == 4 for c in set(hand)) and 'J' in hand) or \
           (any(hand.count(c) == 2 for c in set(hand)) and hand.count('J') == 3) or \
           (any(hand.count(c) == 3 for c in set(hand)) and hand.count('J') == 2)

def is_four_of_a_kind(hand) -> bool:
    """
    Checks if a hand is a four of a kind
    """
    # Ways to make four of a kind:
    # - Natural four of a kind
    # - Three of a kind and one wild Jack
    # - A pair and two wild Jacks
    # - Three jacks
    return any(hand.count(c) == 4 for c in hand) or \
           (any(hand.count(c) == 3 for c in set(hand)) and 'J' in hand) or \
           (any(hand.count(c) == 2 for c in set(hand)) and hand.count('J') == 2 and len(set(hand)) == 3) or \
           hand.count('J') == 3

def is_full_house(hand) -> bool:
    """
    Checks if a hand is a full house
    """
    # Ways to make a full house:
    # - Natural full house
    # - Two pairs and one wild Jack
    counts = [hand.count(c) for c in set(hand)]
    return (3 in counts and 2 in counts) or (counts.count(2) == 2 and 'J' in hand)

def is_three_of_a_kind(hand) -> bool:
    """
    Checks if a hand is a three of a kind
    """
    # Ways to make three-of-a-kind:
    # - Natural three-of-a-kind
    # - One pair and one wild Jack
    # - Two wild Jacks and anything else
    return any(hand.count(c) == 3 for c in hand) or \
           (any(hand.count(c) == 2 for c in set(hand)) and 'J' in hand) or \
           hand.count('J') == 2

def is_two_pair(hand) -> bool:
    """
    Checks if a hand is a two pair
    """
    # Ways to make two pair:
    # - Natural two pair
    # - Jacks never matter because they will always form something stronger
    pairs = [c for c in set(hand) if hand.count(c) == 2]
    return len(pairs) == 2

def is_one_pair(hand) -> bool:
    """
    Checks if a hand is a one pair
    """
    # Ways to make one pair:
    # - Natural pair
    # - A single Jack
    return any(hand.count(c) == 2 for c in hand) or 'J' in hand

def card_ranker(card: str) -> int:
    """
    Returns the rank of a card
    """

    if card == 'A':
        return 14
    elif card == 'K':
        return 13
    elif card == 'Q':
        return 12
    elif card == 'J':
        return 0 # Special case for Jack now being weakest in tie-breakers
    elif card == 'T':
        return 10
    else:
        return int(card)

def hand_ranker(hand: tuple) -> int:
    """
    Returns the rank of a hand
    """
    # First digit will be the order of the hand type
    # Digits 2-5 will be the order of the card values
    hand = hand[0]
    
    hand_type_value = 0x0
    if is_five_of_a_kind(hand):
        hand_type_value = 0x700000
    elif is_four_of_a_kind(hand):    
        hand_type_value = 0x600000
    elif is_full_house(hand):
        hand_type_value = 0x500000
    elif is_three_of_a_kind(hand):
        hand_type_value = 0x400000
    elif is_two_pair(hand):
        hand_type_value = 0x300000
    elif is_one_pair(hand):
        hand_type_value = 0x200000
    else:
        hand_type_value = 0x100000

    for card_num, card in enumerate(hand):
        hand_type_value += card_ranker(card) * (0x10000 >> (4 * card_num)) 
    
    return hand_type_value

def main():
    """
    Main function that reads the input file, parses the hands, sorts them, and calculates
    total winnings
    """

    hands = hand_parser(FILENAME)
    sorted_hands = sorted(hands, key=hand_ranker)

    winnings = 0
    for hand_rank, hand in enumerate(sorted_hands):
        winnings = winnings + (hand_rank + 1) * int(hand[1])
        
    print(f'Winnings: {winnings}')
    
if __name__ == "__main__":
    main()

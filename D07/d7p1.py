"""
This module solves Part One of Day 7's problem of the Advent of Code challenge.
Main insight here is that the hand type can be represented as a 6-digit hex number
where the first digit is the hand type and the remaining digits are the card values.
That way we can sort the hands by their hand type and then by their card values.
We use hex instead of decimal to make it easier to store more than 10 cards in a digit.

We take advantage of Python's ability to take custom keys for sorting.
"""
# --- Day 7: Camel Cards --- 
# Your all-expenses-paid trip turns out to be a one-way, five-minute ride
# in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and
# descends back to Island Island.
#
# "Did you bring the parts?"
#
# You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a
# large camel.
#
# "Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's
# looking for; you're here to figure out why the sand stopped.
#
# "The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.
#
# After riding a bit across the sands of Desert Island, you can see what look like very large rocks
# covering half of the horizon. The Elf explains that the rocks are all along the part of Desert
# Island that is directly above Island Island, making it hard to even get there. Normally, they use
# big machines to move the rocks and filter the sand, but the machines have broken down because
# Desert Island recently stopped receiving the parts they need to fix the machines.
#
# You've already assumed it'll be your job to figure out why the parts stopped when she asks if you
# can help. You agree automatically.
#
# Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel
# Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.
#
# In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of
# each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
# The relative strength of each card follows this order, where A is the highest and 2 is the lowest.
#
# Every hand is exactly one type. From strongest to weakest, they are:
#
# Five of a kind, where all five cards have the same label: AAAAA Four of a kind, where four cards
# have the same label and one card has a different label: AA8AA Full house, where three cards have
# the same label, and the remaining two cards share a different label: 23332 Three of a kind, where
# three cards have the same label, and the remaining two cards are each different from any other
# card in the hand: TTT98 Two pair, where two cards share one label, two other cards share a second
# label, and the remaining card has a third label: 23432 One pair, where two cards share one label,
# and the other three cards have a different label from the pair and each other: A23A4 High card,
# where all cards' labels are distinct: 23456 Hands are primarily ordered based on type; for
# example, every full house is stronger than any three of a kind.
#
# If two hands have the same type, a second ordering rule takes effect. Start by comparing the first
# card in each hand. If these cards are different, the hand with the stronger first card is
# considered stronger. If the first card in each hand have the same label, however, then move on to
# considering the second card in each hand. If they differ, the hand with the higher second card
# wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.
#
# So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is
# stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its
# third card is stronger (and both hands have the same first and second card).
#
# To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle
# input). For example:
#
# 32T3K 765 T55J5 684 KK677 28 KTJJT 220 QQQJA 483 This example shows five hands; each hand is
# followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank,
# where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the
# strongest hand. Because there are five hands in this example, the strongest hand will have rank 5
# and its bid will be multiplied by 5.
#
# So, the first step is to put the hands in order of strength:
#
# 32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1. KK677
# and KTJJT are both two pair. Their first cards both have the same label, but the second card of
# KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3. T55J5 and QQQJA are both
# three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4. Now,
# you can determine the total winnings of this set of hands by adding up the result of multiplying
# each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total
# winnings in this example are 6440.
#
# Find the rank of every hand in your set. What are the total winnings?
# Answer for sample input: 6440
# Answer for input: 251287184

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

    return all(c == hand[0] for c in hand)

def is_four_of_a_kind(hand) -> bool:
    """
    Checks if a hand is a four of a kind
    """

    return any(hand.count(c) == 4 for c in hand)

def is_full_house(hand) -> bool:
    """
    Checks if a hand is a full house
    """

    return any(hand.count(c) == 3 for c in hand) and any(hand.count(c) == 2 for c in hand)

def is_three_of_a_kind(hand) -> bool:
    """
    Checks if a hand is a three of a kind
    """

    return any(hand.count(c) == 3 for c in hand)

def is_two_pair(hand) -> bool:
    """
    Checks if a hand is a two pair
    """

    pairs = [c for c in set(hand) if hand.count(c) == 2]
    return len(pairs) == 2

def is_one_pair(hand) -> bool:
    """
    Checks if a hand is a one pair
    """

    return any(hand.count(c) == 2 for c in hand)

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
        return 11
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

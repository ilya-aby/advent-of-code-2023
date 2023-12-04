# --- Part Two ---
# Just as you're about to report your findings to the Elf, one of you realizes that the rules have actually been printed on the back of every card this whole time.

# There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.

# Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

# Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win any more cards. (Cards will never make you copy a card past the end of the table.)

# This time, the above example goes differently:

# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
# Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
# Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
# Your copy of card 2 also wins one copy each of cards 3 and 4.
# Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
# Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
# Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
# Your one instance of card 6 (one original) has no matching numbers and wins no more cards.
# Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!

# Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of scratchcards, how many total scratchcards do you end up with?

FILENAME = 'input.txt'

# Ingest input file
try:
    with open(FILENAME, 'r') as f:
        data = f.read().splitlines()
except FileNotFoundError:
    print(f"File {FILENAME} not found.")
    exit(1)

def card_parser(data):
    """
    Parses a card file into a array. Each element of the array has two lists: a winning numbers list and a your numbers list 
    """
    cards = []

    for line in data:
        # Splits on the first colon to ditch the game ID string, then splits the second part on the pipe
        # Sample string: 'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53'
        winning_numbers, your_numbers = line.split(':', 1)[1].split('|')
        cards.append((
            [int(num) for num in winning_numbers.split()],
            [int(num) for num in your_numbers.split()]
        ))
    return cards

def get_card_score(card):
    """
    Returns the score of a card.
    """
    matches = 0
    for num in card[1]:
        if num in card[0]:
            matches += 1

    return matches

cards = card_parser(data)

card_counts = {}

# Initialize card count dictionary
for cardID, card in enumerate(cards):
    card_counts[cardID] = 1

# Iterate through cards, get value of each, increment subsequent card counts
for cardID, card in enumerate(cards):
    score = get_card_score(card)

    for i in range(score):
        card_counts[cardID + i + 1] += 1 * card_counts[cardID]

# Sum up card counts
print(f"Sum of total scratchcards: {sum(card_counts.values())}")
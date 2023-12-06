# --- Day 2: Cube Conundrum ---
# You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.
#
# The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. They don't get many visitors up here; would you like to play a game in the meantime?
#
# As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.
#
# To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.
#
# You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).
#
# For example, the record of a few games might look like this:
#
# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.
#
# The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
#
# In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.
#
# Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
# 
# Answer for sample input: 8
# Answer for input: 2632

import re

FILENAME = 'input.txt'
BAG_CONTENTS = {'red': 12, 'green': 13, 'blue': 14}

# Ingest input file
try:
    with open(FILENAME, 'r') as f:
        data = f.read().splitlines()
except FileNotFoundError:
    print(f"File {FILENAME} not found.")
    exit(1)

# Helper function to take a game text file and break it down into game events stored in a dictionary
def game_parser(game_file):
    game_dict = {}
    game_id = 1

    # Clean up each row in the game text file and store it in a dictionary
    # Sample game string: 'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'
    # Cube color revelations are separated by '; '
    for line in game_file:
        game_dict[game_id] = {}

        # Split the string into a list of cube color revelations
        # For instance, a reveal will look like: '3 blue, 4 red'
        cube_reveals = line.split('; ')

        # For each cube reveal string, turn it into a dictionary of cube colors and their counts
        reveal_id = 1
        for reveal in cube_reveals:
            game_dict[game_id][reveal_id] = {'red': 0, 'green': 0, 'blue': 0}

            # User regexp to find the number of cubes of each color
            reveal_colors = re.findall(r'(\d+) (red|blue|green)', reveal)

            for count, color in reveal_colors:
                game_dict[game_id][reveal_id][color] = int(count)
            reveal_id += 1
        game_id += 1
    return game_dict

# Iterate through each game and each reveal in each game
# If we ever exceed the number of cubes in the bag, mark that as an impossible game
games = game_parser(data)
sum_possible_game_ids = 0

print(f"Cubes in bag: {BAG_CONTENTS}")
for game_id, game in games.items():
    game_is_possible = True
    for reveal_id, reveal in game.items():
        if reveal['red'] > BAG_CONTENTS['red'] or reveal['blue'] > BAG_CONTENTS['blue'] or reveal['green'] > BAG_CONTENTS['green']:
            print(f"Game {game_id} is impossible because of this reveal: {reveal}.")
            game_is_possible = False
            break
    if(game_is_possible):
        sum_possible_game_ids += game_id

print(f"Sum of possible game IDs: {sum_possible_game_ids}")
# --- Part Two ---
# The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!
#
# As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?
#
# Again consider the example games from earlier:
#
# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
# Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
# Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
# Game 4 required at least 14 red, 3 green, and 15 blue cubes.
# Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.
#
# For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
#
# Answer for sample input: 2286
# Answer for input: 69629

import re

FILENAME = 'input.txt'

# Ingest input file
try:
    with open(FILENAME, 'r') as f:
        data = f.read().splitlines()
except FileNotFoundError:
    print(f"File {FILENAME} not found.")
    exit(1)

def game_parser(game_file):
    """
    Parses a game text file and returns a dictionary representation of the games.
    """
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

def game_power(game):
    """
    Calculates the "power" of a game, defined as the product of the minimum number of each color cube needed.
    """
    cube_minimums = {'red': 0, 'green': 0, 'blue': 0}

    for reveal_id, reveal in game.items():
        for color in ['red', 'green', 'blue']:
            if game[reveal_id][color] > cube_minimums[color]:
                cube_minimums[color] = game[reveal_id][color]

    return cube_minimums['red'] * cube_minimums['green'] * cube_minimums['blue']


games = game_parser(data)

# Sum up the game powers for each game
sum_of_game_powers = 0
for game in games:
    game_power_value = game_power(games[game])
    sum_of_game_powers += game_power_value
    print(f"Game {game} power: {game_power_value}")

print(f"Sum of game powers: {sum_of_game_powers}")
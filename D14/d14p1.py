"""
This module solves Part One of Day 14's problem of the Advent of Code challenge.
Insight here was that we have to roll by working backwards from the end of the row back to the
first element since the rocks stack up behind each other.
"""
# --- Day 14: Parabolic Reflector Dish ---
# You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish
# attached to the side of another large mountain.
#
# The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the
# shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the
# wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a
# vague direction.
#
# This system must be what provides the energy for the lava! If you focus the reflector dish, maybe
# you can go where it's pointing and use the light to fix the lava production.
#
# Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system
# of ropes and pulleys to a large metal platform below the dish. The platform is covered in large
# rocks of various shapes. Depending on their position, the weight of the rocks deforms the
# platform, and the shape of the platform controls which ropes move and ultimately the focus of the
# dish.
#
# In short: if you move the rocks, you can focus the dish. The platform even has a control panel on
# the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the
# platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of
# all of the empty spaces (.) and rocks (your puzzle input). For example:
#
# O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....
# Start by tilting the lever so all of the rocks will slide north as far as they will go:
#
# OOOO.#.O..
# OO..#....#
# OO..O##..O
# O..#.OO...
# ........#.
# ..#....#.#
# ..O..#.O.O
# ..O.......
# #....###..
# #....#....
# You notice that the support beams along the north side of the platform are damaged; to ensure the
# platform doesn't collapse, you should calculate the total load on the north support beams.
#
# The amount of load caused by a single rounded rock (O) is equal to the number of rows from the
# rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#)
# don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:
#
# OOOO.#.O.. 10
# OO..#....#  9
# OO..O##..O  8
# O..#.OO...  7
# ........#.  6
# ..#....#.#  5
# ..O..#.O.O  4
# ..O.......  3
# #....###..  2
# #....#....  1
# The total load is the sum of the load caused by all of the rounded rocks. In this example, the
# total load is 136.
#
# Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on
# the north support beams?
#
# Answer for sample input: 136
# Answer for input: 103614

import copy

FILENAME = 'input.txt'

def parse_input(file_name: str) -> list[list[str]]:
    """
    Parses pattern records from input file
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    
    # Read all the lines into a 2D list
    rock_map = [list(line) for line in data]

    return rock_map            

def rotate_rocks(rock_map: list[list[str]], rotations: int) -> list[list[str]]:
    """
    Rotates a rock list 90 degrees clockwise for a given number of rotations
    """
    for _ in range(rotations):
        rock_map = [list(reversed(i)) for i in zip(*rock_map)]
    return rock_map

def roll_rocks(rock_map: list[list[str]], direction:str) -> list[list[str]]:
    """
    Rolls the rocks in the rock map and returns the rolled rocks
    """
    
    # We add support for the other directions in part 2
    if direction == "N":
        rotations = 1
    
    rotated_rocks = copy.deepcopy(rotate_rocks(rock_map, rotations))
    
    width = len(rotated_rocks[0])
    for row_id in range(len(rotated_rocks)):
        # Scan backwards from the end of the row to the first element
        for col_id in range(width - 2, -1, -1):
            spaces_rolled = 0
            # Only roll round rocks
            if rotated_rocks[row_id][col_id] in ("#","."):
                continue
            # Scan from here to the end of the row to find out how far to roll
            for col_id2 in range(col_id+1, width):
                # We hit a stopping point
                if rotated_rocks[row_id][col_id2] in ("#", "O"):
                    roll_destination_col_id = col_id2 - 1
                    break
                # We hit the edge and should stop here
                if col_id2 == width - 1:
                    roll_destination_col_id = col_id2
                    spaces_rolled += 1
                    break
                spaces_rolled += 1
            # If we rolled, we need to update the column
            if spaces_rolled > 0:
                rotated_rocks[row_id][col_id] = "."
                rotated_rocks[row_id][roll_destination_col_id] = "O"
                
    return rotated_rocks

def compute_load(rock_map: list[list[str]]) -> int:
    """
    Computes the total load of the rock map
    Assumes it's always rotated so that load of each rock is its column value + 1
    """
    load = 0
    for row in rock_map:
        for col_id, rock in enumerate(row):
            if rock == "O":
                load += col_id + 1
    return load

def main():
    """
    Main function that reads the file, rolls the rocks and gets the total load
    """
    rock_map = parse_input(FILENAME)
    
    rolled_rocks = roll_rocks(rock_map,"N")
    
    load = compute_load(rolled_rocks)
    
    print(f'Total load: {load}')

if __name__ == "__main__":
    main()

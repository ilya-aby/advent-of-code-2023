"""
This module solves Part Two of Day 14's problem of the Advent of Code challenge.
The main difference here is that we have to do cycle detection to get to 1Bn cycles without actually
rolling the rocks. This is done by rolling the rocks until we get back to the first pattern again
and then figuring out the periodicity of the cycle. We can then roll the rocks the remaining number
of cycles. We also extended the roll_rocks function to support rolling in all four directions.
"""
# --- Part Two ---
# The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll
# need to move the rocks to the edges of the platform. Fortunately, a button on the side of the
# control panel labeled "spin cycle" attempts to do just that!
#
# Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then
# south, then east. After each tilt, the rounded rocks roll as far as they can before the platform
# tilts in the next direction. After one cycle, the platform will have finished rolling the rounded
# rocks in those four directions in that order.
#
# Here's what happens in the example above after each of the first few cycles:
#
# After 1 cycle:
# .....#....
# ....#...O#
# ...OO##...
# .OO#......
# .....OOO#.
# .O#...O#.#
# ....O#....
# ......OOOO
# #...O###..
# #..OO#....
#
# After 2 cycles:
# .....#....
# ....#...O#
# .....##...
# ..O#......
# .....OOO#.
# .O#...O#.#
# ....O#...O
# .......OOO
# #..OO###..
# #.OOO#...O
#
# After 3 cycles:
# .....#....
# ....#...O#
# .....##...
# ..O#......
# .....OOO#.
# .O#...O#.#
# ....O#...O
# .......OOO
# #...O###.O
# #.OOO#...O
# This process should work if you leave it running long enough, but you're still worried about the
# north support beams. To make sure they'll survive for a while, you need to calculate the total
# load on the north support beams after 1000000000 cycles.
#
# In the above example, after 1000000000 cycles, the total load on the north support beams is 64.
#
# Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support
# beams?
#
# Answer for sample input: 64
# Answer for input: 83790

import copy
from tqdm import tqdm

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
    
    rotations = {'N': 1, 'E': 0, 'S': 3, 'W': 2}
    
    rotated_rocks = copy.deepcopy(rotate_rocks(rock_map, rotations[direction]))
    
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
    
    # Rotate back to normal orientation
    return rotate_rocks(rotated_rocks, 4 - rotations[direction])
    

def roll_rocks_one_cycle(rock_map: list[list[str]]) -> list[list[str]]:
    """
    Rolls the rocks in the rock map one cycle and returns the rolled rocks
    """
    
    rolled_rocks = copy.deepcopy(rock_map)
    
    # Roll north
    rolled_rocks = roll_rocks(rolled_rocks, "N")
    
    # Roll east
    rolled_rocks = roll_rocks(rolled_rocks, "W")
    
    # Roll south
    rolled_rocks = roll_rocks(rolled_rocks, "S")
    
    # Roll west
    rolled_rocks = roll_rocks(rolled_rocks, "E")
    
    return rolled_rocks

def compute_load(rock_map: list[list[str]]) -> int:
    """
    Computes the total load of the rock map
    Rocks in the top row are worth total row count - current row index
    """
    load = 0
    for row_id, row in enumerate(rock_map):
        for rock in row:
            if rock == "O":
                load += len(rock_map) - row_id
    return load

def main():
    """
    Main function that reads the file, rolls the rocks and gets the total load
    Does cycle detection to get to 1Bn cycles without actually rolling the rocks
    """
    rock_map = parse_input(FILENAME)
    rolled_rocks = rock_map
    
    rock_cache = {}
    
    # Find the first pattern cycle
    cycles = 1
    cycle_start = []
    while True:
        if str(rolled_rocks) in rock_cache:
            cycle_start = rolled_rocks
            break
        new_rolled_rocks = roll_rocks_one_cycle(rolled_rocks)
        rock_cache[str(rolled_rocks)] = new_rolled_rocks
        rolled_rocks = new_rolled_rocks
        cycles += 1
    
    # We've now found a complete list of all the rock maps
    # Now we need to find the periodicity of the cycle
    # We can do this by rolling the rocks until we get back to the first pattern again
    cycle_period = 0
    while True:
        rolled_rocks = rock_cache[str(rolled_rocks)]
        cycle_period += 1
        if rolled_rocks == cycle_start:
            break
    
    target = 1_000_000_000
    needed_cycles = (target - cycles - cycle_period) % cycle_period + 1 
    
    # Now we need to roll the rocks the remaining number of cycles
    # We can do this by rolling the rocks until we get back to the first pattern again
    for _ in tqdm(range(needed_cycles)):
        rolled_rocks = rock_cache[str(rolled_rocks)]
    
    print(f'{compute_load(rolled_rocks)}')

if __name__ == "__main__":
    main()

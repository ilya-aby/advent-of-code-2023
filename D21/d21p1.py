"""
This module solves Part One of Day 21's problem of the Advent of Code challenge.
Just a simple iterative approach to parse every possible location, get its next state, and repeat
"""
# --- Day 21: Step Counter ---
# You manage to catch the airship right as it's dropping someone else off on their all-expenses-paid
# trip to Desert Island! It even helpfully drops you off near the gardener and his massive farm.
#
# "You got the sand flowing again! Great work! Now we just need to wait until we have enough sand to
# filter the water for Snow Island and we'll have snow again in no time."
#
# While you wait, one of the Elves that works with the gardener heard how good you are at solving
# problems and would like your help. He needs to get his steps in for the day, and so he'd like to
# know which garden plots he can reach with exactly his remaining 64 steps.
#
# He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (.),
# and rocks (#). For example:
#
# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take
# one step north, south, east, or west, but only onto tiles that are garden plots. This would allow
# him to reach any of the tiles marked O:
#
# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#O#....
# .##.OS####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# Then, he takes a second step. Since at this point he could be at either tile marked O, his second
# step would allow him to reach any garden plot that is one step north, south, east, or west of any
# tile that he could have reached after the first step:
#
# ...........
# .....###.#.
# .###.##..#.
# ..#.#O..#..
# ....#.#....
# .##O.O####.
# .##.O#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........
# After two steps, he could be at any of the tiles marked O above, including the starting position
# (either by going north-then-south or by going west-then-east).
#
# A single third step leads to even more possibilities:
#
# ...........
# .....###.#.
# .###.##..#.
# ..#.#.O.#..
# ...O#O#....
# .##.OS####.
# .##O.#...#.
# ....O..##..
# .##.#.####.
# .##..##.##.
# ...........
# He will continue like this until his steps for the day have been exhausted. After a total of 6
# steps, he could reach any of the garden plots marked O:
#
# ...........
# .....###.#.
# .###.##.O#.
# .O#O#O.O#..
# O.O.#.#.O..
# .##O.O####.
# .##.O#O..#.
# .O.O.O.##..
# .##.#.####.
# .##O.##.##.
# ...........
# In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to
# reach any of 16 garden plots.
#
# However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger
# than the example map.
#
# Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in
# exactly 64 steps?

from icecream import ic

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    with open(filename, 'r') as file:
        data = file.read().splitlines()

    return ic(data)

def find_steps(garden):
    """
    Steps through the garden array and returns the number of possible positions after 64 steps
    """
    
    # Find the starting position, marked by 'S' in the grid:
    start_row = None
    start_col = None
    for row, line in enumerate(garden):
        if 'S' in line:
            start_row = row
            start_col = line.index('S')
            break
    
    position = (start_row, start_col)

    current_positions = [position]
    steps_taken = 0
    
    while True:
        # Find all possible positions we can reach in the next step
        # This is any position that is one step north, south, east, or west of any possible
        # Locations we could have been at right now
        next_positions = []
        for pos in current_positions:
            for new_row, new_col in [(pos[0],pos[1]+1),
                                     (pos[0],pos[1]-1),
                                     (pos[0]+1,pos[1]),
                                     (pos[0]-1,pos[1])]:
                if is_valid_position(garden, (new_row, new_col)):
                    next_positions.append((new_row, new_col))
                
        current_positions = set(next_positions)
        steps_taken += 1

        
        # If we can't move anywhere, we're done
        if not next_positions:
            break
        if steps_taken == 64:
            break
        
    return len(current_positions)

def is_valid_position(garden, position):
    """
    Checks if a given position is valid to step to in the garden
    """
    row, col = position
    if row < 0 or row >= len(garden):
        return False
    if col < 0 or col >= len(garden[0]):
        return False
    if garden[row][col] == '#':
        return False
    return True

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    garden = parse_input("input.txt")
    print(find_steps(garden))

if __name__ == "__main__":
    main()

"""
This module solves Part One of Day 11's problem of the Advent of Code challenge.
No major trick to this one, just bookkeeping to keep track of the star map and the
galaxy coordinates. The distance calc is simple Manhattan distance. Manhattan distance is 
the sum of the absolute values of the differences of the x and y coordinates.
"""
# --- Day 11: Cosmic Expansion ---
# You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf
# within turns out to be a researcher studying cosmic expansion using the giant telescope here.
#
# He doesn't know anything about the missing machine parts; he's only visiting for this research
# project. However, he confirms that the hot springs are the next-closest area likely to have
# people; he'll even take you straight there once he's done with today's observation analysis.
#
# Maybe you can help him with the analysis to speed things up?
#
# The researcher has collected a bunch of data and compiled the data into a single giant image (your
# puzzle input). The image includes empty space (.) and galaxies (#). For example:
#
# ...#......
# .......#..
# #.........
# ..........
# ......#...
# .#........
# .........#
# ..........
# .......#..
# #...#.....
# The researcher is trying to figure out the sum of the lengths of the shortest path between every
# pair of galaxies. However, there's a catch: the universe expanded in the time it took the light
# from those galaxies to reach the observatory.
#
# Due to something involving gravitational effects, only some space expands. In fact, the result is
# that any rows or columns that contain no galaxies should all actually be twice as big.
#
# In the above example, three columns and two rows contain no galaxies:
#
#    v  v  v
#  ...#......
#  .......#..
#  #.........
# >..........<
#  ......#...
#  .#........
#  .........#
# >..........<
#  .......#..
#  #...#.....
#    ^  ^  ^
# These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:
#
# ....#........
# .........#...
# #............
# .............
# .............
# ........#....
# .#...........
# ............#
# .............
# .............
# .........#...
# #....#.......
# Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:
#
# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# ............6
# .............
# .............
# .........7...
# 8....9.......
# In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't
# matter. For each pair, find any shortest path between the two galaxies using only steps that move
# up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is
# allowed to pass through another galaxy.)
#
# For example, here is one of the shortest paths between galaxies 5 and 9:
#
# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# .##.........6
# ..##.........
# ...##........
# ....##...7...
# 8....9.......
# This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9
# (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example
# shortest path lengths:
#
# Between galaxy 1 and galaxy 7: 15
# Between galaxy 3 and galaxy 6: 17
# Between galaxy 8 and galaxy 9: 5
# In this example, after expanding the universe, the sum of the shortest path between all 36 pairs
# of galaxies is 374.
#
# Expand the universe, then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?


#
# Your puzzle answer was 9536038.
# Answer for sample input: 374
# Answer for input: 9536038

FILENAME = 'sample input.txt'

def parse_input(file_name: str) -> list[list[str]]:
    """
    Parses a star map file and returns a list of lists containing the star map characters
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    
    star_map = [list(line.strip()) for line in data]

    return star_map

def expand_map(star_map: list[list[str]]) -> list[list[str]]:
    """
    Expands the star map by adding one row/col for each row/col that doesn't contain a galaxy
    """
    
    new_star_map = []
    for row in star_map:
        new_star_map.append(row)
        if '#' not in row:
            new_star_map.append(['.'] * len(row))

    star_map = new_star_map

    star_map = new_star_map
    added_cols = 0

    new_star_map = [row.copy() for row in star_map]

    for col in range(len(star_map[0])):
        if '#' not in [row[col] for row in star_map]:
            added_cols += 1
            for row in new_star_map:
                row.insert(col+added_cols, '.')

    return new_star_map

def get_galaxy_coords(star_map: list[list[str]]) -> list[tuple[int, int]]:
    """
    Returns the coordinates of all the # galaxy characters in the star map
    """
    galaxy_coords = []
    for row_idx, row in enumerate(star_map):
        for col_idx, col in enumerate(row):
            if col == '#':
                galaxy_coords.append((row_idx, col_idx))

    return galaxy_coords

def get_sum_shortest_paths(galaxy_coords: list[tuple[int, int]]) -> int:
    """
    Returns the sum of the shortest paths from the galaxy coordinates to all other galaxy 
    coordinates
    """
    shortest_paths = []
    for i, galaxy_one in enumerate(galaxy_coords):
        for galaxy_two in galaxy_coords[i+1:]:
            x_diff = abs(galaxy_one[0] - galaxy_two[0])
            y_diff = abs(galaxy_one[1] - galaxy_two[1])
            shortest_paths.append(x_diff + y_diff)

    return sum(shortest_paths)

def main():
    """
    Main function that reads the input file, parses the starmap, and finds sum of shortest paths
    """
    star_map = parse_input(FILENAME)

    star_map = expand_map(star_map)
    print('Expanded Star Map:')
    for row in star_map:
        print(''.join(row))
    print("\n")

    print(f'Sum of shortest paths: {get_sum_shortest_paths(get_galaxy_coords(star_map))}')

if __name__ == "__main__":
    main()

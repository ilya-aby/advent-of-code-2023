"""
This module solves Part One of Day 13's problem of the Advent of Code challenge.

"""
# --- Day 13: Point of Incidence ---
# With your help, the hot springs team locates an appropriate spring which launches you neatly and
# precisely up to the edge of Lava Island.
#
# There's just one problem: you don't see any lava.
#
# You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered
# around. After a while, you make your way to a nearby cluster of mountains only to discover that
# the valley between them is completely full of large mirrors. Most of the mirrors seem to be
# aligned in a consistent way; perhaps you should head in that direction?
#
# As you move through the valley of mirrors, you find that several of them have fallen from the
# large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of
# the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one
# color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.
#
# You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input);
# perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!
#
# For example:
#
# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.
#
# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#
# To find the reflection in each pattern, you need to find a perfect reflection across either a
# horizontal line between two rows or across a vertical line between two columns.
#
# In the first pattern, the reflection is across a vertical line between two columns; arrows on each
# of the two columns point at the line between the columns:
#
# 123456789
#     ><   
# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.
#     ><   
# 123456789
# In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the
# vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has
# nowhere to reflect onto and can be ignored; every other column has a reflected column within the
# pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5
# matches 6.
#
# The second pattern reflects across a horizontal line instead:
#
# 1 #...##..# 1
# 2 #....#..# 2
# 3 ..##..### 3
# 4v#####.##.v4
# 5^#####.##.^5
# 6 ..##..### 6
# 7 #....#..# 7
# This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a
# hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The
# remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.
#
# To summarize your pattern notes, add up the number of columns to the left of each vertical line of
# reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of
# reflection. In the above example, the first pattern's vertical line has 5 columns to its left and
# the second pattern's horizontal line has 4 rows above it, a total of 405.
#
# Find the line of reflection in each of the patterns in your notes. What number do you get after
# summarizing all of your notes?
#
# Answer for sample input: 405
# Answer for input: 30535

import sys
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
    
    # Patterns are separated by blank lines
    patterns = []
    pattern = []
    for line in data:
        if line:
            pattern.append(line)
        else:
            if pattern:
                patterns.append(pattern)
                pattern = []

    # Append the last pattern if it wasn't followed by a blank line
    if pattern:
        patterns.append(pattern)

    return patterns            

def rotate_pattern(pattern: list[str]) -> list[str]:
    """
    Rotates a pattern 90 degrees clockwise
    """
    return [''.join(reversed(i)) for i in zip(*pattern)]

def are_subsegments_mirrors(set_one, set_two) -> bool:
    """
    Validates whether two sets of mirrors are valid mirrors of each other
    """
    for i, value in enumerate(set_one):
        if i > len(set_two) - 1:
            return True
        if value != set_two[i]:
            return False
    
    return True

def find_mirror_line(pattern: list[str]) -> int:
    """
    Helper function to find a line of horizontal or vertical reflection in a pattern and return the
    index of the mirror position.
    """
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i+1]:
            # We're using ::-1 to reverse the second subset for the mirror comparison
            if are_subsegments_mirrors(pattern[0:i][::-1], pattern[i+2:]):
                return i + 1
    return -1


def get_mirror_value(pattern: list[str]) -> int:
    """
    Looks for a line of horizontal or vertical reflection in a pattern and returns the value of the
    mirror position.
    """
    # Get a 90 degree rotation of the pattern so we can avoid annoying index manipulation to look
    # for vertical lines of reflection
    rotated_pattern = rotate_pattern(pattern)

    mirror_line = find_mirror_line(pattern)
    if mirror_line != -1:
        return mirror_line * 100

    mirror_line = find_mirror_line(rotated_pattern)
    if mirror_line != -1:
        return mirror_line

    print(f'Failed to find mirror line in pattern {pattern}')
    sys.exit(1)

def main():
    """
    Main function that reads the pattern file, calcs sum of mirror positions
    """
    patterns = parse_input(FILENAME)
    
    mirror_values = []
    for pattern in tqdm(patterns):
        mirror_values.append(get_mirror_value(pattern))

    print(f'Sum of mirror values: {sum(mirror_values)}')

if __name__ == "__main__":
    main()

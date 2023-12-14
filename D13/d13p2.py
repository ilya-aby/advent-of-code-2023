"""
This module solves Part Two of Day 13's problem of the Advent of Code challenge.
We look for the smudge in the pattern that causes a different reflection line to be valid.
Only modification is that we need to make sure we scan for a new mirror value even if we find the
old value, since the smudge doesn't necessarily invalidate the old pattern.
"""
# --- Part Two ---
# You resume walking through the valley of mirrors and - SMACK! - run directly into one. Hopefully
# nobody was watching, because that must have been pretty embarrassing.
#
# Upon closer inspection, you discover that every mirror has exactly one smudge: exactly one . or #
# should be the opposite type.
#
# In each pattern, you'll need to locate and fix the smudge that causes a different reflection line
# to be valid. (The old reflection line won't necessarily continue being valid after the smudge is
# fixed.)
#
# Here's the above example again:
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
# The first pattern's smudge is in the top-left corner. If the top-left # were instead ., it would
# have a different, horizontal line of reflection:
#
# 1 ..##..##. 1
# 2 ..#.##.#. 2
# 3v##......#v3
# 4^##......#^4
# 5 ..#.##.#. 5
# 6 ..##..##. 6
# 7 #.#.##.#. 7
# With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows
# 3 and 4 now exists. Row 7 has no corresponding reflected row and can be ignored, but every other
# row matches exactly: row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.
#
# In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:
#
# 1v#...##..#v1
# 2^#...##..#^2
# 3 ..##..### 3
# 4 #####.##. 4
# 5 #####.##. 5
# 6 ..##..### 6
# 7 #....#..# 7
# Now, the pattern has a different horizontal line of reflection between rows 1 and 2.
#
# Summarize your notes as before, but instead use the new different reflection lines. In this
# example, the first pattern's new horizontal line has 3 rows above it and the second pattern's new
# horizontal line has 1 row above it, summarizing to the value 400.
#
# In each pattern, fix the smudge and find the different line of reflection. What number do you get
# after summarizing the new reflection line in each pattern in your notes?
#
# Answer for sample input: 400
# Answer for input: 30844

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
    
def get_mirror_value(pattern: list[str], original_value = None) -> int:
    """
    Looks for a line of horizontal or vertical reflection in a pattern and returns the value of the
    mirror position. Original Value can be passed in to ensure we will keep scanning for a mirror
    value even if we find the original one in the first pass, due to the fact that the smudge
    doesn't necessarily invalidate the old pattern
    """
    # Get a 90 degree rotation of the pattern so we can scan vertical/horizontal with one block
    # of code in one forward pass
    rotated_pattern = rotate_pattern(pattern)

    # Once we find a mirrored line, validate whether the mirrored lines radiating away from both
    # sides are also mirrored. If so, return the mirror value
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i+1]:
            # We're using ::-1 to reverse the second subset for the mirror comparison
            if are_subsegments_mirrors(pattern[0:i][::-1], pattern[i+2:]):
                value = (i + 1) * 100
                if not original_value or value != original_value:
                    return value 
    for i in range(len(rotated_pattern) - 1):
        if rotated_pattern[i] == rotated_pattern[i+1]:
            if are_subsegments_mirrors(rotated_pattern[0:i][::-1], rotated_pattern[i+2:]):
                value = i + 1
                if not original_value or value != original_value:
                    return value 

    return 0

def get_smudge_value(pattern: list[str]) -> int:
    """
    Looks for a symbol that, if flipped, would change the mirror index of the given pattern
    This is just doing a naive search of flipping each character and checking the mirror value
    changes from the original. Surprisingly, this was more than fast enough and didn't require
    caching or anything clever.
    """
    
    original_mirror_value = get_mirror_value(pattern)
    
    # Start by trying naive solution of flipping each char and checking the mirror value
    for i, row in enumerate(pattern):
        for j, char in enumerate(row):
            # Create a new row with the flipped character
            new_row = row[:j] + ('#' if char == '.' else '.') + row[j+1:]
            # Create a new pattern with the modified row
            new_pattern = pattern[:i] + [new_row] + pattern[i+1:]
            new_mirror_value = get_mirror_value(new_pattern, original_mirror_value)
            if new_mirror_value != original_mirror_value and new_mirror_value != 0:
                return new_mirror_value
            
    print(f'ERROR: No smudge value found for pattern {pattern}')
    sys.exit(1)

def main():
    """
    Main function that reads the pattern file, calcs sum of mirror positions
    """
    patterns = parse_input(FILENAME)
    
    mirror_values = []
    for pattern in tqdm(patterns):
        mirror_values.append(get_smudge_value(pattern))

    print(f'Sum of mirror values: {sum(mirror_values)}')

if __name__ == "__main__":
    main()

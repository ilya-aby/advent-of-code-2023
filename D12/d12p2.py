"""
This module solves Part Two of Day 12's problem of the Advent of Code challenge.
We've re-written the backtrack function here to consume the string from left to right and
backtrack over the substrings, instead of backtracking on the entire string and passing an index.
We check for validation as we go to not have to scan the entire parent string for validitity front
to back. We also use a cache to store the results of previous backtrack calls to avoid re-computing
the same subproblems. 
"""
# --- Part Two ---
# As you look out at the field of springs, you feel like there are way more springs than the
# condition records list. When you examine the records, you discover that they were actually folded
# up this whole time!
#
# To unfold the records, on each row, replace the list of spring conditions with five copies of
# itself (separated by ?) and replace the list of contiguous groups of damaged springs with five
# copies of itself (separated by ,).
#
# So, this row:
#
# .# 1
# Would become:
#
# .#?.#?.#?.#?.# 1,1,1,1,1
# The first line of the above example would become:
#
# ???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3
# In the above example, after unfolding, the number of possible arrangements for some rows is now
# much larger:
#
# ???.### 1,1,3 - 1 arrangement
# .??..??...?##. 1,1,3 - 16384 arrangements
# ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
# ????.#...#... 4,1,1 - 16 arrangements
# ????.######..#####. 1,6,5 - 2500 arrangements
# ?###???????? 3,2,1 - 506250 arrangements
# 
# After unfolding, adding all of the possible arrangement counts together produces 525152.
#
# Unfold your condition records; what is the new sum of possible arrangement counts?
#
# Answer for sample input: 525152
# Answer for input: 1566786613613

from functools import cache
from tqdm import tqdm

FILENAME = 'input.txt'

def parse_input(file_name: str) -> list[list[str]]:
    """
    Parses condition records from input file
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    

    spring_list = []
    condition_list = []
    for line in data:
        springs, conditions = line.split()
        # Modified for 5x expansion
        conditions = [int(condition) for condition in conditions.split(',')]
        condition_list.append(conditions * 5)
        spring_list.append('?'.join([springs] * 5))
    return spring_list, condition_list

@cache
def backtrack(spring_str, damage_groups, damaged_seen) -> int:
    """
    Performs a recrusive backtracking search on the given springs
    Consumes the string character by character and backtracks over the substrings
    Relies on cache to avoid re-computing solved subproblems
    """  
    # If we're at the end of the string, we're valid if we've seen all the broken springs we need to
    # and invalid otherwise
    if not spring_str:
        if len(damage_groups) == 0 or ((len(damage_groups) == 1) and damage_groups[0] == damaged_seen):
            return 1
        return 0

    # If we're at a known broken spring, we either:
    # 1) Know that we are invalid because we've seen too many broken springs vs. the expected number
    # 2) Know we could still be valid and backtrack over the rest of the string after incrementing
    # how many broken springs we've seen
    if spring_str[0] == '#':
        damaged_seen += 1
        # If that's too many broken springs, we're invalid
        if len(damage_groups) == 0 or damaged_seen > damage_groups[0]:
            return 0
        return backtrack(spring_str[1:], damage_groups, damaged_seen)
    # If we're at a known good spring, we either:
    # 1) Know that we are invalid because we just saw a too-short broken run vs. the expected number
    # 2) Know we could still be valid and are done consuming this group or we could still be 
    # short of the required number of broken springs and can backtrack over the rest of the string
    elif spring_str[0] == '.':
        if damaged_seen > 0 and damaged_seen != damage_groups[0]:
            return 0
        elif damaged_seen > 0 and damaged_seen == damage_groups[0]:
            return backtrack(spring_str[1:], damage_groups[1:], 0)
        else:
            return backtrack(spring_str[1:], damage_groups, 0)
        
    # If we're at an unknown '? character, we backtrack over the sum of both possible values
    return  backtrack('#' + spring_str[1:], damage_groups, damaged_seen) + \
            backtrack('.' + spring_str[1:], damage_groups, damaged_seen)

def get_sum_of_arrangements(spring_list, condition_list) -> int:
    """
    Returns the sum of the permutations of each list of springs
    """
    num_arrangements = []
    for i in tqdm(range(len(spring_list))):
        num_arrangements.append(backtrack(spring_list[i], tuple(condition_list[i]), 0))

    return sum(num_arrangements)

def main():
    """
    Main function that reads the input file, parses the springs, and finds sum of permutations
    """
    spring_list, condition_list = parse_input(FILENAME)

    print(f'Sum of arrangements: {get_sum_of_arrangements(spring_list, condition_list)}')

if __name__ == "__main__":
    main()

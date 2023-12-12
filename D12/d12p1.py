"""
This module solves Part One of Day 12's problem of the Advent of Code challenge.
This uses a backtracking approach to find the number of ways to arrange the springs.
It's very unoptimized because the is_valid function scans the entire string many times.
In part 2, we will further optimize this to get a large performance gain.
"""
# --- Day 12: Hot Springs ---
# You finally reach the hot springs! You can see steam rising from secluded areas attached to the
# primary, ornate building.
#
# As you turn to enter, the researcher stops you. "Wait - I thought you were looking for the hot
# springs, weren't you?" You indicate that this definitely looks like hot springs to you.
#
# "Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."
#
# You look in the direction the researcher is pointing and suddenly notice the massive metal helixes
# towering overhead. "This way!"
#
# It only takes you a few more steps to reach the main gate of the massive fenced-off area
# containing the springs. You go through the gate and into a small administrative building.
#
# "Hello! What brings you to the hot springs today? Sorry they're not very hot right now; we're
# having a lava shortage at the moment." You ask about the missing machine parts for Desert Island.
#
# "Oh, all of Gear Island is currently offline! Nothing is being manufactured at the moment, not
# until we get more lava to heat our forges. And our springs. The springs aren't very springy unless
# they're hot!"
#
# "Say, could you go up and see why the lava stopped flowing? The springs are too cold for normal
# operation, but we should be able to find one springy enough to launch you up there!"
#
# There's just one problem - many of the springs have fallen into disrepair, so they're not actually
# sure which springs would even be safe to use! Worse yet, their condition records of which springs
# are damaged (your puzzle input) are also damaged! You'll need to help them repair the damaged
# records.
#
# In the giant field just outside, the springs are arranged into rows. For each row, the condition
# records show every spring and whether it is operational (.) or damaged (#). This is the part of
# the condition records that is itself damaged; for some springs, it is simply unknown (?) whether
# the spring is operational or damaged.
#
# However, the engineer that produced the condition records also duplicated some of this information
# in a different format! After the list of springs for a given row, the size of each contiguous
# group of damaged springs is listed in the order those groups appear in the row. This list always
# accounts for every damaged spring, and each number is the entire size of its contiguous group
# (that is, groups are always separated by at least one operational spring: #### would always be 4,
# never 2,2).
#
# So, condition records with no unknown spring conditions might look like this:
#
# #.#.### 1,1,3
# .#...#....###. 1,1,3
# .#.###.#.###### 1,3,1,6
# ####.#...#... 4,1,1
# #....######..#####. 1,6,5
# .###.##....# 3,2,1
#
# However, the condition records are partially damaged; some of the springs' conditions are actually
# unknown (?). For example:
#
# ???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1
# 
# Equipped with this information, it is your job to figure out how many different arrangements of
# operational and broken springs fit the given criteria in each row.
#
# In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three
# broken springs (in that order) can appear in that row: the first three unknown springs must be
# broken, then operational, then broken (#.#), making the whole row #.#.###.
#
# The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different
# arrangements. The last ? must always be broken (to satisfy the final contiguous group of three
# broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be
# both broken springs or they would form a single contiguous group of two; if that were true, the
# numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are
# four possible arrangements of springs.
#
# The last line is actually consistent with ten different arrangements! Because the first number is
# 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or
# higher). However, the remaining run of unknown spring conditions have many different ways they
# could hold groups of two and one broken springs:
#
# ?###???????? 3,2,1
# .###.##.#...
# .###.##..#..
# .###.##...#.
# .###.##....#
# .###..##.#..
# .###..##..#.
# .###..##...#
# .###...##.#.
# .###...##..#
# .###....##.#
# In this example, the number of possible arrangements for each row is:
#
# ???.### 1,1,3 - 1 arrangement
# .??..??...?##. 1,1,3 - 4 arrangements
# ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
# ????.#...#... 4,1,1 - 1 arrangement
# ????.######..#####. 1,6,5 - 4 arrangements
# ?###???????? 3,2,1 - 10 arrangements
# Adding all of the possible arrangement counts together produces a total of 21 arrangements.
#
# For each row, count all of the different arrangements of operational and broken springs that meet
# the given criteria. What is the sum of those counts?
#
# Answer for sample input: 21
# Answer for input: 7110

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
        conditions = [int(condition) for condition in conditions.split(',')]
        condition_list.append(conditions)
        spring_list.append(springs)

    return spring_list, condition_list

def backtrack(springs, arrangements, index) -> int:
    """
    Performs a recrusive backtracking search on the given springs and arrangements starting 
    from the given index.
    """    
    
    # Base case: if we've reached the end of the springs list, check if the arrangement is valid
    if index == len(springs):
        if is_valid(springs, arrangements):
            return 1
        return 0
    
    # If we're at a known broken spring or empty space, no choice to make, just recurse
    if springs[index] in ('#','.'):
        return backtrack(springs, arrangements, index + 1)
    
    # Branch on the possible values of the spring
    spring_variant_one = springs[:index] + '#' + springs[index+1:]
    spring_variant_two = springs[:index] + '.' + springs[index+1:]
    
    return  backtrack(spring_variant_one, arrangements, index + 1) + \
            backtrack(spring_variant_two, arrangements, index + 1)
    
    
def is_valid(candidate_springs, arrangements):
    """
    Returns True if the candidate arrangement of springs is valid, False otherwise
    """

    # If we didn't allocate all broken strings, it's not valid
    if candidate_springs.count('#') != sum(arrangements):
        return False
    
    # For each group of # characters, make sure the amount matches the expected amount
    spring_groups = [group for group in candidate_springs.split('.') if group]
    for group_id, spring_group in enumerate(spring_groups):
        if spring_group.count('#') != arrangements[group_id]:
            return False

    return True

def get_sum_of_arrangements(spring_list, condition_list) -> int:
    """
    Returns the sum of the permutations of each list of springs
    """
    num_arrangements = []
    for i, springs in tqdm(enumerate(spring_list)):
        num_arrangements.append(backtrack(springs, condition_list[i], 0))

    return sum(num_arrangements)

def main():
    """
    Main function that reads the input file, parses the springs, and finds sum of permutations
    """
    spring_list, condition_list = parse_input(FILENAME)

    print(f'Sum of arrangements: {get_sum_of_arrangements(spring_list, condition_list)}')

if __name__ == "__main__":
    main()

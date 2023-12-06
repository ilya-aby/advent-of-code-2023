"""
This module solves Part Two of Day 6's problem of the Advent of Code challenge.
The main insight & improvement is that we can solve for the hold time that exactly gets us 
the record distance by realizing that this problem is just finding the roots of a polynomial
"""
# --- Part Two --- 
# As the race is about to start, you realize the piece of paper with race times and
# record distances you got earlier actually just has very bad kerning. There's really only one race
# - ignore the spaces between the numbers on each line.
#
# So, the example from before:
#
# Time:      7  15   30 
# Distance:  9  40  200 ...now instead means this:
#
# Time:      71530 Distance:  940200 
# 
# Now, you have to figure out how many ways there are to win this
# single race. In this example, the race lasts for 71530 milliseconds and the record distance you
# need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516
# milliseconds and beat the record, a total of 71503 ways!
#
# How many ways can you beat the record in this one much longer race?
#
# Answer for sample input: 71503
# Answer for input: 49240091

import time
import math

FILENAME = 'input.txt'

def race_parser(file_name):
    """
    Parses a race record file into a time and distance
    """
    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            race_data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    
    race_time = int(''.join(race_data[0].split()[1:]))
    race_distance = int(''.join(race_data[1].split()[1:]))

    return race_time, race_distance

def ways_to_win(race_time, race_distance):
    """
    First, solve the hold time that exactly gets you the record distance
    hold time = record distance / (race time - hold time)
    For example, 7 second race, 10 m distance gets you 2 = 10 / (7 - 2))
    So you need to hold for 2 seconds to match that distance
    
    Solving for required hold gets you two polynomial roots
    h1 = t/2 - (t**2 - 4*r)**0.5/2
    h2 = t/2 + (t**2 - 4*r)**0.5/2
    So our ways to win is just the amount of integers between those values
    """
        
    h1 = math.ceil(race_time/2 - (race_time**2 - 4*race_distance)**0.5/2)
    h2 = math.floor(race_time/2 + (race_time**2 - 4*race_distance)**0.5/2)
    
    return h2 - h1 + 1

def main():
    """
    Main function that reads the input file, parses the time & distance
    and calculatesthe ways to win
    """
    
    start_time = time.time()
    race_time, race_distance = race_parser(FILENAME)
    print(f'Total ways to win: {ways_to_win(race_time, race_distance)}')
    elapsed_time = time.time() - start_time
    print(f"Execution time: {round(elapsed_time)*1000}ms")

if __name__ == "__main__":
    main()

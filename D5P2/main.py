"""
This module solves Part Two of Day 5's problem of the Advent of Code challenge.
The primary difference is that we now have a range of seeds to test, rather than a single seed.
This increase in the number of seeds to test makes the naive approach of testing each seed
in the range too slow. Improvements to performance in part 2 include using interval trees to map
values faster and a step search over the seed range to try to find the smallest location faster.
This takes about 50 seconds to solve & could be sped up with a more efficient seed search.
"""
# --- Part Two ---
# Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, 
# it looks like the seeds: line actually describes ranges of seed numbers.
#
# The values on the initial seeds: line come in pairs. Within each pair, the first value is the 
# start of the range and the second value is the length of the range. So, in the first line of the 
# example above:
#
# seeds: 79 14 55 13
# This line describes two ranges of seed numbers to be planted in the garden. The first range 
# starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts 
# with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.
#
# Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.
#
# In the above example, the lowest location number can be obtained from seed number 82, which
# corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and
# location 46. So, the lowest location number is 46.
#
# Consider all of the initial seed numbers listed in the ranges on the first line of the almanac.
# What is the lowest location number that corresponds to any of the initial seed numbers?
#
# Answer for sample input: 46
# Answer for input: 26714516

from intervaltree import IntervalTree
from tqdm import tqdm

FILENAME = 'input.txt'

def map_parser(file_name):
    """
    Parses a map file into a list 
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            map_data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e

    seeds = []
    maps = []
    current_map = []
    in_map = False

    for line in map_data:
        # Ignore empty lines
        if not line.strip():
            continue
        # If the line only contains the initial seed list, store that
        if 'seeds:' in line:
            seeds.extend([int(num) for num in line.split(':')[1].split()])
            continue

        # If the line contains a map heading, start ingesting the rows into the map entry
        if 'map:' in line:
            if in_map:  # if we were already in a map, add it to the list of maps
                maps.append(current_map)
                current_map = []  # start a new map
            in_map = True
        elif in_map:  # if we're in a map, add the line to the current map
            current_map.append(line.split())
    
    # Add the final map to the list
    if current_map:
        maps.append(current_map)
            
    return seeds, maps

def create_interval_trees(maps):
    """
    This function creates interval trees from the provided maps. Each map is converted into an
    interval tree where each interval represents a mapping from a source range to a destination
    offset. The resulting list of interval trees is returned.
    """
    interval_trees = []
    for map_instance in maps:
        tree = IntervalTree()
        for map_entry in map_instance:
            dest_start, src_start, range = map(int, map_entry)
            print(f"Adding interval {src_start}:{src_start + range - 1} -> {dest_start - src_start}")
            tree[src_start:src_start + range] = dest_start - src_start
        interval_trees.append(tree)
    return interval_trees

def traverse_maps(seed, interval_trees):
    """
    Traverses maps starting with the seed and returns the score of the final map.
    """
    value = seed

    for tree in interval_trees:
        intervals = tree.at(value)
        if intervals:
            value = intervals.pop().data + value

    return value


def process_seed_range(start_seed, end_seed, interval_trees):
    """
    This function processes a range of seeds from start_seed to end_seed using the provided interval
    trees. It traverses the maps starting with each seed and returns the smallest location found in
    the range.
    """
    print(f"Working on seeds {start_seed} to {end_seed}")
    
    # Quasi-binary search over the seed range
    smallest_location = None
    
    current_seed = start_seed
    previous_location = None
    previous_seed = None
    step_size = 100000
    
    while current_seed <= end_seed:
        location = traverse_maps(current_seed, interval_trees)
        
        # If this is the new smallest location, store it and keep going
        if smallest_location is None or location < smallest_location:
            smallest_location = location
            current_seed += 1
            continue
        
        # If we're increasing monotonically, try to jump many seeds ahead
        if previous_location is not None and location == previous_location + 1:
            previous_location = location
            previous_seed = current_seed
            current_seed = current_seed + step_size
            if current_seed > end_seed:
                current_seed = current_seed + 1
            continue
        
        # If we jumped too far, go back to the previous seed + 1
        if previous_seed is not None and location != previous_location + step_size:
            current_seed = previous_seed + 1
        
        previous_location = location
        previous_seed = current_seed
        
        current_seed = current_seed + 1
    return smallest_location


def main():
    """
    Main function that reads the input file, parses the cards, calculates the score for each card,
    and prints the total number of scratchcards.
    """

    seeds, maps = map_parser(FILENAME)

    smallest_locations = []
    interval_trees = create_interval_trees(maps)
 
    # The seeds list now contains a seed followed by a range, so we'll ingest two values at a time
    for seed_range in tqdm(range(0, len(seeds), 2)):
        start_seed = seeds[seed_range]
        end_seed = start_seed + seeds[seed_range+1] - 1
        smallest_locations.append(process_seed_range(start_seed, end_seed, interval_trees))
  
    print(f'Smallest location found: {min(smallest_locations)}')

if __name__ == "__main__":
    main()

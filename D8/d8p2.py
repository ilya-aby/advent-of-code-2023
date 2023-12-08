"""
This module solves Part Two of Day 8's problem of the Advent of Code challenge.
The main insight here is that we are running multiple cycles in parallel, but it may take an
infeasible amount of steps until they converge. Instead, we can find the cycle length for each
starting node, and then find the LCM of all of those cycle lengths to find the number of steps
needed until they all converge.
"""
# --- Part Two --- 
# The sandstorm is upon you and you aren't any closer to escaping the wasteland.
# You had the camel follow the instructions, but you've barely left your starting position. It's
# going to take significantly more steps to escape!

# What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the
# laws of spacetime? Only one way to find out.
#
# After examining the maps a bit longer, your attention is drawn to a curious fact: the number of
# nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd
# probably just start at every node that ends with A and follow all of the paths at the same time
# until they all simultaneously end up at nodes that end with Z.
#
# For example:
#
# LR
#
# 11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)
# Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each
# left/right instruction, use that instruction to simultaneously navigate away from both nodes
# you're currently on. Repeat this process until all of the nodes you're currently on end with Z.
# (If only some of the nodes you're on end with Z, they act like any other node and you continue as
# normal.) In this example, you would proceed as follows:

# Step 0: You are at 11A and 22A.
# Step 1: You choose all of the left paths, leading you to 11B and 22B.
# Step 2: You choose all of the right paths, leading you to 11Z and 22C.
# Step 3: You choose all of the left paths, leading you to 11B and 22Z.
# Step 4: You choose all of the right paths, leading you to 11Z and 22B.
# Step 5: You choose all of the left paths, leading you to 11B and 22C.
# Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
# So, in this example, you end up entirely on nodes that end in Z after 6 steps.
#
# Simultaneously start on every node that ends with A. How many steps does it take before you're
# only on nodes that end with Z?
# 
# Answer for sample input: 6
# Answer for input: 22103062509257

import math

FILENAME = 'input.txt'

def parse_map(file_name) -> dict:
    """
    Parses a map file and returns a dictionary of nodes and their connections
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            maps_data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    
    # Ingest the first line of the file into the steps list
    steps = maps_data.pop(0)
    
    # Ingest each line of the file into a dictionary entry with its paths and node type
    # Ignores the blank line at the start of the file
    maps = {}
    for line in maps_data[1:]:
        node_name, path_options = line.split(' = ')
        path_options = path_options.strip('()').split(', ')
        
        maps[node_name] = {
            'L': path_options[0], 
            'R': path_options[1],
            'start': node_name[-1] == 'A',
            'end': node_name[-1] == 'Z'
        }

    return maps, steps

def traverse_map(maps, steps) -> int:
    """
    Traverses a map in parallel for every start node and returns the number of steps needed to reach
    all end nodes at the same time
    """
    # Find all of the start nodes
    current_nodes = [node_name for node_name in maps if maps[node_name]['start']]
    
    # For each starting node, find the length of its cycle to reach the end node
    # At the end, we'll use the LCM of all of these cycle lengths to find the total number of steps
    # This is more efficient than actually running all the cycles and finding the first time they
    # all reach the end node
    cycle_lengths = []
    for node_name in current_nodes:
        step_count = 0
        current_node = node_name
        while not maps[current_node]['end']:
            current_node = maps[current_node][steps[step_count % len(steps)]]
            step_count += 1
        print(f'Cycle length for {node_name} to reach {current_node}: {step_count}')
        cycle_lengths.append(step_count)
    
    # The total number of steps needed is the LCM of all of the cycle lengths, since that's when
    # They'll all reach the end node at the same time
    return math.lcm(*cycle_lengths)

def main():
    """
    Main function that reads the input file, parses the maps, and traverses them
    """
    maps, steps = parse_map(FILENAME)
    steps_needed = traverse_map(maps, steps)
    print(f'Steps needed: {steps_needed}')
    
if __name__ == "__main__":
    main()

"""
This module solves Part One of Day 8's problem of the Advent of Code challenge.

"""
# --- Day 8: Haunted Wasteland --- 
# You're still riding a camel across Desert Island when you spot a
# sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To
# be fair, she had just finished warning you about ghosts a few minutes ago.
#
# One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle
# input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of
# the documents contains a list of left/right instructions, and the rest of the documents seem to
# describe some kind of network of labeled nodes.
#
# It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if
# you have the camel follow the same instructions, you can escape the haunted wasteland!
#
# After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where
# you are now, and you have to follow the left/right instructions until you reach ZZZ.
#
# This format defines each node of the network individually. For example:
#
# RL
#
# AAA = (BBB, CCC)
# BBB = (DDD, EEE)
# CCC = (ZZZ, GGG)
# DDD = (DDD, DDD)
# EEE = (EEE, EEE)
# GGG = (GGG, GGG)
# ZZZ = (ZZZ, ZZZ)
# Starting with AAA, you need to look up the next element based on the next left/right instruction
# in your input. In this example, start with AAA and go right (R) by choosing the right element of
# AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right
# instructions, you reach ZZZ in 2 steps.
#
# Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat
# the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on.
# For example, here is a situation that takes 6 steps to reach ZZZ:
#
# LLR
#
# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)
# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
# 
# Answer for sample input: 2
# Answer for input: 20093

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
        }

    return maps, steps

def traverse_map(maps, steps) -> int:
    """
    Traverses a map and returns the number of steps needed to reach the 'ZZZ' node from 'AAA'
    Repeat steps as necessary if 'ZZZ' has not been reached
    """
    current_node = 'AAA'
    step_count = 0
    
    while current_node != 'ZZZ':
        current_node = maps[current_node][steps[step_count % len(steps)]]
        step_count += 1
    
    return step_count

def main():
    """
    Main function that reads the input file, parses the maps, and traverses them
    """

    maps, steps = parse_map(FILENAME)
    steps_needed = traverse_map(maps, steps)
        
    print(f'Steps needed: {steps_needed}')
    
if __name__ == "__main__":
    main()

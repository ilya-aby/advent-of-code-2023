"""
This module solves Part One of Day 17's problem of the Advent of Code challenge.
Very brutal. Wasted a lot of time building & debugging a depth-first search, got it working
on the sample data, then realized it would take forever to run on the real data. Switched to
Dijkstra's algorithm, which I've never used before, and got it working. Main insight was that
we don't need to branch on one step at a time - we can always branch left & right and go some 
amount of steps between min and max. That made part 2 trivial, but part 1 was very tough.
"""
# --- Day 17: Clumsy Crucible ---
# The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave,
# the reindeer offers you a parachute, allowing you to quickly reach Gear Island.
#
# As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on
# your way up: half of Gear Island is empty, but the half below you is a giant factory city!
#
# You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will
# eventually carry the lava throughout the city, but to make use of it immediately, Elves are
# loading it into large crucibles on wheels.
#
# The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult
# to steer at high speeds, and so it can be hard to go in a straight line for very long.
#
# To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best
# way to get the crucible from the lava pool to the machine parts factory. To do this, you need to
# minimize heat loss while choosing a route that doesn't require the crucible to go in a straight
# line for too long.
#
# Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient
# temperature, and hundreds of other parameters to calculate exactly how much heat loss can be
# expected for a crucible entering any particular city block.
#
# For example:
#
# 2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533
# Each city block is marked by a single digit that represents the amount of heat loss if the
# crucible enters that block. The starting point, the lava pool, is the top-left city block; the
# destination, the machine parts factory, is the bottom-right city block. (Because you already start
# in the top-left block, you don't incur that block's heat loss unless you leave that block and then
# return to it.)
#
# Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it
# can move at most three blocks in a single direction before it must turn 90 degrees left or right.
# The crucible also can't reverse direction; after entering each city block, it may only turn left,
# continue straight, or turn right.
#
# One way to minimize heat loss is this path:
#
# 2>>34^>>>1323
# 32v>>>35v5623
# 32552456v>>54
# 3446585845v52
# 4546657867v>6
# 14385987984v4
# 44578769877v6
# 36378779796v>
# 465496798688v
# 456467998645v
# 12246868655<v
# 25465488877v5
# 43226746555v>
# This path never moves more than three consecutive blocks in the same direction and incurs a heat
# loss of only 102.
#
# Directing the crucible from the lava pool to the machine parts factory, but not moving more than
# three consecutive blocks in the same direction, what is the least heat loss it can incur?
#
# Your puzzle answer was 1244.

import heapq
from icecream import ic

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    
    data = open(filename).read().strip() ## Uncomment to split single-line by char: .split(',')
    lines = data.split('\n')
    output = [[int(val) for val in row] for row in lines]
    
    return output

def get_possible_moves(data, location, vector):
    """ 
    Helper function to return valid next steps & accumulated heat given a location and vector 
    """
    min_steps = 1
    max_steps = 3
    
    turn_left = { 'E': 'N', 'N': 'W', 'W': 'S', 'S': 'E' }
    turn_right = { 'E': 'S', 'S': 'W', 'W': 'N', 'N': 'E' }
    turn_vectors = { 'E': (0,1), 'N': (-1,0), 'W': (0,-1), 'S': (1,0) }

    # Get the vector to the left and right of the current vector
    left_turn = turn_vectors[turn_left[vector]]
    right_turn = turn_vectors[turn_right[vector]]
    left_vector = turn_left[vector]
    right_vector = turn_right[vector]
    
    # Special case: if we're at origin, our 'turn left' actually goes straight
    if location == (0,0):
        left_turn = turn_vectors[vector]
        left_vector = vector
    
    new_locations = []
    for i in range(min_steps, max_steps + 1):
        left_loc = (location[0] + (left_turn[0] * i),
                location[1] + (left_turn[1] * i))
        right_loc = (location[0] + (right_turn[0] * i),
                location[1] + (right_turn[1] * i))
        
        # Check bounds before calculating heat
        if 0 <= left_loc[0] < len(data) and 0 <= left_loc[1] < len(data[0]):
            left_heat = sum(data[loc[0]][loc[1]] 
                            for loc in [(location[0] + (left_turn[0] * j), location[1] + (left_turn[1] * j)) 
                                        for j in range(1, i+1)])
            new_locations.append([left_loc, left_vector, left_heat])
        
        if 0 <= right_loc[0] < len(data) and 0 <= right_loc[1] < len(data[0]):
            right_heat = sum(data[loc[0]][loc[1]] 
                             for loc in [(location[0] + (right_turn[0] * j), location[1] + (right_turn[1] * j)) 
                                         for j in range(1, i+1)])
            new_locations.append([right_loc, right_vector, right_heat])
    
    return new_locations

def dijkstra(data):
    """ 
    Does a breadth-first search with a priority queue to find the minimum heat loss to reach
    the final cell
    """
    queue = [(0, (0, 0), 'E')]  # (heat_loss, location, vector)

    # Initialize the minimum heat loss at each node to infinity
    min_heat_loss = [[[float('inf') for _ in range(4)] 
                      for _ in range(len(data[0]))] 
                     for _ in range(len(data))]

    # The minimum heat loss at the starting node is 0
    min_heat_loss[0][0][0] = 0  # 0 for 'E'

    while queue:
        heat_loss, location, vector = heapq.heappop(queue)
        
        # For each valid next step
        for new_loc, new_vector, new_heat_loss in get_possible_moves(data, location, vector):
            vector_index = {'E': 0, 'N': 1, 'W': 2, 'S': 3}[new_vector]

            # Calculate the new heat loss
            total_heat_loss = heat_loss + new_heat_loss

            # If the new heat loss is less than the current minimum heat loss at the new node, update it
            if total_heat_loss < min_heat_loss[new_loc[0]][new_loc[1]][vector_index]:
                min_heat_loss[new_loc[0]][new_loc[1]][vector_index] = total_heat_loss
                # Add the new node to the queue
                heapq.heappush(queue, (total_heat_loss, new_loc, new_vector))

    # The minimum heat loss to reach the final cell is the minimum heat loss at the final cell
    return min(min_heat_loss[-1][-1])

def debug_drive(data):
    location = (0,0)
    vector = 'E'
    heat = 0
    path = []
    while(True):
        print(f'You\'re at {location} facing {vector}. Heat is {heat}')

        ways_to_go = get_possible_moves(data, location, vector)
        for way_id, way in enumerate(ways_to_go):
            print(f'{way_id+1}. You can go to {way[0]} facing {way[1]}. Heat cost: {way[2]}')
        choice = input('Which way? ')
        if choice == '':
            break

        location = ways_to_go[int(choice)-1][0]
        vector = ways_to_go[int(choice)-1][1]
        path.append((location, vector))
        heat += ways_to_go[int(choice)-1][2]
        data[location[0]][location[1]] = 0
        # Print the grid
        for row in data:
            ic(row)
            

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    data = parse_input("input.txt")
    heat_loss = dijkstra(data)
    print(heat_loss)

if __name__ == "__main__":
    main()

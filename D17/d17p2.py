"""
This module solves Part Two of Day 17's problem of the Advent of Code challenge.
Given how I built part one, this was just a parameter change in the helper function on how far
to project ahead the possible moves when turning left or right.
"""
# --- Part Two ---
# The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the
# machine parts factory. Instead, the Elves are going to upgrade to ultra crucibles.
#
# Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have
# trouble going in a straight line, but they also have trouble turning!
#
# Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in
# that direction before it can turn (or even before it can stop at the end). However, it will
# eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive blocks
# without turning.
#
# In the above example, an ultra crucible could follow this path to minimize heat loss:
#
# 2>>>>>>>>1323
# 32154535v5623
# 32552456v4254
# 34465858v5452
# 45466578v>>>>
# 143859879845v
# 445787698776v
# 363787797965v
# 465496798688v
# 456467998645v
# 122468686556v
# 254654888773v
# 432267465553v
# In the above example, an ultra crucible would incur the minimum possible heat loss of 94.
#
# Here's another example:
#
# 111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991
# Sadly, an ultra crucible would need to take an unfortunate path like this one:
#
# 1>>>>>>>1111
# 9999999v9991
# 9999999v9991
# 9999999v9991
# 9999999v>>>>
# This route causes the ultra crucible to incur the minimum possible heat loss of 71.
#
# Directing the ultra crucible from the lava pool to the machine parts factory, what is the least
# heat loss it can incur?
#
# Your puzzle answer was 1367.
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
    min_steps = 4
    max_steps = 10
    
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

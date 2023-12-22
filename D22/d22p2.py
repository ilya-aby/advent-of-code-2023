"""
This module solves Part Two of Day 22's problem of the Advent of Code challenge.

Running the chain of disintegration actually runs quite quickly because we pre-compute the 
supporting structure of each brick and then run a breadth-first search over each brick to quickly
get the chain of bricks that would fall if it and other bricks it supports were disintegrated.

Also added 3D visualization of the prisms in matplotlib instead of lines.
"""
# --- Part Two ---
# Disintegrating bricks one at a time isn't going to be fast enough. While it might sound dangerous,
# what you really need is a chain reaction.
#
# You'll need to figure out the best brick to disintegrate. For each brick, determine how many other
# bricks would fall if that brick were disintegrated.
#
# Using the same example as above:
#
# Disintegrating brick A would cause all 6 other bricks to fall. Disintegrating brick F would cause
# only 1 other brick, G, to fall. Disintegrating any other brick would cause no other bricks to
# fall. So, in this example, the sum of the number of other bricks that would fall as a result of
# disintegrating each brick is 7.
#
# For each brick, determine how many other bricks would fall if that brick were disintegrated. What
# is the sum of the number of other bricks that would fall?
#
# Your puzzle answer was 80948.

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import cm
import matplotlib.pyplot as plt
from icecream import ic
from tqdm import tqdm

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    
    # Brick line format: 1,0,1~1,2,1
    with open(filename, 'r') as file:
        data = file.read().splitlines()
    
    bricks = {}
    
    for brick_id, line in enumerate(data):
        x1,y1,z1 = map(int, line.split('~')[0].split(','))
        x2,y2,z2 = map(int, line.split('~')[1].split(','))
        bricks[brick_id] = {'x1': x1, 'y1': y1, 'z1': z1, 
                            'x2': x2, 'y2': y2, 'z2': z2, 
                            'supporters':[], 'supporting': []}
    
    return bricks

def check_xy_collision(brick1, brick2):
    """
    Checks if two bricks collide in the x-y plane.
    Returns True if they collide, False otherwise.
    """
    return (max(brick1['x1'], brick2['x1']) <= min(brick1['x2'], brick2['x2'])) and \
           (max(brick1['y1'], brick2['y1']) <= min(brick1['y2'], brick2['y2']))

def get_bricks_below_z(bricks, z):
    """
    Returns all bricks where the minimum of 'z1' and 'z2' is below a certain value.
    Sorts the bricks by the minimum of 'z1' and 'z2' in descending order - in other words, highest
    bricks off the ground first. Used as helper function to sim_gravity()
    """
    bricks_below_z = {brick: brick_data for brick, brick_data in bricks.items() \
        if min(brick_data['z1'], brick_data['z2']) < z}
    return dict(sorted(bricks_below_z.items(), key=lambda item: max(item[1]['z1'], item[1]['z2']), reverse=True))

def sim_gravity(bricks):
    """
    Handles the simulation of initial gravity on the bricks to get them to their final resting
    """
    
    # Sort by z value 
    sorted_bricks = sorted(bricks.items(), key=lambda item: min(item[1]['z1'], item[1]['z2']))
    
    for _, brick_data in sorted_bricks:
        # If the brick is already at the ground level, skip it
        # z=0 is the ground, so z=1 is the lowest level they can fall ot
        if min(brick_data['z1'], brick_data['z2']) == 1:
            continue
        
        # Start by assuming brick will fall to the ground
        # Then get all settled bricks below it and find the first one that it would collide with
        z_to_drop_to = 1
        bricks_below = get_bricks_below_z(bricks, min(brick_data['z1'], brick_data['z2']))
        
        for _, brick_below_data in bricks_below.items():
            # Check if the brick below would block the falling path of this one
            # Overlap if the max of the 1st x/y val of either brick is less than the min of 2nd
            # Brick1: |-----|
            # Brick2:     |-----|
            # x-axis: 0---1---2---3---4---5
            if check_xy_collision(brick_data, brick_below_data):
                z_to_drop_to = max(brick_below_data['z1'], brick_below_data['z2']) + 1
                break
        
        # Update the falling brick's z value to the one it would fall to. Handle both z1 and z2
        # in case the brick is oriented vertically so that it falls proportionately to its size
        z_size = abs(brick_data['z1'] - brick_data['z2']) + 1
        brick_data['z1'] = z_to_drop_to
        brick_data['z2'] = z_to_drop_to + z_size - 1
       
    return

def get_bricks_directly_below_z(bricks, z):
    """
    Returns all bricks where the maximum of 'z1' and 'z2' is 1 unit below the given z.
    """
    return {brick: brick_data for brick, brick_data in bricks.items() if 
            max(brick_data['z1'], brick_data['z2']) == z - 1}

def store_support_structure(bricks):
    """
    Updates brick list to include each brick's supporting bricks.
    Supporting bricks are bricks directly above a brick's z-index that overlap in x-y plane
    """
    for brick, brick_data in bricks.items():        
        bricks_below = get_bricks_directly_below_z(bricks, min(brick_data['z1'], brick_data['z2']))
        for brick_below, brick_below_data in bricks_below.items():
            if check_xy_collision(brick_data, brick_below_data):
                # Add the brick below to the current brick's 'supporters' list
                brick_data['supporters'].append(brick_below)
                # Add the current brick to the brick below's 'supporting' list
                brick_below_data['supporting'].append(brick)
    return

def run_disintegration_chain(bricks):
    """
    For each brick, determine how many other bricks would fall if it were disintegrated
    """
    
    sum_total_disintegrated = 0
    
    for brick, _ in tqdm(bricks.items()):
        # Find any bricks for which this brick is the only supporting brick
        # If there are none, skip this brick. Add any bricks that would fall to the queue
        # so that we can "chain" up the ladder of all the bricks that would fall using BFS
        bricks_zapped = []
        queue = [brick]
        while queue:
            brick_to_zap = queue.pop(0)
            bricks_zapped.append(brick_to_zap)
                
            for other_brick in bricks[brick_to_zap]['supporting']:
                if other_brick not in bricks_zapped and other_brick not in queue:
                    if set(bricks[other_brick]['supporters']).issubset(set(bricks_zapped)):
                        queue.append(other_brick)
                        sum_total_disintegrated += 1

    
    return sum_total_disintegrated

def plot_bricks(bricks):
    """
    Visualize brick arrangement in 3D using matplotlib
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create a colormap
    colormap = cm.get_cmap('viridis')

    for brick_id, brick_data in bricks.items():
        x = [brick_data['x1'], brick_data['x2']]
        y = [brick_data['y1'], brick_data['y2']]
        z = [brick_data['z1'], brick_data['z2']]

    for brick_id, brick_data in bricks.items():
        # Generate all 8 vertices of the rectangular prism
        vertices = [(x, y, z) for x in (brick_data['x1'], brick_data['x2'] + 1) 
                                for y in (brick_data['y1'], brick_data['y2'] + 1) 
                                for z in (brick_data['z1'] - 1, brick_data['z2'])]

        # Generate the 6 faces of the rectangular prism
        faces = [[vertices[0], vertices[1], vertices[5], vertices[4]],
                 [vertices[7], vertices[6], vertices[2], vertices[3]],
                 [vertices[0], vertices[1], vertices[3], vertices[2]],
                 [vertices[7], vertices[6], vertices[4], vertices[5]],
                 [vertices[7], vertices[3], vertices[1], vertices[5]],
                 [vertices[0], vertices[2], vertices[6], vertices[4]]]

        # Create a Poly3DCollection
        color = colormap(brick_id / len(bricks))  # Generate a color based on the brick ID
        collection = Poly3DCollection(faces, alpha=.25, linewidths=0.1, edgecolors='b', facecolors=color)
        ax.add_collection3d(collection)
        
    # Set the axes limits based on the max x/y/z in the dictionary
    ax.set_xlim([0, max(brick_data['x2'] for brick_data in bricks.values())])
    ax.set_ylim([0, max(brick_data['y2'] for brick_data in bricks.values())])
    ax.set_zlim([0, max(brick_data['z2'] for brick_data in bricks.values())])
    
    # Set integer ticks on axes
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.zaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.show()

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    bricks = parse_input("input.txt")
    sim_gravity(bricks)
    store_support_structure(bricks)
    ic(run_disintegration_chain(bricks))
    plot_bricks(bricks)

if __name__ == "__main__":
    main()

"""
This module solves Part One of Day 22's problem of the Advent of Code challenge.
Fairly straightforward - no need to build a 3D list. We just store the coordinates in a dictionary.
Simulating the initial 'gravity drop' is just a matter of finding the lowest z value any brick
can fall to that doesn't have an xy-plane collision with any other brick.

Checking which ones are safe to disintigrate is a matter of checking if the brick is the sole
supporter of any other brick. If it is, then disintegrating it would cause the other brick to fall
as well and the brick isn't safe to disintegrate.

Added some basic line drawing of the bricks in matplotlib. Upgraded to 3d prisms in part 2.
"""
# --- Day 22: Sand Slabs ---
# Enough sand has fallen; it can finally filter water for Snow Island.
#
# Well, almost.
#
# The sand has been falling as large compacted bricks of sand, piling up to form an impressive stack
# here near the edge of Island Island. In order to make use of the sand to filter water, some of the
# bricks will need to be broken apart - nay, disintegrated - back into freely flowing sand.
#
# The stack is tall enough that you'll have to be careful about choosing which bricks to
# disintegrate; if you disintegrate the wrong brick, large portions of the stack could topple, which
# sounds pretty dangerous.
#
# The Elves responsible for water filtering operations took a snapshot of the bricks while they were
# still falling (your puzzle input) which should let you work out which bricks are safe to
# disintegrate. For example:
#
# 1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9
# Each line of text in the snapshot represents the position of a single brick at the time the
# snapshot was taken. The position is given as two x,y,z coordinates - one for each end of the brick
# - separated by a tilde (~). Each brick is made up of a single straight line of cubes, and the
# Elves were even careful to choose a time for the snapshot that had all of the free-falling bricks
# at integer positions above the ground, so the whole snapshot is aligned to a three-dimensional
# cube grid.
#
# A line like 2,2,2~2,2,2 means that both ends of the brick are at the same coordinate - in other
# words, that the brick is a single cube.
#
# Lines like 0,0,10~1,0,10 or 0,0,10~0,1,10 both represent bricks that are two cubes in volume, both
# oriented horizontally. The first brick extends in the x direction, while the second brick extends
# in the y direction.
#
# A line like 0,0,1~0,0,10 represents a ten-cube brick which is oriented vertically. One end of the
# brick is the cube located at 0,0,1, while the other end of the brick is located directly above it
# at 0,0,10.
#
# The ground is at z=0 and is perfectly flat; the lowest z value a brick can have is therefore 1.
# So, 5,5,1~5,6,1 and 0,2,1~0,2,5 are both resting on the ground, but 3,3,2~3,3,3 was above the
# ground at the time of the snapshot.
#
# Because the snapshot was taken while the bricks were still falling, some bricks will still be in
# the air; you'll need to start by figuring out where they will end up. Bricks are magically
# stabilized, so they never rotate, even in weird situations like where a long horizontal brick is
# only supported on one end. Two bricks cannot occupy the same position, so a falling brick will
# come to rest upon the first other brick it encounters.
#
# Here is the same example again, this time with each brick given a letter so it can be marked in
# diagrams:
#
# 1,0,1~1,2,1   <- A
# 0,0,2~2,0,2   <- B
# 0,2,3~2,2,3   <- C
# 0,0,4~0,2,4   <- D
# 2,0,5~2,2,5   <- E
# 0,1,6~2,1,6   <- F
# 1,1,8~1,1,9   <- G
# At the time of the snapshot, from the side so the x axis goes left to right, these bricks are
# arranged like this:
#
#  x
# 012
# .G. 9
# .G. 8
# ... 7
# FFF 6
# ..E 5 z
# D.. 4
# CCC 3
# BBB 2
# .A. 1
# --- 0
# Rotating the perspective 90 degrees so the y axis now goes left to right, the same bricks are
# arranged like this:
#
#  y
# 012
# .G. 9
# .G. 8
# ... 7
# .F. 6
# EEE 5 z
# DDD 4
# ..C 3
# B.. 2
# AAA 1
# --- 0
# Once all of the bricks fall downward as far as they can go, the stack looks like this, where ?
# means bricks are hidden behind other bricks at that location:
#
#  x
# 012
# .G. 6
# .G. 5
# FFF 4
# D.E 3 z
# ??? 2
# .A. 1
# --- 0
# Again from the side:
#
#  y
# 012
# .G. 6
# .G. 5
# .F. 4
# ??? 3 z
# B.C 2
# AAA 1
# --- 0
# Now that all of the bricks have settled, it becomes easier to tell which bricks are supporting
# which other bricks:
#
# Brick A is the only brick supporting bricks B and C. Brick B is one of two bricks supporting brick
# D and brick E. Brick C is the other brick supporting brick D and brick E. Brick D supports brick
# F. Brick E also supports brick F. Brick F supports brick G. Brick G isn't supporting any bricks.
# Your first task is to figure out which bricks are safe to disintegrate. A brick can be safely
# disintegrated if, after removing it, no other bricks would fall further directly downward. Don't
# actually disintegrate any bricks - just determine what would happen if, for each brick, only that
# brick were disintegrated. Bricks can be disintegrated even if they're completely surrounded by
# other bricks; you can squeeze between bricks if you need to.
#
# In this example, the bricks can be disintegrated as follows:
#
# Brick A cannot be disintegrated safely; if it were disintegrated, bricks B and C would both fall.
# Brick B can be disintegrated; the bricks above it (D and E) would still be supported by brick C.
# Brick C can be disintegrated; the bricks above it (D and E) would still be supported by brick B.
# Brick D can be disintegrated; the brick above it (F) would still be supported by brick E. Brick E
# can be disintegrated; the brick above it (F) would still be supported by brick D. Brick F cannot
# be disintegrated; the brick above it (G) would fall. Brick G can be disintegrated; it does not
# support any other bricks. So, in this example, 5 bricks can be safely disintegrated.
#
# Figure how the blocks will settle based on the snapshot. Once they've settled, consider
# disintegrating a single brick; how many bricks could be safely chosen as the one to get
# disintegrated?
# 
# Your puzzle answer was 501.

import matplotlib.pyplot as plt
from icecream import ic

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
                            'supporters':[]}
    
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
    
    for _, brick_data in bricks.items():
        bricks_below = get_bricks_directly_below_z(bricks, min(brick_data['z1'], brick_data['z2']))
        for brick_below, brick_below_data in bricks_below.items():
            if check_xy_collision(brick_data, brick_below_data):
                brick_data['supporters'].append(brick_below)
    return

def get_disintegrate_count(bricks):
    """
    Calculates sum of which single bricks could be disintegrated. A brick may be disintegrated
    if it is never the sole supporting brick for any other brick
    """
    
    sum_disintegrate = 0
    
    # Iterate through each brick
    for brick, _ in bricks.items():
        # Check if the brick appears once and only once in the 'supporters' list of one of 
        # the other bricks
        sole_supporter = False
        for _, other_brick_data in bricks.items():
            if other_brick_data['supporters'].count(brick) == 1 and \
                len(other_brick_data['supporters']) == 1:
                sole_supporter = True
                break
        # If the brick is never the sole supporting brick for any other brick, increment the 
        # disintegrate count
        if not sole_supporter:
            sum_disintegrate += 1
            
    return sum_disintegrate

def plot_bricks(bricks):
    """
    Visualize brick arrangement
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for brick_id, brick_data in bricks.items():
        x = [brick_data['x1'], brick_data['x2']]
        y = [brick_data['y1'], brick_data['y2']]
        z = [brick_data['z1'], brick_data['z2']]
        ax.plot(x, y, z, linewidth = 2)
        
        # Calculate the midpoint of the brick
        mid_x = sum(x) / 2
        mid_y = sum(y) / 2
        mid_z = sum(z) / 2

        # Place a text at the midpoint with the brick ID
        ax.text(mid_x, mid_y, mid_z, str(brick_id))
    
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
    ic(get_disintegrate_count(bricks))
    plot_bricks(bricks)

if __name__ == "__main__":
    main()

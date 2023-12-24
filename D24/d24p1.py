"""
This module solves Part One of Day 24's problem of the Advent of Code challenge.

Approach here is to get y=mx+b for each stone's path, then solve for the intersection of each pair,
check if that intersection is in bounds, check that the collision time is not in the past and
store the collisions in a frozenset to avoid duplicates. Then return the length of the collision
set.
"""

# --- Day 24: Never Tell Me The Odds ---
# It seems like something is going wrong with the snow-making process. Instead of forming snow, the
# water that's been absorbed into the air seems to be forming hail!
#
# Maybe there's something you can do to break up the hailstones?
#
# Due to strong, probably-magical winds, the hailstones are all flying through the air in perfectly
# linear trajectories. You make a note of each hailstone's position and velocity (your puzzle
# input). For example:
#
# 19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3
# Each line of text corresponds to the position and velocity of a single hailstone. The positions
# indicate where the hailstones are right now (at time 0). The velocities are constant and indicate
# exactly how far each hailstone will move in one nanosecond.
#
# Each line of text uses the format px py pz @ vx vy vz. For instance, the hailstone specified by
# 20, 19, 15 @ 1, -5, -3 has initial X position 20, Y position 19, Z position 15, X velocity 1, Y
# velocity -5, and Z velocity -3. After one nanosecond, the hailstone would be at 21, 14, 12.
#
# Perhaps you won't have to do anything. How likely are the hailstones to collide with each other
# and smash into tiny ice crystals?
#
# To estimate this, consider only the X and Y axes; ignore the Z axis. Looking forward in time, how
# many of the hailstones' paths will intersect within a test area? (The hailstones themselves don't
# have to collide, just test for intersections between the paths they will trace.)
#
# In this example, look for intersections that happen with an X and Y position each at least 7 and
# at most 27; in your actual data, you'll need to check a much larger test area. Comparing all pairs
# of hailstones' future paths produces the following results:
#
# Hailstone A: 19, 13, 30 @ -2, 1, -2
# Hailstone B: 18, 19, 22 @ -1, -1, -2
# Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).
#
# Hailstone A: 19, 13, 30 @ -2, 1, -2
# Hailstone B: 20, 25, 34 @ -2, -2, -4
# Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).
#
# Hailstone A: 19, 13, 30 @ -2, 1, -2
# Hailstone B: 12, 31, 28 @ -1, -2, -1
# Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).
#
# Hailstone A: 19, 13, 30 @ -2, 1, -2
# Hailstone B: 20, 19, 15 @ 1, -5, -3
# Hailstones' paths crossed in the past for hailstone A.
#
# Hailstone A: 18, 19, 22 @ -1, -1, -2
# Hailstone B: 20, 25, 34 @ -2, -2, -4
# Hailstones' paths are parallel; they never intersect.
#
# Hailstone A: 18, 19, 22 @ -1, -1, -2
# Hailstone B: 12, 31, 28 @ -1, -2, -1
# Hailstones' paths will cross outside the test area (at x=-6, y=-5).

# Hailstone A: 18, 19, 22 @ -1, -1, -2
# Hailstone B: 20, 19, 15 @ 1, -5, -3
# Hailstones' paths crossed in the past for both hailstones.

# Hailstone A: 20, 25, 34 @ -2, -2, -4
# Hailstone B: 12, 31, 28 @ -1, -2, -1
# Hailstones' paths will cross outside the test area (at x=-2, y=3).
#
# Hailstone A: 20, 25, 34 @ -2, -2, -4
# Hailstone B: 20, 19, 15 @ 1, -5, -3
# Hailstones' paths crossed in the past for hailstone B.
#
# Hailstone A: 12, 31, 28 @ -1, -2, -1
# Hailstone B: 20, 19, 15 @ 1, -5, -3
# Hailstones' paths crossed in the past for both hailstones.
# So, in this example, 2 hailstones' future paths cross inside the boundaries of the test area.
#
# However, you'll need to search a much larger test area if you want to see if any hailstones might
# collide. Look for intersections that happen with an X and Y position each at least 200000000000000
# and at most 400000000000000. Disregard the Z axis entirely.
#
# Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections.
# How many of these intersections occur within the test area?

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    
    # Hailstone format: px py pz @ vx vy vz
    with open(filename, 'r') as file:
        data = file.read().splitlines()
    
    stones = {}
    
    for stone_id, line in enumerate(data):
        x,y,z = map(int, line.split('@')[0].split(','))
        vx,vy,vz = map(int, line.split('@')[1].split(','))
        stones[stone_id] = {'x': x, 'y': y, 'z': z, 
                            'vx': vx, 'vy': vy, 'vz': vz}
    
    return stones

def check_for_collisions(stones):
    """
    Checks if two stones paths ever cross in the xy bounds
    """
    min_xy = 200_000_000_000_000
    max_xy = 400_000_000_000_000
    # min_xy = 7
    # max_xy = 27
    
    collisions = set()
    
    # Consider every pair of stones to check for pairwise collisions
    for stone_id, stone in stones.items():
        for stone2_id, stone2 in stones.items():
            if stone_id == stone2_id:
                continue
            x1, vx1, y1, vy1 = stone['x'], stone['vx'], stone['y'], stone['vy']
            x2, vx2, y2, vy2 = stone2['x'], stone2['vx'], stone2['y'], stone2['vy']

            # Calculate the slopes and y-intercepts
            m1 = vy1 / vx1 if vx1 != 0 else float('inf')
            b1 = y1 - m1 * x1
            m2 = vy2 / vx2 if vx2 != 0 else float('inf')
            b2 = y2 - m2 * x2

            # If the lines are parallel, they'll never cross so there can be no collision
            if m1 == m2:
                continue

            # Calculate the intersection point
            x_intersect = (b2 - b1) / (m1 - m2)
            y_intersect = m1 * x_intersect + b1
            
            # If any collision happened in the past, ignore it
            if any(t < 0 for t in ((x_intersect - x1) / vx1, (y_intersect - y1) / vy1, \
                                  (x_intersect - x2) / vx2, (y_intersect - y2) / vy2)):
                continue
            
            # Check if the intersection point is within the given bounds
            # We're using a set of frozensets to avoid duplicates so (0, 1) and (1,0) are the same
            if min_xy <= x_intersect <= max_xy and min_xy <= y_intersect <= max_xy:
                collisions.add(frozenset((stone_id, stone2_id)))

    return len(collisions)

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    stones = parse_input("input.txt")
    
    print(f"Number of collisions: {check_for_collisions(stones)}")

if __name__ == "__main__":
    main()

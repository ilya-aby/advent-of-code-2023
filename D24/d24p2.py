"""
This module solves Part Two of Day 24's problem of the Advent of Code challenge.

Approach here is to recognize that we're solving a system of equations. If the stone we're solving
for is at position (x, y, z) and velocity (vx, vy, vz) and the other stone is at position (x_i, y_i,
z_i) and velocity (vx_i, vy_i, vz_i) then we can solve for the time of collision using the following
equations:

x + vx * t = x_i + vx_i * t
y + vy * t = y_i + vy_i * t
z + vz * t = z_i + vz_i * t

So we have 3 equations and 7 unknowns. If we consider a second stone, we have 6 equations and 8
unknowns (t2 is the time of collision with the second stone). If we consider a third stone, we have
9 equations and 9 unknowns (t3 is the time of collision with the third stone). We can then solve
this system of equations using a solver and return the sum of the collision vector.

In other words, only 3 stones from the entire input file actually matter. The system is hugely
overdetermined and we can pick any 3 stones and get the same answer.

Sympy did much better than scipy for this problem - scipy was very reliant on the initial guess
and had trouble with the huge integer values in the input. Sympy solves the system right away.
"""

# --- Part Two ---
# Upon further analysis, it doesn't seem like any hailstones will naturally collide. It's up to you
# to fix that!
#
# You find a rock on the ground nearby. While it seems extremely unlikely, if you throw it just
# right, you should be able to hit every hailstone in a single throw!
#
# You can use the probably-magical winds to reach any integer position you like and to propel the
# rock at any integer velocity. Now including the Z axis in your calculations, if you throw the rock
# at time 0, where do you need to be so that the rock perfectly collides with every hailstone? Due
# to probably-magical inertia, the rock won't slow down or change direction when it collides with a
# hailstone.
#
# In the example above, you can achieve this by moving to position 24, 13, 10 and throwing the rock
# at velocity -3, 1, 2. If you do this, you will hit every hailstone as follows:
#
# Hailstone: 19, 13, 30 @ -2, 1, -2
# Collision time: 5
# Collision position: 9, 18, 20
#
# Hailstone: 18, 19, 22 @ -1, -1, -2
# Collision time: 3
# Collision position: 15, 16, 16
#
# Hailstone: 20, 25, 34 @ -2, -2, -4
# Collision time: 4
# Collision position: 12, 17, 18
#
# Hailstone: 12, 31, 28 @ -1, -2, -1
# Collision time: 6
# Collision position: 6, 19, 22
#
# Hailstone: 20, 19, 15 @ 1, -5, -3
# Collision time: 1
# Collision position: 21, 14, 12
# Above, each hailstone is identified by its initial position and its velocity. Then, the time and
# position of that hailstone's collision with your rock are given.
#
# After 1 nanosecond, the rock has exactly the same position as one of the hailstones, obliterating
# it into ice dust! Another hailstone is smashed to bits two nanoseconds after that. After a total
# of 6 nanoseconds, all of the hailstones have been destroyed.
#
# So, at time 0, the rock needs to be at X position 24, Y position 13, and Z position 10. Adding
# these three coordinates together produces 47. (Don't add any coordinates from the rock's
# velocity.)
#
# Determine the exact position and velocity the rock needs to have at time 0 so that it perfectly
# collides with every hailstone. What do you get if you add up the X, Y, and Z coordinates of that
# initial position?

from sympy import symbols, Eq, solve

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

def get_collision_vector(stones):
    """
    Given a set of stones, determine an initial position and velocity vector for a new rock
    that will collide with all of the stones. Relies on the fact that only 3 stones are needed
    to solve the system of equations. We use the solver from sympy to solve the system.
    """
    
    existing_objects = list(stones.values())[:3]
    x, y, z, vx, vy, vz, t1, t2, t3 = symbols('x y z vx vy vz t1 t2 t3')

    eqs = []
    for i, stone in enumerate(existing_objects):
        x_i, y_i, z_i = stone['x'], stone['y'], stone['z']
        vx_i, vy_i, vz_i = stone['vx'], stone['vy'], stone['vz']
        t = [t1, t2, t3][i]
        eqs.append(Eq(x + vx * t, x_i + vx_i * t))
        eqs.append(Eq(y + vy * t, y_i + vy_i * t))
        eqs.append(Eq(z + vz * t, z_i + vz_i * t))

    solution = solve(eqs, dict=True)
    for sol in solution:
        for var, value in sol.items():
            print(f"{var}: {round(float(value.evalf()), 1)}")
        print(f"Sum of positions: {sol[x].evalf() + sol[y].evalf() + sol[z].evalf()}")

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    stones = parse_input("input.txt")
    get_collision_vector(stones)

if __name__ == "__main__":
    main()

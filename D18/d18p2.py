"""
This module solves Part Two of Day 18's problem of the Advent of Code challenge.
Spent a lot of time trying to build a scanline algorithm to solve this, which involved going
down each row and finding the intersections with the polygon. This was super hard to debug
due to the colinear edges. Ended up giving up on that and switching to using Pick's Theorem
and Shoelace Theorem to calculate the area of the polygon and the number of interior points.

Sholeace gives us the geometric area of the polgyon given its vertices. Pick's Theorem gives us
the interior points given the geometric area and the number of boundary points. We then
sum the interior points and boundary points to get the total area of the polygon. 
"""
# --- Part Two ---
# The Elves were right to be concerned; the planned lagoon would be much too small.
#
# After a few minutes, someone realizes what happened; someone swapped the color and instruction
# parameters when producing the dig plan. They don't have time to fix the bug; one of them asks if
# you can extract the correct instructions from the hexadecimal codes.
#
# Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the
# distance in meters as a five-digit hexadecimal number. The last hexadecimal digit encodes the
# direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.
#
# So, in the above example, the hexadecimal codes can be converted into the true instructions:
#
# #70c710 = R 461937
# #0dc571 = D 56407
# #5713f0 = R 356671
# #d2c081 = D 863240
# #59c680 = R 367720
# #411b91 = D 266681
# #8ceee2 = L 577262
# #caa173 = U 829975
# #1b58a2 = L 112010
# #caa171 = D 829975
# #7807d2 = L 491645
# #a77fa3 = U 686074
# #015232 = L 5411
# #7a21e3 = U 500254
# Digging out this loop and its interior produces a lagoon that can hold an impressive 952408144115
# cubic meters of lava.
#
# Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new
# dig plan, how many cubic meters of lava could the lagoon hold?
#
# Your puzzle answer was 93325849869340.

from icecream import ic

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    data = open(filename).read().strip()
    lines = data.split('\n')
    data = []
    dir_map = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
    for row in lines:
        hex_val = row.split(' ')[2].strip('()#')
        amt = int(hex_val[0:5],16)
        vector = dir_map[int(hex_val[5:6])]
        data.append([vector, int(amt)])
    return data

def dig(data):
    """
    Given a list of instructions, determine the area of the polygon created by those instructions.
    """
    vector_map = { 'R': (0,1), 'L': (0,-1), 'U': (-1,0), 'D': (1,0) }
    
    # Generate a list of vertices and get the total length of the boundary
    location = (0,0)
    vertices = []
    for instruction in data:
        vertices.append(location)
        vector, amt = instruction
        vector_offset = vector_map[vector]
        location = (location[0] + amt * vector_offset[0], location[1] + amt * vector_offset[1])
        
    # Boundary length is just the sum of the distances traveled in each instruction
    boundary_length = sum(instruction[1] for instruction in data)

    # Shoelace area is the geometric area of the polygon formed by the vertices
    # With that, we can calculate the number of interior points with Pick's Theorem
    shoelace_area = get_shoelace_area(vertices)
    ic(boundary_length, shoelace_area)
    
    # Pick's Theorem:
    # A = i + b/2 -1
    # Where A is area of a polygon, i is number of interior
    # points and b is number of boundary points
    # So i = A - b/2 + 1
    interior_points = shoelace_area - boundary_length/2 + 1
    total_area = interior_points + boundary_length
    
    return int(total_area)

def get_shoelace_area(vertices):
    """
    Calculate the area of a polygon using the Shoelace theorem.

    vertices: a list of (x, y) pairs representing the vertices of the polygon.
    """
    n = len(vertices) # Number of vertices
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2.0
    return area

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    instructions = parse_input("input.txt")
    area = dig(instructions)
    print(area)

if __name__ == "__main__":
    main()

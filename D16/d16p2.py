"""
This module solves Part Two of Day 16's problem of the Advent of Code challenge.
Factored the code from Part One into a function so I could call it multiple times then generated
multiple possible entry beams and fed them all into that function to find the highest possible
energy value
"""

from icecream import ic

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    
    data = open(filename).read().strip()
    data = data.split('\n')
    data = [[char for char in row] for row in data]
    
    return data

def get_energy_value(data, start_beam):
    """
    Processes the data
    """
    
    energized = [[' ' for _ in range(len(data[0]))] for _ in range(len(data))]
    beams = [start_beam]
    beams_cache = {}
 
    while True:
        if not beams:
            break
        for beam_id, beam in enumerate(beams):
            beam_row, beam_col, beam_heading = beam
            
            # Check if we're out of bounds
            if beam_row < 0 or beam_row >= len(data) or \
                beam_col < 0 or beam_col >= len(data[0]):
                del beams[beam_id]
                continue
            
            # Check if we've processed this beam & heading before. If we have, prune it. Otherwise,
            # add it to the cache
            if beams_cache.get((beam_row, beam_col, beam_heading)):
                del beams[beam_id]
                continue
            else:
                beams_cache[(beam_row, beam_col, beam_heading)] = True
            
            tile = data[beam_row][beam_col]
            energized[beam_row][beam_col] = '#'
            # Case: proceed on vector
            if tile == '.' or \
                (tile == '-' and beam_heading in ('E','W')) or \
                (tile == '|' and beam_heading in ('N','S')):
                if beam_heading == 'E':
                    beam_col += 1
                elif beam_heading == 'W':
                    beam_col -= 1
                elif beam_heading == 'N':
                    beam_row -= 1
                elif beam_heading == 'S':
                    beam_row += 1
                beams[beam_id] = (beam_row, beam_col, beam_heading)
                continue
            # Case: split beam
            elif (tile == '-' and beam_heading in ('N','S')) or \
                (tile == '|' and beam_heading in ('E','W')):
                if beam_heading in ('E','W'):
                    beams.append((beam_row-1, beam_col, 'N'))
                    beams.append((beam_row+1, beam_col, 'S'))
                else:
                    beams.append((beam_row, beam_col-1, 'W'))
                    beams.append((beam_row, beam_col+1, 'E'))
                # Kill the original beam
                del beams[beam_id]
                continue
            # Case: mirror beam to the north
            elif (tile == '/' and beam_heading == 'E') or \
                (tile == '\\' and beam_heading == 'W'):
                beams[beam_id] = (beam_row-1, beam_col, 'N')
                continue
            # Case: mirror beam to the south
            elif (tile == '/' and beam_heading == 'W') or \
                (tile == '\\' and beam_heading == 'E'):
                beams[beam_id] = (beam_row+1, beam_col, 'S')
                continue
            # Case: mirror beam to the west
            elif (tile == '/' and beam_heading == 'S') or \
                (tile == '\\' and beam_heading == 'N'):
                beams[beam_id] = (beam_row, beam_col - 1, 'W')
                continue
            # Case: mirror beam to the east
            elif (tile == '/' and beam_heading == 'N') or \
                (tile == '\\' and beam_heading == 'S'):
                beams[beam_id] = (beam_row, beam_col + 1, 'E')
                continue

    return sum(row.count('#') for row in energized)

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    data = ic(parse_input("input.txt"))
    
    best_beam = (0,0,'E')
    highest_energy = 0
    
    entry_beams = []
    # Create entry beams for top and bottom rows
    for i in range(len(data[0])):
        entry_beams.append((0, i, 'S'))
        entry_beams.append((0, len(data) - 1, 'N'))
    # Create entry beams for left and right rows
    for j in range(len(data)):
        entry_beams.append((j, 0, 'E'))
        entry_beams.append((j, len(data[0]) - 1, 'W'))
    
    for beam in entry_beams:
        energy = get_energy_value(data, beam)
        if energy > highest_energy:
            highest_energy = energy
            best_beam = beam
    
    print(highest_energy, best_beam)
    

if __name__ == "__main__":
    main()

"""
This module solves Part One of Day 16's problem of the Advent of Code challenge.
Probably should have switched on N/E/S/W instead of the way I handled the cases, but this worked.
The only gotcha was not realizing the beams could bounce around the map forever, so I had to
implement a cache to prevent infinite loops and prune cycling beams. The cache has to keep
track of the entire beam, including the heading, since just knowing a tile has been visited
isn't enough to prune a beam.
"""
# --- Day 16: The Floor Will Be Lava ---
# With the beam of light completely focused somewhere, the reindeer leads you deeper still into the
# Lava Production Facility. At some point, you realize that the steel facility walls have been
# replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure
# this is actually just a giant cave.
#
# Finally, as you approach what must be the heart of the mountain, you see a bright light in a
# cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging
# from the cavern wall closest to the facility and pouring all of its energy into a contraption on
# the opposite side.
#
# Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid
# containing empty space (.), mirrors (/ and \), and splitters (| and -).
#
# The contraption is aligned so that most of the beam bounces around the grid, but each tile on the
# grid converts some of the beam's light into heat to melt the rock in the cavern.
#
# You note the layout of the contraption (your puzzle input). For example:
#
# .|...\....
# |.-.\.....
# .....|-...
# ........|.
# ..........
# .........\
# ..../.\\..
# .-.-/..|..
# .|....-|.\
# ..//.|....
# The beam enters in the top-left corner from the left and heading to the right. Then, its behavior
# depends on what it encounters as it moves:
#
# If the beam encounters empty space (.), it continues in the same direction. If the beam encounters
# a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For
# instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's
# column, while a rightward-moving beam that encounters a \ mirror would continue downward from the
# mirror's column. If the beam encounters the pointy end of a splitter (| or -), the beam passes
# through the splitter as if the splitter were empty space. For instance, a rightward-moving beam
# that encounters a - splitter would continue in the same direction. If the beam encounters the flat
# side of a splitter (| or -), the beam is split into two beams going in each of the two directions
# the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a |
# splitter would split into two beams: one that continues upward from the splitter's column and one
# that continues downward from the splitter's column. Beams do not interact with other beams; a tile
# can have many beams passing through it at the same time. A tile is energized if that tile has at
# least one beam pass through it, reflect in it, or split in it.
#
# In the above example, here is how the beam of light bounces around the contraption:
#
# >|<<<\....
# |v-.\^....
# .v...|->>>
# .v...v^.|.
# .v...v^...
# .v...v^..\
# .v../2\\..
# <->-/vv|..
# .|<<<2-|.\
# .v//.|.v..
# Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile
# contains beams moving in multiple directions, the number of distinct directions is shown instead.
# Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):
#
# ######....
# .#...#....
# .#...#####
# .#...##...
# .#...##...
# .#...##...
# .#..####..
# ########..
# .#######..
# .#...#.#..
# Ultimately, in this example, 46 tiles become energized.
#
# The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to
# start by analyzing the current situation. With the beam starting in the top-left heading right,
# how many tiles end up being energized?
#
# Your puzzle answer was 7939.

from icecream import ic

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    
    data = open(filename).read().strip()
    data = data.split('\n')
    data = [[char for char in row] for row in data]
    
    return data

def processor(data):
    """
    Processes the data
    """
    return data


def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    data = parse_input("input.txt")
    
    energized = [[' ' for _ in range(len(data[0]))] for _ in range(len(data))]
    
    beams = [(0,0,'E')]
    beams_cache = {}
    
    while(True):
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

    ic(energized)
    print(sum(row.count('#') for row in energized))

if __name__ == "__main__":
    main()

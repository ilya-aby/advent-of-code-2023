"""
This module solves Part Two of Day 21's problem of the Advent of Code challenge.
No satisfying solution here. The only thing happening here is that the problem has periodic cycles
where a tile "fills up" and starts oscillating between two states. Because we know we are taking
an odd number of steps, we can look at the state of the tile after 131 steps. At that point,
we also step into new tiles that are not part of the cycle, so total step count expands 
quadratically. I just dumped the values at critical points into a quadratic solver and got the
answer that way.

Also considered "eating" a tile once it hits its final cycle length, but that doesn't get you
that far because there are still too many 'edge' tiles to compute this manually, even if you 
freeze all the inner tiles.
"""
# --- Part Two ---
# The Elf seems confused by your answer until he realizes his mistake: he was reading from a list of
# his favorite numbers that are both perfect squares and perfect cubes, not his step counter.
#
# The actual number of steps he needs to get today is exactly 26501365.
#
# He also points out that the garden plots and rocks are set up so that the map repeats infinitely
# in every direction.
#
# So, if you were to look one additional map-width or map-height out from the edge of the example
# map above, you would find that it keeps repeating:
#
# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##...####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##..S####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
# .................................
# .....###.#......###.#......###.#.
# .###.##..#..###.##..#..###.##..#.
# ..#.#...#....#.#...#....#.#...#..
# ....#.#........#.#........#.#....
# .##...####..##...####..##...####.
# .##..#...#..##..#...#..##..#...#.
# .......##.........##.........##..
# .##.#.####..##.#.####..##.#.####.
# .##..##.##..##..##.##..##..##.##.
# .................................
# This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm layout; garden
# plots and rocks repeat as far as you can see. The Elf still starts on the one middle tile marked
# S, though - every other repeated S is replaced with a normal garden plot (.).
#
# Here are the number of reachable garden plots in this new infinite version of the example map for
# different numbers of steps:
#
# In exactly 6 steps, he can still reach 16 garden plots.
# In exactly 10 steps, he can reach any of 50 garden plots.
# In exactly 50 steps, he can reach 1594 garden plots.
# In exactly 100 steps, he can reach 6536 garden plots.
# In exactly 500 steps, he can reach 167004 garden plots.
# In exactly 1000 steps, he can reach 668697 garden plots.
# In exactly 5000 steps, he can reach 16733044 garden plots.
# However, the step count the Elf needs is much larger! Starting from the garden plot marked S on
# your infinite map, how many garden plots could the Elf reach in exactly 26501365 steps?
#

from icecream import ic

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    with open(filename, 'r') as file:
        data = file.read().splitlines()
    
    return data

def update_sub_position(position, garden):
    """
    Helper to do inner loop of position update for caching purposes.
    Outside function retains the tile offset
    """
    next_positions = []
    for row_offset, col_offset in [(0,1),(0,-1),(1,0),(-1,0)]:
        new_row = position[0] + row_offset
        new_col = position[1] + col_offset
        new_row_tile_offset = position[2]
        new_col_tile_offset = position[3]
        # Since map is now infinite, we handle out of bounds by jumping to the other side
        # of the same tile
        if new_row < 0:
            new_row = len(garden) - 1
            new_row_tile_offset -= 1
        elif new_row >= len(garden):
            new_row = 0
            new_row_tile_offset += 1
        if new_col < 0:
            new_col = len(garden[0]) - 1
            new_col_tile_offset -= 1
        elif new_col >= len(garden[0]):
            new_col = 0
            new_col_tile_offset += 1
        if garden[new_row][new_col] == '#':
            continue
        next_positions.append((new_row, new_col, new_row_tile_offset, new_col_tile_offset))
    return next_positions

def update_position(position, garden):
    """
    Given a position, returns a list of all possible positions that can be reached from that
    position in one step
    """
    next_positions = []
    
    stripped_position = (position[0], position[1], 0, 0)
    next_positions = update_sub_position(stripped_position, garden)
    
    return [(pos[0], pos[1], pos[2] + position[2], pos[3] + position[3]) for pos in next_positions]
    

def find_steps(garden):
    """ Calculates possible places elf can be in the garden after N steps """
    
    # Find the starting position, marked by 'S' in the grid:
    start_row = None
    start_col = None
    for row, line in enumerate(garden):
        if 'S' in line:
            start_row = row
            start_col = line.index('S')
            break
    
    # We add tile offsets to the starting position to keep track of where we are on the infinite
    # tile grid, to make sure that equivalent positions on different tiles are not considered the
    # same location
    row_tile_offset = 0
    col_tile_offset = 0
    position = (start_row, start_col, row_tile_offset, col_tile_offset)
    
    steps_taken = 0

    current_positions = set([position])
    num_active_tiles = 1
    
    while True:
        # Find all possible positions we can reach in the next step
        # This is any position that is one step north, south, east, or west of any possible
        # Locations we could have been at right now
        next_positions = set()
        for position in current_positions:
            next_positions.update(update_position(position, garden))
                
        # set() de-dupes the list of positions
        current_positions = next_positions
        
        steps_taken += 1

        tile_counts = {}
        for pos in current_positions:
            tile = (pos[2], pos[3])
            if tile not in tile_counts:
                tile_counts[tile] = 0
            tile_counts[tile] += 1
        
        # Write critical inflection points to log (if we've reached a new tile)
        if len(tile_counts) > num_active_tiles:
            num_active_tiles = len(tile_counts) 
        
            with open('output.log', 'a') as f:
                f.write(f'{steps_taken}: Total reachable {len(current_positions)}\n')
                for tile, count in tile_counts.items():
                    f.write(f'Tile {tile}: {count} positions\n')
        
        if steps_taken == 1000:
            break
        
    return ic(len(current_positions))
        
def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    garden = parse_input("input.txt")
    print(find_steps(garden))

if __name__ == "__main__":
    main()

"""
This module solves Part Two of Day 11's problem of the Advent of Code challenge.
The main trick to this one is to realize that we don't need to actually expand the map. We can
just build a list of expansion factors for each row and column. Then, we can use those expansion
factors when calculating distance. There's no need to touch the map at all.
"""
# --- Part Two ---
# The galaxies are much older (and thus much farther apart) than the researcher initially estimated.
#
# Now, instead of the expansion you did before, make each empty row or column one million times
# larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column
# should be replaced with 1000000 empty columns.
#
# (In the example above, if each empty row or column were merely 10 times larger, the sum of the
# shortest paths between every pair of galaxies would be 1030. If each empty row or column were
# merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be
# 8410. However, your universe will need to expand far beyond these values.)
#
# Starting with the same initial image, expand the universe according to these new rules, then find
# the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
# 
# Answer for sample input: 1030
# Answer for input: 447744640566

FILENAME = 'input.txt'

def parse_input(file_name: str) -> list[list[str]]:
    """
    Parses a star map file and returns a list of lists containing the star map characters
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    
    star_map = [list(line.strip()) for line in data]

    return star_map

def expand_map(expansion_factor: int, star_map: list[list[str]]) -> tuple[list[int], list[int]]:
    """
    Expands the star map by creating row/col arrays to store expansion factor for each row/col that
    doesn't contain a galaxy. Stores 1 for each row/col that contains a galaxy and does not need to
    be expanded
    """
    row_expansions = []
    col_expansions = []

    for row in star_map:
        if '#' not in row:
            row_expansions.append(expansion_factor)
        else:
            row_expansions.append(1)

    for col in range(len(star_map[0])):
        if '#' not in [row[col] for row in star_map]:
            col_expansions.append(expansion_factor)
        else:
            col_expansions.append(1)

    return row_expansions, col_expansions

def get_galaxy_coords(star_map: list[list[str]]) -> list[tuple[int, int]]:
    """
    Returns the coordinates of all the # galaxy characters in the star map
    """
    galaxy_coords = []
    for row_idx, row in enumerate(star_map):
        for col_idx, col in enumerate(row):
            if col == '#':
                galaxy_coords.append((row_idx, col_idx))

    return galaxy_coords

def get_sum_shortest_paths(galaxy_coords:list[tuple[int, int]], 
                           row_expansions:list[int], 
                           col_expansions:list[int]) -> int:
    """
    Returns the sum of the shortest paths from the galaxy coordinates to all other galaxy
    coordinates
    """
    shortest_paths = []
    for i, galaxy_one in enumerate(galaxy_coords):
        for galaxy_two in galaxy_coords[i+1:]:
            x_diff = sum(row_expansions[min(galaxy_one[0], galaxy_two[0]): 
                max(galaxy_one[0], galaxy_two[0])])
            y_diff = sum(col_expansions[min(galaxy_one[1], galaxy_two[1]):
                max(galaxy_one[1], galaxy_two[1])])

            shortest_paths.append(x_diff + y_diff)

    return sum(shortest_paths)

def main():
    """
    Main function that reads the input file, parses the starmap, and finds sum of shortest paths
    """
    expansion_factor = 1000000 
    star_map = parse_input(FILENAME)

    print('Star Map:') 
    for row in star_map:
        print(''.join(row))
    print("\n")

    row_expansions, col_expansions = expand_map(expansion_factor, star_map)

    print(f'Sum of shortest paths: {get_sum_shortest_paths(get_galaxy_coords(star_map), 
          row_expansions, col_expansions)}')

if __name__ == "__main__":
    main()

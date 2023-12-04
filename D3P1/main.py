# --- Day 3: Gear Ratios ---
# You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.
#
# It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.
#
# "Aaah!"
#
# You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.
#
# The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.
#
# The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)
#
# Here is an example engine schematic:
#
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
#
# Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
# 
# Answer for sample input: 4361
# Answer for input: 535235

import re

FILENAME = 'input.txt'

# Ingest input file
try:
    with open(FILENAME, 'r') as f:
        data = f.read().splitlines()
except FileNotFoundError:
    print(f"File {FILENAME} not found.")
    exit(1)

def engine_parser(engine_file):
    """
    Parses an engine file into a 2D array of characters.
    """
    engine = []
    for line in engine_file:
        engine.append(list(line))
    return engine

def find_candidate_part_numbers(engine):
    """
    Returns all candidate part numbers in an engine schematic along with their location in the engine.
    Returns an array of part dictionaries of the form {part_number, row, col}.
    """
    candidate_part_numbers = []

    for row_id, row in enumerate(engine):
        engine_string = ''.join(row)
        
        matches = re.compile(r'\d+').finditer(engine_string)
        for m in matches:
            candidate_part_numbers.append({'part_number': m.group(), 'row': row_id, 'col': m.start()})

    return candidate_part_numbers

def is_symbol(char):
    """
    Returns True if the given character is an engine 'symbol', False otherwise. Periods are not symbols.
    """
    if(char == '.' or char.isdigit()):
        return False
    else:
        return True

def validate_part(part, engine):
    """
    Given a part object of the form {part_number, row, col} and an engine, checks to see if the part is valid.
    An invalid part will have no adjacent symbols
    """

    # Determine the boundaries of the scanning window
    start_col = max(0, part['col'] - 1)
    end_col = min(len(engine[part['row']]) - 1, part['col'] + len(str(part['part_number'])))
    start_row = max(0, part['row'] - 1)
    end_row = min(len(engine) - 1, part['row'] + 1)

    #print(f"Part: {part['part_number']}, Start Col: {start_col}, End Col: {end_col}, Start Row: {start_row}, End Row: {end_row}")

    # Scan the window for symbols
    # If we have at least one valid symbol in the scan window, it's a valid part
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            if(is_symbol(engine[row][col])):
                return True
    return False

engine = engine_parser(data)
candidate_part_numbers = find_candidate_part_numbers(engine)

sum_of_valid_part_numbers = 0
for part in candidate_part_numbers:
    if(validate_part(part, engine)):
        print(f'Part {part["part_number"]} is valid.')
        sum_of_valid_part_numbers += int(part['part_number'])
    else:
        print(f'Part {part["part_number"]} is invalid.')

print(f'Sum of valid part numbers: {sum_of_valid_part_numbers}')
# --- Part Two ---
# The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.
#
# You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.
#
# Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.
#
# The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.
#
# This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.
#
# Consider the same engine schematic again:
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
# In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
#
# What is the sum of all of the gear ratios in your engine schematic?
# 
# Answer for sample input: 467835
# Answer for input: 79844424

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

def find_part_numbers(engine):
    """
    Returns all part numbers in an engine schematic along with their location in the engine.
    Returns an array of part dictionaries of the form {part_number, row, col}.
    We no longer worry about 'invalid' part numbers because they can't be adjacent to gears anyway.
    """
    candidate_part_numbers = []

    for row_id, row in enumerate(engine):
        engine_string = ''.join(row)
        
        matches = re.compile(r'\d+').finditer(engine_string)
        for m in matches:
            candidate_part_numbers.append({'part_number': m.group(), 'row': row_id, 'col': m.start()})

    return candidate_part_numbers

def find_candidate_gears(engine):
    """
    Returns all candidate gears in an engine schematic along with their location in the engine.
    Returns an array of gear dictionaries of the form {gear_number, row, col}.
    """
    candidate_gears = []

    for row_id, row in enumerate(engine):
        for col_id, char in enumerate(row):
            if(char == '*'):
                candidate_gears.append({'gear_number': char, 'row': row_id, 'col': col_id})

    return candidate_gears

def get_gear_ratio(gear, engine, part_numbers):
    """
    Given a gear object of the form {gear_number, row, col}, an engine, and a list of part_numbers, returns the gear ratio.
    """
    adjacent_part_numbers = []

    # Determine the boundaries of the scanning window
    start_col = max(0, gear['col'] - 1)
    end_col = min(len(engine[gear['row']]) - 1, gear['col'] + 1)
    start_row = max(0, gear['row'] - 1)
    end_row = min(len(engine) - 1, gear['row'] + 1)

    # Find all part numbers that are adjacent to this gear
    for part in part_numbers:
        part_length = len(str(part['part_number']))

        # Check if the part number is in this gear's row window
        if(part['row'] >= start_row and part['row'] <= end_row):
            # Check if the part number begins in this gear's column window
            if(part['col'] >= start_col and part['col'] <= end_col):
                adjacent_part_numbers.append(part)

            # Check if the part number ends in this gear's column window
            elif(part['col'] < start_col and part['col'] + part_length - 1 >= start_col):
                adjacent_part_numbers.append(part)

    # If we have exactly two adjacent part numbers, calculate the gear ratio
    # If there are not two adjacent part numbers, the gear ratio is 0 and it's not a valid gear
    if(len(adjacent_part_numbers) == 2):
        gear_ratio = int(adjacent_part_numbers[0]['part_number']) * int(adjacent_part_numbers[1]['part_number'])
    else:
        gear_ratio = 0

    return gear_ratio

engine = engine_parser(data)
part_numbers = find_part_numbers(engine)
candidate_gears = find_candidate_gears(engine)

sum_of_gear_ratios = 0

for gear in candidate_gears:
    gear_ratio = get_gear_ratio(gear, engine, part_numbers)
    sum_of_gear_ratios += gear_ratio

print(f'Sum of gear ratios: {sum_of_gear_ratios}')
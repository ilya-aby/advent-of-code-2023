"""
This module solves Part Two of Day 15's problem of the Advent of Code challenge.
Nothing tricky here - just following problem instructions
"""
# --- Part Two --- You convince the reindeer to bring you the page; the page confirms that your HASH
# algorithm is working.
#
# The book goes on to describe a series of 256 boxes numbered 0 through 255. The boxes are arranged
# in a line starting from the point where light enters the facility. The boxes have holes that allow
# light to pass from one box to the next all the way down the line.
#
#       +-----+  +-----+         +-----+
# Light | Box |  | Box |   ...   | Box |
# ----------------------------------------->
#       |  0  |  |  1  |   ...   | 255 |
#       +-----+  +-----+         +-----+
# Inside each box, there are several lens slots that will keep a lens correctly positioned to focus
# light passing through the box. The side of each box has a panel that opens to allow you to insert
# or remove lenses as necessary.
#
# Along the wall running parallel to the boxes is a large library containing lenses organized by
# focal length ranging from 1 through 9. The reindeer also brings you a small handheld label
# printer.
#
# The book goes on to explain how to perform each step in the initialization sequence, a process it
# calls the Holiday ASCII String Helper Manual Arrangement Procedure, or HASHMAP for short.
#
# Each step begins with a sequence of letters that indicate the label of the lens on which the step
# operates. The result of running the HASH algorithm on the label indicates the correct box for that
# step.
#
# The label will be immediately followed by a character that indicates the operation to perform:
# either an equals sign (=) or a dash (-).
#
# If the operation character is a dash (-), go to the relevant box and remove the lens with the
# given label if it is present in the box. Then, move any remaining lenses as far forward in the box
# as they can go without changing their order, filling any space made by removing the indicated
# lens. (If no lens in that box has the given label, nothing happens.)
#
# If the operation character is an equals sign (=), it will be followed by a number indicating the
# focal length of the lens that needs to go into the relevant box; be sure to use the label maker to
# mark the lens with the label given in the beginning of the step so you can find it later. There
# are two possible situations:
#
# If there is already a lens in the box with the same label, replace the old lens with the new lens:
# remove the old lens and put the new lens in its place, not moving any other lenses in the box. If
# there is not already a lens in the box with the same label, add the lens to the box immediately
# behind any lenses already in the box. Don't move any of the other lenses when you do this. If
# there aren't any lenses in the box, the new lens goes all the way to the front of the box.
# Here is the contents of every box after each step in the example initialization sequence above:
#
# After "rn=1":
# Box 0: [rn 1]
#
# After "cm-":
# Box 0: [rn 1]
#
# After "qp=3":
# Box 0: [rn 1]
# Box 1: [qp 3]
#
# After "cm=2":
# Box 0: [rn 1] [cm 2]
# Box 1: [qp 3]
#
# After "qp-":
# Box 0: [rn 1] [cm 2]
#
# After "pc=4":
# Box 0: [rn 1] [cm 2]
# Box 3: [pc 4]
#
# After "ot=9":
# Box 0: [rn 1] [cm 2]
# Box 3: [pc 4] [ot 9]
#
# After "ab=5":
# Box 0: [rn 1] [cm 2]
# Box 3: [pc 4] [ot 9] [ab 5]
#
# After "pc-":
# Box 0: [rn 1] [cm 2]
# Box 3: [ot 9] [ab 5]
#
# After "pc=6":
# Box 0: [rn 1] [cm 2]
# Box 3: [ot 9] [ab 5] [pc 6]
#
# After "ot=7": Box 0: [rn 1] [cm 2] Box 3: [ot 7] [ab 5] [pc 6] All 256 boxes are always present;
# only the boxes that contain any lenses are shown here. Within each box, lenses are listed from
# front to back; each lens is shown as its label and focal length in square brackets.
#
# To confirm that all of the lenses are installed correctly, add up the focusing power of all of the
# lenses. The focusing power of a single lens is the result of multiplying together:
#
# One plus the box number of the lens in question. The slot number of the lens within the box: 1 for
# the first lens, 2 for the second lens, and so on. The focal length of the lens. At the end of the
# above example, the focusing power of each lens is as follows:
#
# rn: 1 (box 0) * 1 (first slot) * 1 (focal length) = 1
# cm: 1 (box 0) * 2 (second slot) * 2 (focal length) = 4
# ot: 4 (box 3) * 1 (first slot) * 7 (focal length) = 28
# ab: 4 (box 3) * 2 (second slot) * 5 (focal length) = 40
# pc: 4 (box 3) * 3 (third slot) * 6 (focal length) = 72
# So, the above example ends up with a total focusing power of 145.
#
# With the help of an over-enthusiastic reindeer in a hard hat, follow the initialization sequence.
# What is the focusing power of the resulting lens configuration?
#
#
# Answer for sample input: 136
# Answer for input: 103614

FILENAME = 'input.txt'

def parse_input(file_name: str) -> list[list[str]]:
    """
    Parses input file
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e

    return data[0].split(',')            

def convert_to_ascii(segment:str):
    """
    Converts a segment of the instruction set to char_val per given rules
    """
    char_val = 0
    for i in segment:
        char_val += ord(i)
        char_val *= 17
        char_val %= 256
        
    return char_val

def parse_instructions(instructions: list[str]) -> list[dict]:
    """
    Parses instructions into a list of dicts with the relevant properties
    """
    parsed_instructions = []
    
    for instruction in instructions:
        if '-' in instruction:
            operator = '-'
            label = instruction.split('-')[0]
        else:
            operator = '='
            label, focal_length = instruction.split('=')
        parsed_instruction = {'operator': operator, 
                              'label': label, 
                              'box_id': convert_to_ascii(label), 
                              'focal_length': focal_length}
        parsed_instructions.append(parsed_instruction)
    
    return parsed_instructions

def process_instructions(parsed_instructions, boxes, labels_to_focal_lengths):
    for instruction in parsed_instructions:
        box_id = instruction['box_id']
        label = instruction['label']
    
        # Remove lens with the given label
        if instruction['operator'] == '-':
            if boxes[box_id] is None:
                continue
            if label in boxes[box_id]:
                boxes[box_id].remove(label)
                if len(boxes[box_id]) == 0:
                    boxes[box_id] = None
            continue
    
        # Add lens with the given label
        focal_length = instruction['focal_length']
    
        if boxes[box_id] is None:
            boxes[box_id] = [label]
            labels_to_focal_lengths[label] = focal_length
            continue
    
        if label in boxes[box_id]:
            labels_to_focal_lengths[label] = focal_length
            continue
    
        boxes[box_id].append(label)    
        labels_to_focal_lengths[label] = focal_length

def calculate_focusing_power(boxes, labels_to_focal_lengths):
    """ Adds up focusing power per provided rules """    
    total_focusing_power = 0
    for box_id in range(256):
        if boxes[box_id] is None:
            continue
        for lens_id, lens in enumerate(boxes[box_id]):
            factor_one = box_id + 1
            factor_two = lens_id + 1
            factor_three = int(labels_to_focal_lengths[lens])
            focusing_power = factor_one * factor_two * factor_three
            total_focusing_power += focusing_power
    return total_focusing_power

def main():
    """
    Main function that reads the file, parses instructions
    """
    instructions = parse_input(FILENAME)
    
    parsed_instructions = parse_instructions(instructions)

    # Initialize boxes and focal lengths lookup dictionary
    boxes = [None] * 256
    labels_to_focal_lengths = {}
    
    # Process instructions to fill boxes and rearrange lenses
    process_instructions(parsed_instructions, boxes, labels_to_focal_lengths)

    # Sum focusing power
    print(f'Total focusing power: {calculate_focusing_power(boxes, labels_to_focal_lengths)}')    
        
if __name__ == "__main__":
    main()

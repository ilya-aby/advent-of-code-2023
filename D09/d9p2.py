"""
This module solves Part Two of Day 9's problem of the Advent of Code challenge.
Same recursive solution as Part One with trivial differences to look at diffs to the first value
instead of the last value.
"""
# --- Part Two ---
# Of course, it would be nice to have even more history included in your report. Surely it's safe to
# just extrapolate backwards as well, right?
#
# For each history, repeat the process of finding differences until the sequence of differences is
# entirely zero. Then, rather than adding a zero to the end and filling in the next values of each
# previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then
# fill in new first values for each previous sequence.
#
# In particular, here is what the third example history looks like when extrapolating back in time:
#
# 5  10  13  16  21  30  45
#   5   3   3   5   9  15
#    -2   0   2   4   6
#       2   2   2   2
#         0   0   0
# Adding the new values on the left side of each sequence from bottom to top eventually reveals the
# new left-most history value: 5.
#
# Doing this for the remaining example data above results in previous values of -3 for the first
# history and 0 for the second history. Adding all three new values together produces 2.
#
# Analyze your OASIS report again, this time extrapolating the previous value for each history. What
# is the sum of these extrapolated values?
# 
# Answer for sample input: 2
# Answer for input: 1087

FILENAME = 'input.txt'

def parse_sequences(file_name) -> list:
    """
    Parses a sequence file and returns a list of sequences
    """

    # Ingest input file
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
    except (FileNotFoundError, IOError) as e:
        raise RuntimeError(f"An error occurred: {e}") from e
    
    sequences = [line.strip().split() for line in data]

    return sequences

def get_prev_val(sequence: list) -> int:
    """
    Recursively finds the previous value in a sequence by looking at the differences between each
    value until every difference is the same
    """    
    diffs = [int(sequence[i+1]) - int(sequence[i]) for i in range(len(sequence) - 1)]
    
    # If difference between all values is the same, that's the delta to the previous value
    if len(set(diffs)) == 1:
        return int(sequence[0]) - diffs[0]

    return int(sequence[0]) - get_prev_val(diffs)

def main():
    """
    Main function that reads the input file, parses the sequences, and sums the previous values
    """
    sequences = parse_sequences(FILENAME)

    prev_vals = [get_prev_val(sequence) for sequence in sequences]
        
    # Display sum of previous vals
    print(f'Sum of final sequence values: {sum(prev_vals)}')    
     
if __name__ == "__main__":
    main()

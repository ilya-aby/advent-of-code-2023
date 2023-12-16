"""
This module solves Part One of Day X's problem of the Advent of Code challenge.

"""

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    
    data = open(filename).read().strip() ## Uncomment to split single-line by char: .split(',')
    lines = data.split('\n')
    output = [[char for char in row] for row in lines]
    
    return output

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    data = parse_input("sample.txt")
    
    print(data)

if __name__ == "__main__":
    main()
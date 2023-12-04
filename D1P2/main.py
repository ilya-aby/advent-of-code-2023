# --- Part Two ---
# Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
#
# Equipped with this new information, you now need to find the real first and last digit on each line. For example:
#
# two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen
# In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
#
# What is the sum of all of the calibration values?
#
# Answer for sample input: 281
# Answer for input: 54078

import re

FILENAME = 'input.txt'

# Convert a word to a number
def word_to_num(word):
    word_to_digit = {
        "one": 1, "two": 2, "three": 3, "four": 4,"five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    }
    return word_to_digit.get(word.lower(), None)

# Helper function to take a digit like 2 or a word like 'two' and return the string of the integer (e.g. '2') for either
def convert_to_string(num):
    if num.isdigit():
        return str(num)
    else:
        return str(word_to_num(num))

# Ingest input file
try:
    with open(FILENAME, 'r') as f:
        data = f.read().splitlines()
except FileNotFoundError:
    print(f"File {FILENAME} not found.")
    exit(1)

runningTotal = 0

# Go line by line in the input file and compute over each line
for line in data:
    # Using Regexp, look for any matches of numbers or number spelled out as words
    matches = re.findall(r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))', line)
    
    if matches:  
        firstNum = convert_to_string(matches[0])
        lastNum = convert_to_string(matches[-1])

        print(f"Line: {line}; firstNum: {firstNum}; lastNum: {lastNum}")
        finalNum = int(firstNum + lastNum)
        runningTotal += finalNum

print(f"Final total: {runningTotal}")

"""
This module solves Part Two of Day 19's problem of the Advent of Code challenge.
The approach here is to work backwards from the rules with acceptance criteria, and build up a
dictionary of intervals that satisfy the rule. Then the answer is just the product of the number
of permutations in each interval set.
"""
# --- Part Two ---
# Even with your help, the sorting process still isn't fast enough.
#
# One of the Elves comes up with a new plan: rather than sort parts individually through all of
# these workflows, maybe you can figure out in advance which combinations of ratings will be
# accepted or rejected.
#
# Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a
# maximum of 4000. Of all possible distinct combinations of ratings, your job is to figure out which
# ones will be accepted.
#
# In the above example, there are 167409079868000 distinct combinations of ratings that will be
# accepted.
#
# Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort
# is no longer relevant. How many distinct combinations of ratings will be accepted by the Elves'
# workflows?

from icecream import ic

MIN_VAL = 1
MAX_VAL = 4000

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    data = open(filename).readlines()
    rules_list = data[:data.index('\n')]
    
    rule_dict = {}
    for line in rules_list:
        label, rules = line.split('{')
        rules = rules.strip('}\n').split(',')
        rule_dict[label] = rules
    
    return rule_dict

def refine_intervals(rule, intervals, reject = True):
    """
    Given a rule and a set of intervals, refine the intervals to only include values that
    satisfy the rule. If reject = True it will refine the intervals to make sure the
    values are refined to make the rule not be true instead.
    """
    
    test_label = rule[0] # e.g. x, m, a, or s
    test_operator = rule[1] # > or <
    test_value = rule.split(':')[0][2:] # e.g. 1351
    
    min_constraint = intervals[test_label][0]
    max_constraint = intervals[test_label][1]
    
    # If the rule is a reject, we want to refine the intervals to make sure the
    # values are refined to make the rule not be true
    if reject:
        if test_operator == '<':
            if min_constraint < int(test_value):
                min_constraint = int(test_value)
        if test_operator == '>':
            if max_constraint > int(test_value):
                max_constraint = int(test_value)
    else:
        if test_operator == '<':
            if max_constraint > int(test_value):
                max_constraint = int(test_value) - 1
        if test_operator == '>':
            if min_constraint < int(test_value):
                min_constraint = int(test_value) + 1
    
    # Create a new tuple with the refined intervals and update the constraints dictionary
    intervals[test_label] = (min_constraint, max_constraint)
    
    return

def find_prior_rule(rule_key, rule_dict):
    """
    Given a rule key, find the prior rule set and rule id that led to it
    """
    for key in rule_dict.keys():
        for rule_id, rule in enumerate(rule_dict[key]):
            if rule.endswith(':' + rule_key) or rule == rule_key:
                return key, rule_dict[key], rule_id

    return

def get_intervals_for_rule_set(rule_key_for_final_rule_set, final_rule_id, rule_dict):
    """
    For each rule with an acceptance in a rule set, work backwards from the end to find 
    valid ranges
    """
    
    # Ranges begin completely unbounded from 1 to 4000
    # We refine them as we work backwards through the rules
    intervals = {'x': (MIN_VAL, MAX_VAL),
                 'm': (MIN_VAL, MAX_VAL),
                 'a': (MIN_VAL, MAX_VAL),
                 's': (MIN_VAL, MAX_VAL)}
    
    rule_key = rule_key_for_final_rule_set
    rule_set = rule_dict[rule_key]
    rule_id = final_rule_id
    
    while True:
        # This is the heart of the logic that makes this solution work. 
        # - If we're looking at a 'normal' evaluation rule, tighten the constraints to make it true
        # - Then slide backwards through this rule set to make all the predecessor rules evaluate to 
        # false, because that's the only way we could have arrived at this rule. 
        # - Then look at the label of this rule and find the prior rule set that led to it since
        # we know there is one and only one possible jump here 
        # - Then repeat the process until we reach the 'in' rule that starts execution
        # - This gets us a set of intervals that get us to the final condition we started
        # working backwards from
        if rule_set[rule_id] != 'A' and rule_set[rule_id] not in rule_dict.keys():
            refine_intervals(rule_set[rule_id], intervals, False)
        for predecessor_rule_id in range(rule_id - 1, -1, -1):
            refine_intervals(rule_set[predecessor_rule_id], intervals, True)
        if rule_key == 'in':
            break
        rule_key, rule_set, rule_id = find_prior_rule(rule_key, rule_dict)
    return intervals

def count_permutations(constraints):
    """
    Given a dictionary of constraints, count the number of permutations that satisfy the constraints
    """
    total_permutations = 1
    for lower, upper in constraints.values():
        total_permutations *= (upper - lower + 1)
    return total_permutations

def find_accepted_combinations(rule_dict):
    """
    Finds all combinations of x, m, a, and s that satisfy the rules
    
    Approach: use dynamic programming and interval trees. Work backwards from rules with
    acceptance criteria, and build up a dictionary of intervals that satisfy the rule.
    Then, merge the intervals and repeat until we have a single interval that satisfies
    all rules. Finally, count the number of integers in the merged interval.
    """
    
    rules_with_acceptances = []
    
    # Find any rule that has an acceptance criteria
    # We will work backwards from the rule set that contains it
    # To find valid ranges for each of the four values
    for key in rule_dict.keys():
        for rule_id, rule in enumerate(rule_dict[key]):
            if 'A' in rule:
                rules_with_acceptances.append((key, rule_id)) 
    
    # For each rule, work backwards from the end to find valid ranges
    intervals = []
    for rule_key, rule_id in rules_with_acceptances:
        intervals.append(get_intervals_for_rule_set(rule_key, rule_id, rule_dict))

    ic(intervals)

    # Sum up the combinations implied by each interval range we found working backwards
    # from each acceptance criteris
    total_combinations = 0
    for interval in intervals:
        total_combinations += count_permutations(interval)
    
    return total_combinations

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    rule_dict = parse_input("input.txt")
    
    print(f'Total combinations: {find_accepted_combinations(rule_dict)}')
    
    return

if __name__ == "__main__":
    main()

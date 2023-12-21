"""
This module solves Part Two of Day 20's problem of the Advent of Code challenge.
Sort of an unsatisfying non-generalized solution that we found by working backwards from the
four modules pointing at the final rx module. We find when each of them activates and then take
the LCM to get the amount of cycles it takes to get them to fire at the same time, which then
turns on the final module. Also added a bit of code to visualize the modules as a graphviz file.
"""
import heapq
import math
from icecream import ic
import graphviz

modules = {}

def parse_input(filename):
    """
    Reads in the input file and returns the contents
    """
    with open(filename, 'r') as file:
        data = file.read().splitlines()
    
    # Create initial modules list
    for line in data:
        category = None
        label = None
        state = None
        links = []
        label, links = line.split(' -> ')
        links = links.split(', ')
        if label[0] == '%':
            category = 'flipflop'
            label = label[1:]
            state = 'off'
        elif label[0] == '&':
            category = 'conj'
            label = label[1:]
        elif label == 'broadcaster':
            category = 'broadcaster'
        else:
            category = 'rx'
        modules[label] = {'category': category, 
                          'links': links, 
                          'state': state,
                          'inbound_links': {},
                          'transmissions': {'low': 0, 'high': 0}}

    # Manually create the rx module
    modules['rx'] = {'category': 'rx',
                     'links': [],
                     'state': None,
                     'inbound_links': {},
                     'transmissions': {'low': 0, 'high': 0}}

    # Set each module's inbound links
    for label, module in modules.items():
        # Look at its downstream links and set the inbound links for each to point to us
        for downstream_link in module['links']:
            if downstream_link in modules:
                modules[downstream_link]['inbound_links'][label] = 'low'

    return modules

def process_signal(sender, strength, receiver):
    """
    Given a signal strength and destination, process the signal and return a list of new signals
    """
    
    if sender != 'button':
        modules[sender]['transmissions'][strength] += 1
    
    new_signals = []
    # If the module isn't in our module list, assume it's a debug output and ignore it
    if receiver not in modules or modules[receiver]['category'] == 'rx':
        return new_signals
    
    # Broadcast module relays signal sent to it to all downstream links
    if modules[receiver]['category'] == 'broadcaster':
        for link in modules[receiver]['links']:
            heapq.heappush(new_signals, (receiver, strength, link))
        return new_signals
    
    if modules[receiver]['category'] == 'flipflop':
        # Flip-flops receiving high pulse does nothing
        if strength == 'high':
            return new_signals
        
        # Flip-flops change state and send low or high pulse depending on state
        new_state = 'on' if modules[receiver]['state'] == 'off' else 'off'
        new_strength = 'high' if new_state == 'on' else 'low'
        modules[receiver]['state'] = new_state
        for link in modules[receiver]['links']:
            heapq.heappush(new_signals, (receiver, new_strength, link))
        return new_signals
    
    if modules[receiver]['category'] == 'conj':
        # Conjunctions keep a memory of past signals received
        # First, update the memory with the new signal
        modules[receiver]['inbound_links'][sender] = strength
        
        # Then check if our 'memory' remembers high signals from all links
        # If so, send a low signal to all links
        if all([modules[receiver]['inbound_links'][link] == 'high' \
                for link in modules[receiver]['inbound_links'].keys()]):
            new_strength = 'low'
        else:
            new_strength = 'high'
            
        for link in modules[receiver]['links']:
            heapq.heappush(new_signals, (receiver, new_strength, link))

        return new_signals
    
    ic(modules)
    return

def push_button():
    """
    Sends initial pulse and traces out the signals
    """
    # Stack will contain tuples that represent a signal strength & destination
    # Initial button press sends low pulse to broadcast
    times_button_pressed = 0
    
    queue = []

    pulses_sent = {'low': 0, 'high': 0}
    high_pri_signals = []

    while True:
        if queue:
            new_signals = []
            sender, strength, receiver = heapq.heappop(queue)
            pulses_sent[strength] += 1
            new_signals = process_signal(sender, strength, receiver)
            for signal in new_signals:
                heapq.heappush(queue, signal)

            target_modules = ['jq', 'cc', 'sp', 'nx']
            for signal in new_signals:
                if signal[0] in target_modules and signal[1] == 'high':
                    high_pri_signals.append(times_button_pressed)
                    print(f'High pulse sent from {signal[0]} after {times_button_pressed} button presses')
                    if len(high_pri_signals) == 4:
                        print(f'High pulse sent from all modules: {high_pri_signals}')
                        print(f'LCM of pulses: {math.lcm(*[signal for signal in high_pri_signals])}')
                        return
        else:
            # We can push the button again if no signals in queue
            times_button_pressed += 1
            heapq.heappush(queue, ('button', 'low', 'broadcaster'))
    return

def visualize_modules():
    """ Code from Eugene to export graphviz notation of modules for render """
    dot = graphviz.Digraph(comment="Modules")
    for name, module in modules.items():
        # flip is red, conj is blue
        color = "black"
        if module['category'] == "flipflop":
            color = "red"
        elif module['category'] == "conj":
            color = "blue"
        dot.node(name, name, color=color)
        for dest in module['links']:
            dot.edge(name, dest)
    with open('digraph.txt', 'w') as f:
        f.write(dot.source)

def main():
    """
    Reads in the input file, processes and outputs the solution
    """
    parse_input("input.txt")
    visualize_modules()
    push_button()

if __name__ == "__main__":
    main()

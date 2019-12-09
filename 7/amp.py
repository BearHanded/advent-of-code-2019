from intcode import XmasComputer

# Prep Program  and kick off ###############
fp = open('./input.txt', 'r')
original_state = list(map(lambda x: int(x), fp.read().split(",")))
program = original_state[:]
xmasComputer = XmasComputer(program)

# Run and compare
program_result = xmasComputer.run()

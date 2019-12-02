import sys

fp = open('./input.txt', 'r')


def addition(a_idx, b_idx, out_idx):
    program[program[out_idx]] = program[program[a_idx]] + program[program[b_idx]]
    return


def multiply(a_idx, b_idx, out_idx):
    program[program[out_idx]] = program[program[a_idx]] * program[program[b_idx]]
    return


def exit_program():
    print "--------------------------"
    print "program exit: ", program[0]


def run():
    opcodes = {
        1: addition,
        2: multiply,
        99: exit_program
    }
    cursor = 0

    print program

    while cursor <= len(program):
        if (program[cursor]) == 99:
            exit_program()
            break

        # Pass indexes to operation
        operation = opcodes.get(program[cursor])
        try:
            operation(cursor + 1, cursor + 2, cursor + 3)
        except:
            print "An error in the program occured"
            break
        cursor += 4  # move to the next opcode
    return program[0]


# RUN
original_state = map(lambda x: int(x), fp.read().split(","))
program = original_state[:]
goal = 19690720

for noun in range(0, 100):
    for verb in range(0, 100):
        # Setup program state
        program = original_state[:]
        print program
        program[1] = noun
        program[2] = verb

        # Run and compare
        program_result = run()
        print noun, verb
        if program_result == goal:
            print "--------------------------"
            print noun, verb
            sys.exit();
run()

import sys
test_math_input = './test_input.txt'
test_mult = './test_input_mult.txt'
puzzle_input = './input.txt'
test_in_out = './in_out.txt'
PROGRAM_INPUT = 20
PROGRAM_FILE = puzzle_input

# OPERATIONS ############
def add(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
    idx_out = program[cursor + 3]

    program[idx_out] = params[0] + params[1]
    return


def multiply(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
    idx_out = program[cursor + 3]

    program[idx_out] = params[0] * params[1]
    return


def write_in(cursor):
    idx_out = program[cursor + 1]
    user_input = input("Program Input: ")
    user_input = int(user_input)
    program[idx_out] = user_input
    return


def write_out(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1])
    print("---", params[0])
    return


def exit_program(cursor):
    print("-------- PROGRAM END ---------")
    print(program)
    print("Result: ", program[0])
    exit()


def jump_if_true(cursor):
    return

def jump_if_false(cursor):
    return


def less_than(cursor):
    return

def equals(cursor):
    return
# Helper Functions ##############

def get_vals_from_mode(op_idx, parameter_idxs):
    values = []
    operation_with_modes = program[op_idx]

    mode_idx = 0
    mode_list = str(operation_with_modes)[:-2][::-1]  # this is dumb
    for parameter_idx in parameter_idxs:
        # Determine Mode
        if mode_idx < len(mode_list):
            mode = int(mode_list[mode_idx])
        else:
            mode = 0

        # pass through or access memory
        if int(mode) == 1:
            values.append(program[parameter_idx])  # just use the value at the location
        else:
            values.append(program[program[parameter_idx]])  # Use the value at the address listed

        mode_idx += 1

    return values



# Main Cycle ####################
def run():
    opcodes = {
        1: (add, 3),
        2: (multiply, 3),
        3: (write_in, 1),
        4: (write_out, 1),
        5: (jump_if_true, 2),
        6: (jump_if_false, 2),
        7: (less_than, 3),
        8: (equals, 3)
        99: (exit_program, 1)
    }
    cursor = 0

    print(program)

    while cursor < len(program):
        # Pass indexes to operation
        operation_entry = opcodes.get(program[cursor] % 100)
        operation = operation_entry[0]
        operation_length = operation_entry[1] + 1

        # Perform instruction
        operation(cursor)

        cursor += operation_length  # move to the next opcode
    return program[0]


# Prep Program  and kick off ###############
fp = open(PROGRAM_FILE, 'r')
original_state = list(map(lambda x: int(x), fp.read().split(",")))
program = original_state[:]
goal = 19690720

# Run and compare
program_result = run()

import sys

test_math_input = './test_input.txt'
test_mult = './test_input_mult.txt'
puzzle_input = './input.txt'
puzzle_two = './puzzle_2.txt'
test_in_out = './in_out.txt'
test_part_2 = './test_part_2.txt'
PROGRAM_FILE = puzzle_two
instruct_pointer = 0
program = []


# OPERATIONS ############
def add(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
    idx_out = program[cursor + 3]

    program[idx_out] = params[0] + params[1]
    return True


def multiply(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
    idx_out = program[cursor + 3]

    program[idx_out] = params[0] * params[1]
    return True


def write_in(cursor):
    out_idx = program[cursor + 1]
    user_input = input("Program Input: ")
    user_input = int(user_input)
    program[out_idx] = user_input
    return True


def write_out(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1])
    print("- ", params[0])
    return True


def exit_program(cursor):
    print("-------- PROGRAM END ---------")
    print(program)
    print("Result: ", program[0])
    exit()


def jump_if_true(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
    if params[0] != 0:
        global instruct_pointer
        instruct_pointer = params[1]
        return False
    return True


def jump_if_false(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
    if params[0] == 0:
        global instruct_pointer
        instruct_pointer = params[1]
        return False
    return True


def less_than(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
    out_idx = program[cursor + 3]
    if params[0] < params[1]:
        program[out_idx] = 1
    else:
        program[out_idx] = 0
    return True


def equals(cursor):
    params = get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
    out_idx = program[cursor + 3]
    if params[0] == params[1]:
        program[out_idx] = 1
    else:
        program[out_idx] = 0
    return True


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
        8: (equals, 3),
        99: (exit_program, 1)
    }

    print(program)
    global instruct_pointer
    while instruct_pointer < len(program):
        # Pass indexes to operation
        operation_entry = opcodes.get(program[instruct_pointer] % 100)
        operation = operation_entry[0]
        operation_length = operation_entry[1] + 1

        # Perform instruction
        continue_normal = operation(instruct_pointer)
        if continue_normal:
            instruct_pointer += operation_length  # move to the next opcode
    return program[0]


# Prep Program  and kick off ###############
fp = open(PROGRAM_FILE, 'r')
original_state = list(map(lambda x: int(x), fp.read().split(",")))
program = original_state[:]

# Run and compare
program_result = run()

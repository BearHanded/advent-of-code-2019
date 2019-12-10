from itertools import permutations


def main():
    # Prep Program  and kick off ###############
    fp = open('./input.txt', 'r')
    # TODO verify big numbers
    # TODO add to any address
    original_state = list(map(lambda x: int(x), fp.read().split(",")))

    program = original_state[:]
    xmas_computer = XmasComputer(program, queue_out=[])
    output = xmas_computer.run()
    print(program)
    print(output)
    print(xmas_computer.queue_out)


class XmasComputer:
    memory = []
    exit_flag = False
    instruct_pointer = 0
    program_input = None
    program_output = None
    queue_in = None
    queue_out = None
    awaiting = False
    relative_base = 0

    def set_memory(self, program):
        self.memory = program

    def __init__(self):
        self.set_memory([])

    def __init__(self, program, queue_in=None, queue_out=None):
        self.set_memory(program[:])
        self.exit_flag = False
        self.queue_in = queue_in
        self.queue_out = queue_out

    # OPERATIONS ############
    def add(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        idx_out = self.read(cursor + 3)

        self.save(idx_out, params[0] + params[1])
        self.instruct_pointer += 4
        return

    def multiply(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        idx_out = self.read(cursor + 3)

        self.save(idx_out, params[0] * params[1])
        self.instruct_pointer += 4
        return

    def write_in(self, cursor):
        out_idx = self.read(cursor + 1)

        if self.program_input is not None and len(self.program_input) > 0:
            user_input = int(self.program_input.pop(0))
            self.save(out_idx, user_input)
        elif self.queue_in is not None:
            if len(self.queue_in) <= 0:
                self.awaiting = True
                return
            else:
                user_input = int(self.queue_in.pop(0))
                self.save(out_idx, user_input)

        else:
            user_input = input("Program Input Requested: ")
            user_input = int(user_input)
            self.save(out_idx, user_input)

        self.instruct_pointer += 2
        return

    def write_out(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1])
        if self.queue_out is not None:
            self.queue_out.append(params[0])
        self.program_output = params[0]

        self.instruct_pointer += 2
        return

    def exit_program(self, cursor):
        self.exit_flag = True

    def jump_if_true(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        if params[0] != 0:
            self.instruct_pointer = params[1]
            return
        self.instruct_pointer += 3
        return

    def jump_if_false(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        if params[0] == 0:
            self.instruct_pointer = params[1]
            return
        self.instruct_pointer += 3
        return

    def less_than(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        out_idx = self.read(cursor + 3)
        if params[0] < params[1]:
            self.save(out_idx, 1)
        else:
            self.save(out_idx, 0)
        self.instruct_pointer += 4
        return

    def equals(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        out_idx = self.read(cursor + 3)
        if params[0] == params[1]:
            self.save(out_idx, 1)
        else:
            self.save(out_idx, 0)
        self.instruct_pointer += 4
        return

    def relative_base_offset(self, cursor):
        self.relative_base += self.read(cursor + 1)
        self.instruct_pointer += 2
        return

    # Helper Functions ##############
    def get_vals_from_mode(self, op_idx, parameter_idxs):
        values = []
        operation_with_modes = self.read(op_idx)

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
                values.append(self.read(parameter_idx))  # just use the value at the location
            elif int(mode) == 2:
                values.append(self.read(parameter_idx + self.relative_base))
            else:
                values.append(self.read(self.read(parameter_idx)))  # Use the value at the address listed

            mode_idx += 1

        return values

    def save(self, index, value):
        if index >= len(self.memory):
            n = index - len(self.memory) + 1
            # TODO keep an eye on this deep vs shallow ref
            self.memory.extend([0 for i in range(n)])

        self.memory[index] = value
        return

    def read(self, index):
        if index >= len(self.memory):
            n = index - len(self.memory) + 1
            self.memory.extend([0 for i in range(n)])

        return self.memory[index]

    # Main Cycle ####################
    def run(self, params=None):
        self.program_input = params

        opcodes = {
            1: self.add,
            2: self.multiply,
            3: self.write_in,
            4: self.write_out,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.relative_base_offset,
            99: self.exit_program,
        }
        if self.awaiting and len(self.queue_in) > 0:
            self.awaiting = False
        while self.instruct_pointer < len(self.memory) and not self.exit_flag and not self.awaiting:
            # Pass indexes to operation
            operation = opcodes.get(self.memory[self.instruct_pointer] % 100)

            # Perform instruction
            operation(self.instruct_pointer)
        if self.awaiting:
            return
        else:
            return self.program_output


main()

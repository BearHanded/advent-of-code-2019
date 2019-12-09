from itertools import permutations


def main():
    # Prep Program  and kick off ###############
    fp = open('./input.txt', 'r')
    original_state = list(map(lambda x: int(x), fp.read().split(",")))

    perms = [''.join(p) for p in permutations('56789')]
    max_value = 0

    for entry in perms:
        amplifiers = []
        queues = []

        for phase_setting in entry:
            queues.append([])

        total_amplifiers = len(queues)
        amplifier_number = 0
        for phase_setting in entry:
            program = original_state[:]
            if amplifier_number == total_amplifiers - 1:
                output_queue = 0
            else:
                output_queue = amplifier_number
            xmas_computer = XmasComputer(program, queue_in=queues[amplifier_number], queue_out=queues[output_queue])
            amplifiers.append(xmas_computer)
            amplifier_number += 1

        halted_count = 0
        curr_amplifier = 0
        first_run = True
        while halted_count < total_amplifiers:
            print(entry, curr_amplifier, amplifiers[curr_amplifier].exit_flag)
            if not amplifiers[curr_amplifier].exit_flag:
                if first_run:
                    signal_out = amplifiers[curr_amplifier].run([0])
                    first_run = False
                else:
                    signal_out = amplifiers[curr_amplifier].run()
                if amplifiers[curr_amplifier].exit_flag:
                    halted_count += 1

            curr_amplifier += 1
            if curr_amplifier >= total_amplifiers:
                curr_amplifier = 0
                print(queues)

        print("signal_out = ", signal_out)


class XmasComputer:
    memory = []
    exit_flag = False
    instruct_pointer = 0
    program_input = None
    program_output = None
    queue_in = None
    queue_out = None
    awaiting = False

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
        idx_out = self.memory[cursor + 3]

        self.memory[idx_out] = params[0] + params[1]
        self.instruct_pointer += 4
        return

    def multiply(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        idx_out = self.memory[cursor + 3]

        self.memory[idx_out] = params[0] * params[1]
        self.instruct_pointer += 4
        return

    def write_in(self, cursor):
        out_idx = self.memory[cursor + 1]

        if self.program_input is not None and len(self.program_input) > 0:
            user_input = int(self.program_input.pop(0))
            self.memory[out_idx] = user_input
        elif self.queue_in is not None:
            if len(self.queue_in) <= 0:
                self.awaiting = True
                return
            else:
                user_input = int(self.program_input.pop(0))
                self.memory[out_idx] = user_input

        else:
            user_input = input("Program Input Requested: ")
            user_input = int(user_input)
            self.memory[out_idx] = user_input

        self.instruct_pointer += 2
        return

    def write_out(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1])
        if self.queue_out is None:
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
        self.instruct_pointer += 2
        return

    def jump_if_false(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        if params[0] == 0:
            self.instruct_pointer = params[1]
            return
        self.instruct_pointer += 2
        return

    def less_than(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        out_idx = self.memory[cursor + 3]
        if params[0] < params[1]:
            self.memory[out_idx] = 1
        else:
            self.memory[out_idx] = 0
        self.instruct_pointer += 4
        return

    def equals(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        out_idx = self.memory[cursor + 3]
        if params[0] == params[1]:
            self.memory[out_idx] = 1
        else:
            self.memory[out_idx] = 0
        self.instruct_pointer += 4
        return

    # Helper Functions ##############
    def get_vals_from_mode(self, op_idx, parameter_idxs):
        values = []
        operation_with_modes = self.memory[op_idx]

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
                values.append(self.memory[parameter_idx])  # just use the value at the location
            else:
                values.append(self.memory[self.memory[parameter_idx]])  # Use the value at the address listed

            mode_idx += 1

        return values

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
            99: self.exit_program,
        }
        if self.awaiting and len(self.queue_in) > 0:
            self.awaiting == False
        while self.instruct_pointer < len(self.memory) and not self.exit_flag and not self.awaiting:
            print(self.instruct_pointer)
            # Pass indexes to operation
            operation = opcodes.get(self.memory[self.instruct_pointer] % 100)

            # Perform instruction
            operation(self.instruct_pointer)
        if self.awaiting:
            return
        else:
            return self.program_output


main()

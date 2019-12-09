class XmasComputer:
    memory = []
    exit_flag = False
    instruct_pointer = 0

    def set_memory(self, program):
        self.memory = program

    def __init__(self):
        self.set_memory([])

    def __init__(self, program):
        self.set_memory(program)

    # OPERATIONS ############
    def add(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        idx_out = self.memory[cursor + 3]

        self.memory[idx_out] = params[0] + params[1]
        return True

    def multiply(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        idx_out = self.memory[cursor + 3]

        self.memory[idx_out] = params[0] * params[1]
        return True

    def write_in(self, cursor):
        out_idx = self.memory[cursor + 1]
        user_input = input("Program Input: ")
        user_input = int(user_input)
        self.memory[out_idx] = user_input
        return True

    def write_out(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1])
        print("- ", params[0])
        return True

    def exit_program(self, cursor):
        print("-------- PROGRAM END ---------")
        print(self.memory)
        print("Result: ", self.memory[0])
        self.exit_flag = True

    def jump_if_true(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        if params[0] != 0:
            self.instruct_pointer = params[1]
            return False
        return True

    def jump_if_false(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        if params[0] == 0:
            self.instruct_pointer = params[1]
            return False
        return True

    def less_than(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        out_idx = self.memory[cursor + 3]
        if params[0] < params[1]:
            self.memory[out_idx] = 1
        else:
            self.memory[out_idx] = 0
        return True

    def equals(self, cursor):
        params = self.get_vals_from_mode(cursor, [cursor + 1, cursor + 2])
        out_idx = self.memory[cursor + 3]
        if params[0] == params[1]:
            self.memory[out_idx] = 1
        else:
            self.memory[out_idx] = 0
        return True

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
    def run(self):
        self.exit_flag = False
        opcodes = {
            1: (self.add, 3),
            2: (self.multiply, 3),
            3: (self.write_in, 1),
            4: (self.write_out, 1),
            5: (self.jump_if_true, 2),
            6: (self.jump_if_false, 2),
            7: (self.less_than, 3),
            8: (self.equals, 3),
            99: (self.exit_program, 1)
        }

        print(self.memory)
        while self.instruct_pointer < len(self.memory) and not self.exit_flag:
            # Pass indexes to operation
            operation_entry = opcodes.get(self.memory[self.instruct_pointer] % 100)
            operation = operation_entry[0]
            operation_length = operation_entry[1] + 1

            # Perform instruction
            continue_normal = operation(self.instruct_pointer)
            if continue_normal:
                self.instruct_pointer += operation_length  # move to the next opcode
        return self.memory[0]
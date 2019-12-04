import time
import copy

start_time = time.time()


########################
# Distance Calculation and search
########################
def find_closest_intersection(w_grid):
    for w_map in w_grid:
        match_found = False
        x_len = len(w_map[0])
        y_len = len(w_map)
        for distance in range(1, x_len + y_len):
            curr_y = distance
            curr_x = 0

            while curr_y > 0:
                if curr_y < y_len and curr_x < x_len and w_map[curr_y][curr_x][0] == "X":
                    print '-------------------------------------- ', time.time() - start_time
                    print "  Match found at: ", curr_x, ", ", curr_y
                    print "  Distance: ", distance
                    print "  Wire lengths: ", w_map[curr_y][curr_x][1]
                    print "      ", w_map[curr_y][curr_x][1][1] + w_map[curr_y][curr_x][1][3]

                    match_found = True
                    break

                curr_x += 1
                curr_y -= 1

    return match_found


########################
# Map Building and Management
########################
def add_wire(x, y, char, wire_name, steps=None):
    opposite_wire = "A" if wire_name == "B" else "B"

    # Select grid clockwise
    if x >= 0 and y >= 0:
        wire_map = wire_grid[0]
    elif x >= 0 and y < 0:
        wire_map = wire_grid[1]
    elif x < 0 and y < 0:
        wire_map = wire_grid[2]
    elif x < 0 and y >= 0:
        wire_map = wire_grid[3]

    # Add items
    if x == 0 and y == 0:
        wire_map[abs(y)][abs(x)][0] = "o"
    if opposite_wire in wire_map[abs(y)][abs(x)][1]:
        wire_map[abs(y)][abs(x)][0] = "X"
        wire_map[abs(y)][abs(x)][1].append(wire_name)
        wire_map[abs(y)][abs(x)][1].append(steps)  # quick hack to finish part 2 of the prompt
        print '-------------------------------------- ', time.time() - start_time
        print "  INTERSECTION STEP COUNT: ", x, ", ", y
        print "  STEPS: ", wire_map[abs(y)][abs(x)][1]
    else:
        wire_map[abs(y)][abs(x)][0] = char
        wire_map[abs(y)][abs(x)][1].append(wire_name)
        wire_map[abs(y)][abs(x)][1].append(steps)  # quick hack to finish part 2 of the prompt


    return


def get_x_value(instruct):
    direction = instruct[0]
    distance = int(instruct[1:])

    if direction == "R":
        return distance
    elif direction == "L":
        return distance * -1
    else:
        return 0


def get_y_value(instruct):
    direction = instruct[0]
    distance = int(instruct[1:])

    if direction == "U":
        return distance
    elif direction == "D":
        return distance * -1
    else:
        return 0


# Creates a grid of 4 maps of max_x, max_y to handle negatives in each direction
def create_map(wire_map):
    max_x = 0
    max_y = 0
    for wire in wire_map:
        curr_x = 0
        curr_y = 0
        for instruction in wire:
            curr_x += get_x_value(instruction)
            curr_y += get_y_value(instruction)
            max_x = max(max_x, abs(curr_x))
            max_y = max(max_y, abs(curr_y))

    # Prevent some padding & off by one issues
    max_x += 3
    max_y += 3

    print "DIMENSIONS: ", max_x, max_y
    print time.time() - start_time, "s"
    base_map = [[[".", []] for i in range(max_x)] for j in range(max_y)]

    # Log this because the input is friggin huge
    print "CREATED 1"
    print time.time() - start_time, "s"
    grid = [base_map]
    print "INSERTED 1"

    grid.append([[[".", []] for i in range(max_x)] for j in range(max_y)])
    print "CREATED 2"
    print time.time() - start_time, "s"

    grid.append([[[".", []] for i in range(max_x)] for j in range(max_y)])
    print "CREATED 3"
    print time.time() - start_time, "s"

    grid.append([[[".", []] for i in range(max_x)] for j in range(max_y)])

    print "CREATED 4"
    print time.time() - start_time, "s"

    return grid


def pretty_print(w_grid):
    for column in range(len(w_grid[0]) - 1, -1, -1):
        char_map = map(lambda x: x[0], w_grid[0][column])
        print ''.join(char_map)
    return


def trace_wire(wire_route, wire_name):
    cursor_x = 0
    cursor_y = 0
    wire_length = 0

    add_wire(0, 0, "o", wire_name)
    for instruction in wire_route:
        direction = instruction[0]
        distance = int(instruction[1:])
        instruction_start = cursor_x, cursor_y

        add_wire(instruction_start[0], instruction_start[1], "+", wire_name)
        if direction == "L":
            for unit in range(0, distance):
                cursor_x -= 1
                wire_length += 1
                add_wire(cursor_x, cursor_y, "-", wire_name, steps=wire_length)
        elif direction == "R":
            for unit in range(0, distance):
                cursor_x += 1
                wire_length += 1
                add_wire(cursor_x, cursor_y, "-", wire_name, steps=wire_length)
        elif direction == "U":
            for unit in range(0, distance):
                cursor_y += 1
                wire_length += 1
                add_wire(cursor_x, cursor_y, "|", wire_name, steps=wire_length)
        elif direction == "D":
            for unit in range(0, distance):
                cursor_y -= 1
                wire_length += 1
                add_wire(cursor_x, cursor_y, "|", wire_name, steps=wire_length)
    return


########################
#  RUN
########################
# Read in lazy
fp = open('./input.txt', 'r')
# fp = open('./test_input.txt', 'r')
# fp = open('./simple_input.txt', 'r')

wires = [
    fp.readline().split(","),
    fp.readline().split(",")
]
wire_grid = create_map(wires)

trace_wire(wires[0], "A")
trace_wire(wires[1], "B")

# Don't run pretty print for 15,000 lines
# pretty_print(wire_grid)

find_closest_intersection(wire_grid)

print time.time() - start_time, "s"

import math


# Fuel required to launch a given module is based on its mass.
# Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

def calculate_fuel(mass):
    return math.floor(mass / 3) - 2


fp = open('./input.txt', 'r')

str_array = fp.readlines()
module_array = map(lambda x: int(x), str_array)

total_fuel = 0
for module in module_array:
    fuel_cost = calculate_fuel(module)
    module_cost = fuel_cost
    while fuel_cost > 0:
        fuel_cost = calculate_fuel(fuel_cost)
        if fuel_cost > 0:
            module_cost += fuel_cost

    total_fuel += module_cost

print(total_fuel)

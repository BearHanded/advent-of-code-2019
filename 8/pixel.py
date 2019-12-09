from functools import partial

fp = open('./input.txt', 'r')
dimensions = 25, 6
layer_size = dimensions[0] * dimensions[1]

target = ''
min_zero = 999999999999999

for layer in iter(partial(fp.read, layer_size), ''):

    zero_count = layer.count('0')

    if zero_count < min_zero:
        target = layer
        min_zero = zero_count


print(target.count('1') * target.count('2'))
from functools import partial

fp = open('./input.txt', 'r')
dimensions = 25, 6
layer_size = dimensions[0] * dimensions[1]

msg = []
for layer in iter(partial(fp.read, layer_size), ''):
    msg.append(layer)

print(msg)
focused_image = []
for idx in range(0, layer_size):
    focused_image.append(' ')
    for level in range(0, len(msg)):
        if msg[level][idx] != '2':
            focused_image[idx] = msg[level][idx]
            break

print(focused_image)

rows = list(map(''.join, zip(*[iter(focused_image)]*25)))
for row in rows:
     print(row)

print('----')
for row in rows:
     print(row.replace('0', ' '))
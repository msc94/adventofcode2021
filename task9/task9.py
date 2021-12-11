import functools

with open("task9/example.txt") as f:
    data = f.read()

lines = [x.strip() for x in data.splitlines()]

height = len(lines)
width = len(lines[0])

array = []
array.append([(9, -1) for _ in range(width + 2)])

for l in lines:
    array.append([(9, -1)] + [(int(c), -1) for c in l] + [(9, -1)])

array.append([(9, -1) for _ in range(width + 2)])

def print_array(array):
    for l in array:
        print(l)

current_basin = 0

def flow_cell(array, x, y, basin):
    c = array[y][x]

    if c[1] != -1:
        # Already part of a basin
        return

    array[y][x] = (c[0], basin)

    if array[y - 1][x] < c:
        flow_cell(array, x, y - 1, basin)
    if array[y][x - 1] < c:
        flow_cell(array, x - 1, y, basin)

    if array[y + 1][x] < c:
        flow_cell(array, x, y + 1, basin)
    if array[y][x + 1] < c:
        flow_cell(array, x + 1, y, basin)

def flow(array, value):
    global current_basin
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            if array[y][x][0] == value:
                print(f"\nFlowing value {value} at {(x, y)}")

                flow_cell(array, x, y, current_basin)
                current_basin += 1

                print(f"Result:")
                print_array(array)

for c in range(8, 0, -1):
    print(f"Flowing all with {c}")
    flow(array, c)
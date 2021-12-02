with open("task2/input.txt") as f:
    lines = f.readlines()

horizontal = 0
depth = 0
aim = 0

for l in lines:
    parts = l.split(" ")
    command = parts[0]
    argument = int(parts[1])

    if command == "forward":
        horizontal += argument
        depth += aim * argument
    elif command == "down":
        aim += argument
    elif command == "up":
        aim -= argument
    else:
        raise Exception()

print(f"h: {horizontal}")
print(f"d: {depth}")
print(f"r: {horizontal * depth}")
with open("task22/example.txt") as f:
    data = f.read()

lines = data.splitlines()

def parse_interval(s) -> tuple:
    parts = s.split("..")
    min_value = int(parts[0])
    max_value = int(parts[1])
    return min_value, max_value

class Field():
    def __init__(self):
        self.field = dict()

    def turn_on(self, x, y, z):
        self.field[(x, y, z)] = 1

    def turn_off(self, x, y, z):
        self.field.pop((x, y, z), None)

    def turned_on(self):
        return len(self.field.keys())


f = Field()

for l in lines:
    parts = l.split(" ")
    cmd = parts[0]
    coords = parts[1]

    parts = coords.split(",")
    interval_x = parse_interval(parts[0][2:])
    interval_y = parse_interval(parts[1][2:])
    interval_z = parse_interval(parts[2][2:])

    print(f"Command {cmd} from x={interval_x}, y={interval_y}, z={interval_z}")

    for x in range(interval_x[0], interval_x[1] + 1):
        for y in range(interval_y[0], interval_y[1] + 1):
            for z in range(interval_z[0], interval_z[1] + 1):
                if cmd == "on":
                    f.turn_on(x, y, z)
                elif cmd == "off":
                    f.turn_off(x, y, z)

    print(f"{f.turned_on()} turned on")

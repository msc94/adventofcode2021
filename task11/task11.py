octopi = {}

def print_octopi(octopi):
    print()

    for y in range(10):
        for x in range(10):
            octopus = octopi[(x, y)]
            print(octopus.energy, end="")
        print()

class Octopus(object):
    def __init__(self, position: tuple, energy: int):
        self.position = position
        self.energy = energy
        self.flashed = False

    def increment_energy(self):
        self.energy += 1

    def reset(self):
        if self.flashed:
            self.energy = 0
            self.flashed = False

    def try_flash(self):
        if self.flashed:
            return

        if not self.energy == 9:
            return

        self.flashed = True

        # Let neighbours flash
        for y in range(-1, 2):
            for x in range(-1, 2):
                (sx, sy) = self.position
                n = octopi.get((sx + x, sy + y), None)

                if n is not None:
                    n.try_flash()

    def __repr__(self) -> str:
        return f"{self.position} {self.energy}"


with open("task11/example.txt") as f:
    data = f.read()
    lines = data.splitlines()

for y in range(10):
    for x in range(10):
        octopi[(x, y)] = Octopus((x, y), int(lines[y][x]))

flashes = 0

for _ in range(10):
    print_octopi(octopi)

    for o in octopi.values():
        o.increment_energy()

    for o in octopi.values():
        o.try_flash()

    for o in octopi.values():
        if o.flashed:
            flashes += 1

    for o in octopi.values():
        o.reset()

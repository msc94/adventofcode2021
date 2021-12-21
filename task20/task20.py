
change_padding = False

class Image():
    def __init__(self):
        self.pixels = dict()
        self.padding = "."

    def set_pixel(self, x, y, value):
        self.pixels[(x, y)] = value

    def get_pixel(self, x, y):
        pos = (x, y)
        if pos in self.pixels:
            return self.pixels[pos]
        else:
            return self.padding

    def minmax_xy(self) -> tuple:
        xs = [x for x, _ in self.pixels.keys()]        
        ys = [y for _, y in self.pixels.keys()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return (min_x, max_x, min_y, max_y)

    def print(self) -> str:
        (min_x, max_x, min_y, max_y) = self.minmax_xy()
        
        for y in range(min_y - 5, max_y + 6):
            for x in range(min_x - 5, max_x + 6):
                print(self.get_pixel(x, y), end="")
            print()

    def num_lit(self):
        return len([x for x in self.pixels.values() if x == "#"])

    def enhance(self, algo):
        global change_padding

        (min_x, max_x, min_y, max_y) = self.minmax_xy()
        enhanced = Image()

        if change_padding:
            enhanced.padding = "." if self.padding == "#" else "#"

        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                pixel_range = []

                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        pixel = self.get_pixel(x + dx, y + dy)
                        pixel_range.append(pixel)

                pixel_string = "".join(pixel_range)
                pixel_string = pixel_string.replace(".", "0")
                pixel_string = pixel_string.replace("#", "1")

                pixel_int = int(pixel_string, 2)
                enhanced.set_pixel(x, y, algo[pixel_int])

        return enhanced

with open("task20/input.txt") as f:
    data = f.read()

lines = data.splitlines()

algo = lines[0]
assert(len(algo) == 512)

if algo[0] == "#":
    change_padding = True

width = len(lines[2])
height = len(lines) - 2
image = Image()

for y, line in enumerate(lines[2:]):
    for x, char in enumerate(line):
        image.set_pixel(x, y, char)

image.print()
print()

for i in range(50):
    image = image.enhance(algo)
    # image.print()
    print(f"Lit after {i + 1}: {image.num_lit()}")
    print()



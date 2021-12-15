from collections import Counter

with open("task14/example.txt") as f:
    data = f.read()
    lines = data.splitlines()

patterns = {}

for i, v in enumerate(lines):
    if i == 0:
        start = v
    elif i > 1:
        parts = v.split(" -> ")
        assert(parts[0] not in patterns)
        patterns[parts[0]] = parts[1]

pairs = {}
characters = dict(Counter(start))

for i in range(len(start) - 1):
    a = start[i]
    b = start[i + 1]
    pairs[a + b] = 1

print(start)
print(patterns)
print(pairs)
print(characters)

def step(pairs: dict, characters: dict):
    # Check all places where we insert things
    new_pairs = {}

    for p in pairs.keys():
        insert = patterns.get(p, None)
        if insert is not None:
            new_pairs.setdefault(p[0] + insert, 0)
            new_pairs[p[0] + insert] += 1

            new_pairs.setdefault(insert + p[1], 0)
            new_pairs[insert + p[1]] += 1

            characters.setdefault(insert, 0)
            characters[insert] += 1
        else:
            new_pairs.insert(p, pairs[p])

    return new_pairs

for i in range(10):
    pairs = step(pairs, characters)
    print(f"\nAfter step {i + 1}")
    print(characters)
    print(pairs)

ctr = Counter(characters)
common = ctr.most_common()

print(common)
print(common[0][1] - common[-1][1])
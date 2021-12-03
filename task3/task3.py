with open("task3/input.txt") as f:
    lines = f.read()
    lines = lines.splitlines()

same = [len(x) == len(lines[0]) for x in lines]
assert(all(same))

length = len(lines[0])

lsrn = [int(x, 2) for x in lines]
csrn = lsrn.copy()

for i in reversed(range(length)):
    if len(lsrn) == 1:
        break

    ones = 0
    zeros = 0
    mask = 1 << i

    for number in lsrn:
        if number & mask > 0:
            ones += 1
        else:
            zeros += 1

    if ones >= zeros:
        # Keep numbers with one bit
        lsrn = [x for x in lsrn if (x & mask) > 0]
    else:
        # Keep numbers with zero bit
        lsrn = [x for x in lsrn if (x & mask) == 0]

for i in reversed(range(length)):
    if len(csrn) == 1:
        break

    ones = 0
    zeros = 0
    mask = 1 << i

    for number in csrn:
        if number & mask > 0:
            ones += 1
        else:
            zeros += 1

    if zeros > ones:
        # Keep numbers with one bit
        csrn = [x for x in csrn if (x & mask) > 0]
    else:
        # Keep numbers with zero bit
        csrn = [x for x in csrn if (x & mask) == 0]

print(f"R: {lsrn[0] * csrn[0]}")
    


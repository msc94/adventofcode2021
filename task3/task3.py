with open("task3/input.txt") as f:
    lines = f.read()
    lines = lines.splitlines()

same = [len(x) == len(lines[0]) for x in lines]
assert(all(same))

length = len(lines[0])

lsrn = [int(x, 2) for x in lines]
csrn = lsrn.copy()

def filter(x, f):
    for i in reversed(range(length)):
        if len(x) == 1:
            break

        ones = 0
        zeros = 0
        mask = 1 << i

        for number in x:
            if number & mask > 0:
                ones += 1
            else:
                zeros += 1

        x = f(ones, zeros, mask, x)
        
    return x

def flsrn(ones, zeros, mask, list):
    if ones >= zeros:
        # Keep numbers with one bit
        return [x for x in list if (x & mask) > 0]
    else:
        # Keep numbers with zero bit
        return [x for x in list if (x & mask) == 0]

def fcsrn(ones, zeros, mask, list):
    if zeros > ones:
        # Keep numbers with one bit
        return [x for x in list if (x & mask) > 0]
    else:
        # Keep numbers with zero bit
        return [x for x in list if (x & mask) == 0]


lsrn = filter(lsrn, flsrn)
csrn = filter(csrn, fcsrn)

# 6775520
print(f"R: {lsrn[0] * csrn[0]}")
    


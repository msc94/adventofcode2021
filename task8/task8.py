from functools import reduce
from itertools import combinations
from z3 import *

vals = dict(zip('abcdefg', range(1, 8)))
inv_vals = dict((v, k) for k, v in vals.items())
digits = ["abcefg", "cf", "acdeg", "acdfg", "bcdf",
        "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]
of_length = reduce(lambda h, k: h.setdefault(
    len(k), []).append(k) or h, digits, {})


def add_clause(k, vars):
    ors = []
    summand = reduce(lambda a, b: a + b, [vars[c] for c in k])
    for k_ in of_length[len(k)]:
        ors.append(summand == sum(vals[c] for c in k_))
    return Or(ors)


def parse(m, vars, k):
    segs = sorted([inv_vals[m[vars[c]].as_long()] for c in k])
    return digits.index(''.join(segs))


def solve_line(l):
    inp, outp = l.split(" | ")
    s = Solver()
    a, b, c, d, e, f, g = Ints('a b c d e f g')
    vars = dict(zip('abcdefg', [a, b, c, d, e, f, g]))
    for (i1, i2) in combinations([a, b, c, d, e, f, g], 2):
        s.add(i1 != i2)
    for observed in inp.split():
        s.add(add_clause(observed, vars))
    s.check()
    m = s.model()
    return [parse(m, vars, k) for k in outp.split()]


res = solve_line(
    "cbedf baged adfeb bgeacd gebafd bfa afdg af gcfedba gfacbe | edbaf fabed gbedcfa fadgbe")
print(res)
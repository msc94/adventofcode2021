import copy
import numpy as np


def merge(s1, s2):
    assert len(s1) == len(s2)

    result = []
    for i, v1 in enumerate(s1):
        v2 = s2[i]
        result.append(1 if v1 == 1 or v2 == 1 else 0)
    return result


def fold_up(arr: np.ndarray, y):
    above = arr[:y, :]

    below = arr[y + 1 :, :]
    below = np.flip(below, axis=0)

    result = above | below

    return result


def fold_left(arr, x):
    left = arr[:, :x]

    right = arr[:, x + 1 :]
    right = np.flip(right, axis=1)

    result = left | right

    return result


def read_file(path: str):
    with open(path) as f:
        data = f.read()

    lines = data.splitlines()

    points = []
    folds = []

    for l in lines:
        if "," in l:
            parts = l.split(",")
            points.append((int(parts[0]), int(parts[1])))
        elif "fold along" in l:
            folds.append(l.split(" ")[2])

    return points, folds


points, folds = read_file("task13/input.txt")

width = max([x[0] for x in points]) + 1
height = max([x[1] for x in points]) + 1

array = np.zeros(shape=(height, width), dtype=np.int32)

for x, y in points:
    array[y, x] = 1

print(array)

for f in folds:
    coord = int(f.split("=")[1])
    if f.startswith("y="):
        array = fold_up(array, coord)

        print("\nAfter fold up")
        print(array)
    elif f.startswith("x="):
        array = fold_left(array, coord)

        print("\nAfter fold left")
        print(array)

print(f"Sum: {np.sum(array)}")
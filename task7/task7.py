def parse(input: str):
    return [int(x.strip()) for x in input.split(",")]


def main():
    input_str = open("task7/input.txt").read()
    input = parse(input_str)

    # Calculate average
    minvalue = min(input)
    maxvalue = max(input)

    min_cost = 10000000000000000
    min_value = -1

    for x in range(minvalue, maxvalue + 1):
        costs = 0

        for y in input:
            steps = abs(y - x)
            costs += steps * (steps + 1) // 2

        print(f"Costs for {x}: {costs}")
        if costs < min_cost:
            min_cost = costs
            min_value = x

    print(f"Costs for {min_value}: {min_cost}")


if __name__ == "__main__":
    main()

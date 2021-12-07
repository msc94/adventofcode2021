import itertools

def parse_state(state: str) -> dict:
    numbers = [int(x.strip()) for x in state.split(",")]
    result = {n: 0 for n in range(9)}

    for n in numbers:
        result[n] += 1

    return result


def main():
    # initial_state = "3,4,3,1,2"
    initial_state = "3,4,3,1,2,1,5,1,1,1,1,4,1,2,1,1,2,1,1,1,3,4,4,4,1,3,2,1,3,4,1,1,3,4,2,5,5,3,3,3,5,1,4,1,2,3,1,1,1,4,1,4,1,5,3,3,1,4,1,5,1,2,2,1,1,5,5,2,5,1,1,1,1,3,1,4,1,1,1,4,1,1,1,5,2,3,5,3,4,1,1,1,1,1,2,2,1,1,1,1,1,1,5,5,1,3,3,1,2,1,3,1,5,1,1,4,1,1,2,4,1,5,1,1,3,3,3,4,2,4,1,1,5,1,1,1,1,4,4,1,1,1,3,1,1,2,1,3,1,1,1,1,5,3,3,2,2,1,4,3,3,2,1,3,3,1,2,5,1,3,5,2,2,1,1,1,1,5,1,2,1,1,3,5,4,2,3,1,1,1,4,1,3,2,1,5,4,5,1,4,5,1,3,3,5,1,2,1,1,3,3,1,5,3,1,1,1,3,2,5,5,1,1,4,2,1,2,1,1,5,5,1,4,1,1,3,1,5,2,5,3,1,5,2,2,1,1,5,1,5,1,2,1,3,1,1,1,2,3,2,1,4,1,1,1,1,5,4,1,4,5,1,4,3,4,1,1,1,1,2,5,4,1,1,3,1,2,1,1,2,1,1,1,2,1,1,1,1,1,4"
    num_days = 256

    state = parse_state(initial_state)
    print(f"Initial state: {state}")

    for d in range(num_days):
        new_state = {n: 0 for n in range(9)}

        # Create new fish
        new_state[8] = state[0]
        new_state[6] = state[0]

        for k in range(1, 9):
            new_state[k - 1] += state[k]
        
        state = new_state

        print(f"\nNumber of fish after day {d + 1}: {sum(state.values())}")
        print(f"State after day {d + 1}: {state}")


if __name__ == "__main__":
    main()

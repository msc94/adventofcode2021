from itertools import cycle

example = True

if example:
    p1_start = 4
    p2_start = 8
else:
    p1_start = 7
    p2_start = 2

dice_values = cycle(range(1, 101))
position_values = cycle(range(1, 11))

def step(pos, dice):
    number = 0

    for _ in range(3):
        number += dice
        print(f"{dice}, ", end="")
        
        dice = increment_wrap(dice, 1, 1, 100)

    pos = increment_wrap(pos, number, 1, 10)

    return pos, dice, number


p1_pos, p2_pos = p1_start, p2_start
p1_score, p2_score = 0, 0

dice = 1
num_rolled = 0

while True:
    p1_pos, dice, number = step(p1_pos, dice)
    p1_score += p1_pos
    num_rolled += 3
    print(f"Player 1 rolled {number}, moved to {p1_pos} and has score {p1_score}")

    if p1_score >= 1000:
        print(
            f"Player 1 won. Dice was rolled {num_rolled} times. Player 2 score: {p2_score}. Result: {num_rolled * p2_score}"
        )
        break

    p2_pos, dice, number = step(p2_pos, dice)
    p2_score += p2_pos
    num_rolled += 3
    print(f"Player 2 rolled {number}, moved to {p2_pos} and has score {p2_score}")

    if p2_score >= 1000:
        print(
            f"Player 1 won. Dice was rolled {num_rolled} times. Player 2 score: {p2_score}. Result: {num_rolled * p2_score}"
        )
        break

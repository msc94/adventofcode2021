with open("input_1.txt") as f:
    lines = f.read()

numbers = [int(x) for x in lines.splitlines()]

sums = []
for i in range(len(numbers) - 2):
    sums.append(numbers[i] + numbers[i + 1] + numbers[i + 2])

increments = 0
for i in range(len(sums) - 1):
    if sums[i] < sums[i + 1]:
        increments += 1

print(increments)
import re

INPUT_PATH = "input.txt"
PATTERN = re.compile(r"([^a-zA-Z0-9_.]|[\d]+)")


def load_input(path):
    with open(path, mode="r", encoding="utf-8") as file:
        lines = file.read().splitlines()
        row = 0
        for line in lines:
            yield row, line
            row += 1


def get_positions(path):
    positions = {}
    total = 0
    for row, line in load_input(path):
        matches = PATTERN.finditer(line)
        for match in matches:
            column = match.span()[0]
            try:
                element = int(match.group())
                total += element
            except ValueError:
                element = match.group()
            item = {(row, column): element}
            positions.update({(row, column): element})
            print(f"Added element {item}")
    return positions, len(line)


def get_part_numbers(positions, row_length):
    part_numbers = []
    maybe_gears = {}
    for k, v in positions.items():
        row = k[0]
        column = k[1]
        if isinstance(v, int):
            for row_offset in range(-1, 2):
                span = range(column - 1, column + 1 + len(str(v)))
                for c in span:
                    try:
                        index = (row + row_offset, c)
                        if not isinstance(positions[index], int):
                            print(f"marking {v} at {k} for remove")
                            part_numbers.append((row, column))
                    except KeyError:
                        print(f"No symbol at {index}")
        elif v == "*":
            parts = []
            for row_offset in range(-1, 2):
                for c in range(row_length):
                    index = (row + row_offset, c)
                    try:
                        span = range(c - 1, c + 1 + len(str(positions[index])))
                        if isinstance(positions[index], int) and column in span:
                            print(f"found gear {positions[index]} for * at {k}")
                            parts.append(positions[index])
                    except KeyError:
                        print(f"no element at {index}")
            maybe_gears.update({k: parts})
        gears = {k: v for k, v in maybe_gears.items() if len(v) == 2}
    return part_numbers, gears


positions, row_length = get_positions(INPUT_PATH)
part_numbers, gears = get_part_numbers(positions, row_length)
total = sum([v for k, v in positions.items() if k in part_numbers])
print(total)
gear_sum = 0
for gear, parts in gears.items():
    product = 1
    for part in parts:
        product = product * part
    gear_sum += product

print(gear_sum)

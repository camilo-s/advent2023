import re

INPUT_PATH = "input.txt"


def load_input(path):
    with open(path, mode="r", encoding="utf-8") as file:
        lines = file.read().splitlines()
        row = 0
        for line in lines:
            yield row, line
            row += 1


def parse_elements(lines):
    pattern = re.compile(r"\d+")
    for row, line in lines:
        pair = []
        for segment in line.split(":")[1].split("|"):
            content = pattern.findall(segment)
            pair.append(tuple(content))
        yield pair


def get_winners(pairs):
    for pair in pairs:
        winners = [number for number in pair[1] if number in pair[0]]
        yield winners


def get_total(winners):
    total = 0
    for winner in winners:
        amount = len(winner)
        if amount == 0:
            value = 0
        else:
            value = 2 ** (amount - 1)
        total += value
    return total


def get_cards(winners):
    index = 0
    cards = {}
    for winner in winners:
        cards.update({index: len(winner)})
        index += 1
    return cards


# total_1 = get_total(get_winners(parse_elements(load_input(INPUT_PATH))))
# print(total_1)


def reproduce_cards(n, cards):
    """Do recursive stuff."""
    if n == 0:
        return {i: 1 for i in range(len(cards))}
    else:
        new_cards = reproduce_cards(n - 1, cards)
        for i in range(n, n + cards[n - 1]):
            new_cards[i] += new_cards[n - 1]
        return new_cards


cards = get_cards(get_winners(parse_elements(load_input(INPUT_PATH))))
print(cards)

total_cards = len(cards)

print(sum(reproduce_cards(total_cards, cards).values()))

import re

PATH = "input.txt"

DIGIT_STRINGS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

# Need positive lookahead assertion to account for overlapping, e.g. oneight
PATTERN = "(?=(" + "|".join([k for k in DIGIT_STRINGS.keys()]) + "|\d))"


def load_input(path):
    with open(path, mode="r") as file:
        lines = file.readlines()
        for line in lines:
            yield line


def get_digit(digit_string):
    digit = DIGIT_STRINGS.get(digit_string, digit_string)
    try:
        int(digit)
        return digit
    except ValueError:
        print(f"{digit} is not a digit")
        return None


def match_lines(path):
    total = 0
    for line in load_input(path):
        digits = re.findall(PATTERN, line)
        real_digits = [get_digit(d) for d in digits]
        digit_concat = int(real_digits[0] + real_digits[-1])
        total += digit_concat
    return total


print(match_lines(PATH))

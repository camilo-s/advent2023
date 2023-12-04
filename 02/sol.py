import re


def load_input(path):
    with open(path, mode="r") as file:
        lines = file.readlines()
        for line in lines:
            yield line


def check_draw_feasible(r=0, g=0, b=0):
    R_MAX = 12
    G_MAX = 13
    B_MAX = 14
    if r > R_MAX or g > G_MAX or b > B_MAX:
        return False
    else:
        return True


def check_game_feasible(game):
    game_content = game.split(":")[-1]
    draws = game_content.split(";")
    for draw in draws:
        draw_dict = {}
        draw_strings = draw.split(",")
        for draw_string in draw_strings:
            draw_dict.update(parse_draw(draw_string))
        if not check_draw_feasible(**draw_dict):
            return False
    else:
        return True


def parse_draw(draw_string):
    draw_match = re.search(
        r"(?P<number>[\d]+) (?P<color>(red|green|blue))", draw_string
    )
    draw_string_dict = draw_match.groupdict()
    return {draw_string_dict["color"][0]: int(draw_string_dict["number"])}


def process_input(path):
    id_sum = 0
    for game in load_input(path):
        game_id = int(re.search(r"[\d]+", game).group())
        if check_game_feasible(game):
            id_sum += game_id
    return id_sum


print(process_input("input.txt"))

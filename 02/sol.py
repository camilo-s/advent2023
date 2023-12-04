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
    game_max = {"r": 0, "g": 0, "b": 0}

    for draw in draws:
        draw_strings = draw.split(",")
        for draw_string in draw_strings:
            draw_dict = parse_draw(draw_string)
            color = draw_dict["color"][0]
            number = draw_dict["number"]
            if draw_dict["number"] > game_max[color]:
                draw_item = {color: number}
                game_max.update(draw_item)
    game_power = 1
    for v in game_max.values():
        game_power = game_power * v
    if not check_draw_feasible(**game_max):
        return [game_power, False]
    else:
        return [game_power, True]


def parse_draw(draw_string):
    draw_match = re.search(
        r"(?P<number>[\d]+) (?P<color>(red|green|blue))", draw_string
    )
    draw_string_dict = draw_match.groupdict()
    draw_string_dict.update({"number": int(draw_string_dict["number"])})
    return draw_string_dict


def process_input(path):
    id_sum = 0
    power_sum = 0
    for game in load_input(path):
        game_id = int(re.search(r"[\d]+", game).group())
        game_power, game_feasible = check_game_feasible(game)
        power_sum += game_power
        if game_feasible:
            id_sum += game_id
    return [id_sum, power_sum]


print(process_input("input.txt"))

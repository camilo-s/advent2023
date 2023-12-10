import re

INPUT_PATH = "input.txt"

PARSE_MAP_NAME = re.compile(r"(?P<map_name>[a-z-]+[a-z])\s(map)")
PARSE_MAP_IDS = re.compile(r"[\d]+")


def load_input(path):
    with open(path, mode="r", encoding="utf-8") as file:
        lines = file.read().splitlines()
        for line in lines:
            yield line


def parse_lines(lines):
    map_name = ""
    map_content = []
    for line in lines:
        match = PARSE_MAP_NAME.match(line)
        if match is not None:
            if len(map_content) > 0:
                yield map_name, map_content
            map_name = match.group("map_name")
            map_content = []
        else:
            map_ids = [int(map_id) for map_id in PARSE_MAP_IDS.findall(line)]
            if len(map_ids) > 0 and map_name != "":
                map_content.append(tuple(map_ids))
    else:
        yield map_name, map_content


def get_map_list(lines):
    map_name = ""
    map_content = []
    map_list = []
    for line in lines:
        match = PARSE_MAP_NAME.match(line)
        if match is not None:
            if len(map_content) > 0:
                map_list.append((map_name, map_content))
            map_name = match.group("map_name")
            map_content = []
        else:
            map_ids = [int(map_id) for map_id in PARSE_MAP_IDS.findall(line)]
            if len(map_ids) > 0 and map_name != "":
                map_content.append(tuple(map_ids))
    else:
        map_list.append((map_name, map_content))
    return map_list


def apply_map(map_content, i):
    for ranges in map_content:
        range_length = ranges[2]
        destination_range_start = ranges[0]
        source_range_start = ranges[1]
        source_offset = i - source_range_start
        if source_offset >= 0 and source_offset < range_length:
            return destination_range_start + source_offset
    else:
        return i


def iterate_map(map_list, i):
    s = i
    for map_name, map_content in map_list:
        mapped_seed = apply_map(map_content, s)
        # print("map_content", map_content)
        # print(f"{map_name}({s})={mapped_seed}")
        s = mapped_seed
    return mapped_seed


def get_seed_ranges(lines):
    for line in lines:
        if re.match(r"seeds: [\d\s]+", line):
            i = 0
            seed_ranges = []
            for s in PARSE_MAP_IDS.finditer(line):
                seed = int(s.group())
                if i % 2 == 0:
                    range_start = seed
                else:
                    range_length = seed
                    seed_ranges.append((range_start, range_length))
                i += 1
    return seed_ranges


def find_minimum(range_start, range_length, map_list):
    if range_length == 1:
        return iterate_map(map_list, range_start)
    else:
        mid_length = range_length // 2
        rest_length = range_length - mid_length

        return min(
            find_minimum(range_start, mid_length, map_list),
            find_minimum(range_start + mid_length, rest_length, map_list),
        )


def collect_minima(seed_ranges, map_list):
    global_minimum = 2**64
    for seed_range in seed_ranges:
        range_start = seed_range[0]
        range_length = seed_range[1]
        minimum = find_minimum(range_start, range_length, map_list)
        print("minimum", minimum)
        if minimum < global_minimum:
            global_minimum = minimum
    return global_minimum


seed_ranges = get_seed_ranges(load_input(INPUT_PATH))
map_list = get_map_list(load_input(INPUT_PATH))
print(collect_minima(seed_ranges, map_list))

from itertools import islice, cycle


def fill_pattern(pattern: list[str], chords: list[str]) -> list[str]:
    if len(pattern) == len(chords):
        return pattern
    elif len(pattern) < len(chords):
        return list(islice(cycle(pattern), len(chords)))
    else:
        return list(islice(cycle(chords), len(pattern)))


def length_to_duration(length: str) -> int:
    durs = {
        "s": 0.125,
        "e": 0.25,
        "q": 0.5,
        "h": 1,
        "w": 2,
        "2": 4,
        "3": 6,
        "4": 8,
    }
    return durs.get(length, 1)
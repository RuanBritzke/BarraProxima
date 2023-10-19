from math import sqrt


def distance(a: tuple[float, float], b: tuple[float, float]):
    x1, y1 = a
    x2, y2 = b
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


import re


def extract_year_month(dir):
    match = re.search(r"(\d{4})\\(\d{2})", str(dir))
    if match:
        year, month = match.groups()
        return int(year), int(month)
    return None, None

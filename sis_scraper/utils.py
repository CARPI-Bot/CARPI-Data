def map_day_codes_to_days(day_code):
    day_map = {
        'M': 'monday',
        'T': 'tuesday',
        'W': 'wednesday',
        'R': 'thursday',
        'F': 'friday',
        'S': 'saturday',
        ' ': 'other',
    }
    return [day_map[code] for code in day_code]

def clean_instructors(input):
    return ", ".join(
        [" ".join("".join(x.split("(P)")).split()) for x in input.split(",")]
    )

def get_term(year, semester):
    if semester == "fall":
        return f"{year}09"
    elif semester == "summer":
        return f"{year}05"
    elif semester == "spring":
        return f"{year}01"
    else:
        return True
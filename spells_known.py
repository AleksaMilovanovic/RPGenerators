

def spells_known_full_cast(level):
    spells_known = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    if level > 2:
        spells_known[0] = 4
    else:
        spells_known[0] = 1 + level
        return spells_known

    if level > 4:
        spells_known[1] = 3
    else:
        spells_known[1] = level - 1
        return spells_known

    if level > 6:
        spells_known[2] = 3
    else:
        spells_known[2] = level - 3
        return spells_known

    if level > 8:
        spells_known[3] = 3
    else:
        spells_known[3] = level - 6
        return spells_known

    if level > 10:
        spells_known[4] = 2
    else:
        spells_known[4] = level - 8
        return spells_known

    spells_known[5] = 1
    if level < 13:
        return spells_known

    spells_known[6] = 1
    if level < 15:
        return spells_known

    spells_known[7] = 1
    if level < 17:
        return spells_known

    spells_known[8] = 1
    if level == 17:
        return spells_known

    spells_known[4] = 3
    if level == 18:
        return spells_known

    spells_known[5] = 2
    if level == 19:
        return spells_known

    spells_known[6] = 2
    return spells_known


def spells_known_half_cast(level):
    spells_known = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    if level == 1:
        return spells_known

    if level <= 4:
        if level > 2:
            spells_known[0] = 2
        else:
            spells_known[0] = 1
        return spells_known
    spells_known[0] = 4

    if level <= 8:
        if level <= 6:
            spells_known[1] = 2
        else:
            spells_known[1] = 3
        return spells_known
    spells_known[1] = 3

    if level <= 12:
        if level <= 10:
            spells_known[2] = 2
        else:
            spells_known[2] = 3
        return spells_known
    spells_known[2] = 3

    if level <= 16:
        if level <= 14:
            spells_known[3] = 1
        else:
            spells_known[3] = 2
        return spells_known
    spells_known[3] = 3

    if level <= 18:
        spells_known[4] = 1
    else:
        spells_known[4] = 2
    return spells_known



def spells_known_warlock(level):
    # HARD CODED FOR NATURAL PROGRESSION WITHOUT SWAPPING LOWER SLOTS
    if level < 11:
        num_known = level + 1
    else:
        num_known = 10 + int((level - 9)/2)
    if num_known <= 3:
        return [num_known, 0, 0, 0, 0, 0, 0, 0, 0]
    spells_known = [3, 0, 0, 0, 0, 0, 0, 0, 0]
    num_known -= 3
    index = 1
    while num_known > 2 and index < 4:
        spells_known[index] = 2
        num_known -= 2
        index += 1
    index = 1
    while num_known > 3:
        spells_known[index] += 1
        num_known -= 1
        index += 1

    spells_known[index] = num_known
    return spells_known


def get_cantrips(cl, level):
    if cl == "ranger" or cl == "paladin":
        return 0

    if level < 4:
        num_cantrips = 2
    elif level < 10:
        num_cantrips = 3
    else:
        num_cantrips = 4

    if cl == "bard" or cl == "druid" or cl == "warlock":
        return num_cantrips
    elif cl == "wizard" or "cleric":
        return num_cantrips + 1
    elif cl == "sorcerer":
        return num_cantrips + 2



FULL_CASTERS = ["wizard", "bard", "sorcerer", "druid", "cleric"]
HALF_CASTERS = ["paladin", "ranger"]

def get_spells_known(cl, level):
    if cl in FULL_CASTERS:
        spells_known = spells_known_full_cast(level)
    elif cl in HALF_CASTERS:
        spells_known = spells_known_half_cast(level)
    elif cl == "warlock":
        spells_known = spells_known_warlock(level)
    else:
        return []
    cantrips = get_cantrips(cl, level)
    return [cantrips] + spells_known


if __name__ == "__main__":
    for level in range(1, 21):
        print(get_spells_known("paladin", level))

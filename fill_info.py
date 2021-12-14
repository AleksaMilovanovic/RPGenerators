import json

spells_by_class = {}
spells_by_level_then_class = {}
spell_data = {}
spell_tier_by_class = {}


def pretty_print(m, indent=0):
    for key, value in m.items():
        print("\t" * indent + key)
        if isinstance(value, dict):
            pretty_print(value, indent + 1)
        else:
            print("\t" * (indent + 1) + str(value))


def pull_info_2():
    f = open("all_spells.json")
    data = json.load(f)
    for spell in data:
        spell_data[spell['name']] = spell
        for cl in spell['class'].split(", "):
            cl = cl.lower()
            category = spells_by_class.get(cl, [])
            category.append(spell['name'])
            spells_by_class[cl] = category

            level = spell["level"][0]
            if level == "C":
                level = "cantrip"
            spells_by_level = spells_by_level_then_class.get(level, {})
            spells_in_class_level = spells_by_level.get(cl, [])
            spells_in_class_level.append(spell['name'])
            spells_by_level[cl] = spells_in_class_level
            spells_by_level_then_class[level] = spells_by_level

    f = open("spell_tiers.txt")
    for line in f:
        tokens = line[:-1].split(',', )
        for i, _ in enumerate(tokens):
            tokens[i] = tokens[i].strip()
        cl = spell_tier_by_class.get(tokens[0], {})
        tier = cl.get(tokens[2], [])
        tier.append(tokens[1])
        cl[tokens[2]] = tier
        spell_tier_by_class[tokens[0]] = cl

    # pretty_print(spells_by_class)


def pull_info():
    f = open("spells.json")
    data = json.load(f)
    for spell in data:
        spell_data[spell['name']] = spell
        for cl in spell['classes']:
            category = spells_by_class.get(cl, [])
            category.append(spell['name'])
            spells_by_class[cl] = category

            spells_by_level = spells_by_level_then_class.get(spell["level"], {})
            spells_in_class_level = spells_by_level.get(cl, [])
            spells_in_class_level.append(spell['name'])
            spells_by_level[cl] = spells_in_class_level
            spells_by_level_then_class[spell['level']] = spells_by_level

    f = open("spell_tiers.txt")
    for line in f:
        tokens = line[:-1].split(',', )
        for i, _ in enumerate(tokens):
            tokens[i] = tokens[i].strip()
        cl = spell_tier_by_class.get(tokens[0], {})
        tier = cl.get(tokens[2], [])
        tier.append(tokens[1])
        cl[tokens[2]] = tier
        spell_tier_by_class[tokens[0]] = cl


def print_spells_to_file(file):
    f = open(file, "w+")
    for spell, data in spell_data.items():
        f.write("wizard, " + spell + ", 1\n")


def get_spell_tiers(cl):
    for tier in spell_tier_by_class[cl].items():
        print(tier)


def get_class_spell_diff(cl):
    spells = {}
    for tier, spells_in_tier in spell_tier_by_class[cl].items():
        for spell in spells_in_tier:
            spells[spell] = 1
    for name, spell in spell_data.items():
        if cl in spell["classes"]:
            spells[name] = spells.get(name, 0) + 2
    for name, val in spells.items():
        if val < 3:
            print(name, val)


def fill_data_files():
    direc = "data/"
    classes = ["wizard", "bard", "sorcerer", "druid", "cleric", "paladin", "ranger", "warlock"]
    for cl in classes:
        filename = direc + cl + "_tiers.txt"
        f = open(filename, "w+")
        for spell in spells_by_class[cl]:
            f.write(f"{cl}, {spell}, -1\n")



def get_all():
    pull_info_2()
    return spells_by_class, spells_by_level_then_class, spell_tier_by_class, spell_data


def main():
    pull_info_2()
    fill_data_files()


if __name__ == "__main__":
    main()

import random
import spells_known, fill_info


spells_by_class = {}
spells_by_level_then_class = {}
spell_data = {}
spell_tier_by_class = {}


def pull_info():
    sbc, sbltc, stbc, sd = fill_info.get_all()
    spells_by_class.update(sbc)
    spells_by_level_then_class.update(sbltc)
    spell_tier_by_class.update(stbc)
    spell_data.update(sd)


def pick_best_spells(cl, population, sampling_size=1, optimize=True):
    if not optimize:
        return random.sample(population, sampling_size)
    else:
        tier = 4
        selected = []
        num_to_select = sampling_size
        next_tier = spell_tier_by_class[cl].get(str(tier), [])
        while tier > 0:
            spells_in_tier = []
            for spell in next_tier:
                if spell in population:
                    spells_in_tier.append(spell)
            if len(spells_in_tier) > num_to_select:
                sampling = random.sample(spells_in_tier, num_to_select)
                for sample in sampling:
                    selected.append(sample)
                return selected
            for spell in spells_in_tier:
                selected.append(spell)
            num_to_select -= len(spells_in_tier)
            tier -= 1



def generate_spells_known(cl, level, optimize=True):
    spells_known_num_array = spells_known.get_spells_known(cl, level)
    # print(spells_known_num_array)
    cantrips_known_num = spells_known_num_array[0]
    spells_known_num_array = spells_known_num_array[1:]

    list_cantrips = spells_by_level_then_class["cantrip"][cl]
    known_cantrips = pick_best_spells(cl, list_cantrips, cantrips_known_num, optimize=optimize)
    print(f"Cantrips known: {known_cantrips}")

    for spell_level, nums in enumerate(spells_known_num_array):
        if nums == 0:
            continue
        spell_level += 1
        list_spells = spells_by_level_then_class[str(spell_level)][cl]
        print(f"Level {spell_level} spells known: {pick_best_spells(cl, list_spells, nums, optimize=optimize)}")


# def ability_score_explain():
#     pass



SPELLCASTERS = ["wizard", "druid", "warlock", "paladin", "ranger", "bard", "cleric", "sorcerer", "artificer"]
MARTIAL_CLASSES = ["barbarian", "fighter", "monk", "rogue"]


#def ability_score_generate(cl, AS_gen):


# Begins calculator
def calc_start(optimize=True):
    choice = input("Please input class: ").lower().strip()
    while choice not in SPELLCASTERS:
        # In loop to check in case of mispellings
        if choice in MARTIAL_CLASSES:
            print("You have selected a MARTIAL class. These do not require spell lists.")
            print("Exceptions do exist, but these exceptions are not yet supported.")
            print("If you would like a spell list, consider another class.")
            exit(0)
        print("Class not recognized. Please try again or type \"quit\"")
        choice = input("Please input class: ").lower().strip()
        if choice.lower() == "quit":
            exit(0)

    cl = choice
    CL_UPPER = cl.capitalize()
    print("You have selected a SPELLCASTER. Continuing...")
    level = int(input("What level character are you creating? "))
    while level < 1 or level > 20:
        if level == 0:
            print("Level 0 is interesting, but unsupported. Level 0 characters are unsupported by official material. To "
                  "play a level 0 character, consider playing a Commoner's stat block until you gain a level.")
            cont = input("Continue or exit? Type anything but \"exit\" to continue.")
            if cont.lower() == "exit":
                exit(0)
        print("Level invalid - must be between 1 and 20. Please try again or type \"quit\"")
        level = input("Please input level: ").lower().strip()
        if level.lower() == "quit":
            exit(0)
        level = int(level)

    print()
    print(f"Creating Level {level} {CL_UPPER} character...")
    print()

    # AS_METHODS = ["1d20", "4d6dl", "3d6", "point buy", "standard array"]
    #
    # print("ABILITY SCORE GENERATION")
    # answer = input("Do you need an explanation on the different kinds of generation for ability scores?").lower()
    # if answer == "y" or answer == "yes":
    #     ability_score_explain()
    # AS_gen = input("Now then, would you like Standard Array, 1d20, 4d6DL, or 3d6?")
    # while AS_gen.lower() not in AS_METHODS:
    #     AS_gen = input("Please select a valid method from the previous or type \"quit\". ")
    #     if AS_gen.lower() == "quit":
    #         exit(0)
    # ability_scores = ability_score_generate(cl, AS_gen)

    generate_spells_known(cl, level, optimize=optimize)


def main():
    pull_info()
    # get_spell_tiers("wizard")
    # print_spells_to_file("wizard_spells")
    # get_class_spell_diff('wizard')
    calc_start(optimize=True)


if __name__ == "__main__":
    main()

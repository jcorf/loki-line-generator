from collections import defaultdict
import re
global scene_counter


def is_character(name):
    """ Returns whether the given name is all capitals (excluding digits, etc.) ex. LOKI 49-S vs Loki"""
    regex = "^[0-9A-Z\s-]+[^a-z]:?"
    return re.match(regex, name) is not None


def get_character(obj):
    """ gets the text inside the bold tags """
    try:
        return obj.find("b").text.strip(":")
    except AttributeError:
        return None


def get_actions(obj):
    """ gets actions that are in i tags, that are formatted in [brackets]"""
    actions = []
    for item in obj.find_all("i"):
        actions.append("[" + item.text + "]")

    return actions


def get_expressions(obj):
    """ get expressions that are in (parentheseses tag)"""
    expressions = []
    text = obj.text

    while text.find("(") != -1 and text.find(")") != -1:
        beg = text.find("(")
        end = text.find(")")
        expressions.append(text[beg:end + 1])
        text = text[end + 2:]

    return expressions


# def get_dialogue(obj):
#     """get remaining dialogue after expressions, actions, characters names removed """
#     character = get_character(obj) + ":"
#     actions = get_actions(obj)
#     expressions = get_expressions(obj)
#
#     dialogue = obj.text.strip("\n")
#     dialogue = dialogue.replace(character, "")
#
#     for action in actions:
#         dialogue = dialogue.replace(action, "")
#
#     for exp in expressions:
#         dialogue = dialogue.replace(exp, "")
#
#     return dialogue.strip()


def get_text(dialogue, character, actions, expressions):
    """get remaining dialogue after expressions, actions, characters names removed """
    if character is not None:
        dialogue = dialogue.replace(character + ":", "")

    for action in actions:
        dialogue = dialogue.replace(action, "")

    for exp in expressions:
        dialogue = dialogue.replace(exp, "")

    return dialogue.strip()


def get_location(obj, places, boundries):
    """get the location of an object based on boundries"""
    line = obj.sourceline
    for index, b in enumerate(boundries):
        if b > line:
            return places[index - 1]

    return places[-1]


def structure_dialogue(obj, last_speaking, old_structure, places, boundries, last_location, c, scene_counter):
    """ returns a formalized structure """
    try:
        structure = old_structure
        location = get_location(obj, places, boundries)

        character = get_character(obj)
        expressions = get_expressions(obj)
        actions = get_actions(obj)
        dialogue = get_text(obj.text, character, actions, expressions)

        last = last_speaking

        uq_sc = scene_counter

        if get_character(obj) is None:
            if dialogue != "":
                structure[last_speaking]["actions"][uq_sc].extend(actions)
                structure[last_speaking]["expressions"][uq_sc].extend(expressions)
                structure[last_speaking]["dialogue"][uq_sc].append(dialogue)
                structure[last_speaking]["locations"].append(location)
                structure[last_speaking]["lines"][uq_sc].append(len(dialogue.split(" ")))

                last = last_speaking

            else:
                print
                structure["None"]["actions"][uq_sc].extend(actions)
                structure["None"]["expressions"][uq_sc].extend(expressions)
                structure["None"]["locations"].append(location)
        else:

            structure[character]["actions"][uq_sc].extend(actions)
            structure[character]["expressions"][uq_sc].extend(expressions)
            structure[character]["dialogue"][uq_sc].append(dialogue)
            structure[character]["locations"].append(location)
            structure[character]["lines"][uq_sc].append(len(dialogue.split(" ")))
            structure[character]["switches"][uq_sc].append((last, character))

            last = character

            if location == last_location:
                c += 1
            else:
                return last, structure, location, 0, scene_counter

        return last, structure, last_location, c, scene_counter
    except KeyError:
        return last_speaking, structure, last_location, c, scene_counter


scene_counter = 1


def create_structure(soup_obj, characters, places):
    """ creates a structure for a given soup object """
    global scene_counter
    last = "None"

    structure = {char: {"actions": defaultdict(list), "expressions": defaultdict(list), "dialogue": defaultdict(list),
                        "locations": [], "lines": defaultdict(list), "switches": defaultdict(list)} for char in
                 characters}
    structure["None"] = {"actions": defaultdict(list), "expressions": defaultdict(list), "dialogue": defaultdict(list),
                         "locations": [], "lines": defaultdict(list), "switches": defaultdict(list)}

    structure["lines_in_scenes"] = defaultdict(list)
    structure["scenes"] = defaultdict(list)

    boundries = [soup_obj.find("span", {"id": place_id}).sourceline for place_id in places]

    last_loc = ""
    counter = 0

    for index, item in enumerate(soup_obj.find_all("p")):
        old_counter = counter
        old_location = last_loc
        last, structure, last_loc, counter, scene_counter = structure_dialogue(item, last, structure, places, boundries,
                                                                               last_loc, counter, scene_counter)
        if counter == 0 and old_counter != 0:
            structure["lines_in_scenes"][old_location].append(old_counter)
            structure["scenes"][scene_counter].append(old_location)

            scene_counter += 1

    structure["scenes"][scene_counter].append(last_loc)
    scene_counter += 1

    return structure

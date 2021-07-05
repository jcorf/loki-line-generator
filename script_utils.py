import re


def is_character(name):
    regex = "^[0-9A-Z\s-]+[^a-z]:?"
    return re.match(regex, name) != None


def get_character(obj):
    try:
        return obj.find("b").text.strip(":")
    except AttributeError:
        return None


def get_actions(obj):
    actions = []
    for item in obj.find_all("i"):
        actions.append("[" + item.text + "]")

    return actions


def get_expressions(obj):
    expressions = []
    text = obj.text

    while text.find("(") != -1 and text.find(")") != -1:
        beg = text.find("(")
        end = text.find(")")
        expressions.append(text[beg:end + 1])
        text = text[end + 2:]

    return expressions


def get_dialogue(obj):
    character = get_character(obj) + ":"
    actions = get_actions(obj)
    expressions = get_expressions(obj)

    dialogue = obj.text.strip("\n")
    dialogue = dialogue.replace(character, "")

    for action in actions:
        dialogue = dialogue.replace(action, "")

    for exp in expressions:
        dialogue = dialogue.replace(exp, "")

    return dialogue.strip()


def get_text(dialogue, character, actions, expressions):
    if character != None:
        dialogue = dialogue.replace(character + ":", "")

    for action in actions:
        dialogue = dialogue.replace(action, "")

    for exp in expressions:
        dialogue = dialogue.replace(exp, "")

    return dialogue.strip()


def structure_dialogue(obj, last_speaking, old_structure):
    try:
        structure = old_structure
        character = get_character(obj)
        expressions = get_expressions(obj)
        actions = get_actions(obj)
        dialogue = get_text(obj.text, character, actions, expressions)
        last = last_speaking

        if get_character(obj) == None:
            if (dialogue != ""):
                structure[last_speaking]["actions"].extend(actions)
                structure[last_speaking]["expressions"].extend(expressions)
                structure[last_speaking]["dialogue"].append(dialogue)
                last = last_speaking
            else:
                structure["None"]["actions"].extend(actions)
                structure["None"]["expressions"].extend(expressions)
        else:

            structure[character]["actions"].extend(actions)
            structure[character]["expressions"].extend(expressions)
            structure[character]["dialogue"].append(dialogue)
            last = character
        return last, structure
    except KeyError:
        return last_speaking, structure


def create_structure(soup_obj, characters):
    last = "None"

    structure = {char: {"actions": [], "expressions": [], "dialogue": []} for char in characters}
    structure["None"] = {"actions": [], "expressions": [], "dialogue": []}

    for item in soup_obj.find_all("p"):
        last, structure = structure_dialogue(item, last, structure)

    return structure

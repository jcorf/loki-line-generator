from collections import defaultdict
from script_cleaner import ScriptCleaner


class ScriptStructure:
    def __init__(self):
        self.characters = set()
        self.expressions = defaultdict(list)
        self.dialogue = defaultdict(list)
        self.places = defaultdict(list)
        self.actions = defaultdict(list)
        self.place_ids = defaultdict(str)

    def add_place_ids(self, place_id_dict):
        for place_id, place in place_id_dict.items():
            self.place_ids[place_id] = place

    def add_set(self, name, expressions, actions, dialogue, places):
        self.characters.add(name)
        self.expressions[name].extend(expressions)
        self.actions[name].extend(actions)
        self.dialogue[name].extend(dialogue)
        self.places[name].extend(places)

    def get_characters(self):
        return self.characters

    def get_expressions_of(self, name):
        if name in self.characters:
            return self.expressions[name]
        else:
            return "character not found!"

    def get_actions_of(self,name):
        if name in self.characters:
            return self.actions[name]
        else:
            return "character not found!"

    def get_dialogue_of(self, name):
        if name in self.characters:
            return self.dialogue[name]
        else:
            return "character not found!"

    def get_places_of(self, name):
        if name in self.characters:
            return self.places[name]
        else:
            return "character not found!"

    def get_unique_places(self):
        return set(self.place_ids.values())

    def get_all_dialogue(self):
        dialogue = []

        for dialogue_list in self.dialogue.values():
            dialogue.extend(dialogue_list)

        return dialogue

    def get_all_actions(self):
        actions = []

        for action_list in self.actions.values():
            actions.extend(action_list)

        return actions

    def get_all_expressions(self):
        expressions = []

        for expression_list in self.expressions.values():
            expressions.extend(expression_list)

        return expressions

    def get_all_places(self):
        return self.place_ids


def combine_scripts(*episodes: ScriptCleaner):
    structure = ScriptStructure()

    for ep in episodes:
        structure.add_place_ids(ep.get_places())
        for character in ep.get_characters():
            structure.add_set(character,
                              ep.get_expressions_of(character),
                              ep.get_actions_of(character),
                              ep.get_lines_of(character),
                              ep.get_places_of(character))

    return structure
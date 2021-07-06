import requests
from bs4 import BeautifulSoup
import script_utils as su

"""
Works with Loki Script URLS from https://transcripts.fandom.com/
"""


class ScriptCleaner:
    def __init__(self, url):
        self.url = url
        r = requests.get(url)
        self.soup = BeautifulSoup(r.content, "html.parser")
        self.characters = set([item.text.strip(":") for item in self.soup.find_all("b") if su.is_character(item.text)])
        self.places = {item.get("id"): item.text for item in self.soup.find_all("span", {"class": "mw-headline"}) if
                       item.text != "Credits"}

        self.structure = su.create_structure(self.soup, self.characters, list(self.places.keys()))

    def get_soup(self):
        return self.soup

    def get_characters(self):
        return self.characters

    def pretty(self):
        return self.soup.prettify()

    def get_places(self):
        return self.places

    def get_structure(self):
        return self.structure

    def get_lines_of(self, character):
        try:
            return self.structure[character]["dialogue"]
        except KeyError:
            return "character not in script!"

    def get_expressions_of(self, character):
        try:
            return self.structure[character]["expressions"]
        except KeyError:
            return "character not in script!"

    def get_actions_of(self, character):
        try:
            return self.structure[character]["actions"]
        except KeyError:
            return "character not in script!"

    def get_places_of(self, character):
        try:
            return self.structure[character]["places"]
        except KeyError:
            return "character not in script!"


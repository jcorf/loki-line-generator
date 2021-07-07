from nltk.tokenize import regexp_tokenize
from nltk import TrigramCollocationFinder
from random import choices, choice
import re
from collections import Counter


class TextGenerator:
    def __init__(self, dialogue_list):
        self.tokens = tokenize(dialogue_list)
        self.tcf = TrigramCollocationFinder.from_words(self.tokens)
        self.tgf = sorted(self.tcf.ngram_fd.items(), key=lambda t: (-t[1], t[0]))

    def trigram_beginning_with(self, word1, word2):
        trigrams = [item for item in self.tgf if item[0][0] == word1 and item[0][1] == word2]
        return trigrams

    def __end_word__(self, word):
        regex = "[0-9A-z]+[.!?]{1,}$"
        return re.match(regex, word) != None

    def __start_word__(self, word):
        regex = "[A-Z]{1}[A-z-]$"
        return re.match(regex, word) != None

    def __random_trigram__(self):
        return choice([item[0] for item in self.tgf])

    def random_trigram_starts_with(self, word1, word2):
        trigrams = self.trigram_beginning_with(word1, word2)
        population = [item[0][2] for item in trigrams]
        counts = [item[1] for item in trigrams]
        total = float(sum(counts))
        rel_weights = [item[1] / total for item in trigrams]
        word3 = choices(population, rel_weights)[0]

        return (word1, word2, word3)

    def create_sentence(self, length):
        begin_trigram = self.__random_trigram__()
        while not self.__start_word__(begin_trigram[0]):
            begin_trigram = self.__random_trigram__()

        sent = []
        sent.append(begin_trigram[0])

        head = begin_trigram[1]
        tail = begin_trigram[2]

        while True:
            sent.append(head)
            new_trigram = self.random_trigram_starts_with(head, tail)

            head = new_trigram[1]
            tail = new_trigram[2]

            if len(sent) == length - 1 and self.__end_word__(head):
                sent.append(head)
                break
            elif len(sent) == length - 2 and self.__end_word__(tail):
                sent.append(head)
                sent.append(tail)
                break
            elif len(sent) >= length and self.__end_word__(head):
                sent.append(head)
                break
            elif len(sent) >= length and self.__end_word__(tail):
                sent.append(head)
                sent.append(tail)
                break

        return " ".join(sent)

    def get_tokens(self):
        return self.tokens

    def get_trigrams(self):
        return self.tgf


def tokenize(dialogue_list):
    tokens = []

    for line in dialogue_list:
        tokens.extend(regexp_tokenize(line, "[0-9A-z'\-.?!]+"))

    return tokens

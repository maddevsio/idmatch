# coding: utf-8
from .blocks import Blocks
from .rules import NUMBERS_RULES
from .rules import LATIN_RULES
from .rules import KYRILLIC_RULES
from .rules import WHITESPACE_RULES


class Sanitizer:
    def __replace_letters(self, text, rules):
        if text is not None:
            for key in rules.iterkeys():
                text = text.replace(key, rules[key])
        else:
            text = "" #ugly hack
        return text

    def whitespaces(self, text):
        if text is not None:
            for item in WHITESPACE_RULES:
                text = text.replace(item, "")
        else:
            text = "" #ugly hack2
        return text

    def numbers(self, text):
        return self.__replace_letters(text, NUMBERS_RULES)

    def latin(self, text):
        return self.__replace_letters(text, LATIN_RULES)

    def kyrillic(self, text):
        return self.__replace_letters(text, KYRILLIC_RULES)

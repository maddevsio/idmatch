# coding: utf-8
from .blocks import Blocks
from .rules import NUMBERS_RULES
from .rules import LATIN_RULES
from .rules import KYRILLIC_RULES
from .rules import WHITESPACE_RULES


class Sanitizer:
    def __replace_letters(self, text, rules):
        text = text.upper()
        for key in rules.iterkeys():
            text = text.replace(key, rules[key])
        return text

    def whitespaces(self, text):
        for item in WHITESPACE_RULES:
            text = text.replace(item, "")
        return text

    def numbers(self, text):
        return self.__replace_letters(text, NUMBERS_RULES)

    def latin(self, text):
        return self.__replace_letters(text, LATIN_RULES)

    def kyrillic(self, text):
        return self.__replace_letters(text, KYRILLIC_RULES)

    def gender(self, text):
        pass

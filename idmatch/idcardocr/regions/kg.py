# coding: utf-8
import re


class Sanitizer(object):
    def sanitize_serial(self):
        self.serial = self.sanitizer_remove_whitespaces(self.serial)
        self.serial = self.sanitizer_to_latin(self.serial)
        self.serial = self.sanitizer_to_numbers(self.serial)
        pattern = re.compile("^[A-Z][A-Z]\d\d\d\d\d\d\d$")
        if not pattern.match(self.serial):
            self.errors.append("604: Serial sanitization failed")

    def sanitize_firstname(self):
        self.firstname = self.sanitizer_to_kyrillic(self.firstname)

        if "П" in self.firstname:
            self.errors.append('605: Warning: check surname for "Л/П" misplacement')

        pattern = re.compile("^[A-Z]$")
        if pattern.match(self.firstname):
            self.errors.append("606: Firstname sanitization failed")

        pattern = re.compile("^[0-9]$")
        if pattern.match(self.firstname):
            self.errors.append("607: Firstname sanitization failed")

    def sanitize_surname(self):
        self.surname = self.sanitizer_to_kyrillic(self.surname)

    def sanitize_middlename(self):
        self.middlename = self.sanitizer_to_kyrillic(self.middlename)

    def sanitize_nationality(self):
        pass

    def sanitize_birthday(self):
        pass

    def sanitize_inn(self):
        self.inn = self.sanitizer_to_numbers(self.inn)

    def sanitize_gender(self):
        pass

    def sanitizer_remove_whitespaces(self, text):
        text = text.replace(" ", "")
        text = text.replace("\t", "")
        text = text.replace("\r", "")
        text = text.replace("\n", "")
        return text

    def _replace_letters(self, text, rules):
        for key in rules.iterkeys():
            text = text.upper().replace(key, rules[key])
        return text

    def sanitizer_to_numbers(self, text):
        rules = {
            "О": "0",
            "O": "0",
            "З": "3",
            "I": "1",
            "I": "1",
            "L": "1",
            "S": "5",
            "b": "6",
            "B": "8",
        }
        return self._replace_letters(text, rules)

    def sanitizer_to_latin(self, text):
        text = text.upper()
        rules = {
            "У": "Y",
            "К": "K",
            "Е": "E",
            "Н": "H",
            "Х": "X",
            "В": "B",
            "А": "A",
            "Р": "P",
            "О": "O",
            "С": "C",
            "М": "M",
            "Т": "T"
        }
        return self._replace_letters(text, rules)

    def sanitizer_to_kyrillic(self, text):
        text = text.upper()
        rules = {
            "Y": "У",
            "K": "К",
            "E": "Е",
            "H": "Н",
            "X": "Х",
            "B": "В",
            "A": "А",
            "P": "Р",
            "O": "О",
            "C": "С",
            "M": "М",
            "T": "Т"
        }
        return self._replace_letters(text, rules)


class Info(Sanitizer):
    # TODO: DI for idcard regions (it will allow
    # to add another id's in future)
    serial = ""
    firstname = ""
    surname = ""
    middlename = ""
    nationality = ""
    birthday = ""
    inn = ""
    gender = ""
    errors = []

    def __init__(self, blocks):
        self.blocks = self.blocks_normalize(blocks)

    def blocks_normalize(self, blocks):
        left = 1e10
        right = -1e10
        top = 1e10
        bottom = -1e10

        for block in blocks:
            if left > block['x']:
                left = block['x']
            if right < block['x'] + block['w']:
                right = block['x'] + block['w']
            if top > block['y']:
                top = block['y']
            if bottom < block['y'] + block['h']:
                bottom = block['y'] + block['h']

        for block in blocks:
            block['x'] -= left
            block['y'] -= top

            block['x'] = float(block['x']) / (float(right) - float(left))
            block['y'] = float(block['y']) / (float(bottom) - float(top))
            block['w'] = float(block['w'] / (float(right) - float(left)))
            block['h'] = float(block['h']) / (float(bottom) - float(top))
        return blocks

    def find_common(self, x, y):
        result = None
        distance = 1e10
        for block in self.blocks:
            distance_x = abs(x - block['x'])
            distance_y = abs(y - block['y'])
            if (distance_x + distance_y > distance):
                continue

            distance = distance_x + distance_y
            result = block['text']

        if not result:
            self.errors.append("603: Region not found")
            return

        return result

    def find_serial(self):
        self.serial = self.find_common(0.07, 0.85)
        self.sanitize_serial()
        return self.serial

    def find_surname(self):
        self.surname = self.find_common(0.325, 0.268)
        self.sanitize_surname()
        return self.surname

    def find_firstname(self):
        self.firstname = self.find_common(0.325, 0.4)
        self.sanitize_firstname()
        return self.firstname

    def find_middlename(self):
        self.middlename = self.find_common(0.325, 0.536)
        self.sanitize_middlename()
        return self.middlename

    def find_birthday(self):
        block = None
        distance = 1e10
        for block in self.blocks:
            distance_x = abs(0.325 - block['x'])
            distance_y = abs(0.65 - block['y'])
            if distance_x + distance_y > distance:
                continue
            distance = distance_x + distance_y
            result = block

        if not result:
            self.errors.append("601: Birthday element not found")
            return

        parts = []
        for block in self.blocks:
            distance_gender = abs(0.71 - block['x'])
            distance_y = abs(0.65 - block['y'])

            if 0.03 > distance_y and 0.1 < distance_gender and block['x'] - result['x'] >= 0.0:
                parts.append(block)

        if not parts:
            self.errors.append("602: Required birthday regions not found")
            return
        # parts_sorted = sort(parts,  key=lambda b: b['x'],  reverse=True)
        self.birthday = "".join([part['text'] for part in parts])
        self.birthday = self.sanitizer_remove_whitespaces(self.birthday)
        return self.birthday

    def find_nationality(self):
        self.nationality = self.find_common(0.325, 0.88)
        return self.nationality

    def find_inn(self):
        self.inn = self.find_common(0.82, 0.94)
        return self.inn

    def find_gender(self):
        self.gender = self.find_common(0.71, 0.65)
        return self.gender


def regionskir(blocks):
    blocks = Info(blocks)
    data = {
        'surname': blocks.find_surname(),
        'middlename': blocks.find_middlename(),
        'firstname': blocks.find_firstname(),
        'birthday': blocks.find_birthday(),
        'serial': blocks.find_serial(),
        'gender': blocks.find_gender(),
        'inn': blocks.find_inn(),
        'nationality': blocks.find_nationality(),
        'errors': ", ".join(blocks.errors)
    }
    return {k: value.decode('utf-8') for k, value in data.iteritems()}

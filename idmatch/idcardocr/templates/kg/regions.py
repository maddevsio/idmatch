# coding: utf-8
from idmatch.idcardocr.core.regions.mapping import IDcardSanitizer
from idmatch.idcardocr.core.regions.blocks import Blocks


class IDcard(IDcardSanitizer, Blocks):
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
        self.birthday = "".join([part['text'] for part in parts])
        self.birthday = self.sanitize_birthday()
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

    def data(self):
        data = {
            'surname': self.find_surname(),
            'middlename': self.find_middlename(),
            'firstname': self.find_firstname(),
            'birthday': self.find_birthday(),
            'serial': self.find_serial(),
            'gender': self.find_gender(),
            'inn': self.find_inn(),
            'nationality': self.find_nationality(),
            'errors': ", ".join(self.errors)
        }
        for k, v in data.iteritems():
            print(k)
            print(v)
        return {k: v for k, v in data.iteritems()}


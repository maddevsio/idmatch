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

    def __init__(self, blocks, size):
        self.size = size
        self.blocks = self.blocks_normalize(blocks)

    def find_serial(self):
        self.serial = self.find_common(0.127, 0.83)
        self.sanitize_serial()
        return self.serial

    def find_surname(self):
        self.surname = self.find_common(0.36, 0.38)
        self.sanitize_surname()
        return self.surname

    def find_firstname(self):
        self.firstname = self.find_common(0.36, 0.48)
        self.sanitize_firstname()
        return self.firstname

    def find_middlename(self):
        self.middlename = self.find_common(0.36, 0.58)
        self.sanitize_middlename()
        return self.middlename

    def find_nationality(self):
        self.nationality = self.find_common(0.36, 0.88)
        return self.nationality

    def find_inn(self):
        self.inn = self.find_common(0.63, 0.91)
        self.sanitize_inn()
        return self.inn

    def find_birthday(self):
        self.sanitize_birthday()
        return self.birthday

    def find_gender(self):
        self.gender = self.find_common(0.71, 0.65)
        self.sanitize_gender()
        return self.gender

    def data(self):
        data = {
            'surname': self.find_surname(),
            'firstname': self.find_firstname(),
            'middlename': self.find_middlename(),
            'inn': self.find_inn(),
            'birthday': self.find_birthday(),
            'serial': self.find_serial(),
            'gender': self.find_gender(),
            'nationality': self.find_nationality(),
            'errors': ", ".join(self.errors)
        }       
        return {k: v.decode('utf-8') if v else "" for k, v in data.iteritems()}



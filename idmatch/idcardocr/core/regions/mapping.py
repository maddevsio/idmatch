# coding: utf-8
import re
from .sanitizer import Sanitizer

class IDcardSanitizer(Sanitizer):
    def sanitize_serial(self):
        self.serial = self.whitespaces(self.serial)
        self.serial = self.latin(self.serial)
        self.serial = self.numbers(self.serial)
        pattern = re.compile("^[A-Z][A-Z]\d\d\d\d\d\d\d$")
        if not pattern.match(self.serial):
            self.errors.append("604: Serial sanitization failed")

    def sanitize_firstname(self):
        self.firstname = self.kyrillic(self.firstname)

        if "П" in self.firstname:
            self.errors.append('605: Warning: check surname for "Л/П" misplacement')

        pattern = re.compile("^[A-Z]$")
        if pattern.match(self.firstname):
            self.errors.append("606: Firstname sanitization failed")

        pattern = re.compile("^[0-9]$")
        if pattern.match(self.firstname):
            self.errors.append("607: Firstname sanitization failed")

    def sanitize_surname(self):
        self.surname = self.kyrillic(self.surname)

    def sanitize_middlename(self):
        self.middlename = self.kyrillic(self.middlename)
    
    def sanitize_gender(self):
        if "З" in self.gender:
            self.gender = "Э"

    def sanitize_nationality(self):
        pass

    def sanitize_birthday(self):
        if len(self.birthday) == 8:
            self.birthday = self.birthday[:2]+"."+self.birthday[2:4]+"."+self.birthday[4:]
        else:
            self.birthday = None
            self.errors.append("601: Birthday element not found")

    def sanitize_inn(self):
        self.inn = self.numbers(self.inn)

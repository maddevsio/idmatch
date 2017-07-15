# coding: utf-8
import re
from .sanitier import Sanitizer

class IDcardSanitizer(Sanitizer):
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

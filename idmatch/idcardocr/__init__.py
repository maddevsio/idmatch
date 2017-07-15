# coding: utf-8
from .idcardocr import recognize_card

class CardReader:
    def __init__(self, template):
        self.template = template        

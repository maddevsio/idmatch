# coding: utf-8
from idcardocr.core.processing.idcardocr import recognize_card


def processing(image):
    return recognize_card(image)

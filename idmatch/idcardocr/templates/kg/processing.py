# coding: utf-8
from idmatch.idcardocr.core.processing.idcardocr import recognize_card


def processing(image):
    return recognize_card(image)

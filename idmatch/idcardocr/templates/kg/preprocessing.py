# coding: utf-8
from idmatch.idcardocr.core.preprocessing.card import remove_borders


def preprocessing(image):
    return remove_borders(image)

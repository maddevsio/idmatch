# coding: utf-8
from .preprocessing import preprocessing
from .processing import processing
from .regions import IDcard


class CardKG:
    def __init__(self, image):
        self.image = image

    def processing(self):
        preprocessed_image = preprocessing(self.image)
        block_text = processing(preprocessed_image)
        regions = IDcard(block_text)
        return regions.data()


# coding: utf-8
from .preprocessing import preprocessing
from .processing import processing
from .regions import regions


class CardKG:
    def processing(self, image):
        preprocessed_image = preprocessing(image)
        block_text = processing(preprocessed_image)
        regions = regions(block_text)
        return regions.data()


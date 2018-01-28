# coding: utf-8
from .preprocessing import preprocessing
from .processing import processing
from .regions import IDcard
from PIL import Image

class CardKG:
    def __init__(self, image):
        self.image = image

    def processing(self):
            preprocessed_image = preprocessing(self.image)
            img, block_text = processing(preprocessed_image)
            im = Image.fromarray(preprocessed_image)
            regions = IDcard(block_text, im.size)
            return img, regions.data()

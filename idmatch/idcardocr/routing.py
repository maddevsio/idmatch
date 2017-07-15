# coding: utf-8
from .templates.kg import CardKG


class CardReader:
    def __init__(self, template, image):
        self.template = template
        self.image = image

    def route(self):
        method = 'template_{0}'.format(self.template)
        if not hasattr(self, method):
            return 'Unknown idcard template'
        return getattr(self, method)()

    def template_kg(self):
        card = CardKG(self.image)
        return card.processing()
        

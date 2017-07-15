# coding: utf-8
from template.kg import CardKG


class CardReader:
    def __init__(self, template, image):
        self.template = template
        self.image = image

    def router(self):
        method = 'template_{0}'.format(self.template)
        if not hasattr(self, method):
            return 'Unknown idcard template'
        return getattr(self, method)

    def template_kg(self):
        card = CardKG(image)
        return card.processing()
        

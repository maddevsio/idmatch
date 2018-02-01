# coding: utf-8
from .templates.kg import CardKG
import json

class CardReader:
    def __init__(self, template, image, preview=False):
        self.preview = preview
        self.template = template
        self.image = image

    def route(self):
        method = 'template_{0}'.format(self.template)
        if not hasattr(self, method):
            return 'Unknown idcard template'
        return getattr(self, method)()

    def template_kg(self):
        img, text = CardKG(self.image).processing()
        if self.preview:
            return img, text
        return img, json.dumps(text, sort_keys=False, ensure_ascii=False, indent=3)

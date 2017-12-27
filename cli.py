#!/usr/bin/env python
# coding: utf-8
import click
import json
from idmatch.idcardocr import CardReader


@click.command()
@click.option('--image', help='ID card image path.')
@click.option('--template', help='ID card image path.')
def cardocr(image, template='kg'):
    reader = CardReader('kg', 'demo.jpg')
    print(reader.route())


if __name__ == '__main__':
    cardocr()

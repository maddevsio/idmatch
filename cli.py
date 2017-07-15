#!/usr/bin/env python
# coding: utf-8
import click
import json
from idmatch.matching import match


@click.command()
@click.option('--img', help='Webcam image path.')
@click.option('--idcard', help='ID card image path.')
def matching(img, idcard):
    result = match(img, idcard)
    click.echo(json.dumps(result, indent=4))


@click.command()
@click.option('--idcard', help='ID card image path.')
def cardocr(idcard):
    return cardreader(idcard)


if __name__ == '__main__':
    cardocr()

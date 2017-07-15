# -*- coding: utf-8 -*-
import cv2
import numpy as np
import argparse
from skimage.filters import threshold_adaptive

from .image import resize
from .utils import four_point_transform


def remove_borders(image):
    image = cv2.imread(image)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        print(len(approx) == 4)
        if len(approx) == 4:
            screenCnt = approx
            break
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    if screenCnt is not None and len(screenCnt) > 0:
        return four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    cv2.imwrite('original.jpg', orig)
    return 'original.jpg'

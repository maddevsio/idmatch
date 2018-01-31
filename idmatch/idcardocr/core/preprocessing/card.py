# -*- coding: utf-8 -*-
import cv2
import numpy as np
import argparse
from PIL import Image
from skimage.filters import threshold_adaptive

from .image import resize
from .utils import four_point_transform

def remove_borders(image):
    image = cv2.imread(image)
    orig = image.copy()
    ratio = image.shape[0] / 500.0
    image = resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(7,7),0)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # contrasted = clahe.apply(blur)
    
    edged = cv2.Canny(blur, 20, 170)
    # todo check hierarchy. seems we can get largest rectangle with cv2.RETR_TREE or RETR_EXTERNAL.
    # RETR_EXTERNAL retrieves only the extreme outer contours. It sets `hierarchy[i][2]=hierarchy[i][3]=-1` for
    # all the contours.
    _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    largest_area = 0
    for cont in cnts:
        r = cv2.minAreaRect(cont)
        area = r[1][0]*r[1][1]
        if area > largest_area:
            largest_area = area
            rect = r

    screenCnt = np.int0(cv2.boxPoints(rect))
    im = Image.fromarray(edged)

    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    im = Image.fromarray(image)

    if screenCnt is not None and len(screenCnt) > 0:
        return four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    return orig
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import argparse
from skimage.filters import threshold_adaptive

from .image import resize
from .utils import four_point_transform


def remove_borders(image):
    image = cv2.imread(image)
    orig = image.copy()
    ratio = image.shape[0] / 500.0
    image = resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray,9,75,75)
    edged = cv2.Canny(blur, 25, 200)
    _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    largest_area = 0
    for c in cnts:
        r = cv2.minAreaRect(c)
        area = r[1][0]*r[1][1]
        if area > largest_area:
            largest_area = area
            rect = r

    screenCnt = np.int0(cv2.boxPoints(rect))
        
    # from PIL import Image
    # cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    # im = Image.fromarray(image)
    # im.save("contours.jpeg")
  
    if screenCnt is not None and len(screenCnt) > 0:
        return four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    cv2.imwrite('original.jpg', orig)
    return 'original.jpg'

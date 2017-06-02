# coding: utf-8
import os
import sys

import cv2
import pytesseract
from PIL import Image

from processing.border_removal import remove_borders
from regions import regionskir

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.join(BASE_DIR, '../idmatch'))

from matching.utils import detect_face
from matching.utils import save_image

MAX_HEIGHT = 40
MIN_HEIGHT = 16
MAX_WIDTH = 330
MIN_WIDTH = 16


def recognize_text(original):
    idcard = original
    gray = cv2.cvtColor(idcard, cv2.COLOR_BGR2GRAY)

    # Morphological gradient:
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)

    # Binarization
    ret, binarization = cv2.threshold(opening, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Connected horizontally oriented regions
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(binarization, cv2.MORPH_CLOSE, kernel)

    # find countours
    _, contours, hierarchy = cv2.findContours(
        connected, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    return contours, hierarchy


def detect_dpi(img):
    x, y, w, h = detect_face(img)
    return w


def recognize_card(original_image, country='kg', preview=False):
    from processing.border_removal import resize
    from processing.crop import process_image
    result = []
    cropped_image = "croped-image.jpg"
    process_image(original_image, cropped_image)
    idcard = cv2.imread(cropped_image, cv2.COLOR_BGR2GRAY)
    idcard = resize(idcard, width=720)

    scale_down = (8 * 170 / detect_dpi(idcard))
    if scale_down <= 4:
        rows, cols = idcard.shape[:2]
        idcard = cv2.resize(idcard, (scale_down * cols / 8, scale_down * rows / 8))
        # cv2.imwrite('resized' + original_image)
        # image = cv2.imread('resized' + original_image)
    contours, hierarchy = recognize_text(idcard)

    for index, contour in enumerate(contours):
        [x, y, w, h] = cv2.boundingRect(contour)
        gray = cv2.cvtColor(idcard, cv2.COLOR_RGB2GRAY)
        roi = gray[y:y + h, x:x + w]
        if cv2.countNonZero(roi) / h * w > 0.55:
            if h > 16 and w > 16:
                filename = '%s.jpg' % index
                cv2.imwrite(filename, roi)
                text = pytesseract.image_to_string(
                    Image.open(filename), lang="kir+eng", config="-psm 7"
                )                
                item = {'x': x, 'y': y, 'w': w, 'h': h, 'text': text}
                result.append(item)
                cv2.rectangle(idcard, (x, y), (x + w, y + h), (255, 0, 255), 2)
    if preview:
        original_image = original_image.split('/')[-1]
        location = save_image('regions' + original_image, idcard)
        return location, regionskir(result)
    return regionskir(result)

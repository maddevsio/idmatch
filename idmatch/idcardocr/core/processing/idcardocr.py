# coding: utf-8
import hashlib
import cv2
import pytesseract
import numpy as np
from PIL import Image

def recognize_text(original):
    idcard = original
    # gray = cv2.cvtColor(idcard, cv2.COLOR_BGR2GRAY)

    # Morphological gradient:
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(idcard, cv2.MORPH_GRADIENT, kernel)

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

def recognize_card(idcard):
    result = []
    # TODO: 
    # process_image(original_image, cropped_image)
    # idcard = cv2.imread(cropped_, cv2.COLOR_BGR2GRAY)

    # In some cases resized image gives worse results
    # idcard = resize(idcard, width=720)

    gray = cv2.cvtColor(idcard, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 3, 7, 21)
    
    contours, hierarchy = recognize_text(gray)
    mask = np.zeros(gray.shape, np.uint8)

    for index, contour in enumerate(contours):
        [x, y, w, h] = cv2.boundingRect(contour)
        if h < 16 or w < 16:
            continue

        mskRoi = mask[y:y+h, x:x+w]
        cv2.drawContours(mask, [contour], 0, 255, -1) #CV_FILLED
        nz = cv2.countNonZero(mskRoi)
        ratio = (float)(nz) / (float)(h*w)
        
        # got this value from left heel
        if ratio > 0.55 and ratio < 0.9:
            roi = denoised[y:y+h, x:x+w] 
            text = pytesseract.image_to_string(Image.fromarray(roi), lang="kir+eng", config="-psm 7")
            if text:                
                item = {'x': x, 'y': y, 'w': w, 'h': h, 'text': text}
                result.append(item)
                cv2.rectangle(idcard, (x, y), (x + w, y + h), (255, 0, 255), 2)
    # need to restore settings
    hash_object = hashlib.sha256(idcard)
    hex_dig = hash_object.hexdigest()
    cv2.imwrite("/webapp/web/static/"+hex_dig+".jpeg", idcard)
    return "static/"+hex_dig+".jpeg", result

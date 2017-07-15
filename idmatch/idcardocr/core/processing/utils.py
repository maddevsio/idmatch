# coding: utf-8
import hashlib
import numpy as np
import cv2


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def extract_file_hashsum(image):
    img = open(image, 'r')
    content = img.read()
    img.close()
    hash_sum = hashlib.sha256(content)
    return hash_sum.hexdigest()


def save_contours(ratio, orig, contours):
    filename = extract_file_hashsum(orig)
    image = four_point_transform(orig, contours.reshape(4, 2) * ratio)
    cv2.imwrite(filename, image)
    return filename

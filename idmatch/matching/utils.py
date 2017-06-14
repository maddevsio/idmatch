# coding: utf-8
import cv2
import hashlib
import os

from settings import FACE_CASCADE, BASE_DIR, STATIC_DIR


def save_image(name, img):
    location = os.path.join(STATIC_DIR, name)
    cv2.imwrite(location, img)
    return location


def extract_hash(image):
    hash_md5 = hashlib.md5()
    with open(image, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)
    face = faces[0]
    if len(faces) > 2:
        for item in faces[1:]:
            if item[2] > face[2]:
                face = item
    # x, y, w, h = face
    # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), thickness=2)
    return face


def extract_face(original_image):
    filename = extract_hash(original_image) + ".jpg"
    img = cv2.imread(original_image)
    x, y, w, h = detect_face(img)
    preview_path = save_image('preview-' + filename, img)
    sub_face = img[y:y+h, x:x+w]
    cv2.imwrite(filename, sub_face)
    return preview_path, filename


def matching_message(score):
    if score < 0.85:
        return "Match"
    elif score < 0.95:
        return "Probably match"
    return "Not match"

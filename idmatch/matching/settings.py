import os
import cv2
import numpy as np

from fixtures import COREY_VECTOR, WILDE_VECTOR


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_PATH = os.path.dirname(os.path.dirname(BASE_DIR))

UPLOAD_DIR = os.path.join(ROOT_PATH, "temp_data")
STATIC_DIR = os.path.join(ROOT_PATH, "web/static")

HAARCASCADE_FILE = 'haarcascades/haarcascade_frontalface_default.xml'
HAARCASCADE = os.path.join(BASE_DIR, HAARCASCADE_FILE)

VGG_PROTO_PATH = 'model/VGG_FACE_deploy.prototxt'
PROTO_PATH = os.path.join(BASE_DIR, VGG_PROTO_PATH)

VGG_CAFFE_PATH = 'model/VGG_FACE.caffemodel'
CAFFE_PATH = os.path.join(BASE_DIR, VGG_CAFFE_PATH)


MATRIX_LENGTH = len(COREY_VECTOR)
COREY_MATRIX = np.zeros((1, MATRIX_LENGTH), dtype=np.float32)
WILDE_MATRIX = np.zeros((1, MATRIX_LENGTH), dtype=np.float32)


FACE_CASCADE = cv2.CascadeClassifier(HAARCASCADE)


for i in range(MATRIX_LENGTH):
    COREY_MATRIX[0][i] = COREY_VECTOR[i]
    WILDE_MATRIX[0][i] = WILDE_VECTOR[i]

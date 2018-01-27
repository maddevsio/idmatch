# coding: utf-8
import cv2
import caffe
import numpy as np
import utils
import settings

try:
    net = caffe.Net(settings.PROTO_PATH, settings.CAFFE_PATH, caffe.TEST)
except:
    net = None


def compile_image(img):
    img = caffe.io.load_image(img)
    img = caffe.io.resize_image(img, (224, 224))
    img = img[:, :, ::-1] * 255.0
    avg = np.array([129.1863, 104.7624, 93.5940])
    img = img - avg
    img = img.transpose((2, 0, 1))
    img = img[None, :]
    return img


def normalize_result(webcam, idcard):
    diff_correy = cv2.norm(settings.COREY_MATRIX, idcard, cv2.NORM_L2)
    diff_wilde = cv2.norm(settings.WILDE_MATRIX, idcard, cv2.NORM_L2)
    diff_min = diff_correy if diff_correy < diff_wilde else diff_wilde
    diff = cv2.norm(webcam, idcard, cv2.NORM_L2)
    score = float(diff) / float(diff_min)
    percentage = (1.28 - score * score * score) * 10000 / 128
    return {
        'percentage': percentage,
        'score': score,
        'message': utils.matching_message(score)
    }


def matching_pipeline(image):
    path_to_face, face = utils.extract_face(image)
    return path_to_face, compile_image(face)


def net_learn(image):
    preview_path, face = matching_pipeline(image)
    net.forward_all(data=face)
    fc8_layer = net.blobs['fc8'].data.copy()
    return fc8_layer, preview_path


def match(webcam, idcard, preview=False):
    webcam_layer, face_path = net_learn(webcam)
    idcard_layer, idcard_path = net_learn(idcard)
    result = normalize_result(webcam_layer, idcard_layer)
    if preview:
        result.update({
            'face': face_path,
            'idcard': idcard_path
        })
    return result

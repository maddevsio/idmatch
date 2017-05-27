# coding: utf-8
import json
import os
import sys
from flask import Flask, Response, render_template, request
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(1, os.path.join(BASE_DIR, '../idmatch'))

from idmatch.matching import match
from idmatch.idcardocr import recognize_card

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def idmatch_landing():
    return render_template('idmatch_landing.html', **locals())


@app.route('/', methods=['POST'])
def idmatch_landing_demo():
    result = {}
    face = save_file(request.files['face'])
    idcard = save_file(request.files['id'])
    result['Match'] = match(face, idcard, preview=True)
    result['Match']['percentage'] = int(result['Match']['percentage'])
    result['Match']['face'] = "/".join(result['Match']['face'].split("/")[-2:])
    image, result['OCR'] = recognize_card(idcard, preview=True)
    result['Match']['idcard'] = 'static/' + "/".join(image.split("/")[-2:])
    return render_template('idmatch_landing.html', **locals())


@app.route('/match-and-ocr', methods=['POST'])
def idmatch_api():
    result = {}
    face = save_file(request.files['face'])
    idcard = save_file(request.files['id'])
    result['Match'] = match(face, idcard)
    result['OCR'] = recognize_card(idcard)
    return Response(json.dumps(result, indent=4), mimetype='application/json')


def save_file(request_file):
    filename = secure_filename(request_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    request_file.save(file_path)
    return file_path


if __name__ == '__main__':
    app.run()

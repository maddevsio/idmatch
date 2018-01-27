# coding: utf-8
import datetime
import json
import os
import sys
from flask import Flask, Response, render_template, request, session
from flask_babel import Babel
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

sys.path.insert(1, BASE_DIR)

from idmatch.matching import match
from idmatch.idcardocr import CardReader

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'web/uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

babel = Babel(app)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@babel.localeselector
def get_locale():
    return session.get('lang', 'en')
    return request.accept_languages.best_match(['ru', 'en'])


@app.route('/', methods=['GET'], defaults={'lang': 'en'})
@app.route('/<lang>', methods=['GET'])
def idmatch_landing(lang):
    session['lang'] = lang or 'en'
    print(session['lang'])
    return render_template('idmatch_landing.html', **locals())


@app.route('/', methods=['POST'], defaults={'lang': 'en'})
@app.route('/<lang>', methods=['POST'])
def idmatch_landing_demo(lang):
    session['lang'] = lang or 'en'
    result = {}
    face = ''
    idcard = save_file(request.files['id'])
    if len(request.form['faceWebcam']) != 0:
        face = save_webcam(request.form['faceWebcam'])
    elif len(request.files['face'].filename) != 0:
        face = save_file(request.files['face'])
    if face != '':
        result['Match'] = match(face, idcard, preview=True)
        result['Match']['percentage'] = int(result['Match']['percentage'])
        result['Match']['face'] = "/".join(result['Match']['face'].split("/")[-2:])
    image, result['OCR'] = CardReader(template='kg', image=idcard, preview=True).route()
    result['OCR']['idcard'] = image
    return render_template('idmatch_landing.html', **locals())


@app.route('/match-and-ocr', methods=['POST'])
def idmatch_api():
    face = save_file(request.files['face'])
    idcard = save_file(request.files['id'])
    result = {
        'Match': match(face, idcard),
        'OCR': CardReader(template='kg', image=idcard).route()
    }
    return Response(json.dumps(result, indent=4), mimetype='application/json')


def save_file(request_file):
    filename = secure_filename(request_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    request_file.save(file_path)
    return file_path

def save_webcam(webcam_image):
    webcam_image = webcam_image.replace('data:image/png;base64,', '')
    now = datetime.datetime.now()
    filename = "webcam-%s.jpg" % str(now.strftime("%Y-%m-%d-%H:%M:%S"))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, "wb") as fh:
        fh.write(webcam_image.decode('base64'))
    return file_path


if __name__ == '__main__':
    app.run()
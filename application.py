from flask import Flask, request, render_template, jsonify, json
import speechML
import os
import glob

"""
    Author: Ali Afzal
    Last Updated: Friday Dec 19th
    Python3
"""


application = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))


def predict(file):
    speech_ml = speechML.Speech()
    pred = speech_ml.get_prediction(file)
    acc = speech_ml.get_accuracy()
    return str(pred[0]), acc

@application.route('/')
def start():
    return render_template("index.html")

@application.route('/files', methods = ['GET'])
def getFiles():
    files = glob.glob("data/**/*.wav", recursive=True)
    
    return json.dumps(files)

@application.route('/predict', methods = ['POST'])
def prediction():
    if request.method == 'POST':
        filename = request.form.get('file-list')
        pred, acc = predict("data/" + filename)
        return jsonify(status="success", prediction=pred, accuracy=acc)

if __name__ == '__main__':
    application.run()
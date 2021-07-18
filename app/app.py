# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
# from app import app
# import app.server as server
from server import Text2TfIdfTransformer, Ringkas, preprocessing, model, testing
from flask import Flask, redirect, url_for, render_template, json, request, jsonify
from jinja2 import TemplateNotFound
from pandas.tseries.offsets import DateOffset
import pandas as pd
import numpy as np
from pandas import DataFrame
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator

import os
import csv
import math
import pickle
# import Flask
from flask import Flask

# Inject Flask magic
app = Flask(__name__)

# App Config - the minimal footprint
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'S#perS3crEt_JamesBond'


ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class MyCustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "server"
        return super().find_class(module, name)


# App main route + generic routing
# @app.route('/')
# def hello():
    # raise BaseException('Bummer! Exception')
    # return 'Hello world'

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
    # raise BaseException('Bummer! Exception')
    try:
        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(path)

    except TemplateNotFound:
        return render_template('page-404.html'), 404


detik = {
    "class": "detail__body-text itp_bodycontent",
    "noise": ["\n", "\r", "}", "#div-gpt-ad-1572507980488-0 iframe{", "border: 0px;",
              "vertical-align: bottom;",
              "position: fixed !important;",
              "z-index: 1 !important;",
              "left: 0px;",
              "right: 0;",
              "margin: auto;",
              "googletag.cmd.push(function() { googletag.display(\'div-gpt-ad-1572507980488-0\');  );",
              "Baca juga:",
              ]
}


@app.route('/training', methods=['GET', 'POST'])
def training():
    
    if request.method == 'POST':
        doks = request.files['inputfile']
        # data = []
        # if 'file' not in request.files:
        #     return redirect(request.url)
        # elif doc.filename == '':
        #     return redirect(request.url)
        # else:
        xgb, kasus = model(doks)
        print(kasus.columns.values)
        print(list(list(map(list, kasus.itertuples(index=False)))))
        filename = secure_filename(doks.filename)
        # return redirect(url_for('train',filename=filename))
        # return redirect("http://127.0.0.1:5000/training#preprocessing")
        return render_template('result_training.html', section=preprocessing, zip=zip, column_names=kasus.columns.values, row_data=list(list(map(list, kasus.itertuples(index=False)))))
    else:
        return render_template('training.html')
    # return render_template('training.html')
    # @app.route('/train/<filename>')
    # def train(filename):
    #     filepath = os.path.join(app.config['UPLOAD_FOLDER_TRAIN'], filename)


@app.route('/testing', methods=['GET', 'POST'])
def testing():

    if request.method == "POST":
        links = request.form["link"]

        with open('C:/Users/ROG STRIX/Desktop/Model', 'rb') as f:
            unpickler = MyCustomUnpickler(f)
            obj = unpickler.load()

        teks = Ringkas(detik, links)
        hasilpreprocessing = preprocessing(teks)
        res = obj.predict(hasilpreprocessing)
        data = {"hasil": res}
        # hasil_data = jsonify(data)
        return render_template('testing.html', isi_berita=teks, hasil_klasifikasi=res, link=links)

    else:
        return render_template('testing.html')

    # if request.method == "POST":

    #     link = request.form["link"]
    #     hasil = ml.testing()
        # data = []
        # data = {"data": data}
        # return jsonify(data)

    #     res = json.dumps(hasil)
    #     return res

    

@app.route("/hpReport", methods=["GET"])
def tampilReport():

    
    data = []

    # ini mengambil file hasil prediksi
    # jadi file hasil prediksi mu di eksport dulu ke csv
    # tentukan nama filenya jangan yang berubah-ubah mis "hasilPrediksi" atau yang lain
    # tapi kalau mau bikin yang dinamis jg Gaskeun
    with open('static\assets\img\evaluation\report_combined.csv', encoding='utf-8') as csvfile:
        data_csv = csv.DictReader(csvfile, delimiter=',')
        for row in data_csv:
            data.append(dict(row))
    data = {"data": data}
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)

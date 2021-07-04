# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from app import app
from app import server as ml
from flask import Flask, redirect, url_for, render_template, json, request, jsonify
from jinja2  import TemplateNotFound
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

class MyCustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "ml"
        return super().find_class(module, name)


# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404



@app.route('/testing', methods=['GET', 'POST'])
def testing():

    if request.method == "POST":
        data = []
        
        link = request.form["link"]
        source = 'detik'

        with open('C:/users/asus/desktop/Model','rb') as f:
            # mp = pickle.load(f)
            unpickler = MyCustomUnpickler(f)
            mp = unpickler.load()

        link = ml.Ringkas(source)
        hasilpreprocessing= ml.preprocessing(link)
        res = mp.predict(hasilpreprocessing)
        data = {"data": data}
        hasil_data = jsonify(data)
        return render_template('testing.html', hasil_data=hasil_data)
    
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

   
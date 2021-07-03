# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from app import app
from app import server as ml
from flask import render_template, json, request, jsonify
from jinja2  import TemplateNotFound
from pandas.tseries.offsets import DateOffset
import pandas as pd
import numpy as np
from pandas import DataFrame
from werkzeug.utils import secure_filename
import os
import csv
import math



# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404



@app.route('/testing.html', methods=['GET', 'POST'])
def testing():

    if request.method == "POST":
        data = []
        
        link = request.form["link"]
        source = 'detik'

        with open('C:/users/asus/desktop/Model','rb') as f:
            mp = ml.pickle.load(f)
        link = ml.Ringkas(source)
        hasilpreprocessing= ml.preprocessing(link)
        res = ml.mp.predict(hasilpreprocessing)
        data = {"data": data}
        return jsonify(data)
    
    # if request.method == "POST":

    #     link = request.form["link"]
    #     hasil = ml.testing()
        # data = []
        # data = {"data": data}
        # return jsonify(data)

    #     res = json.dumps(hasil)
    #     return res

    return render_template('testing.html')
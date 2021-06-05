# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template
from jinja2  import TemplateNotFound

# App modules
from app import app

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404



@app.route('/testing.html')
def testing():
    isi_berita = 'Jakarta - Korps Adhyaksa digegerkan dengan database atau basis data mereka diretas dan hendak dijual Usut punya usut, peretas database Kejaksaan Agung (Kejagung) itu seorang anak baru gede (ABG) berumur 16 tahun di Lahat, Sumatera Selatan (Sumsel).Kejagung berkoordinasi Badan Siber dan Sandi Negara (BSSN) untuk membongkar sosok peretas database mereka. Kejagung memperoleh informasi dugaan peretasan dan penjualan database mereka di situs raidforums.com."Dari penelusuran yang didapatkan identitas pelaku berinisial adalah M atau panjangannya ada MFW," kata Kapuspenkum Kejagung, Leonard Eben Ezer Simanjuntak, dalam konferensi pers di Kejagung, Jl Sultan Hasanuddin, Jakarta Selatan, Jumat (19/2/2021).'
    klasifikasi= 'peretasan'
    return render_template('testing.html', isi_berita=isi_berita, klasifikasi=klasifikasi)




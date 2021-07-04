import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from gensim.summarization import summarize
import requests
from bs4 import BeautifulSoup
import re
import pickle
from sklearn.base import BaseEstimator
nltk.download('punkt')
nltk.download('stopwords')


from sklearn.base import BaseEstimator
from sklearn import utils as skl_utils
from tqdm import tqdm
from sklearn.metrics import accuracy_score,classification_report
import multiprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
import xgboost as xgb
from xgboost import XGBClassifier
import pickle

#training

class Text2TfIdfTransformer(BaseEstimator):

    def __init__(self):
        self._model = TfidfVectorizer()
        pass

    def fit(self, df_x, df_y=None):
        df_x = df_x
        #.apply(lambda x : clean_text(x))
        self._model.fit(df_x)
        return self

    def transform(self, df_x):
        return self._model.transform(df_x)

def traning(data):
    df = pd.read_csv(data, encoding = 'ISO-8859-1')
    df_x = df['kasus']
    df_y = df['label']
    
    tfidf_transformer = Text2TfIdfTransformer()
    tfidf_vectors = tfidf_transformer.fit(df_x).transform(df_x)
    
    pl_xgb_tf_idf = Pipeline(steps=[('tfidf',Text2TfIdfTransformer()),
                         ('xgboost', xgb.XGBClassifier(objective='multi:softmax'))])
    

    scores = cross_val_score(pl_xgb_tf_idf, df_x, df_y, cv=10)
    xgbst=pl_xgb_tf_idf.fit(df_x, df_y) 
    akurasi= "Accuracy for Tf-Idf & XGBoost Classifier : ", scores.mean()
    with open('/content/drive/MyDrive/Model','wb') as f:
        pickle.dump(xgbst,f)
    
    return akurasi

def model(data):
    df = pd.read_csv(data, encoding = 'ISO-8859-1')
    df_x = df['kasus']
    df_y = df['label']
    
    tfidf_transformer = Text2TfIdfTransformer()
    tfidf_vectors = tfidf_transformer.fit(df_x).transform(df_x)
    
    pl_xgb_tf_idf = Pipeline(steps=[('tfidf',Text2TfIdfTransformer()),
                         ('xgboost', xgb.XGBClassifier(objective='multi:softmax'))])

    #model xgboost
    xgbst=pl_xgb_tf_idf.fit(df_x, df_y) 
    with open('/content/drive/MyDrive/Model','wb') as f:
        pickle.dump(xgbst,f)
    
    return model

def testing(data):
    df = pd.read_csv(data, encoding = 'ISO-8859-1')
    df_x = df['kasus']
    df_y = df['label']
    with open('/content/drive/MyDrive/Model','rb') as f:
        mp = pickle.load(f)
    res = mp.predict(df_x)
    
    #classification report
    hasil = print(classification_report(res,df_y))
    #pembuatan Confusiion Matrix
    labels = ['ancaman', 'carding', 'hoax', 'peretasan', 'bukan kasus']
    cf_matrix = confusion_matrix(res,df_y)
    ax = sns.heatmap(cf_matrix, annot=True, xticklabels = labels, yticklabels=labels, cmap="YlGnBu")
    plt.xlabel('prediction')
    plt.ylabel('actual')
    plt.show()
    return hasil

def prepro(data):
    df = pd.read_csv(data)
    data = df
    c2=data['kasus']
    
    return c2

def mentah(data1):
    df1 = pd.read_excel(data1)
    data1 = df1
    c1=data1['kasus']
    
    return c1

#testing

def clean(kasus):
    kasus = ''.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(\w+:\/\/\S+)|(http\S+)", " ", kasus)) #hapus #,@,url
    kasus = re.sub(r'[^A-Za-z\s\/]' ,' ', kasus) #hapus simbol dan tanda baca
    kasus = re.sub(r'_', '', kasus) 
    kasus = re.sub(r'/', ' ', kasus)
    kasus = re.sub(r'\d+', '', kasus) 
    kasus = re.sub(r'\n', ' ', kasus) 
    kasus = re.sub(r'\s{2,}', ' ', kasus)
    kasus = re.sub(r"baca juga", ' ', kasus)
    return kasus
def remove_stop_words(kasus):
    stop_words = set(stopwords.words('indonesian'))
    no_stop_words=[word for word in kasus.split() if word not in stop_words]
    no_step_sentence = ' '.join(no_stop_words)
    return no_step_sentence

def casefolding(kasus):
    kasus = kasus.lower().strip() #case folding
    return kasus

def stemming(kasus):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(kasus)

def token(kasus):
    tokenizer = RegexpTokenizer('\w+')
    kasus = tokenizer.tokenize(kasus)
    return kasus
def preprocessing(data):
    hasilpreprocessing = []

    cl = clean(data)
    cf = casefolding(cl)
    stop = remove_stop_words(cf)
    stem = stemming(stop)
    tok = token(stem)

    hasilpreprocessing = pd.Series(str(tok), dtype=str)
    
    return hasilpreprocessing


detik = {
    "class" : "detail__body-text itp_bodycontent",
    "noise" : ["\n", "\r", "}", "#div-gpt-ad-1572507980488-0 iframe{", "border: 0px;",
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


def Scrap_News(source, url):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find('div', class_=source["class"])
  results = results.get_text()

  for i in source["noise"]:
    results = results.replace(i, " ")

  return results
  
def Paging_Number(source, url):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  max_paging = soup.find('div', class_=source["paging"])
  return int(max_paging[-1])+1
  
def Ringkas(source):
  URL = input()

  if source!="tribun":
    text = Scrap_News(source, URL)
    sum = text

  else:
    num_page = Paging_Number(source,URL)
    res_ = []
    
    for i in range(1, num_page):
      url = url + "?page=" + str(i)
      res = Scrap_News(source, url)
      res_.append(res)

    text = " ".join(res_)

    for i in source["noise"]:
      text = text.replace(i, " ")

  return text


def testing():
    with open('C:/users/asus/desktop/Model','rb') as f:
        mp = pickle.load(f)
    link = Ringkas(detik)
    hasilpreprocessing= preprocessing(link)
    res = mp.predict(hasilpreprocessing)
    
    return link, res

# link, res = testing()
# print(link, res)


import os
import re

import requests
from bs4 import BeautifulSoup

import numpy as np
from tensorflow import keras
from keras.models import load_model
import joblib

from sklearn.feature_selection import SelectKBest, mutual_info_classif, chi2, f_classif

dict_ = {'bat dong san': 1,
         'chinh tri': 2,
         'giai tri': 5,
         'giao duc': 6,
         'khoa hoc': 7,
         'kinh doanh': 8,
         'phap luat': 11,
         'suc khoe': 12,
         'the gioi': 13,
         'the thao': 14,
         'thuc pham': 15,
         'xe': 16}

def load_stopwords():
    stopwords = []
    with open("./vietnamese-stopwords.txt", 'r', encoding='utf8') as file:
        for line in file:
            stopwords.append(line.strip())
    return stopwords

def load_dictionary():
    dictionary = []
    with open("words.txt", 'r', encoding='utf8') as file:
        for line in file:
            dictionary.append(line.strip())
    return dictionary

stopwords = load_stopwords()
dictionary = load_dictionary()
special_words = ['chép liên kết', 'bình luận', 'chủ đề nổi bật', 'vietnamnet', 'vnexpress', 'dantri', 'tuoitre', 'facebook', 'aa', 'email', 'hc', 'zalo']


def load_model_(al, fs, nf):
    if fs == "Mutual Information":
        fs_var = "mutual_information"
    elif fs == "Chi-square":
        fs_var = "chi_square"
    elif fs == "ANOVA F":
        fs_var = "anova_f"
    else:
        fs_var = "None"

    if str(nf) == str(2500):
        nf_var = "2500"
    elif str(nf) == str(5000):
        nf_var = "5000"
    elif str(nf) == str(7500):
        nf_var = "7500"
    else:
        nf_var = "0"

    if (fs_var == "None" or nf_var == "None"):
        fs_var = "None"
        nf_var = "0"
        
    if al == "Neural Networks":
        model = load_model('../TaoModel/nn_%s_%s_model.h5' % (fs_var, nf_var), compile = False)
    elif al == "SVM":
        model = joblib.load('../TaoModel/svm_%s_%s_model.joblib' % (fs_var, nf_var))
    elif al == "KNN":
        model = joblib.load("../TaoModel/knn_%s_%s_model.joblib" % (fs_var, nf_var))

    print(model)
    return model
        

def read_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return True, soup, "Success"
    except Exception as e:
        print(e)
        return False, None, str(e)


def htmltag_remove(soup):
    # Bỏ tất cả thẻ a chứa href dẫn đến trang khác
    for a in soup.find_all('a', href=True):
        a.decompose()

    body = soup.find("body").get_text().strip()
    try:
        header = soup.find("body").find("header").get_text().strip()
        footer = soup.find("body").find("footer").get_text().strip()
        dt = body.replace(header, "").replace(footer, "")
    except :
        dt = body

    try:
        header = soup.find_all('div', {'class': re.compile("header.*")})
        for h in header:
            h = h.get_text().strip()
            dt = dt.replace(h, "")
    
    except Exception as e:
        print(e)
        dt = body

    return dt

def special_character_remove(dt):
    dt = dt.lower()
    # Bỏ từ ngữ chứa số
    dt = re.sub(r'\S*\d\S*', ' ', dt)
    # Bỏ ký tự đặc biệt
    dt = re.sub('[^\w+]', ' ', dt)
    #
    for w in special_words:
        dt = dt.replace(w, '')
        
    return dt

def stopwords_remove(dt):
    dt = dt.split()
    for d in dt:
        if d in stopwords:
            dt.remove(d)
    dt = " ".join(dt)

    # Bỏ khoảng trắng
    dt = " ".join([d.strip() for d in dt.split()])
    return dt


def rarewords_remove(dt):
    # Bỏ rareword
    dt = dt.split(" ")
    new_dt = []
    for d in dt:
        if d in dictionary:
            new_dt.append(d)
            
    dt = " ".join(new_dt)
    return dt

def create_bow_vector(text):
    # Tách các từ trong văn bản
    words = text.lower().split()
    
    # Khởi tạo vector số bag of words với các phần tử bằng 0
    bow_vector = [0] * len(dictionary)
    
    # Đếm số lần xuất hiện của từng từ trong từ điển
    for word in words:
        if word in dictionary:
            bow_vector[dictionary.index(word)] += 1
    
    return bow_vector

def feature_select(vector, fs, nf):
    if fs == "Mutual Information":
        fs_var = "mutual_information"
    elif fs == "Chi-square":
        fs_var = "chi_square"
    elif fs == "ANOVA F":
        fs_var = "anova_f"
    else:
        return vector

    if str(nf) == str(2500):
        nf_var = "2500"
    elif str(nf) == str(5000):
        nf_var = "5000"
    elif str(nf) == str(7500):
        nf_var = "7500"
    else:
        return vector

    features = joblib.load("features_%s_%s.joblib" % (fs_var, nf_var))
    print(features)
    
    return vector
    


def classification(vector, algorithm, fs, nf):
    model = load_model_(algorithm, fs, nf)
    result = model.predict([vector])
    
    if algorithm == "Neural Networks":
        result = np.argmax(result)

    for key in dict_.keys():
        if dict_[key] == int(result):
            return key
    




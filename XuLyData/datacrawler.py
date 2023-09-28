import requests, bs4
from urllib.parse import urlsplit
import sys, os
import pandas as pd

import PickFileDialogGUI

def get_filename_from_url(url=None):
    if url is None:
        return None
    urlpath = urlsplit(url).path
    return urlpath

imageLink = PickFileDialogGUI.pickExcel()
try:
    df = pd.read_csv(imageLink)
except:
    df = pd.read_excel(imageLink)

folder = imageLink.split('/')[-1].replace('.csv', '').replace('.xlsx', '')

print(folder)
if not os.path.exists(folder):
    os.mkdir(folder)

i = 1
for url in df['Links']:
    try:
        #print('Crawling data from %s...' % url)
        page = requests.get(url)
        page.raise_for_status()
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        file = open('.\\' + folder + get_filename_from_url(url) ,'w', encoding='utf8')
        file.write(page.text)
        file.close()
        i += 1
    except Exception as e:
        print(e)
        continue
    

print('Done!')

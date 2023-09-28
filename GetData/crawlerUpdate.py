import requests, bs4
from urllib.parse import urlsplit
import sys, os
import pandas as pd

def get_filename_from_url(url=None):
    if url is None:
        return None
    urlpath = urlsplit(url).path
    return os.path.basename(urlpath)

df = pd.read_excel("nt1.xlsx")
for url in df['URL']:
    print('Crawling data from %s...' % url)
    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = bs4.BeautifulSoup(page.text)

        file = open(os.path.join('./NghethuatData', get_filename_from_url(url)) + '.html','wb')
        for i in page.iter_content(1000000):
            file.write(i)
        file.close()
    except Exception as e:
        print("Error crawling %s: %s" % (url, str(e)))
        continue

print('Done!')
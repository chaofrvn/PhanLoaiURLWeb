import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas

# Lấy thông tin từ trang web
def get_url(web, tag, page):
    return f"{web}/{tag}-page{page}"

def writeData(csvFile, fieldnames, data_rows, isFirstPage):
    if isFirstPage:
        with open(csvFile, "w", encoding="utf8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",", quotechar="\"")
            writer.writeheader()
            for row in data_rows:
                if row:
                    writer.writerow(row)
    else:
        with open(csvFile, "a", encoding="utf8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=",", quotechar="\"") 
            for row in data_rows:
                if row:
                  writer.writerow(row)

web = "https://vietnamnet.vn"
tag = "giao-duc"
page = 1
fieldnames = ['title', 'link', 'category']

isFirstPage = False

# Lấy tiêu đề bài báo
while True:
    try:
        url = get_url(web, tag, page)
        print(f"Crawling link from %s..." % url)
        response = requests.get(url)

        # Phân tích HTML để lấy các thông tin cần thiết
        soup = BeautifulSoup(response.content, "html.parser")

        article_list = []
        
        articles = soup.find_all("div", {"class": "horizontalPost"})
        for a in articles:
            cate = a.find("div", {"class": "horizontalPost__main-cate"}).find("a").get("title")
            main_title = a.find("h3", {"class": "horizontalPost__main-title"}).find("a")

            title = main_title.get_text().strip()
            link = web + main_title.get("href")
            article_list.append({'title': title, 'category': cate, 'link': link})
        
        page += 1

        writeData(tag + '.csv', fieldnames, article_list, isFirstPage)
                                
    except Exception as e:
        print(e)
        page += 1
        continue


    
    
    

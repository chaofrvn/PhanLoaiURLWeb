import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas

# Lấy thông tin từ trang web
def get_url(web, tag, page):
    return f"{web}/{tag}/trang-{page}.htm"

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


web  = "https://dantri.com.vn"
tag = "giao-duc-huong-nghiep"
page = 2
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
        
        articles = soup.find_all("article", {"class": "article-item"})
        print(len(articles))
        for a in articles:
            try:
                cate = ""

                title_main = a.find("h3", {"class": "article-title"}).find("a")
                title = title_main.get_text().strip()
                link = title_main.get("href")
                article_list.append({'title': title, 'category': cate, 'link': link})
            except:
                continue

        page += 1

        writeData(tag + '.csv', fieldnames, article_list, isFirstPage)
                                
    except Exception as e:
        print(e)
        page += 1
        continue


    
    
    

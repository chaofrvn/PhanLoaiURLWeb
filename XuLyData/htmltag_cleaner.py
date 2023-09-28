import re
import bs4
import os

folder = 'txt'
if not os.path.exists(folder):
    os.mkdir(folder)

def htmltag_cleaner(file, i):
    print(i)
    with open(file, 'r', encoding="utf8") as file:
        data = file.read()
        
    soup = bs4.BeautifulSoup(data, "html.parser")

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

    dt = dt.lower()
    # Bỏ từ ngữ chứa số
    dt = re.sub(r'\S*\d\S*', ' ', dt)
    # Bỏ ký tự đặc biệt
    dt = re.sub('[^\w+]', ' ', dt)
    # Bỏ khoảng trắng
    dt = " ".join([d.strip() for d in dt.split()])

    file = open(os.path.join('.\\txt', str(i) + '.txt'),'w', encoding = "utf8")
    file.write(dt)
    file.close()

i = 0
for file in os.listdir('.'):
    if '.html' in file:
        i += 1
        htmltag_cleaner(file, i)
    

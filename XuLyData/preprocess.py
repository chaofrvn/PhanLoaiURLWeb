import re
import bs4
import os

stopwords = []

special_words = ['chép liên kết', 'bình luận', 'chủ đề nổi bật', 'vietnamnet', 'vnexpress', 'dantri', 'tuoitre', 'facebook', 'aa', 'email', 'hc', 'zalo']
with open("vietnamese-stopwords.txt", 'r', encoding='utf8') as file:
    for line in file:
        stopwords.append(line.strip())

def htmltag_and_stopwords_cleaner(file, dir_, i):
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

    try:
        header = soup.find_all('div', {'class': re.compile("header.*")})
        for h in header:
            h = h.get_text().strip()
            dt = dt.replace(h, "")
    
    except Exception as e:
        print(e)
        dt = body

    dt = dt.lower()
    # Bỏ từ ngữ chứa số
    dt = re.sub(r'\S*\d\S*', ' ', dt)
    # Bỏ ký tự đặc biệt
    dt = re.sub('[^\w+]', ' ', dt)
    

    # Bỏ Stopword
    dt = dt.split()
    for d in dt:
        if d in stopwords:
            dt.remove(d)
    dt = " ".join(dt)

    for w in special_words:
        dt = dt.replace(w, '')

    # Bỏ khoảng trắng
    dt = " ".join([d.strip() for d in dt.split()])

    file = open(os.path.join('.\\' + dir_, str(i) + '.txt'),'w', encoding = "utf8")
    file.write(dt)
    file.close()

i = 0
dir_ = os.getcwd().split('\\')[-1]

folder = dir_
if not os.path.exists(folder):
    os.mkdir(folder)

for file in os.listdir('.'):
    if '.html' in file or '.htm' in file:
        i += 1
        htmltag_and_stopwords_cleaner(file, dir_, dir_ + '-' + str(i))
    

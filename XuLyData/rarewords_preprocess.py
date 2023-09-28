import re
import bs4
import os

words = []

with open("words.txt", 'r', encoding='utf8') as file:
    for line in file:
        words.append(line.strip())
    print(len(words))

def rarewords_remove(file, path, dir_):
    with open(file, 'r', encoding="utf8") as f:
        dt = f.read()
        
    # Bỏ rareword
    dt = dt.split(" ")
    new_dt = []
    for d in dt:
        if d in words:
            new_dt.append(d)
    dt = " ".join(new_dt)

    file_path = os.path.join(path, dir_, file)
    file = open(file_path,'w', encoding = "utf8")
    file.write(dt)
    file.close()

FJoin = os.path.join
def GetFiles(path):
    file_list, dir_list = [], []
    for dir, subdirs, files in os.walk(path):
        file_list.extend([FJoin(dir, f) for f in files])
        dir_list.extend([FJoin(dir, d) for d in subdirs])
    return file_list, dir_list

path = r'D:\Projects\Python\Crawler and Scraper\Web Classification Dataset Crawler\data_xử lý2'

if __name__ == "__main__":
    files, dirs = GetFiles(os.path.expanduser(os.getcwd()))
    for d in dirs:
        os.chdir(d)
        print(d)

        dir_ = os.getcwd().split('\\')[-1]

        folder = os.path.join(path, dir_)
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        for file in os.listdir('.'):
            if '.txt' in file and "words.txt" not in file:
                try:
                    rarewords_remove(file, path, dir_)
                except Exception as e:
                    print(e)
                    continue
    

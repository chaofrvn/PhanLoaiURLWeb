import numpy as np
import os
import pandas as pd

dict_ = {'bat dong san': 1,
         'chinh tri': 2,
         'doi song': 3,
         'du lich': 4,
         'giai tri': 5,
         'giao duc': 6,
         'khoa hoc': 7,
         'kinh doanh': 8,
         'mua sam': 9,
         'nghe thuat': 10,
         'phap luat': 11,
         'suc khoe': 12,
         'the gioi': 13,
         'the thao': 14,
         'thuc pham': 15,
         'xe': 16}

def convert_data(path, vector_template):
    for dirpath, dirnames, filenames in os.walk(path):
        data_ = []
        tag_ = dirpath.split('\\')[-1]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r', encoding='utf8') as file:
                word_dict = {}
                content = file.read()
                words = content.split()

                for word in words:
                    if word not in word_dict:
                        word_dict[word] = 1
                    else:
                        word_dict[word] += 1

                vector = np.zeros(len(vector_template) + 1)
                for i, word in enumerate(vector_template):
                    vector[i] = word_dict.get(word, 0)

                vector[-1] = dict_[tag_]
                data_.append(vector)
                print("Converting {}...".format(tag_))
        df = pd.DataFrame(data_)
        df.to_csv('./{}.csv'.format(tag_), index=False)

def convert_vector_template(path):
    vector_template = []
    with open(path, 'r', encoding='utf-8') as file_vector_template:
        for line in file_vector_template:
            vector_template.append(line.strip())
    return vector_template

root_dir = './data_xuly2'
file_words = './words.txt'
vector_template = convert_vector_template(file_words)
convert_data(root_dir, vector_template)

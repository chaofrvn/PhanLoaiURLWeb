import os
import json

FJoin = os.path.join

def GetFiles(path):
    file_list, dir_list = [], []
    for dir, subdirs, files in os.walk(path):
        file_list.extend([FJoin(dir, f) for f in files])
        dir_list.extend([FJoin(dir, d) for d in subdirs])
    return file_list, dir_list


words = {}
if __name__ == "__main__":
    files, dirs = GetFiles(os.path.expanduser("."))
    for file in files:
        if '.txt' in file:
            #print(file)
            with open(file, 'r', encoding='utf8') as f:
                dt = f.read()
                for d in dt.split():
                    words[d] = words.setdefault(d, 0) + 1
    print(len(words))
    sum_ = sum(words.values())
    avr = sum_ / len(words)
    print('avr: ', avr) #327
    
    r_key = []
    for key in words.keys():
        if words[key] < 55:
            r_key.append(key)
    for k in r_key:
        del words[k]
            
    words = dict(sorted(words.items(), key=lambda x:x[1], reverse=True))

    print("---")
    print(len(words))
    sum_ = sum(words.values())
    avr = sum_ / len(words)
    print('avr: ', avr) #327

    with open("words.txt", "w", encoding='utf8') as f:
        for w in words.keys():
            f.write(w)
            f.write('\n')
        f.close()

    with open("words.json", "w", encoding='utf8') as outfile:
        json.dump(words, outfile, ensure_ascii=False)
        outfile.close()
    print('Done!')



            

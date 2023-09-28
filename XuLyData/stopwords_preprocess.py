stopwords = []
with open("vietnamese-stopwords.txt", 'r', encoding='utf8') as file:
    for line in file:
        stopwords.append(line.strip())

dt = ""

dt = dt.split()
for d in dt:
    if d in stopwords:
        dt.remove(d)
dt = " ".join(dt)

print(dt)

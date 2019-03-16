
import pandas as pd
import copy
import math


df = pd.read_csv('train.csv')

now = df[['title', 'Category']][df.image_path.str.startswith('beauty_image')]
# print(now.head())
train_length = now.shape[0]
print("train_length == " + str(train_length))

lis = {}

brand = {}
rbrand = {
    # "Foundation":1,
    # "Face Palette":0,
    # "Concealer":7,
    # "Lip Gloss":14,
    # "Blush On":2,
    # "Highlighter":8,
    # "BB & CC Cream":5,
    # "Other Face Cosmetics":4,
    # "Lip Tint":13,
    # "Bronzer":11,
    # "Lip Liner":15,
    # "Powder":3,
    # "Setting Spray":10,
    # "Primer":9,
    # "Contour":6,
    # "Other Lip Cosmetics":16,
    # "Lipstick":12,

    "foundation": 1,
    "aquaboost": 1,

    # "face palette": 0,
    # "Palette": 0,
    "concealer":7,
    "lip gloss":14,
    "blush": 2,
    "blusher": 2,
    "blushon": 2,
    "cheeklit": 2,
    "flush": 2,

    "highlighter":8,
    # "cc":5,
    # "dd": 5,

    "other face cosmetics":4,
    "lip tint":13,
    "bronzer":11,
    "lip liner":15,
    "powder":3,
    "bedak": 3,
    "loose": 3,

    "setting spray":10,
    "primer":9,
    "contour":6,
    "Other Lip Cosmetics":16,
    "lipstick":12,
}




tmp = copy.deepcopy(list(rbrand.items()))
rbrand.clear()
for key, val in tmp:
    rbrand[key.lower()] = val
# print(rbrand)
for it in rbrand:
    brand[rbrand[it]] = it
# print(brand)



NUM_CLASSES = 17
CLASS_OFFSET = 0

train_categories = now["Category"].tolist()
train_titles = now["title"].tolist()

for i in range(train_length):
    idx = train_categories[i] - CLASS_OFFSET
    cur = train_titles[i].split()
    for it in cur:
        word = it.lower()
        if word not in lis:
            lis[word] = [0 for _ in range(NUM_CLASSES + 1)]
        lis[word][idx] += 1
        lis[word][-1] += 1

for it in lis:
    for i in range(NUM_CLASSES):
        lis[it][i] /= lis[it][-1]

# cnt = 0
# for it in lis:
#     if lis[it][-1] < 5:
#         continue
#     print(it, [ '%.2f' % elem for elem in lis[it]])
#     cnt += 1
#     if cnt > 50:
#         break



df2 = pd.read_csv('test.csv')
ans_length = df2.shape[0]
tot = 0
print("length == " + str(ans_length))




image_paths = df2['image_path'].tolist()
itemids = df2['itemid'].tolist()
titles = df2['title'].tolist()


ans_list = [None for _ in range(ans_length)]




for i in range(ans_length):
    s = image_paths[i]
    if not s.startswith('beauty_image'):
        ans_list[i] = 100
        continue
    cur = titles[i].split()
    vec = [0 for _ in range(NUM_CLASSES + 1)]
    idx = -1
    tot += 1
    for it in cur:
        word = it.lower()
        if word in rbrand:
            idx = rbrand[word]
            break
        if word not in lis or lis[word][-1] < 5:
            continue
        vec[-1] += lis[word][-1]
        weight = 1 # math.sqrt(lis[word][-1])
        for j in range(NUM_CLASSES):
            vec[j] += lis[word][j] * weight
    if idx == -1:
        if vec[-1] < 100:
            idx = 4 # TODO
        else:
            rec = 0
            mem = -1
            for j in range(NUM_CLASSES):
                if vec[j] > rec:
                    rec = vec[j]
                    mem = j
            idx = mem + CLASS_OFFSET
    ans_list[i] = idx

print("tot predicted == " + str(tot))



ans = pd.DataFrame({"itemid": itemids, "Category": ans_list})
ans.to_csv('beauty_ans.csv', index = False, sep = ',')



good = bad = 0
for i in range(train_length):
    cur = train_titles[i].split()
    idx = train_categories[i]
    ans = -1
    vec = [0 for _ in range(NUM_CLASSES + 1)]
    for it in cur:
        word = it.lower()
        if word in rbrand:
            ans = rbrand[word]
            break
        if lis[word][-1] < 5:
            continue
        vec[-1] += lis[word][-1]
        weight = 1 # lis[word][-1]**(1./3.)
        for j in range(NUM_CLASSES):
            vec[j] += lis[word][j] * weight
    if ans == -1:
        if vec[-1] < 100:
            ans = 4 # TODO
        else:
            rec = 0
            mem = -1
            for j in range(NUM_CLASSES):
                if vec[j] > rec:
                    rec = vec[j]
                    mem = j
            ans = mem + CLASS_OFFSET
    if ans == idx:
        good += 1
    else:
        bad += 1

print(good, bad, good + bad)
print("accuracy: {}".format(good / (good + bad)))


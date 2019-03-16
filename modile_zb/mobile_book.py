import pandas as pd
import copy
import math


df = pd.read_csv('train.csv')

now = df[['title', 'Category']][df.image_path.str.startswith('mobile_image')]
length = now.shape[0]
print(length)


lis = {}
brand = {}
rbrand = {
    "Smartfren": 53,
    "Infinix": 40,
    "Brandcode": 39,
    "Icherry": 52,
    "Advan": 45,
    "Iphone": 31,
    "Realme": 51,
    "Motorola": 49,
    "Maxtron": 56,
    "Nokia": 38,
    "Xiaomi": 34,
    "Mito": 46,
    "Sony": 33,
    "SPC": 57,
    "Lenovo": 37,
    "Alcatel": 55,
    "Samsung": 32,
    "Vivo": 42,
    "Evercoss": 44,
    "Strawberry": 50,
    "Blackberry": 36,
    "Asus": 43,
    "Honor": 54,
    "Oppo": 41,
    "Huawei": 47,
    "Sharp": 48
}


tmp = copy.deepcopy(list(rbrand.items()))
rbrand.clear()
for key, val in tmp:
    rbrand[key.lower()] = val
print(rbrand)
for it in rbrand:
    brand[rbrand[it]] = it
print(brand)


titles = now['title'].tolist()
cats = now['Category'].tolist()

for i in range(length):
    idx = cats[i] - 31
    cur = titles[i].split()
    for it in cur:
        word = it.lower()
        if word not in lis:
            lis[word] = [0 for _ in range(28)]
        lis[word][idx] += 1
        lis[word][-1] += 1

for it in lis:
    for i in range(27):
        lis[it][i] /= lis[it][-1]

cnt = 0
for it in lis:
    print(it, lis[it])
    cnt += 1
    if cnt > 50:
        break


cats = now['Category'].tolist()

good = bad = 0
for i in range(length):
    cur = titles[i].split()
    idx = cats[i]
    ans = -1
    vec = [0 for _ in range(28)]
    consider = 0
    for it in cur:
        word = it.lower()
        if word in rbrand:
            ans = rbrand[word]
            break
        vec[-1] += lis[word][-1]
        for j in range(27):
            vec[j] += lis[word][j]
    if ans == -1:
        if vec[-1] < 5 * consider:
            ans = 35
        else:
            rec = 0
            mem = -1
            for j in range(27):
                if vec[j] > rec:
                    rec = vec[j]
                    mem = j
            ans = mem + 31
    if ans == idx:
        good += 1
    else:
        bad += 1

print(good, bad, good + bad, good / (good + bad))


df2 = pd.read_csv('test.csv')
length = df2.shape[0]
tot = 0
print(length)


image_paths = df2['image_path'].tolist()
itemids = df2['itemid'].tolist()
titles = df2['title'].tolist()
# print(len(image_paths))
# print(len(itemids))
# print(len(titles))

ans_list = [None for _ in range(length)]


for i in range(length):
    s = image_paths[i]
    if not s.startswith('mobile_image'):
        ans_list[i] = 100
        continue
    cur = titles[i].split()
    vec = [0 for _ in range(28)]
    idx = -1
    tot += 1
    consider = 0
    for it in cur:
        word = it.lower()
        if word in rbrand:
            idx = rbrand[word]
            break
        if word not in lis:
            continue
        vec[-1] += lis[word][-1]
        for j in range(27):
            vec[j] += lis[word][j]
    if idx == -1:
        if vec[-1] < 5 * consider:
            idx = 35
        else:
            rec = 0
            mem = -1
            for j in range(27):
                if vec[j] > rec:
                    rec = vec[j]
                    mem = j
            idx = mem + 31
    ans_list[i] = idx
print(tot)


ans = pd.DataFrame({"itemid": itemids, "Category": ans_list})
ans.to_csv('mobile_ans.csv', columns = ['itemid', 'Category'], index = False, sep = ',')

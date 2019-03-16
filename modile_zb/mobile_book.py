
# coding: utf-8

# In[1]:


import pandas as pd
import copy
import math


df = pd.read_csv('train.csv')

now = df[['title', 'Category']][df.image_path.str.startswith('mobile_image')]
# print(now.head())
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


# In[2]:


tmp = copy.deepcopy(list(rbrand.items()))
rbrand.clear()
for key, val in tmp:
    rbrand[key.lower()] = val
print(rbrand)
for it in rbrand:
    brand[rbrand[it]] = it
print(brand)


# In[3]:



for i in range(length):
    idx = now.iloc[i]['Category'] - 31
    cur = now.iloc[i]['title'].split()
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


# In[4]:



df2 = pd.read_csv('test.csv')
length = df2.shape[0]
# ans = pd.DataFrame(columns = ('itemid', 'Category'))
tot = 0
print(length)


# In[5]:


image_paths = df2['image_path'].tolist()
itemids = df2['itemid'].tolist()
titles = df2['title'].tolist()
print(len(image_paths))
print(len(itemids))
print(len(titles))

ans_list = [None for _ in range(length)]


# In[6]:


for i in range(length):
    if i % 10000 == 0:
        print(i)
    s = image_paths[i]
    if not s.startswith('mobile_image'):
#         row = {'itemid': itemids[i], 'Category': 100}
        ans_list[i] = 100
        continue
    cur = titles[i].split()
    vec = [0 for _ in range(28)]
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
        weight = math.sqrt(lis[word][-1])
        for j in range(27):
            vec[j] += lis[word][j] * weight
    if idx == -1:
        if vec[-1] < 100:
            idx = 35
        else:
            rec = 0
            mem = -1
            for j in range(27):
                if vec[j] > rec:
                    rec = vec[j]
                    mem = j
            idx = mem + 31
#     row = {'itemid': df2.loc[i]['itemid'], 'Category': idx}
    ans_list[i] = idx
print(tot)


# In[7]:


ans = pd.DataFrame({"itemid": itemids, "Category": ans_list})
ans.to_csv('mobile_ans_2.csv', index = False, sep = ',')


# In[ ]:


# good = bad = 0
# for i in range(length):
#     cur = now.iloc[i]['title'].split()
#     idx = now.iloc[i]['Category']
#     ans = -1
#     vec = [0 for _ in range(28)]
#     for it in cur:
#         word = it.lower()
#         if word in rbrand:
#             ans = rbrand[word]
#             break
#         if lis[word][-1] < 5:
#             continue
#         vec[-1] += lis[word][-1]
#         weight = math.sqrt(lis[word][-1])
#         for j in range(27):
#             vec[j] += lis[word][j] * weight
#     if ans == -1:
#         if vec[-1] < 100:
#             ans = 35
#         else:
#             rec = 0
#             mem = -1
#             for j in range(27):
#                 if vec[j] > rec:
#                     rec = vec[j]
#                     mem = j
#             ans = mem + 31
#     if ans == idx:
#         good += 1
#     else:
#         bad += 1
#
# print(good, bad, good + bad)


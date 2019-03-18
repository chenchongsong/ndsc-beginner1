#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import copy
import math


# In[16]:


df = pd.read_csv('train.csv')

now = df[['title', 'Category']][df.image_path.str.startswith('fashion_image')]
length = now.shape[0]
print(length)
print(now)


# In[17]:





# In[18]:





# In[19]:





# In[20]:


lis = {}
brand = {}
rbrand = {
     "Wedding Dress": 23, 
     "Shirt": 27, 
     "Casual Dress": 18, 
     "Maxi Dress": 20, 
     "Big Size Dress": 24, 
     "Bodycon Dress": 22, 
     "Party Dress": 19, 
     "Blouse": 26, 
     "Tshirt": 25, 
     "Crop Top ": 29, 
     "Tanktop": 28,   
     "A Line Dress": 21, 
     "Big Size Top": 30
}


# In[21]:


tmp = copy.deepcopy(list(rbrand.items()))
rbrand.clear()
for key, val in tmp:
    rbrand[key.lower()] = val
print(rbrand)
for it in rbrand:
    brand[rbrand[it]] = it
print(brand)


# In[ ]:





# In[22]:



titles = now['title'].tolist()
cats = now['Category'].tolist()

for i in range(length):
    idx = cats[i] - 18
    cur = titles[i].split()
    for it in cur:
        word = it.lower()
        if word not in lis:
            lis[word] = [0 for _ in range(14)]
        lis[word][idx] += 1
        lis[word][-1] += 1

for it in lis:
    for i in range(13):
        lis[it][i] /= lis[it][-1]

cnt = 0
for it in lis:
    print(it, lis[it])
    cnt += 1
    if cnt > 50:
        break




# In[23]:


cats = now['Category'].tolist()

good = bad = 0
for i in range(length):
    cur = titles[i].split()
    idx = cats[i]
    ans = -1
    vec = [0 for _ in range(14)]
    consider = 0
    for it in cur:
        word = it.lower()
        if word in rbrand:
            ans = rbrand[word]
            break
        vec[-1] += lis[word][-1]
        for j in range(13):
            vec[j] += lis[word][j]
    if ans == -1:
        if vec[-1] < 5 * consider:
            ans = 17
        else:
            rec = 0
            mem = -1
            for j in range(13):
                if vec[j] > rec:
                    rec = vec[j]
                    mem = j
            ans = mem + 18
    if ans == idx:
        good += 1
    else:
        bad += 1

print(good, bad, good + bad, good / (good + bad))


# In[24]:


df2 = pd.read_csv('test.csv')
length = df2.shape[0]
tot = 0
print(length)


# In[25]:


image_paths = df2['image_path'].tolist()
itemids = df2['itemid'].tolist()
titles = df2['title'].tolist()
# print(len(image_paths))
# print(len(itemids))
# print(len(titles))


# In[26]:


ans_list = [None for _ in range(length)]


for i in range(length):
    s = image_paths[i]
    if not s.startswith('fashion_image'):
        ans_list[i] = 100
        continue
    cur = titles[i].split()
    vec = [0 for _ in range(14)]
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
        for j in range(13):
            vec[j] += lis[word][j]
    if idx == -1:
        if vec[-1] < 5 * consider:
            idx = 17
        else:
            rec = 0
            mem = -1
            for j in range(13):
                if vec[j] > rec:
                    rec = vec[j]
                    mem = j
            idx = mem + 18
    ans_list[i] = idx
print(tot)


# In[27]:


ans = pd.DataFrame({"itemid": itemids, "Category": ans_list})
ans.to_csv('fashion_ans.csv', columns = ['itemid', 'Category'], index = False, sep = ',')


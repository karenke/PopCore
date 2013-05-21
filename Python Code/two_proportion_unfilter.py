import csv as csv
import numpy as np
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date, num2epoch
from collections import Counter

from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
from sklearn.neighbors import KNeighborsClassifier



def validDate(str):
  Result = True
  try:
    d = DT.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
  except ValueError, e:
    Result = False
  return Result


f = open('friend_pairs.csv', 'rb')
csv_file_object = csv.reader(f) 

fri_pairs = []
for row in csv_file_object:
	t = (row[0],row[1])
	fri_pairs.append(t)
	# print row
#print fri_pairs
f.close()

f = open('allUser_like_unfilter.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file
# data=[] #Creat a variable called 'data'

user_like = {} #['uid' : list of page_url]

user_url = {} #['(uid,page_url' : like_date]

for row in csv_file_object: #Skip through each row in the csv file
  uid = row[0]
  page_url = row[1]
  like_date = row[2]
  if uid not in user_like:
    l = []
    l.append(page_url)
    user_like[uid] = l
  else:
    user_like[uid].append(page_url)
  t = (uid,page_url)
  user_url[t] = like_date

f.close()

# delta is the time limit of influence
one_day = date2num(DT.datetime.strptime("2012-1-2 0:0:0", "%Y-%m-%d %H:%M:%S")) - date2num(DT.datetime.strptime("2012-1-1 0:0:0", "%Y-%m-%d %H:%M:%S"))
delta = one_day*3
# print delta

pair_share = {} # for each friend pair: ratio of required common items/ total common items 
Jaccard_coefficient = {}

user_influence = {} # <user_id : number of items influenced by other users>

for pair in fri_pairs:
  u1 = pair[0]
  u2 = pair[1]
  t = (u2,u1)
  
  if pair not in pair_share and t not in pair_share:
    if u1 in user_like and u2 in user_like:
      l1 = user_like[u1]
      l2 = user_like[u2]
      l3 = [val for val in l1 if val in l2] #common items
      l4 = list(set(l1) | set(l2)) # union

      if l3 and l4: #not empty
        Jaccard_coefficient[pair] = float(len(l3))/len(l4)
        # print Jaccard_coefficient[pair]

        for url in l3:
          t1 = (u1,url)
          t2 = (u2,url)
          like_date1 = DT.datetime.strptime(user_url[t1], "%Y-%m-%d %H:%M:%S")
          like_date2 = DT.datetime.strptime(user_url[t2], "%Y-%m-%d %H:%M:%S")
          time_diff = date2num(like_date1) - date2num(like_date2)
          #print time_diff

          countRequired = 0
          if time_diff >= -delta and time_diff <= delta:
            countRequired += 1

          if time_diff >= 0 and time_diff <= delta: # u1 influence u2
            if u2 not in user_influence:
              li = []
              li.append(url)
              user_influence[u2] = li
            else:
              if url not in user_influence[u2]:
                user_influence[u2].append(url)

          if time_diff <= 0 and time_diff >= -delta: # u2 influence u1
            if u1 not in user_influence:
              li = []
              li.append(url)
              user_influence[u1] = li
            else:
              if url not in user_influence[u1]:
                user_influence[u1].append(url)

        pair_share[pair] = countRequired/len(l3)


      else: # is empty
        pair_share[pair] = 0
        Jaccard_coefficient[pair] = 0

f = open('friend_pair_Jaccard.csv','w')
for t in Jaccard_coefficient:
  if Jaccard_coefficient[t] > 0:
    line = str(t[0])+','+str(t[1]) + ','+ str(Jaccard_coefficient[t])+'\n'
    f.write(line)
    # print str(t) + ':'+ str(Jaccard_coefficient[t])
f.close()


user_proportion = {}
for uid in user_like:
  if uid in user_influence:
    user_proportion[uid] = float(len(user_influence[uid]))/len(user_like[uid])
  else:
    user_proportion[uid] = 0


f = open('user_proportion.csv', 'w')
for uid in user_proportion:
  line = str(uid)+','+str(user_proportion[uid])+'\n'
  f.write(line)
f.close()


data2 = []
for row in Jaccard_coefficient:
  if Jaccard_coefficient[row] > 0:
    t = []
    t.append(row)
    t.append(Jaccard_coefficient[row])
    data2.append(t)

data2.sort(key=lambda  tup: float(tup[1]), reverse=True)
data2 = np.array(data2)

c2 = 1
x2 = []
y2 = []
for row in data2:
  # t = []
  # t.append(c2)
  # t.append(round(float(row[1]),2))
  # x2.append(t)
  x2.append(c2)
  y2.append(round(float(row[1]),2))
  c2 += 1

x2 = np.array(x2)
y2 = np.array(y2)


plt.plot(x2,y2,'b^')
# plt.axis([0, 180, 0, 1.0])

plt.show()



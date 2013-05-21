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

fri_pairs = [] # list of tuples of friend pairs
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

for pair in fri_pairs:
  u1 = pair[0]
  u2 = pair[1]
  t = (u2,u1)
  
  if pair not in pair_share and t not in pair_share:
    if u1 in user_like and u2 in user_like:
      l1 = user_like[u1]
      l2 = user_like[u2]
      l3 = [val for val in l1 if val in l2] #common items
      total = len(l3)
      if l3: #not empty
        # print l3
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
        pair_share[pair] = countRequired/total

      else: #l3 is empty
        pair_share[pair] = 0



# # print pair_avg

data = []
for row in pair_share:
  t = []
  t.append(row)
  t.append(pair_share[row])
  data.append(t)

data.sort(key=lambda  tup: float(tup[1]), reverse=True)
data = np.array(data)
# print data

c = 1
x = []
y = []
for row in data:
  t = []
  t.append(c)
  t.append(round(float(row[1]),2))
  x.append(t)
  # x.append(count)
  # y.append(round(float(row[1]),2))
  c += 1

x = np.array(x)
y = np.array(y)

# print x.max()
print x[:].min()
print x[:,0].max()
print x[:,1].min()
print x[:,1].max()
# print y



n_neighbors = 10

h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

from sklearn.neighbors import NearestNeighbors
neigh = NearestNeighbors(n_neighbors=15)
neigh.fit(x) 

    # Plot also the training points
plt.scatter(x[:, 0], x[:, 1], c=y, cmap=cmap_bold)
plt.axis('tight')

plt.show()



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

fri_pairs = [] # store the list of friend pairs, each element is a pair of user id
for row in csv_file_object:
	t = (row[0],row[1])
	fri_pairs.append(t)
	# print row
#print fri_pairs
f.close()

f = open('allUser_like_unfilter.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file
# data=[] #Creat a variable called 'data'

user_like = {} # store the list of the user's like in the format of ['uid' : list of page_url]

user_url = {} # key is the tuple of user id and item url, and value is the like_date ['(uid,page_url' : like_date]

for row in csv_file_object: # read files and store the value into corresponding data structure
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


pair_avg = {} # dict store sum of the average time difference for each pair of friends <fri_pair: sum(avg(time_diff))>
count = {} # store the number of common influenced item

for pair in fri_pairs:
  u1 = pair[0]
  u2 = pair[1]
  if u1 in user_like and u2 in user_like:
    l1 = user_like[u1]
    l2 = user_like[u2]
    l3 = [val for val in l1 if val in l2]
    if l3: #not empty
      # print l3
      for url in l3:
        t1 = (u1,url)
        t2 = (u2,url)
        like_date1 = DT.datetime.strptime(user_url[t1], "%Y-%m-%d %H:%M:%S")
        like_date2 = DT.datetime.strptime(user_url[t2], "%Y-%m-%d %H:%M:%S")
        time_diff = date2num(like_date1) - date2num(like_date2)
        #print time_diff

        if time_diff >= 0 and time_diff <= delta: # find the items within the time limit so that they are influenced
        # if time_diff >= 0:  
          if pair not in pair_avg:
            pair_avg[pair] = time_diff
            count[pair] = 1
          else:
            pair_avg[pair] += time_diff
            count[pair] += 1
        if time_diff <= 0 and time_diff >= -delta:
        # if time_diff <= 0:
          p = (u2, u1)
          if p not in pair_avg:
            pair_avg[p] = -time_diff
            count[p] = 1
          else:
            pair_avg[p] += -time_diff
            count[p] += 1


data = [] # store the actual average time difference, each element is a tuple of (friend_pair, avg_time_diff)
for pair in pair_avg: 
  pair_avg[pair] /= count[pair]
  m = []
  m.append(pair)
  m.append(pair_avg[pair])
  data.append(m)

# print pair_avg

# print data
f2 = open('fri_pair_td.csv', 'w') # put the result into files
for row in data:
  line = row[0][0]+','+row[0][1]+','+str(row[1])+'\n'
  f2.write(line)
f2.close()


data.sort(key=lambda  tup: float(tup[1]), reverse=True) # sort the average time difference in descending order
data = np.array(data)
# print data

c = 1
x = []
y = []
for row in data: 
  t = []
  t.append(c) # hashing the friend pair id
  t.append(round(float(row[1]),2))
  x.append(t)
  # x.append(count)
  # y.append(round(float(row[1]),2))
  c += 1

x = np.array(x)
y = np.array(y)

# print x.max()
print x[:,0].min()
print x[:,0].max()
print x[:,1].min()
print x[:,1].max()
#print y


# plt.plot(x,y,'b^')
# plt.axis([0, 3500, 0, 2000])

# plt.show()


n_neighbors = 15

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



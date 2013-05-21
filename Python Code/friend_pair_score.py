import csv as csv
import numpy as np
import math as math
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date, num2epoch
from collections import Counter

from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
from sklearn.neighbors import KNeighborsClassifier



f = open('fri_pair_td.csv', 'rb')
csv_file_object = csv.reader(f) 


user_list = {} # dict <user id : list of tuples (friend_id, avg_time_diff)>
for row in csv_file_object:
	uid = row[0]
	fri_id = row[1]
	time_diff = 1/float(row[2])

	if uid not in user_list:
		li = []
		t = (fri_id, time_diff)
		li.append(t)
		user_list[uid] = li
	else:
		t = (fri_id, time_diff)
		user_list[uid].append(t)

f.close()

# print user_list

friend_pair_score = {} # dict <friend_pair: avg_time_diff>
for uid in user_list:
	li = user_list[uid]
	for tup in li:
		pair = (uid,tup[0])
		if pair not in friend_pair_score:
			friend_pair_score[pair] = tup[1]

# print friend_pair_score

score_sum = 0
for pair in friend_pair_score:
	score_sum += friend_pair_score[pair]*friend_pair_score[pair]

friend_pair_score_normalized = {}
sqrt_sum = math.sqrt(score_sum)
for pair in friend_pair_score: # normalize the score
	friend_pair_score_normalized[pair] = friend_pair_score[pair]/sqrt_sum
	
# print friend_pair_score_normalized
# print math.sqrt(score_sum)


f = open('friend_pair_Jaccard.csv', 'rb')
csv_file_object = csv.reader(f) 

friend_pair_Jaccard = {}
for row in csv_file_object:
	pair = (row[0],row[1])
	pair_re = (row[1],row[0])
	# print pair
	if pair in friend_pair_score:
		friend_pair_Jaccard[pair] = row[2]
	if pair_re in friend_pair_score:
		friend_pair_Jaccard[pair_re] = row[2]

f.close()

# print friend_pair_Jaccard

x1 = []
y1 = []
x2 = []
y2 = []
c = 1

friend_pair_Jaccard = sorted(friend_pair_Jaccard.items(), key=lambda x: float(x[1]), reverse=True) # sort according to the Jaccard Coefficient in descending order

for pair in friend_pair_Jaccard:
	# print pair[0]
	x1.append(c)
	y1.append(friend_pair_score_normalized[pair[0]])
	# y1.append(friend_pair_score_normalized[pair])
	x2.append(c)
	y2.append(friend_pair_Jaccard[c-1][1])
	c += 1

plt.figure()                # the first figure
plt.subplot(111)   
plt.plot(x1,y1,'r',x2,y2,'b')
plt.title('friend_pair')
plt.show()





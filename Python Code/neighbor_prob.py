import csv as csv
import numpy as np
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date, num2epoch
from collections import Counter

from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
from sklearn.neighbors import KNeighborsClassifier



f = open('fri_pair_td.csv', 'rb')
csv_file_object = csv.reader(f) 


user_total = {} # <user_id : total of the time difference>
user_list = {} # <user_id : list of tuples (friend_id, 1/time_diff)>
for row in csv_file_object:
	uid = row[0]
	fri_id = row[1]
	time_diff = 1/float(row[2])

	if uid not in user_list:
		li = []
		t = (fri_id, time_diff)
		li.append(t)
		user_list[uid] = li
		user_total[uid] = time_diff
	else:
		t = (fri_id, time_diff)
		user_list[uid].append(t)
		user_total[uid] += time_diff

f.close()

user_prob = {} # <user_id: list of tuples (friend_id, normalized prob)>
for row in user_list:
	li = []
	for tup in user_list[row]:
		t = (tup[0],tup[1]/user_total[row])
		# print t
		li.append(t)
	user_prob[row] = li

print user_prob
# print user_list
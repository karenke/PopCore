import csv as csv
import numpy as np
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date, num2epoch
from collections import Counter

def validDate(str):
  Result = True
  try:
    d = DT.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
  except ValueError, e:
    Result = False
  return Result

f = open('django_facebook_facebookfriendlike.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file

fri_pair = [] # store the pairs of friend

item = {} # for each item, store lists of the user_id and the like_date
for row in csv_file_object: 
	if validDate(row[6]):
		u1 = row[1]
		uid = row[2]
		like_date = row[6]
		page_url = row[9] #row[9] is url, row[3] is facebook_id
		if page_url not in item:
			l = []
			t = (uid, like_date)
			l.append(t)
			item[page_url] = l
		else:
			t = (uid, like_date)
			#print 'bf:'+str(item[page_url])
			item[page_url].append(t)
			#print 'af:'+str(item[page_url])
		t1 = (u1,uid)
		fri_pair.append(t1)
 
f.close()

cnt = Counter()
counts = Counter(fri_pair) # remove duplicates of pairs

# for t in counts.items():
# 	print t[0][0]

f = open('django_facebook_facebooklike.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file


for row in csv_file_object: #Skip through each row in the csv file
	if validDate(row[5]):
		uid = row[1]
		like_date = row[5]
		page_url = row[8]
		if page_url not in item:
			l = []
			t = (uid, like_date)
			l.append(t)
			item[page_url] = l
		else:
			t = (uid, like_date)
			#print 'bf:'+str(item[page_url])
			item[page_url].append(t)
			#print 'af:'+str(item[page_url])
f.close()

#print item

f2 = open('item_list.csv', 'w')
for row in item:
	line = str(row)+','+str(item[row])+'\n'
	f2.writelines(line)
	
f2.close()

f2 = open('friend_pairs.csv', 'w')
for row in counts.items(): #Skip through each row in the csv file
	line = str(row[0][0])+','+str(row[0][1])+'\n'
	f2.writelines(line)
	
f2.close()



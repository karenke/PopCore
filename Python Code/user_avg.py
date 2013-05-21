import csv as csv
import numpy as np
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date, num2epoch
from matplotlib.ticker import MultipleLocator, FormatStrFormatter



def validDate(str):
  Result = True
  try:
    d = DT.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
  except ValueError, e:
    Result = False
  return Result

f = open('allUser_filtered.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file

data = {} # <user_id: total of difference>
count = {} # <user_id: number of items>
for row in csv_file_object: #Skip through each row in the csv file
	t = []
	uid = row[0]
	#print uid
	like_num = date2num(DT.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"))
	debut_num = date2num(DT.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"))
	diff = like_num - debut_num
	if diff > 1:
		if uid not in data:
			data[uid] = diff
			count[uid] = 1
		else:
			data[uid] = data[uid] + diff
			count[uid] = count[uid] + 1
 
f.close()


like_pair = [] # store the list of tuples (user_id, avg_time_diff)
for uid in data:
	data[uid] /= count[uid]
	m = []
	m.append(uid)
	m.append(data[uid])
	like_pair.append(m)


f2 = open('user_avg_td.csv', 'w')
for row in like_pair: #Skip through each row in the csv file
	uid = row[0]
	diff = float(row[1]*365*5/1462) #days
	line = str(uid)+','+str(diff)+'\n'
	f2.writelines(line)
	
f2.close()

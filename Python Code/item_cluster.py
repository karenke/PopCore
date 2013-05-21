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

f = open('django_facebook_facebookfriendlike.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file
data = {} # <item id : total time_diff>
count = {} # <item id : total number of likes>
for row in csv_file_object: #Skip through each row in the csv file
	if validDate(row[6]) and validDate(row[7]):
		if DT.datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S") > DT.datetime.strptime('2003-1-1 0:0:0', "%Y-%m-%d %H:%M:%S"):
			# print row[5], row[6]
			item_id = row[9]
			diff = date2num(DT.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S")) - date2num(DT.datetime.strptime(row[7	], "%Y-%m-%d %H:%M:%S"))
			if item_id not in data:
				data[item_id] = diff
				count[item_id] = 1
			else:
				data[item_id] = data[item_id] + diff
				count[item_id] = count[item_id] + 1

f = open('item.arff', 'w')

for t in data:
	data[t] = data[t] / count[t]
	line = '\''+ str(t) +'\'' + ',' + str(data[t]) + '\n'
	f.writelines(line)

f.close()

#print data
# print count
# c = 0
# for t in count:
# 	c = c + count[t]

# print c



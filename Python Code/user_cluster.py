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
data = {} # <user id : sum of time_diff>
count = {} # <user id : number of items>
for row in csv_file_object: #Skip through each row in the csv file
	if validDate(row[6]) and validDate(row[7]):
		if DT.datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S") > DT.datetime.strptime('2003-1-1 0:0:0', "%Y-%m-%d %H:%M:%S"):
			# print row[5], row[6]
			uid = row[2]
			diff = date2num(DT.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S")) - date2num(DT.datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S"))
			if diff < 0:
				print row[6] + ', '+ row[7]
			if uid not in data:
				data[uid] = diff
				count[uid] = 1
			else:
				data[uid] = data[uid] + diff
				count[uid] = count[uid] + 1

# f = open('user.arff', 'w')

# for t in data:
# 	data[t] = data[t] / count[t]
# 	line = str(t) + ',' + str(data[t]) + '\n'
# 	f.writelines(line)

# f.close()

#print data
#print count
c = 0
co = 0
for t in count:
	co = co +1
	c = c + count[t]
print co
print c



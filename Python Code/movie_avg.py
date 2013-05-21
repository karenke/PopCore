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

f = open('allUser+movie_filtered.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file


data = []
for row in csv_file_object: #Skip through each row in the csv file
	t = []
	uid = row[0]
	item_id = row[1]
	like_date = DT.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
	debut_date = DT.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
	t.append(uid)
	t.append(item_id)
	t.append(like_date)
	t.append(debut_date)
	data.append(t)
 
f.close()

data = np.array(data)


x = []
y = []
period_start = '2008-1-1 0:0:0'
period_end = '2008-7-31 0:0:0'
for row in data:
	if row[3] > DT.datetime.strptime(period_start, "%Y-%m-%d %H:%M:%S") and row[3] < DT.datetime.strptime(period_end, "%Y-%m-%d %H:%M:%S"):
 		x.append(row[3])
 		y.append(row[2])

# print x
#print y

fig = plt.figure()

graph = fig.add_subplot(111)

graph.scatter(x, y, s=20, c='b', marker='o')

graph.xaxis.set_major_locator(MultipleLocator(300))
graph.yaxis.set_major_locator(MultipleLocator(100))

graph.set_xlabel('Moive Release Time')
graph.set_ylabel('Liked date')
graph.set_title('Time difference of movie debut and user like')

plt.show()
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


f = open('user_proportion.csv', 'rb')
csv_file_object = csv.reader(f) 

data = []
for row in csv_file_object:
	if float(row[1]) > 0:
		t = []
		t.append(row[0]) # user id
		t.append(row[1]) # value of proportion
		data.append(t)
	
data.sort(key=lambda  tup: float(tup[1]), reverse=True) # sort the value in decreasing order
data = np.array(data)

c = 1
x = []
y = []
for row in data:
  # t = []
  # t.append(c2)
  # t.append(round(float(row[1]),2))
  # x2.append(t)
  x.append(c)
  y.append(round(float(row[1]),2))
  c += 1

x = np.array(x)
y = np.array(y)


plt.plot(x,y,'b^')
# plt.axis([0, 180, 0, 1.0])

plt.show()



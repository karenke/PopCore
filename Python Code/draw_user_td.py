import csv as csv
import numpy as np
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date, num2epoch
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets
from sklearn.neighbors import KNeighborsClassifier

f = open('user_avg_td.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file

data = []
for row in csv_file_object:
	t = []
	uid = row[0]
	time_diff = row[1]
	t.append(uid)
	t.append(time_diff)
	data.append(t)
f.close()

data.sort(key=lambda  tup: float(tup[1]), reverse=True) # sort the time difference in decreasing order
data = np.array(data)
#print data

count = 1
x = []
y = []
for row in data:
	t = []
	t.append(count)
	t.append(round(float(row[1]),2))
	x.append(t)
	y.append(1)
	# x.append(count)
	# y.append(round(float(row[1]),2))
	count += 1

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


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
data=[] #Creat a variable called 'data'
for row in csv_file_object: #Skip through each row in the csv file
	t = []
	t.append(row[6]) # like date
	t.append(row[7]) # release date
	data.append(t)
 
data = np.array(data) #Then convert from a list to an array
#print data
f.close()

newData = []
for t in data:
	m = []
	if validDate(t[0]) and validDate(t[1]):
		if DT.datetime.strptime(t[1], "%Y-%m-%d %H:%M:%S") > DT.datetime.strptime('2010-1-1 0:0:0', "%Y-%m-%d %H:%M:%S"):
			m.append(DT.datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S"))
			m.append(DT.datetime.strptime(t[1], "%Y-%m-%d %H:%M:%S"))
	if len(m) == 2:
 		newData.append(m)

newData = np.array(newData)

min_x = [t[0] for t in newData]
print min(min_x)



#print newData

time_dict = {} #value is the average time difference
time_count = {}
y = []
x = []
for t in newData:
	# print t[0] + " " + t[1]
	like_num = date2num(t[0])
	debut_num = date2num(t[1])
	temp = like_num - debut_num
	if temp > 1:
		x.append(debut_num)
		y.append(temp)
		if debut_num not in time_dict:
			time_dict[debut_num] = temp
		else:
			time_dict[debut_num] += temp
		if debut_num not in time_count:
			time_count[debut_num] = 1
		else:
			time_count[debut_num] += 1


debut_pair = [] # list of tuples (release id, avg_time_diff)
for debut_num in time_dict:
	time_dict[debut_num] /= time_count[debut_num]
	m = []
	m.append(debut_num)
	m.append(time_dict[debut_num])
	debut_pair.append(m)


x = [num2date(date) for (date, value) in debut_pair]
y = [value*5/1462 for (date, value) in debut_pair]

fig = plt.figure()

graph = fig.add_subplot(111)

graph.scatter(x, y, s=20, c='b', marker='o')

graph.xaxis.set_major_locator(MultipleLocator(600))
graph.yaxis.set_major_locator(MultipleLocator(25))

graph.set_xlabel('Debut Date')
graph.set_ylabel('Time difference (year)')
graph.set_title('Time difference of movie debut and user like')

plt.show()

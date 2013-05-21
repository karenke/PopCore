import csv as csv
import numpy as np
import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date, num2epoch

def validDate(str):
  Result = True
  try:
    d = DT.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
  except ValueError, e:
    Result = False
  return Result


f = open('django_facebook_facebooklike.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file
data=[] #Creat a variable called 'data'
for row in csv_file_object: #Skip through each row in the csv file
	t = []
	t.append(row[5]) # like date
	t.append(row[6]) # release date
	data.append(t)
 
data = np.array(data) #Then convert from a list to an array
#print data
f.close()


newData = []

for t in data:
	m = []
	if validDate(t[0]) and validDate(t[1]):
		m.append(DT.datetime.strptime(t[0], "%Y-%m-%d %H:%M:%S"))
		m.append(DT.datetime.strptime(t[1], "%Y-%m-%d %H:%M:%S"))
	 #	t[1] = DT.datetime.strptime(t[1], "%Y-%m-%d %H:%M:%S")
	# print m 
	if len(m) == 2:
		# print t[0] + " " + t[1]
		# print m
 		newData.append(m)

newData = np.array(newData)

#print newData

x = []
for t in newData:
	# print t[0] + " " + t[1]
	temp = date2num(t[0]) - date2num(t[1])
	if temp > 1:
		x.append(temp)
		#print temp
		#print num2date(temp)
#print newData
x = sorted(x)
print x
print len(x)
# print min(x)
# print max(x)

count = []
interval = 1462 #five years
bound = interval
cur_count = 0;
for i in range(len(x)):
	if bound > 1462*6:
		cur_count += 1
		continue
	if x[i] < bound:
		cur_count = cur_count + 1
	else:
		bound += interval
		count.append(cur_count)
		cur_count = 1

count.append(cur_count)

print count

ind = np.arange(len(count))
width = 0.35

fig = plt.figure()
ax = fig.add_subplot(111)
rects1 = ax.bar(ind, count, width, color='b')

ax.set_xlabel('Time difference (Years)')
ax.set_ylabel('Distribution')
ax.set_title('Time difference of movie debut and user like')
ax.set_xticks(ind+width/2)
ax.set_xticklabels( ('5', '10', '15', '20', '25', '30', '>30') )

print num2date(interval)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

autolabel(rects1)

plt.show()


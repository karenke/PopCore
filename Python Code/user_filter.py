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

join_date = {} # <user id: join_date>
for row in csv_file_object: #Skip through each row in the csv file
	if validDate(row[6]):
		uid = row[2]
		if uid not in join_date:
			join_date[uid] = date2num(DT.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S"))
		else:
			if date2num(DT.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S")) < join_date[uid]:
				join_date[uid] = date2num(DT.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S"))

	if validDate(row[6]) and validDate(row[7]):
		t = []
		t.append(row[2]) # user id
		t.append(row[6]) # like date
		t.append(row[7]) # release date
		t.append(row[9]) # page_url
		data.append(t)
 
f.close()

f = open('django_facebook_facebooklike.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file

for row in csv_file_object: #Skip through each row in the csv file
	if validDate(row[5]):
		uid = row[1]
		if uid not in join_date:
			join_date[uid] = date2num(DT.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"))
		else:
			if date2num(DT.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")) < join_date[uid]:
				join_date[uid] = date2num(DT.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"))

	if validDate(row[5]) and validDate(row[6]):
		t = []
		t.append(row[1]) # user id
		t.append(row[5]) # like date
		t.append(row[6]) # release date
		t.append(row[8]) # page_url
		data.append(t)
 
data = np.array(data) #Then convert from a list to an array
#print data
f.close()


f2 = open('allUser_filtered.csv', 'w')
for row in data: #Skip through each row in the csv file
	uid = row[0]
	if date2num(DT.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")) > join_date[uid]:
		line = str(uid)+','+str(row[1])+','+str(row[2])+','+str(row[3])+'\n'
		f2.writelines(line)
	
f2.close()



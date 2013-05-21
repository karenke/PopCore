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

f = open('allUser_filtered.csv', 'rb')
csv_file_object = csv.reader(f) #Load in the csv file
# data=[] #Creat a variable called 'data'

user_like = [] #store the list of user's like, each element is a tuple of <uid, page_url, like_date>
join_date = {} # dictionary < uid: join_date>

for row in csv_file_object: #Skip through each row in the csv file
	uid = row[0]
	like_date = row[1] #like date
	page_url = row[3] #row[9] is url, row[3] is facebook_id
	t = (uid,page_url,like_date)
	user_like.append(t)
	
f.close()

f2 = open('allUser_like.csv', 'w')
for row in user_like: #Skip through each row in the csv file
	line = str(row[0])+','+str(row[1])+','+str(row[2])+'\n'
	f2.writelines(line)
	
f2.close()

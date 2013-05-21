import csv as csv
import numpy as np
import datetime as DT

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

join_date = {} # dictionary < uid: join_date>
for row in csv_file_object: #Skip through each row in the csv file
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


user_like = [] #store the list of user's like, each element is a tuple of <uid, page_url, like_date>

for row in data: #Skip through each row in the csv file
	uid = row[0]
	like_date = row[1] #like date
	page_url = row[3] #row[9] is url, row[3] is facebook_id
	t = (uid,page_url,like_date)
	user_like.append(t)
	
f.close()

f2 = open('allUser_like_unfilter.csv', 'w')
for row in user_like: #Skip through each row in the csv file
	line = str(row[0])+','+str(row[1])+','+str(row[2])+'\n'
	f2.writelines(line)
	
f2.close()

	



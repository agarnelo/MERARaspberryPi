import json
import datetime
import sqlite3
import os

#Class Container is going to hold information for each Container stored in the device
class Container:
	dispenserID = 0
	pillCount = 0
	scheduledTime = ""
	dailyTime = ""
	frequency = 0
	dose = 0

#Containers Dictionary
	#Containers -> Key: the Container ID & the Value: Container Class
Containers = {}


#VARIABLES TO BE CHANGED (FIRST LINE)
sqliteDB = '/Users/anahigarnelo/Documents/Fall 2015/Capstone/MeraRP/PiDatabase'

#Check if the database Exists
if os.path.isfile(sqliteDB):
	print "Exists"
	conn = sqlite3.connect(sqliteDB)
	c = conn.cursor()
	
	#DISPENSER INFORMATION
	c.execute('''SELECT * FROM dispenser''')
	for row in c:
		dispenserID = row[0]
		startTime = row[1]
		endTime = row[2]
	print dispenserID
	print startTime
	print endTime


	c.execute('''SELECT * FROM container''')
#	print "\nContainer"
#	print "container ID, Pill Count, Dispenser ID"

	for row in c:
		contain = Container()
		Containers[row[0]] = contain
		Containers[row[0]].pillCount = row[1]
		Containers[row[0]].dispenserID = row[2]

	c.execute('''SELECT * FROM medication''')
#	print "\nMedication"
#	print "Dose, Scheduled Time, Daily Time, Frequency, Container Stored In"
	for row in c:
		Containers[row[4]].dose = row[0]
		Containers[row[4]].scheduledTime = row[1]
		Containers[row[4]].dailyTime = row[2]
		Containers[row[4]].frequency = row[3]
	conn.close()

	#Print out the Containers Information
	for each in Containers:
		print Containers[int(each)].dispenserID
		print Containers[int(each)].pillCount
		print Containers[int(each)].scheduledTime
		print Containers[int(each)].dailyTime
		print Containers[int(each)].frequency
		print Containers[int(each)].dose
		print "\n"

else:
	print "Doesn't exist"








#http://stackoverflow.com/questions/12932607/how-to-check-with-python-and-sqlite3-if-one-sqlite-database-file-exists




import json
import datetime
import requests
import string
import sqlite3
import os

#VARIABLES TO BE CHANGED (FIRST 3 LINES)
sqliteDB = '/Users/anahigarnelo/Documents/Fall 2015/Capstone/MeraRP/PiDatabase'
url = "http://localhost:9000/dispenser?id="
dispenserID = 1

str = "Error" + datetime.datetime.today().strftime("%Y_%m_%d") + ".txt"

dispenserRequest = url + repr(dispenserID)
r = requests.get(dispenserRequest)
data = r.json()

print r.status_code

if (r.status_code==200):
	print "Successful HTTP Request to MERA Website"

#	dispenserID = data['Dispenser ID']
#	oET = data['Operation End Time']
#	oST = data['Operation Start Time']

	#Update Database because DB Already Exists
	if os.path.isfile(sqliteDB):
		print "Exists"
		conn = sqlite3.connect(sqliteDB)
		c = conn.cursor()
		for eachContainer in data['Containers']:
			c.execute(''' INSERT OR REPLACE INTO container(containerID, pillCount, attachedTo) VALUES(?,?,?) ''', (eachContainer['Container ID'],eachContainer['Pill Count'],data['Dispenser ID']))
			c.execute(''' INSERT OR REPLACE INTO medication(dose, scheduledTime, dailyTime, frequency, storedIn) VALUES(?,?,?,?,?) ''', (eachContainer['Medication']['Dose'], eachContainer['Medication']['Scheduled Time'], eachContainer['Medication']['Daily Time'],eachContainer['Medication']['Frequency'],eachContainer['Container ID']))
		
		conn.commit()
		conn.close()
	

	else:
		print "Doesn't exist"
		conn = sqlite3.connect(sqliteDB)
		c = conn.cursor()
		c.execute('''CREATE TABLE dispenser(dispenserID bigserial primary key not null, startTime time, endTime time, CONSTRAINT dispenserIDUnique UNIQUE(dispenserID)) ''')
		c.execute('''CREATE TABLE container(containerID bigserial primary key not null, pillCount bigint, attachedTo bigserial, foreign key(attachedTo) References dispenser(dispenserID), CONSTRAINT containerIDUnique UNIQUE(containerID))''')
		c.execute('''CREATE TABLE medication(dose bigint, scheduledTime time, dailyTime time, frequency bigint, storedIn bigserial, foreign key(storedIn) References container(containerID), CONSTRAINT medicationIDUnique UNIQUE(storedIn))''')
		c.execute(''' INSERT INTO dispenser(dispenserID, startTime, endTime) VALUES(?,?,?) ''', (data['Dispenser ID'],data['Operation Start Time'],data['Operation End Time']))
		for eachContainer in data['Containers']:
			c.execute(''' INSERT INTO container(containerID, pillCount, attachedTo) VALUES(?,?,?) ''', (eachContainer['Container ID'],eachContainer['Pill Count'],data['Dispenser ID']))
			c.execute(''' INSERT INTO medication(dose, scheduledTime, dailyTime, frequency, storedIn) VALUES(?,?,?,?,?) ''', (eachContainer['Medication']['Dose'], eachContainer['Medication']['Scheduled Time'], eachContainer['Medication']['Daily Time'],eachContainer['Medication']['Frequency'],eachContainer['Container ID']))
		conn.commit()
		conn.close()

	conn = sqlite3.connect(sqliteDB)
	c = conn.cursor()

	c.execute('''SELECT * FROM dispenser''')
	print "\nDispenser"
	print "Dispenser ID, startTime, endTime"
	for row in c: print(row)

	c.execute('''SELECT * FROM container''')
	print "\nContainer"
	print "container ID, Pill Count, Dispenser ID"
	for row in c: print(row)
	
	c.execute('''SELECT * FROM medication''')
	print "\nMedication"
	print "Dose, Scheduled Time, Daily Time, Frequency, Container Stored In"
	for row in c: print(row)
	conn.close()



#http://stackoverflow.com/questions/12932607/how-to-check-with-python-and-sqlite3-if-one-sqlite-database-file-exists




import json
import datetime
import requests
import string
import sqlite3


str = "Error" + datetime.datetime.today().strftime("%Y_%m_%d") + ".txt"

url = "http://localhost:9000/dispenser?id="
dispenserID = 1

dispenserRequest = url + repr(dispenserID)

r = requests.get(dispenserRequest)

data = r.json()

print r.status_code

if (r.status_code==200):
	print "Hello"

	dispenserID = data['Dispenser ID']
	oET = data['Operation End Time']
	oST = data['Operation Start Time']
	
	conn = sqlite3.connect('/Users/anahigarnelo/Documents/Fall 2015/Capstone/PiDatabase')
	c = conn.cursor()
	c.execute('''CREATE TABLE dispenser(dispenserID bigserial primary key not null, startTime time, endTime time)''')
	c.execute('''CREATE TABLE container(containerID bigserial primary key not null, pillCount bigint,empty boolean, attachedTo bigserial, foreign key(attachedTo) References dispenser(dispenserID))''')
	c.execute('''CREATE TABLE medication(dose bigint, scheduledTime time, dailyTime time, frequency bigint, storedIn bigserial, foreign key(storedIn) References container(containerID));''')
	c.execute(''' INSERT INTO dispenser(dispenserID, startTime, endTime) VALUES(?,?,?) ''', (data['Dispenser ID'],data['Operation Start Time'],data['Operation End Time']))
	for eachContainer in data['Containers']:
		c.execute(''' INSERT INTO container(containerID, pillCount, attachedTo) VALUES(?,?,?) ''', (eachContainer['Container ID'],eachContainer['Pill Count'],data['Dispenser ID']))
		c.execute(''' INSERT INTO medication(dose, scheduledTime, dailyTime, frequency, storedIn) VALUES(?,?,?,?,?) ''', (eachContainer['Medication']['Dose'], eachContainer['Medication']['Scheduled Time'], eachContainer['Medication']['Daily Time'],eachContainer['Medication']['Frequency'],eachContainer['Container ID']))
	conn.commit()

	c.execute('''SELECT * FROM dispenser''')
	for row in c:
		print(row)

	conn.close()







import json
import urllib2

postData = {"Containers":[{"Container ID": 1, "Available":True},{"Container ID": 2, "Available":True},{"Container ID": 3, "Available":False}], "Dispenser ID":10}

try:
	req = urllib2.Request('http://localhost:9000/containers')
	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, json.dumps(postData))
except:
	print "HTTP Post Error"


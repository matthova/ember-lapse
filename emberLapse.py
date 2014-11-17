import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
import requests
import json

def checkStatus(url, params, photoTaken):
        r = requests.post(url, params)
	decoded = json.loads(r.text)
	try:
		state = decoded['response']['state']
		print state
		if state == 'exposing':
			photoTaken = True
			GPIO.output(7,1)
			time.sleep(.1)
			GPIO.output(7,0)
		elif state == 'delaminating':
			photoTaken = False
		elif state == 'homing':
			GPIO.output(7,1)
			time.sleep(.1)
			GPIO.output(7,0)
	except(ValueError, KeyError, TypeError):
		print "JSON format error"
	return photoTaken

try:
	GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
	GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT	

	GPIO.output(7,1)
	time.sleep(2)
	GPIO.output(7,0)

	url = 'http://10.140.68.85/command'
	params = {'command':'getstatus'}
	photoTaken = False
	while(1):
		photoTaken = checkStatus(url, params, photoTaken)
		time.sleep(.5)

except KeyboardInterrupt:
	GPIO.cleanup()

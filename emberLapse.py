import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
import requests
import json

layer_count = 0
layers_per_photo = 4
photoTaken = False

def checkStatus(url, params):
	global layer_count, layers_per_photo, photoTaken
        r = requests.post(url, params)
	decoded = json.loads(r.text.lower())
	try:
		state = decoded['response']['state']
		print state
		if state == 'exposing':
			if photoTaken == False:
				photoTaken = True
				print layer_count
				print layers_per_photo
				print layer_count % layers_per_photo
				print ' '
				if layer_count % layers_per_photo == 0:
					GPIO.output(7,1)
					time.sleep(.1)
					GPIO.output(7,0)
				layer_count += 1
		elif state == 'separating':
			photoTaken = False
		elif state == 'homing' or state == "movingtostartposition":
			GPIO.output(7,1)
			time.sleep(.1)
			GPIO.output(7,0)
	except(ValueError, KeyError, TypeError):
		print "JSON format error"

try:
	GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
	GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT	

	GPIO.output(7,1)
	time.sleep(2)
	GPIO.output(7,0)

	url = 'http://10.140.68.74/command'
	params = {'command':'getstatus'}
	while(1):
		checkStatus(url, params)
		time.sleep(.5)

except KeyboardInterrupt:
	GPIO.cleanup()

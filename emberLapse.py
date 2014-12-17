import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
import requests
import json
import math

layer_count = 0
layers_per_photo = 4
total_layers = 0
fps = 60
seconds = 20
photoTaken = False
photoPin = 7

def checkStatus(url, params):
	global layer_count, layers_per_photo, photoTaken, total_layers
        r = requests.post(url, params)
	decoded = json.loads(r.text.lower())
	try:
		state = decoded['response']['state']
		print state
		if state == 'exposing':
			if photoTaken == False:
				photoTaken = True
				if layer_count % layers_per_photo == 0:
					takePhoto()
				layer_count += 1
		elif state == 'separating':
			photoTaken = False
		elif state == 'homing' or state == "movingtostartposition":
			takePhoto()
		elif state == 'home'
			total_layers = 0

	except(ValueError, KeyError, TypeError):
		print "JSON format error"

def takePhoto()
	GPIO.output(photoPin, 1)
	time.sleep(.1)
	GPIO.output(photoPin, 0)

def updateLayersPerPhoto(url, params):
	global layers_per_photo, total_layers
	r = requests.post(url, params)
	decoded = json.loads(r.text.lower())
	try:
		total_layers = int(decoded['response']['total_layers'])
		print str(total_layers)
		if total_layers > 0:
			layers_per_photo = math.ceil(total_layers / fps / seconds)
			print "Layers per photo: " + str(layers_per_photo)
			print "Total photos to be taken: " + str(math.floor(total_layers/layers_per_photo))
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
		if total_layers == 0:
			updateLayersPerPhoto(url, params)
		time.sleep(.5)

except KeyboardInterrupt:
	GPIO.cleanup()

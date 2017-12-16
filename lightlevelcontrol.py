#!/usr/bin/python



# Import the necessary packages
import requests
import json
import os
import numpy as np
import argparse
import cv2
from PIL import Image


# UUID and Token - enter your own here
uuid = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Change path accordingly 
tokenid = open('/home/pi/PVR/CAM/image/token.txt','r').read()

# Webcam feed - Use Google to find a good reliable feed - enter your own path to save the images
os.system("sudo wget --spider  http://eightyone.dyn-o-saur.com:22145/snap720p -O /home/pi/PVR/CAM/image/webcam.jpg")
filename = '/home/pi/PVR/CAM/image/webcam.jpg'
def average_image_color(filename):
	i = Image.open(filename)
	h = i.histogram()

	# Split into red, green, blue
	r = h[0:256]
	g = h[256:256*2]
	b = h[256*2: 256*3]

	# Perform the weighted average of each channel:
	# the *index* is the channel value, and the *value* is its weight
	return (
		sum( i*w for i, w in enumerate(r) ) / sum(r),
		sum( i*w for i, w in enumerate(g) ) / sum(g),
		sum( i*w for i, w in enumerate(b) ) / sum(b)
	)



# Variables containing the integer value of each colour channel
value = average_image_color(filename)
redchan = int(value[0])
greenchan = int(value[1])
bluechan = int(value[2])



print value

# Change values to work with your webcam feed 

if redchan in range(10,136):
	# Red
	print 'Pass RED'	
	if greenchan in range(10,136):
	# Green 
		print 'Pass GREEN'
		if bluechan in range(10,138):
		# Blue 
			print 'Pass BLUE'
			
      #Plug 1
			res = requests.get("https://eu-wap.tplinkcloud.com/?token="+tokenid)
			url = "https://eu-wap.tplinkcloud.com/?token="+tokenid
      # Set your own deviceId below
			payload = {"method" : "passthrough", "params": {"deviceId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "requestData": "{\"system\":{\"set_relay_state\":{\"state\":1}}}"}}
			result = requests.post(url, data=json.dumps(payload))
			response = result.text
			print 'Plug 1 ON'
			#Plug 2
			res = requests.get("https://eu-wap.tplinkcloud.com/?token="+tokenid)
			url = "https://eu-wap.tplinkcloud.com/?token="+tokenid
			payload = {"method" : "passthrough", "params": {"deviceId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "requestData": "{\"system\":{\"set_relay_state\":{\"state\":1}}}"}}
			result = requests.post(url, data=json.dumps(payload))
			response = result.text
			print 'Plug 2 ON'
      
			# Remove image otherwise lights will come on when run the next day
			os.remove("/home/pi/PVR/CAM/image/webcam.jpg")
      
			# If the token exipires run this command to generate new token
			if "Token expired" in response:
				res = requests.get("https://wap.tplinkcloud.com")
				url     = "https://wap.tplinkcloud.com"
				payload = {"method" : "login", "params": {"appType": "Kasa_Android", "cloudUserName": "youremailaddress@email.com", "cloudPassword": "yourpassword", "terminalUUID": uuid }}
				result = requests.post(url, data=json.dumps(payload))
				tokenresponse = result.text
				print 'Token Exipired - Renewed'
				with open('token.txt','w') as f:
					f.write(tokenresponse[92:-3])

# If the level of light is too high delete the image
else:
	print 'failed'
	os.remove("/home/pi/PVR/CAM/image/webcam.jpg")

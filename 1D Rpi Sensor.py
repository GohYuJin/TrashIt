# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 13:55:11 2017

@author: Yu Jin
"""
import RPi.GPIO as GPIO
from firebase import firebase
import time

url = 'https://f03-grp-meh.firebaseio.com/' #Put in the URL
token = 'a3u2a3mtdcGfOZOkg4J1EzGTXYJjyPlBgRP8DGef' #unique token from firebase

firebase = firebase.FirebaseApplication(url, token)

currscore = None
state = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)

while True:
    while state == 0:
        if firebase.get('/initialize') == "True":
            try:
                currscore = int(firebase.get('/current/score'))
                state = 1
            except:
                currscore = None
    
    starttime = time.time()
                
    if state == 1:
        print "app started"
        while (time.time() - starttime) < 63:
            
            if GPIO.input(25) == GPIO.HIGH:
                currscore = currscore + 1
                firebase.put('/current', '/score', str(currscore))
                time.sleep(1.5)
        
        if firebase.get('/initialize') == "False":
            state = 0
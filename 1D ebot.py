from eBot import eBot
from time import sleep
from firebase import firebase
import random

url = 'https://f03-grp-meh.firebaseio.com/' #Put in the URL
token = 'a3u2a3mtdcGfOZOkg4J1EzGTXYJjyPlBgRP8DGef' #unique token from firebase

firebase = firebase.FirebaseApplication(url, token)
e = eBot.eBot()
e.connect()
while True:
#    e.connect()
    
    initialize = False
    while initialize == False:
        check = firebase.get('/initialize') #Test if there is the gamestart command is uploaded.
        if check == 'False':
            sleep (0.5)
        else:
            initialize = True
            print 'game starting'
    
    def rightturn():
        e.wheels(0.5, -0.5)
        sleep (6)
        e.wheels(0,0)
    
    def leftturn():
        e.wheels(-0.5,0.5)
        sleep(6)
        e.wheels(0,0)
    
    n = random.randint(1,5)
    if n%2 == 0:
        rightturn()
        sleep(n)
    elif n%2 != 0:
        leftturn()
        sleep(n)
        
#    seconds = 1*60
#    while seconds>0: 
#        print 'on'
#        n = random.randint(1,5)
#        if n+6>seconds:
#            pass
#        elif n%2 == 0:
#            rightturn()
#            sleep(n)
#        elif n%2 != 0:
#            leftturn()
#            sleep(n)
#        seconds -= n+6
#    sleep(10)
#    e.disconnect()
            
        
    


    
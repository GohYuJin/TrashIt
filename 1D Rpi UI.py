# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 00:18:04 2017

@author: Yu Jin
"""

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from firebase import firebase
import time

url = 'https://f03-grp-meh.firebaseio.com/' #Put in the URL
token = 'a3u2a3mtdcGfOZOkg4J1EzGTXYJjyPlBgRP8DGef' #unique token from firebase

firebase = firebase.FirebaseApplication(url, token)

class LogIn(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout()
        layout = GridLayout(cols=2, rows =1)
        # Add your code below to add the two Buttons
        x = firebase.get('/stored')

        values = x.values()
        keys = x.keys()
        highscore = 0
        secondscore = 0
        thirdscore = 0
        for ite in range (len(values)):
            passScore = values[ite].split()
            score = int(passScore[1])
            if score >= highscore:
                highscore = score
                user1 = keys[ite]
        for ite in range (len(values)):
            passScore = values[ite].split()
            score = int(passScore[1])
            if score <= highscore and score >= secondscore and keys[ite]!=user1:
                secondscore = score
                user2 = keys[ite]
        for ite in range (len(values)):
            passScore = values[ite].split()
            score = int(passScore[1])
            if score <= secondscore and score >= thirdscore and keys[ite]!=user2:
                thirdscore = score
                user3 = keys[ite]
        self.HighscoreUsers ="Username"+ "\n\n" + "%s"%user1 + "\n" + "%s"%user2 + "\n" +"%s"%user3
        self.Highscore = "Score" + "\n\n" + "%s"%highscore + "\n" + "%s"%secondscore + "\n" +"%s"%thirdscore
        self.passkey = ""
        self.prevcount = 0
        
        
        self.button1 = Button(text = "Log In", on_press = self.change_to_invest)
        self.UserID = TextInput(text = "")
        layout.add_widget(Label(text="User ID: "))
        layout.add_widget(self.UserID)
        
        self.layout2=BoxLayout()
        layout2 = GridLayout(cols=2, rows =1)
        self.Password = TextInput(text = "" )
        self.Password.bind(text = self.on_text)
        layout2.add_widget(Label(text="Password"))
        layout2.add_widget(self.Password)
        
        self.layout3 = BoxLayout()
        layout3 = GridLayout(cols=1, rows =4)
        layout3.add_widget(layout)
        layout3.add_widget(layout2)
        self.Check = Label(text = "")
        layout3.add_widget(self.Check)
        layout3.add_widget(self.button1)
        
        self.layout4=BoxLayout()
        layout4 = GridLayout(cols=2, rows =1)
        self.highscoreusers = Label(text= self.HighscoreUsers, font_size = 24, halign='left',valign='middle')
        layout4.add_widget(self.highscoreusers)
        self.highscore = Label(text= self.Highscore, font_size = 24, halign='center',valign='middle')
        layout4.add_widget(self.highscore)
        
        self.layout6= BoxLayout()
        layout6 = GridLayout(cols =1, rows =2)
        img = Image(source = 'TRASHIT.png')
        layout6.add_widget(img)
        layout6.add_widget(layout4)
        
        self.layout5=BoxLayout()
        layout5 = GridLayout(cols=2, rows =1)
        layout5.add_widget(layout6)
        layout5.add_widget(layout3)
        
        self.add_widget(layout5)

        
    def on_enter(self):
        #extracts new highscore
        x = firebase.get('/stored')

        values = x.values()
        keys = x.keys()
        highscore = 0
        secondscore = 0
        thirdscore = 0
        for ite in range (len(values)):
            passScore = values[ite].split()
            score = int(passScore[1])
            if score >= highscore:
                highscore = score
                user1 = keys[ite]
        for ite in range (len(values)):
            passScore = values[ite].split()
            score = int(passScore[1])
            if score <= highscore and score >= secondscore and keys[ite]!=user1:
                secondscore = score
                user2 = keys[ite]
        for ite in range (len(values)):
            passScore = values[ite].split()
            score = int(passScore[1])
            if score <= secondscore and score >= thirdscore and keys[ite]!=user2:
                thirdscore = score
                user3 = keys[ite]
        self.HighscoreUsers ="Username"+ "\n\n" + "%s"%user1 + "\n" + "%s"%user2 + "\n" +"%s"%user3
        self.Highscore = "Score" + "\n\n" + "%s"%highscore + "\n" + "%s"%secondscore + "\n" +"%s"%thirdscore
        self.highscoreusers.text = self.HighscoreUsers
        self.highscore.text = self.Highscore
        self.UserID.text = ""
        self.Password.text = ""
        self.Check.text = ""
        
    def change_to_invest(self, value):
        user = self.UserID.text
        password = self.passkey
        check = firebase.get('/stored/%s'%user)
        
        if check == None:
            found = 2 #new user
            print ('new user')
        else:
            x = check.split()
            if x[0] == password:
                found = 0 #played before
                print ('played before')
            else:
                found = 1 #wrong password
                print ('wrong password')
        
        if found == 0:
            #upload current user data
            self.score = int(x[1])
            self.manager.transition.direction = 'left'
            self.manager.current= 'StartGame'
            firebase.put('/current', '/userID', user)
            firebase.put('/current', '/password', password)
            firebase.put('/current', '/score', str(self.score))
            
        elif found == 1:
            self.Check.text = "Invalid Password"
            
        else:
            #upload new user data
            self.score = 0
            firebase.put('/stored', '/%s'%user, password + ' 0') #uploading new data
            self.manager.transition.direction = 'left'
            self.manager.current= 'StartGame'
            firebase.put('/current', '/userID', user)
            firebase.put('/current', '/password', password)
            firebase.put('/current', '/score', str(self.score))
#        
    def on_text(self, value, value2):
        count = len(self.Password.text)
        if count > self.prevcount:
            self.passkey = self.passkey + self.Password.text.strip('*')
            self.Password.text = len(self.passkey)* '*'
        elif count < self.prevcount:
            self.passkey = self.passkey[0:(len(self.passkey)-1)]
            self.Password.text = len(self.passkey)* '*'
        print (self.passkey)
        self.prevcount = len(self.Password.text)
        

class StartGame(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout()
        img = Image(source = 'Start.png')
        self.startbutton = Button(text = "Start Game", on_press = self.change_to_countdown , pos_hint={'x': .25, 'center_y': .5},size_hint=(0.5, 0.1))
        self.add_widget(img)
        self.add_widget(self.startbutton)
        
    def change_to_countdown(self, value):
        self.manager.transition.direction = 'left'
        firebase.put('/', 'initialize', 'True')
        # modify the current screen to a different "name"
        self.manager.current= 'countdown'


class Countdown(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        #change here
        self.label = Label(text = "60", font_size=200)
        self.quit = Button(text = "Quit Game", pos_hint={'x': 0.8, 'center_y': 0.05},size_hint=(0.2, 0.1) ,on_press = self.quit_app)
        x = firebase.get('/current')
        if x == None:
            self.currscore = 0
            
        else:
            self.currscore = int(firebase.get('/current/score'))
            
        self.score = Label(text = "Score: %d"%self.currscore, pos_hint={'x': 0, 'center_y': 0.8},font_size = 36)
        img = Image(source='timer screen-01.png')
        self.add_widget (img)
        self.add_widget(self.label)
        self.add_widget(self.quit)
        self.add_widget(self.score)
        
    def quit_app(self, value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'endgame'
        firebase.put('/','initialize','False')
    
    def on_enter(self):
        self.score.text = '0'
        self.start_time = time.time()
        t = 1.0
        self.event = Clock.schedule_interval(self.update, t)
        Clock.schedule_once(self.change_to_endgame, 60.3) #change here
        
    def change_to_endgame(self,value):
        #update firebase final score here
        self.manager.transition.direction = 'left'
        self.manager.current= 'endgame'
        self.event.cancel()
        firebase.put('/','initialize','False')
        
        
    
    def update(self, dt):
        self.label.text = str(int(self.start_time + 60 - time.time()))   
        
        currscore = firebase.get('/current/score')
        if currscore == None:
            currscore = 0
            
        else:
            currscore = int(currscore) #insert firebase curr score here
            
            if currscore < 10:
                self.score.text = "Score :0" + str(currscore)
            else:
                self.score.text = "Score :" + str(currscore)
        
class EndGame(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout()
        self.currscore = firebase.get('/current/score')
        
        self.label = Label(text = "Your Score Is:", font_size=50, pos_hint={'x': 0, 'center_y': 0.75})
        self.score = Label(text = str(self.currscore), font_size=200, pos_hint={'x': 0, 'center_y': 0.5})
        img = Image(source = 'scoring screen-01.png')
        
        self.endbutton = Button(text = "Save and back to Login", pos_hint={'x': 0.8, 'center_y': 0.05},size_hint=(0.2, 0.1) ,on_press = self.change_to_login)
        self.add_widget(img)
        self.add_widget(self.endbutton)
        self.add_widget(self.label)
        self.add_widget(self.score)
        
        
    def on_enter(self):
        # extract current username
        # add current username and score to dictionary
        self.score.text = '--'
        x = firebase.get('/current')
        if x == None:
            self.score.text = '--'
        else:
            userID = firebase.get('/current/userID')
            password = firebase.get('/current/password')
            score = firebase.get('/current/score')
            firebase.put('/stored', '/%s'%userID, password + ' ' + score)
            self.score.text = score
        

    def change_to_login(self,value):
        self.manager.transition.direction = 'right'
        firebase.put('/', 'current', None)
        # modify the current screen to a different "name"
        self.manager.current= 'login'
        
        
class TrashItApp(App):
    def build(self):
        sm=ScreenManager()
        lg=LogIn(name='login')
        cd=Countdown(name='countdown')
        sg=StartGame(name='StartGame')
        eg=EndGame(name='endgame')
        sm.add_widget(eg)
        sm.add_widget(lg)
        sm.add_widget(sg)
        sm.add_widget(cd)
        sm.current='login'
        return sm


if __name__=='__main__':
	TrashItApp().run()

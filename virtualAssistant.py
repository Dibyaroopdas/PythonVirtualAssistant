import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from googlesearch import *
import requests
import json
import pyjokes
import json
import pyowm  


BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)                                                
def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if(hour>=4 and hour <12):
        speak("Good Morning!")
    elif (hour>=12 and hour <18):
        speak("Good Afternoon!")
    else:
        speak('Good Evening!')
    speak("I am your Personal Assistant! Please tell me what can I help you with ?")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1 
        audio=r.adjust_for_ambient_noise(source)
        audio=r.listen(source,10)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')                        
        print(f"You said :  {query}\n")
        
    except sr.WaitTimeoutError:
        speak("Couldn't hear you. Did you say anything?")
        
        
    except Exception as e:
        print("Didn't get that! Please Repeat")
        return "None"
    return query

def googleSearch(query):
    chrome_path = r'C:\\Program Files (x86)\\Google\\Chrome\\Application %s'
    for url in search(query, tld="co.in", num=1, stop = 1, pause = 2):
        webbrowser.open("https://google.com/search?q=%s" % query)


def takeNotes():
    while(True):
        speak("Please dictate your notes")
        notes=takeCommand()
        with open("notes.txt","a+") as f:
            f.writelines(notes)
        speak("Do you want to add anything else ? ")
        choice=takeCommand().lower()
        if "no" in choice or 'exit' in choice:
            speak("notes saved..")
            break


    
def readNotes():
    with open("notes.txt","r") as f:
       notes=f.read() 
    speak(notes)



def readNews():
    count = 0
    speak("Today's Headlines.:")
    url="http://newsapi.org/v2/top-headlines?country=in&apiKey=6b972898fccb4aa5abf380e110e44127"    
    news=requests.get(url).text
    news_json=json.loads(news)
    articles=news_json.get('articles')
    for article in articles:
        speak(article.get("title"))
        count = count + 1
        if count == 10:
            return
        

def getLocation():
    send_url = "http://api.ipstack.com/check?access_key=56304e0b9167548627ee9f0a72b858fb"
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    city = geo_json['city']    
    region = geo_json['region_name']
    country = geo_json['country_name']
    speak("Your current location is " + city +","+ region+","+country)

def getWeather():
    send_url = "http://api.ipstack.com/check?access_key=56304e0b9167548627ee9f0a72b858fb"
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    city = geo_json['city']    
    region = geo_json['region_name']
    owm =pyowm.OWM('c31ac708d107fc2df2a90219b9725f0f')
    mgr = owm.weather_manager()
    place = region
    obv = mgr.weather_at_place(place)
    w = obv.weather
    tempa = w.temperature('celsius')
    speak("The current temperature of " + city +" " + region +  f" is {tempa['temp']}" + "degree celsius")


def randomJokes():
    joke = pyjokes.get_joke(language="en", category="all") 
    return joke 

def continueSearch():
    speak("Do you want me to do anything more")
    newquery = takeCommand().lower()
    if 'yes' in newquery:
        speak("Please tell me, I am listening")
        return 1
    if 'no' in newquery:
        speak("Thank you, have a nice day")
        return -1

print("speak.....")
query = takeCommand().lower()
if 'assistant' in query:
    boolquery = True
    wishMe()
else:
    boolquery = False

while boolquery:
    query=takeCommand().lower()
            
    if 'who is' in query:
        speak("Searching wikipedia......")
        query=query.replace("who is"," ")
        results=wikipedia.summary(query,sentences=3)
        speak("According to Wikipedia...")
        speak(results)
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False


    elif "open youtube" in query:
        speak("opening youtube")
        chrome_path = r'C:\\Program Files (x86)\\Google\\Chrome\\Application %s'
        webbrowser.open("youtube.com")
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False
            
            

    elif "open google" in query:
        speak("opening google")
        chrome_path = r'C:\\Program Files (x86)\\Google\\Chrome\\Application %s'
        webbrowser.open("google.com")
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False       

    elif "joke" in query:
        Loljoke = randomJokes()
        speak(Loljoke)
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False
         

    elif "time" in query:
        strTime=datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False
            
    elif "take notes" in query:
        takeNotes()
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False


    elif "read" in query and "notes" in query:
        readNotes()
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False
               
            
    elif "news" in query:
        readNews()
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False

    elif "temperature" in query:
        getWeather()
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False
        
    elif "current location" in query:
        getLocation()
        i = continueSearch()
        if i == 1:
            boolquery = True
        else:
            boolquery = False
            
    else:
        speak("Searching wikipedia......")
        results=wikipedia.summary(query,sentences=3)
        speak("According to Wikipedia...")
        speak(results)
        speak("Do you want to make a google search")
        newquery = takeCommand().lower()
        if 'yes' in newquery:
            googleSearch(query)
            i = continueSearch()
            if i == 1:
                boolquery = True
            else:
                boolquery = False
        if 'no' in newquery:
            i = continueSearch()
            if i == 1:
                boolquery = True
            else:
                boolquery = False
                    
            

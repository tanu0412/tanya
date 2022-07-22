import pyttsx3
import speech_recognition as sr
import datetime
import os
import sys
import requests
import re
import webbrowser
import smtplib
#import subprocess
from pyowm import OWM
import youtube_dl
#import vlc
import urllib
#import urllib2
from bs4 import BeautifulSoup as soup
#from urllib2 import urlopen
from urllib.request import urlopen
import wikipedia
from time import strftime
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        print("Good Morning!")
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        print("Good Afternoon!")
        speak("Good Afternoon!")

    else:
        print("Good Evening!")
        speak("Good Evening!")
    
    print(" Please tell me how may I help you")
    speak(" Please tell me how may I help you")


def myCmd():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        cmd = r.recognize_google(audio).lower()
        print('You said: ' + cmd + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        cmd = myCmd();
    return cmd

def assistant(cmd):
    "if statements for executing commands"

    #open subreddit Reddit
    if 'open reddit' in cmd:
        reg_ex = re.search('open reddit (.*)', cmd)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        print('The Reddit content has been opened for you Sir.')
        speak('The Reddit content has been opened for you Sir.')

    elif 'shutdown' in cmd or 'exit' in cmd or 'stop' in cmd:
        print('Bye Sir. Have a nice day')
        speak('Bye Sir. Have a nice day')
        sys.exit()

    #open website
    elif 'open' in cmd:
        reg_ex = re.search('open (.+)', cmd)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain + '.com'
            webbrowser.open(url)
            print('The website you have requested has been opened for you Sir.')
            speak('The website you have requested has been opened for you Sir.')
        else:
            pass

    #greetings
    elif 'hello' in cmd:
        day_time = int(strftime('%H'))
        if day_time < 12:
            speak('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            speak('Hello Sir. Good afternoon')
        else:
            speak('Hello Sir. Good evening')

    elif 'help' in cmd:
        print("""
        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Tell a joke/another joke : Says a random dad joke.
        5. Current weather in {cityname} : Tells you the current condition and temperture
        7. Greetings
        8. play me a video : Plays song in your VLC media player
        9. change wallpaper : Change desktop wallpaper
        10. news for today : reads top news of today
        11. time : Current system time
        12. top stories from google news (RSS feeds)
        13. tell me about xyz : tells you about xyz
        """)
        speak("You can use these commands and I'll help you out:")
        
    #top stories from google news
    elif 'news for today' in cmd:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:15]:
                print(news.title.text.encode('utf-8'))
                speak(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)

    #current weather
    elif "weather" in cmd:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name=myCmd()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print('Temperature in kelvin unit :', str(current_temperature))
                speak('Temperature is :' + str(current_temperature))
                print('humidity :', str(current_humidiy) + '%')
                speak('humidity is ' + str(current_humidiy))
                print('description :', str(weather_description))
                speak('description  ' + str(weather_description))
    #time
    elif 'time' in cmd:
        import datetime
        now = datetime.datetime.now()
        print("%d:%d"%(now.hour, now.minute))
        speak('Current time is %d hours %d minutes' % (now.hour, now.minute))

    #send email
    elif 'email' in cmd:
        speak('Who is the recipient?')
        recipient = myCmd()
        if 'david' in recipient:
            speak('What should I say to him?')
            content = myCmd()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('xyz@gmail.com', '*************')
            mail.sendmail('abc.com', 'amdp.hauhan@gmail.com', content)
            mail.close()
            speak('Email has been sent successfuly. You can check your inbox.')
        else:
            speak('I don\'t know what you mean!')
            
    #play youtube song
    elif 'play me a song' in cmd:
        path = '/Users/hp2/Videos'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        speak('What song shall I play Sir?')
        mysong = myCmd()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urllib2.urlopen(url)
            html = response.read()
            soup1 = soup(html,"lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)

            url = url_list[0]
            ydl_opts = {}

            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            vlc.play(path)

            if flag == 0:
                speak('I have not found anything in Youtube ')

    #ask me anything
    if 'tell me about' in cmd or 'wikipedia' in cmd:
        lst = ['tell','me','about']
        lst1 = cmd.split()
        for i in lst1:
            if i not in lst:
                cmd = i
        print(cmd)
        speak('Searching Wikipedia...')
        results = wikipedia.summary(cmd, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
wishMe()
speak('I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')

#loop to continue executing multiple commands
while True:
    assistant(myCmd())
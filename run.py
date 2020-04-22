from controller import *
from selenium import webdriver
import time
import webbrowser
import re
import os
from selenium.webdriver.common.keys import Keys
import sys
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import urllib
import urllib.request as urllib2
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import random
from time import strftime
import vlc

cache = set()


def browserResponse(audio):
    browserAssistantResponse(audio)


def assistant(command):
    global cache
    # if statements for executing commands
    # browserResponse('Processing')
    # def beep(x): return os.system("echo -n '\a';sleep 0.2;" * x)
    beepy.beep(sound=3)
    if 'facebook' in command and 'open' not in command and 'login' not in command:
        browserResponse('Do you want me to login or open the facebook webpage')
        cache.add('facebook')
    elif 'open' in command:
        if('facebook' in cache):
            openWebpage('facebook')
            cache.discard('facebook')
        elif 'facebook' in command:
            openWebpage('facebook')
        elif 'twitter' in command:
            openWebpage('twitter')
        elif 'google' in command:
            openWebpage('google')
        elif 'browser' in command:
            openChrome()
        else:
            browserResponse('What you want me to open')
    elif 'window' in command:
        if 'first' in command:
            switchTab('forward', 'first')
        if 'last' in command:
            switchTab('forward', 'last')
    elif 'forward' in command:
        switchTab('backward', 'ignore')
    elif 'backward' in command:
        switchTab('backward', 'ignore')
    elif 'shutdown' in command:
        browserResponse('Bye bye Sir. Have a nice day')
        sys.exit()
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            browserResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            browserResponse('Hello Sir. Good afternoon')
        else:
            browserResponse('Hello Sir. Good evening')
    elif 'scroll' in command and 'up' in command:
        scrollBrowser('up')
    elif 'scroll' in command and 'down' in command:
        scrollBrowser('down')
    elif 'help me' in command or 'do' in command:
        browserResponse(
            'You can use these commands and I will help you out: 1. Open xyz.com : replace xyz with facebook, twitter or google website name 2. Ask for Weather in any city, time, joke. 3. Login facebook 4.Read me news 4. Switch tabs say command First window, last window, forward and backward 5. Close and open browser 6. Maximize and Minimize browser 7. Scroll web page 8. Search content by saying search')
    # maximize and minimize windows
    elif 'maximize' in command:
        maximize()
    elif 'minimize' in command:
        minimize()
    # joke
    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"})
        if res.status_code == requests.codes['ok']:
            browserResponse(str(res.json()['joke']))
        else:
            browserResponse('oops!I ran out of jokes')
    elif 'read news' in command:
        newsRead()
    elif 'search' in command:
        search()

    elif 'login' in command:
        print(cache)
        if('facebook' in cache):
            loginFacebook()
            cache.discard('facebook')
        elif 'facebook' in command:
            loginFacebook()
    # current weather
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            browserResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (
                city, k, x['temp_max'], x['temp_min']))
    elif 'close' in command:
        if 'window' in command:
            close('window')
        elif 'browser' in command:
            close('browser')

        # time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        browserResponse('Current time is %d hours %d minutes' %
                        (now.hour, now.minute))

    # play youtube song
    # elif 'play me a song' in command:
    #     browserResponse('What song shall I play Sir?')
    #     mysong = myCommand()
    #     if mysong:
    #         flag = 0
    #         url = "https://www.youtube.com/results?search_query=" + \
    #             mysong.replace(' ', '+')
    #         response = urllib2.urlopen(url)
    #         html = response.read()
    #         soup1 = soup(html, "lxml")
    #         url_list = []
    #         for vid in soup1.findAll(attrs={'class': 'yt-uix-tile-link'}):
    #             if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
    #                 flag = 1
    #                 final_url = 'https://www.youtube.com' + vid['href']
    #                 url_list.append(final_url)
    #                 url = url_list[0]
    #         ydl_opts = {}
    #         # os.chdir(path)
    #         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #             ydl.download([url])
    elif 'download songs' in command:
        path = '/Users/akshaysehgal/pythonprojects/videos'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        browserResponse('What song shall I download Sir?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + \
                mysong.replace(' ', '+')
            response = urllib2.urlopen(url)
            html = response.read()
            soup1 = soup(html, "lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class': 'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
                    print(url_list)
                    url = url_list[0]
                    print(url)
            ydl_opts = {}
            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            media = vlc.MediaPlayer(path)
            media.play()
            # p = vlc.MediaPlayer(path)
            # p.play()
            if flag == 0:
                browserResponse('I have not found anything in Youtube ')

        if flag == 0:
            browserResponse(
                'I have not found anything in Youtube ')
    elif len(command) != 0:
        ErrorPrompt()


initalPrompt()
while True:
    assistant(myCommand())

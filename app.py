import speech_recognition as sr
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
import wikipedia
import random
from time import strftime


def openChrome():
    global tabFlag
    tabFlag = False
    global browser
    browser = webdriver.Chrome()
    print(browser)


def switchTabForward(direction, flag):
    global browser
    if flag == 'ignore':
        if direction == 'forward':
            browser.switch_to_window(browser.window_handles[browser.window_handles.index(
                browser.current_window_handle)+1])
        if direction == 'backward':
            browser.switch_to_window(browser.window_handles[browser.window_handles.index(
                browser.current_window_handle)-1])
    if flag == 'first':
        browser.switch_to_window(browser.window_handles[0])
    if flag == 'last':
        browser.switch_to_window(browser.window_handles[-1])
    # print(browser.current_window_handle)
    # print(browser.window_handles.index(browser.current_window_handle))


def openWebpage(name):
    global browser
    global tabFlag
    if name == 'facebook':
        if tabFlag:
            browser.execute_script(
                '''window.open("https://www.facebook.com","_blank");''')
        else:
            browser.get('https://www.facebook.com')
            tabFlag = True
        time.sleep(2)
        sofiaResponse('The requested website has been opened.')

    if name == 'twitter':
        if tabFlag:
            browser.execute_script(
                '''window.open("https://www.twitter.com","_blank");''')
        else:
            browser.get('https://www.twitter.com')
            tabFlag = True
        time.sleep(2)
        sofiaResponse('The requested website has been opened.')

    if name == 'google':
        if tabFlag:
            browser.execute_script(
                '''window.open("https://www.google.com","_blank");''')
        else:
            browser.get('https://www.google.com')
            tabFlag = True
        time.sleep(2)
        sofiaResponse('The requested website has been opened.')


def maximize():
    global browser
    browser.maximize_window()


def minimize():
    browser.minimize_window()


def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command


def sofiaResponse(audio):
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

# web Scrapping


def newsRead():
    global browser
    browser.get('https://news.google.com/?hl=en-US&gl=US&ceid=US:en')
    elem = browser.find_elements_by_xpath('//*[@class="DY5T1d"]')
    i = 0
    li = []
    sofiaResponse('Top five news for today are')
    for x in elem:
        i = i + 1
        li.append(x.text + ' ')
        sofiaResponse(x.text)
        if i == 5:
            break


def assistant(command):
    global browser
    "if statements for executing commands"
    if 'open' in command:
        if command == 'open':
            sofiaResponse('What you want me to open.')
        else:
            if 'facebook' in command:
                openWebpage('facebook')
            if 'twitter' in command:
                openWebpage('twitter')
            if 'google' in command:
                openWebpage('google')
            if 'browser' in command:
                openChrome()
    elif 'window' in command:
        if 'first' in command:
            switchTabForward('forward', 'first')
        if 'last' in command:
            switchTabForward('forward', 'last')
    elif 'forward' in command:
        switchTabForward('backward', 'ignore')
    elif 'backward' in command:
        switchTabForward('backward', 'ignore')
    elif 'shutdown' in command:
        sofiaResponse('Bye bye Sir. Have a nice day')
        sys.exit()
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sofiaResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            sofiaResponse('Hello Sir. Good afternoon')
        else:
            sofiaResponse('Hello Sir. Good evening')
    elif 'help me' in command:
        sofiaResponse("""
        You can use these commands and I'll help you out:
        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Current weather in {cityname} : Tells you the current condition and temperture
        5. Hello
        6. play me a video : Plays song in your VLC media player
        7. change wallpaper : Change desktop wallpaper
        8. news for today : reads top news of today
        9. time : Current system time
        10. top stories from google news (RSS feeds)
        11. tell me about xyz : tells you about xyz
        """)
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
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse('oops!I ran out of jokes')
    elif 'read me google news' in command:
        newsRead()
    # top stories from google news
    elif 'news for today' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            for news in news_list[:15]:
                sofiaResponse(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)
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
            sofiaResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (
                city, k, x['temp_max'], x['temp_min']))
    elif 'close browser' in command:
        global browser
        browser.quit()
        # time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes' %
                      (now.hour, now.minute))
        # reg_ex = re.search('open reddit (.*)', command)
        # url = 'https://www.reddit.com/'
        # if reg_ex:
        #     subreddit = reg_ex.group(1)
        #     url = url + 'r/' + subreddit
        # webbrowser.open(url)
        # sofiaResponse('The Reddit content has been opened for you Sir.')
    # play youtube song
    elif 'play me a song' in command:
        # path = '/Users/nageshsinghchauhan/Documents/videos/'
        # folder = path
        # for the_file in os.listdir(folder):
        #     file_path = os.path.join(folder, the_file)
        #     try:
        #         if os.path.isfile(file_path):
        #             os.unlink(file_path)
        #     except Exception as e:
        #         print(e)
        sofiaResponse('What song shall I play Sir?')
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
                    url = url_list[0]
                    ydl_opts = {}
                    os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        if flag == 0:
            sofiaResponse('I have not found anything in Youtube ')


while True:
    assistant(myCommand())

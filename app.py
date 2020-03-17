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
import certifi


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


def browserNotOpen():
    sofiaResponse(
        'Please open the browser. Use command open browser to open chrome browser')


def initalPrompt():
    sofiaResponse('Welcome to browser Assistant. How can I help you?')


def ErrorPrompt():
    sofiaResponse('I didn’t understand. I can help you with opening and closing of websites, switch tabs, read news for you, tell you about weather, time and jokes, login into facebook and more. Please refer to the set of commands to perform tasks.')


def scrollBrowser():
    global browser
    browser.execute_script("window.scrollBy(0,1000)")
    # browserNotOpen()


def search():
    global browser
    global tabFlag
    openChrome()
    if tabFlag:
        browser.execute_script(
            '''window.open("https://www.google.com","_blank");''')
    else:
        browser.get('https://www.google.com')
        tabFlag = True
    elem = browser.find_element_by_name('q')
    elem.clear()
    sofiaResponse('what you want me to search')
    entity = myCommand()
    elem.send_keys(entity)
    button = browser.find_element_by_name('btnK')
    button.submit()


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


def ErrorResponse():
    sofiaResponse(
        'I did not understand that. I can help you with time, opening and closing of browser and')


def loginFacebook():
    global browser
    global tabFlag
    if tabFlag:
        browser.execute_script(
            '''window.open("https://www.facebook.com","_blank");''')
    else:
        browser.get('https://www.facebook.com')
        tabFlag = True
    username = browser.find_element_by_id(
        'email')
    username.clear()
    username.send_keys("shivamagarwal2996@gmail.com")
    pwd = browser.find_element_by_id('pass')
    pwd.clear()
    pwd.send_keys("alpha123")
    login = browser.find_element_by_id('u_0_2')
    login.click()


def close(value):
    global browser
    if value == 'browser':
        browser.quit()
    if value == 'window':
        browser.switch_to_window(browser.window_handles[browser.window_handles.index(
            browser.current_window_handle)])
        browser.close()


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
        sofiaResponse(
            'You can use these commands and I will help you out: 1. Open reddit subreddit : Opens the subreddit in default browser. 2. Open xyz.com : replace xyz with any website name 3. Send email/email : Follow up questions such as recipient name, content will be asked in order. 4. Current weather in {cityname} : Tells you the current condition and temperture. 5. time : Current system time')
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
    elif 'read me news' in command:
        newsRead()
    elif 'search' in command:
        search()
    # top stories from google news
    # elif 'news for today' in command:
    #     try:
    #         news_url = "https://news.google.com/news/rss"
    #         # Client = urlopen(news_url)
    #         Client = urllib2.urlopen(news_url, cafile=certifi.where())
    #         xml_page = Client.read()
    #         Client.close()
    #         soup_page = soup(xml_page, "lxml")
    #         news_list = soup_page.findAll("item")
    #         for news in news_list[:15]:
    #             sofiaResponse(news.title.text.encode('utf-8'))
    #     except Exception as e:
    #         print(e)
    elif 'login facebook' in command:
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
            sofiaResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (
                city, k, x['temp_max'], x['temp_min']))
    elif 'scroll' in command:
        scrollBrowser()
    elif 'close' in command:
        if 'window' in command:
            close('window')
        elif 'browser' in command:
            close('browser')

        # time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes' %
                      (now.hour, now.minute))

    # play youtube song
    elif 'play me a song' in command:
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
                    # os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        if flag == 0:
            sofiaResponse('I have not found anything in Youtube ')
    elif len(command) != 0:
        ErrorPrompt()


tabFlag = False
initalPrompt()
while True:
    assistant(myCommand())

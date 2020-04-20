import time
from responses import *
from selenium import webdriver
import speech_recognition as sr

tabFlag = False
browserFlag = False


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


def maximize():
    global browser
    global browserFlag
    if browserFlag:
        browser.maximize_window()
    else:
        browserAssistantResponse('I am sorry, but the browser is not open')


def minimize():
    global browser
    global browserFlag
    if browserFlag:
        browser.minimize_window()
    else:
        browserAssistantResponse('I am sorry, but the browser is not open')


def search():
    global browser
    global tabFlag
    global browserFlag
    if browserFlag:
        if tabFlag:
            # tabflag
            browser.execute_script(
                '''window.open("https://www.google.com","_blank");''')
        else:
            browser.get('https://www.google.com')
            tabFlag = True
    else:
        openChrome()
        browser.get('https://www.google.com')
        tabFlag = True
    elem = browser.find_element_by_name('q')
    elem.clear()
    browserAssistantResponse('what you want me to search')
    entity = myCommand()
    elem.send_keys(entity)
    button = browser.find_element_by_name('q')
    button.submit()


def openWebpage(name):
    global browser
    global tabFlag
    global browserFlag
    if browserFlag:
        if name == 'facebook':
            if tabFlag:
                browser.execute_script(
                    '''window.open("https://www.facebook.com","_blank");''')
            else:
                browser.get('https://www.facebook.com')
                tabFlag = True
            time.sleep(2)
            browserAssistantResponse(
                'The requested website has been opened.')

        if name == 'twitter':
            if tabFlag:
                browser.execute_script(
                    '''window.open("https://www.twitter.com","_blank");''')
            else:
                browser.get('https://www.twitter.com')
                tabFlag = True
            time.sleep(2)
            browserAssistantResponse(
                'The requested website has been opened.')

        if name == 'google':
            if tabFlag:
                browser.execute_script(
                    '''window.open("https://www.google.com","_blank");''')
            else:
                browser.get('https://www.google.com')
                tabFlag = True
            time.sleep(2)
            browserAssistantResponse(
                'The requested website has been opened.')
    else:
        openChrome()
        openWebpage(name)


def newsRead():
    global browser
    global browserFlag
    global tabFlag
    if browserFlag:
        if tabFlag:
            browser.execute_script(
                '''window.open("https://news.google.com/?hl=en-US&tab=wn1&gl=US&ceid=US:en","_blank");''')
            time.sleep(10)
        else:
            browser.get(
                'https://news.google.com/?hl=en-US&tab=wn1&gl=US&ceid=US:en')
            tabFlag = True
        elem = browser.find_elements_by_xpath('//*[@class="DY5T1d"]')
        i = 0
        li = []
        browserAssistantResponse('Top five news for today are')
        for x in elem:
            i = i + 1
            li.append(x.text + ' ')
            browserAssistantResponse(x.text)
            if i == 5:
                break
    else:
        # browserAssistantResponse(
        #     'Please say open browser command to open browser and then read news')
        openChrome()
        newsRead()


def close(value):
    global browser
    global tabFlag
    global browserFlag
    if value == 'browser':
        browser.quit()
        tabFlag = False
        browserFlag = False
    if value == 'window':
        # browser.switch_to_window(browser.window_handles[browser.window_handles.index(
        #     browser.current_window_handle)])
        browser.close()


def loginFacebook():
    global browser
    global tabFlag
    global browserFlag
    if browserFlag:
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
        login = browser.find_element_by_id('u_0_b')
        time.sleep(1)
        login.click()
        browserAssistantResponse('Login Successful')
    else:
        openChrome()
        loginFacebook()


def scrollBrowser():
    global browser
    global browserFlag
    if browserFlag:
        browser.execute_script("window.scrollBy(0,1000)")
    else:
        browserNotOpen()
    # browserNotOpen()


def switchTabForward(direction, flag):
    global browser
    if browserFlag:
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
    else:
        browserNotOpen()


def openChrome():
    global browserFlag
    global tabFlag
    browserFlag = True
    tabFlag = False
    global browser
    browser = webdriver.Chrome()
    print(browser)

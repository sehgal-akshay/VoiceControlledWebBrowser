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
            updateParent()
        else:
            browser.get('https://www.google.com')
            tabFlag = True
            setParent()
    else:
        openChrome()
        browser.get('https://www.google.com')
        setParent()
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
            updateParent()
        else:
            browser.get(
                'https://news.google.com/?hl=en-US&tab=wn1&gl=US&ceid=US:en')
            tabFlag = True
            setParent()
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
    global parent
    if value == 'browser':
        browser.quit()
        tabFlag = False
        browserFlag = False
        parent = None
    if value == 'window':
        if browser:
            length = len(browser.window_handles)
            if(length > 1):
                browser.close()
                updateParent()
            else:
                browser.quit()
                tabFlag = False
                browserFlag = False
                parent = None


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


def scrollBrowser(flag):
    global browser
    global browserFlag
    if browserFlag:
        if flag == 'down':
            browser.execute_script("window.scrollBy(0,1000)")
        elif flag == 'up':
            browser.execute_script("window.scrollBy(0,-1000)")
    else:
        browserNotOpen()
    # browserNotOpen()


def switchTab():
    global browser
    global browserFlag
    if browserFlag:
        updateParent()
    else:
        browserNotOpen()


def setParent():
    global parent
    global browser
    print('set parent')
    parent = browser.window_handles[0]
    print(parent)


def updateParent():
    global parent
    # global child
    global browser
    if parent:
        print(parent)
        for entity in browser.window_handles:
            if entity != parent:
                print('here')
                browser.switch_to_window(entity)
                browser.switch_to.window(entity)
                parent = entity
                break
            print(entity)
    print(parent)


def openChrome():
    global browserFlag
    global tabFlag
    browserFlag = True
    tabFlag = False
    global browser
    browser = webdriver.Chrome()
    print(browser)

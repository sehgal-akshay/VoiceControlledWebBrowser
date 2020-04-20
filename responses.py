import os
import beepy


def browserAssistantResponse(audio):
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)


def ErrorPrompt():
    beepy.beep(sound=3)
    browserAssistantResponse(
        'I didn’t understand. Say help me to know more.')


def initalPrompt():
    browserAssistantResponse(
        'Welcome to browser Assistant. How can I help you?')


def browserNotOpen():
    browserAssistantResponse(
        'Please open the browser. Use command open browser to open chrome browser')

import logging

from random import randint
import pygame

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from playsound import playsound

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():
    pygame.mixer.init()
    pygame.mixer.music.load("haha2.mp3")
    pygame.mixer.music.play()
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("ChooseIntent", convert={'first': int})
def ask_choose(first):
    session.attributes['first'] = first
    ask = render_template('ask')
    return question(ask)


@ask.intent("StopIntent")
def stop():
    pygame.mixer.music.stop()
    return question('')


@ask.intent("AgainIntent")
def again():
    pygame.mixer.music.load("britney.mp3")
    pygame.mixer.music.play()
    return question('')


@ask.intent("AMAZON.YesIntent")
def yes_ans():
    first = session.attributes['first']
    if first % 3 == 0:
        msg = render_template('win')
    else:
        msg = render_template('lose')

    return statement(msg)


@ask.intent("AMAZON.NoIntent")
def no_ans():
    first = session.attributes['first']
    if first % 3 != 0:
        msg = render_template('win')
    else:
        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)

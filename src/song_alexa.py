import logging

from random import randint
import pygame

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from playsound import playsound
from lyrics import read_songs

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def init():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("LoveIntent")
def love(line):
    return question('I love you too babe')


@ask.intent("MatchIntent", convert={'first': str})
def match(first):
    next_line, artist_song = read_songs()
    return question(artist_song[first])


if __name__ == '__main__':
    app.run(debug=True)

import logging

from random import randint
import pygame

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from playsound import playsound
from lyrics import read_songs
from nltk.metrics import edit_distance

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

    query = first.lower()
    q = min(artist_song.keys(), key=lambda x: edit_distance(x, query))
    dist = edit_distance(q, query)
    print(dist)
    if dist > 10:
        pass
    return question(str(artist_song[q][0]) + ': ' + str(artist_song[q][1]))


if __name__ == '__main__':
    app.run(debug=True)

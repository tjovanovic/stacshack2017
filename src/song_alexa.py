import logging

from random import randint
import pygame

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from playsound import playsound
from lyrics import read_songs
from nltk.metrics import edit_distance
from youtube import *
import time
from flask import send_file, request
from sentiment import sentiment

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@app.route('/image')
def get_image():
    return send_file("sentiment.jpg", mimetype='image/jpg')

@ask.launch
def init():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("LoveIntent")
def love():
    return question('I love you too babe')


@ask.intent("SetModeIntent", convert={'first': str})
def set_mode(first):
    if first == 'find song name':
        session.attributes['mode'] = 1
        msg = 'mode set to find the song name and artist'

    elif first == 'find next line':
        session.attributes['mode'] = 2
        msg = 'mode set to find the next line'

    elif first == 'find audio':
        session.attributes['mode'] = 3
        msg = 'mode set to find audio'

    else:
        session.attributes['mode'] = 1
        msg = 'mode not regonized, default find song name set'

    return question(msg)


@ask.intent("AskIntent", convert={'second': str})
def ask(second):
    session.attributes['lyric line'] = second

    if session.attributes['mode'] == 1:
        return match()
    elif session.attributes['mode'] == 2:
        return next_line()
    elif session.attributes['mode'] == 3:
        return youtube()


def match():
    second = session.attributes['lyric line']
    next_line, artist_song = read_songs()
    query = second.lower()
    q = min(artist_song.keys(), key=lambda x: edit_distance(x, second))
    dist = edit_distance(q, query)
    print(dist)
    if dist > 10:
        pass
    return question(str(artist_song[q][0]) + ': ' + str(artist_song[q][1]))


def next_line():
    second = session.attributes['lyric line']
    next_line, artist_song = read_songs()
    query = second.lower()
    q = min(artist_song.keys(), key=lambda x: edit_distance(x, second))
    dist = edit_distance(q, query)
    print(dist)
    if dist > 10:
        pass
    msg = next_line[q]
    return question(msg)


def youtube():
    lyrics = session.attributes['lyric line']
    playFromYoutube(lyrics)
    time.sleep(10)
    if sentiment():
        msg = "Whats up, do you not like this song ?"
    else:
        msg = "I'm glad you liked the song ?"
    return question(msg)


if __name__ == '__main__':
    app.run(debug=True)

"""
Modes:

1. state artist name, song name (done)
2. sing next line (doing)
3. play song (youtube?)
"""

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
def love():
    return question('I love you too babe')

@ask.intent("SetModeIntent", convert={'first':str})
def set_mode(first):

	if first == 'find song name':
		session.attribute['mode'] = 1
		msg = 'mode set to find the song name and artsit'

	elif first == 'find next line':
		session.attribute['mode'] = 2
		msg = 'mode set to find the next line'

	elif first == 'find audio':
		session.attribute['mode'] = 3
		msg = 'mode set to find audio'

	else:
		session.attribute['mode'] = 1
		msg = 'mode not regonized, default find song name set'

	return question(msg)





@ask.intent("AskIntent", convert={'first':str})
def ask():
	return 0



def match(first):

    next_line, artist_song = read_songs()
    query = first.lower()
    q = min(artist_song.keys(), key=lambda x: edit_distance(x, query))
    dist = edit_distance(q, query)
    print(dist)
    if dist > 10:
        pass
    return question(str(artist_song[q][0]) + ': ' + str(artist_song[q][1]))



def next_line(first):

	next_line, artist_song = read_songs()
	msg = next_line[first]
	return question(msg)

# @ask.intent("YoutubeIntent", convert={'first':str})
# def youtube():
# 	return 0



if __name__ == '__main__':
    app.run(debug=True)



"""
Modes:

1. state artist name, song name (done)
2. sing next line (doing)
3. play song (youtube?)
"""
import urllib
from subprocess import Popen, PIPE
from apiclient.discovery import build
from selenium import webdriver

#vlc = Popen(["/Applications/VLC.app/Contents/MacOS/VLC", "-I", "macosx", "--extraintf", "rc"], stdin=PIPE)
youtube = build("youtube", "v3", developerKey = "AIzaSyBLirIv2SpgAkQgRZwtnrowK_QhbEfPpQw")

def playFromYoutube(query, queryType = "video"):
    print(query, queryType)

    response = youtube.search().list(q=urllib.unquote(query), part="id,snippet", maxResults=5, type=queryType).execute()

    results = response.get("items", [])

    if queryType == "video" and not len(results) == 0:
        playYoutubeVideos([results[0]["id"]["videoId"]])
    elif queryType == "playlist" and not len(results) == 0:
        playYoutubePlaylist(results[0]["id"]["playlistId"])


def playYoutubeVideos(videoIds):
    #vlc.stdin.write("clear\nrandom off\n")

    driver = webdriver.Chrome()
    if not len(videoIds) == 0:git
        driver.get("http://youtube.com/watch?v=%s" % videoIds[0])
        raw_input()
        # videoUrl = "http://youtube.com/watch?v=%s" % videoIds[0]
        # vlc.stdin.write("add %s \n" % videoUrl)

    for videoId in videoIds[1:]:
        print "http://youtube.com/watch?v=%s" % videoId
        # vlc.stdin.write("enqueue %s \n" % videoUrl)

def playYoutubePlaylist(playlistId):
    response = youtube.playlistItems().list(part="id,snippet", playlistId=playlistId, maxResults = 50).execute()

    results = response.get("items", [])

    videoIds = map(lambda result: result["snippet"]["resourceId"]["videoId"], results)

    playYoutubeVideos(videoIds)

import sys
lyrics = sys.argv[1]
playFromYoutube(lyrics)
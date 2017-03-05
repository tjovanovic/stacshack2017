import urllib.parse
from subprocess import Popen, PIPE
from apiclient.discovery import build
import webbrowser
from selenium import webdriver

#vlc = Popen(["/Applications/VLC.app/Contents/MacOS/VLC", "-I", "macosx", "--extraintf", "rc"], stdin=PIPE)
youtube = build("youtube", "v3", developerKey = "AIzaSyBLirIv2SpgAkQgRZwtnrowK_QhbEfPpQw")

def playFromYoutube(query, queryType = "video"):
    print(query, queryType)

    response = youtube.search().list(q=urllib.parse.unquote(query), part="id,snippet", maxResults=5, type=queryType).execute()

    results = response.get("items", [])

    if queryType == "video" and not len(results) == 0:
        playYoutubeVideos([results[0]["id"]["videoId"]])
    elif queryType == "playlist" and not len(results) == 0:
        playYoutubePlaylist(results[0]["id"]["playlistId"])


def playYoutubeVideos(videoIds):
    #vlc.stdin.write("clear\nrandom off\n")

    # chop = webdriver.ChromeOptions()
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/aapocclcgogkmnckokdopfmhonfmgoek')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/nmmhkkegccagdldgiimedpiccmgmieda')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/aohghmighlieiainnegkcijnfilokake')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/felcaaldnbdncclmgdcncolpebgiejap')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/oghpjbnnbligjpjgojilaelgonehgnie')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/apdfllckaahabafndbhieahigkjlhalf')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/fngmhnnpilhplaeedifhccceomclgfbg')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/pjkljhegncpnkpknbcohdijeoejaedia')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/blpcfgokakmgnkcojhhkbfbldkacnbeo')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/ghbmnnjooekpmoecnnnilnnbdlolhkhi')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/pkedcjkdefgpdelpbcmbmeomcjbeemfm')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/boadgeojelhgndaghljhdicfkmllpafd')
    # chop.add_extension('load-extension=' + '~/Library/Application Support/Google/Chrome/Default/Extensions/mkfacllkmhcdnlfmhlcnnlfmkeahpmia')
    #driver = webdriver.Chrome()

    if not len(videoIds) == 0:
        url = "http://youtube.com/watch?v=%s" % videoIds[0]+"?t=20s"
        webbrowser.open(url)
        # videoUrl = "http://youtube.com/watch?v=%s" % videoIds[0]
        # vlc.stdin.write("add %s \n" % videoUrl)

    for videoId in videoIds[1:]:
        pass
       # print "http://youtube.com/watch?v=%s" % videoId
        # vlc.stdin.write("enqueue %s \n" % videoUrl)

def playYoutubePlaylist(playlistId):
    response = youtube.playlistItems().list(part="id,snippet", playlistId=playlistId, maxResults = 50).execute()

    results = response.get("items", [])

    videoIds = map(lambda result: result["snippet"]["resourceId"]["videoId"], results)

    playYoutubeVideos(videoIds)
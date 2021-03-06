import logging
import urllib.parse
import urllib.request
import re
import xml.etree.ElementTree as ET
import html
import pickle

#import local_settings


logger = logging.getLogger(__name__)


LYRICS_URL_FORMAT = 'http://lyrics.wikia.com/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles={}:{}'
HELP_URL_FORMAT = 'http://lyrics.wikia.com/api.php?action=lyrics&func=getSong&fmt=xml&artist={}&song={}'
TOP_URL_FORMAT = 'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&limit={}&api_key={}&page={}'


lyrics_pattern = re.compile(r'&lt;lyrics&gt;(.*)&lt;/lyrics&gt;', re.DOTALL)
redirect_pattern = re.compile(r'#REDIRECT \[\[(.*):(.*)]]')
non_alphanum_pattern = re.compile(r'[^ 0-9a-z]+')


def fetch_url(url):
    logger.debug('Requesting %s', url)

    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')

    return text


def quote(s):
    return urllib.parse.quote(s, safe='')


def fetch_help(artist, title):
    url = HELP_URL_FORMAT.format(quote(artist), quote(title))
    text = fetch_url(url)
    tree = ET.fromstring(text)
    if tree.find('lyrics').text != 'Not found':
        return fetch_lyrics(tree.find('artist').text, tree.find('song').text)


def fetch_lyrics(artist, title):
    url = LYRICS_URL_FORMAT.format(quote(artist), quote(title))
    text = fetch_url(url)

    result = redirect_pattern.search(text)
    if result:
        return fetch_lyrics(result.group(1), result.group(2))

    result = lyrics_pattern.search(text)
    if not result:
        return fetch_help(artist, title)

    lyrics_text = result.group(1)

    lines = []
    for line in lyrics_text.split('\n'):
        line = non_alphanum_pattern.sub('', html.unescape(line).strip().lower())
        if line:
            lines.append(line)

    return lines


def fetch_top(num):

    pages = num//1000
    reminaing = num - pages*1000

    top = []
    for page in range(pages):
        url = TOP_URL_FORMAT.format(1000, local_settings.LASTFM_API_KEY, page+1)
        text = fetch_url(url)

        tree = ET.fromstring(text)
        for track in tree[0]:
            title = track.find('name').text
            artist = track.find('artist').find('name').text
            top.append((artist, title))

    if reminaing > 0:
        url = TOP_URL_FORMAT.format(reminaing, local_settings.LASTFM_API_KEY, pages+1)
        text = fetch_url(url)

        tree = ET.fromstring(text)
        for track in tree[0]:
            title = track.find('name').text
            artist = track.find('artist').find('name').text
            top.append((artist, title))


    return top


def save_songs():
    # print(fetch_lyrics('Sia', 'Unstoppable'))
    # print(fetch_lyrics('Adele', "That's It, I Quit, I'm Movin' On"))
    next_line = {}
    artist_song = {}
    for artist, title in fetch_top(100):
        lyrics = fetch_lyrics(artist, title)
        if lyrics:
            for line in lyrics:
                artist_song[line] = artist, title
            for line1, line2 in zip(lyrics, lyrics[1:]):
                next_line[line1] = line2

    pickle.dump((next_line, artist_song), open('songs', 'wb'))

    return next_line, artist_song


def read_songs():
    return pickle.load(open('/Users/patrick.green/stacshack2017/src/songs.txt', 'rb'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    # save_songs()
    
    # next_line, artist_song = read_songs()
    top_5000 = fetch_top(5000)
    for artist, title in top_5000:
        lyrics = fetch_lyrics(artist, title)
    
    # for bla in next_line.keys():
    #     print(bla)
    


    # print(next_line.keys())
    # print(artist_song)

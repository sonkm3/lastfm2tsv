# -*- coding: utf-8 -*-
import csv, datetime, hashlib, json, math, sys
import httplib2
from optparse import OptionParser

def get_option():
    parser = OptionParser()
    parser.add_option("-k", "--apikey", dest="api_key", help="last.fm api key", metavar="API_KEY")
    parser.add_option("-u", "--username", dest="user_name", help="target user name", metavar="USER_NAME")
    parser.add_option("-p", "--page", dest="page", help="start page", metavar="PAGE")
    parser.add_option("-i", "--item-per-page", dest="item_per_page", help="item per page", metavar="ITEMPERPAGE")
    parser.add_option("-m", "--max-page", dest="max_page", help="max page", metavar="MAXPAGE")

    (option, args) = parser.parse_args()

    return option

def get_recent_tracks(page, limit, user_name, api_key):
    base_url = 'http://ws.audioscrobbler.com/2.0/'
    url = '%s?method=user.getrecenttracks&user=%s&api_key=%s&format=json&extended=1&page=%d&limit=%d' % (base_url, user_name, api_key, page, limit)
    
    client = httplib2.Http()
    resp, content = client.request(url, 'GET')
    return content

def get_player_info(user_name, api_key):
    base_url = 'http://ws.audioscrobbler.com/2.0/'
    url = '%s?method=user.getinfo&user=%s&api_key=%s&format=json' % (base_url, user_name, api_key)

    client = httplib2.Http()
    resp, content = client.request(url, 'GET')
    return content

def format_scrobbled_track(track):
    scrobble_info = {}

    scrobble_info['album_name'] = track['album']['#text']
    scrobble_info['album_mbid'] = track['album']['mbid']
    scrobble_info['artist_name'] = track['artist']['name']
    scrobble_info['artist_mbid'] = track['artist']['mbid']
    scrobble_info['track_name'] = track['name']
    scrobble_info['track_mbid'] = track['mbid']
    
    if 'date' in track:
        scrobble_info['datetime'] = datetime.datetime.fromtimestamp(int(track['date']['uts']))# - datetime.timedelta(hours=9)
        scrobble_info['timestamp'] = int(track['date']['uts'])
    else:
        scrobble_info['datetime'] = ''
        scrobble_info['timestamp'] = ''

    return (
        str(scrobble_info['timestamp']) + "\t" +
        str(scrobble_info['datetime']) + u"\t" +
        scrobble_info['artist_name'] + u"\t" +
        scrobble_info['artist_mbid'] + u"\t" +
        scrobble_info['album_name'] + u"\t" +
        scrobble_info['album_mbid'] + u"\t" +
        scrobble_info['track_name'] + u"\t" +
        scrobble_info['track_mbid'] + u"\t" +
        hashlib.sha1(
            scrobble_info['artist_name'].encode('utf-8') +
            scrobble_info['album_name'].encode('utf-8') +
            scrobble_info['track_name'].encode('utf-8')
            ).hexdigest()
        ).encode('utf-8')

def get_play_count(user_name, api_key):
    raw_player_info = get_player_info(user_name, api_key)
    player_info = json.loads(raw_player_info)
    return player_info['user']['playcount']

def loop(user_name, api_key, page, item_per_page, max_page = None):

    playcount = get_play_count(user_name, api_key)
    if max_page == None:
      max_page = int(math.ceil(float(playcount)/float(item_per_page)))

    while True:
        raw_recent_tracks = get_recent_tracks(page, item_per_page, user_name, api_key)
        recent_tracks = json.loads(raw_recent_tracks)

        for track in recent_tracks['recenttracks']['track']:
            print format_scrobbled_track(track)

        sys.stderr.write(str(page))
        sys.stderr.write("/")
        sys.stderr.write(str(max_page))
        sys.stderr.write("\n")

        if page == max_page:
            break

        page = page + 1

def main():
    option = get_option()

    if option.page and option.page.isdigit():
        page = int(option.page)
    else:
        page = 1
        
    if option.item_per_page and option.item_per_page.isdigit():
        item_per_page = int(option.item_per_page)
    else:
        item_per_page = 200

    if option.max_page and option.max_page.isdigit():
        max_page = int(option.max_page)
    else:
        max_page = None

    loop(option.user_name, option.api_key, page, item_per_page, max_page)

if __name__ == "__main__":
    main()

# track json.
#{
#    u'album': {u'mbid': u'74efa40a-725a-4815-9a98-01df81e5be2c', u'#text': u'All Or Nothing'},
#    u'loved': u'0',
#    u'streamable': u'0',
#    u'name': u'Seeing Red',
#    u'artist': {
#        u'url': u'Pennywise',
#        u'mbid': u'5c210861-2ce2-4be3-9307-bbcfc361cc01',
#        u'name': u'Pennywise',
#        u'image': [
#            {u'#text': u'http://userserve-ak.last.fm/serve/34/10886395.jpg', u'size': u'small'},
#            {u'#text': u'http://userserve-ak.last.fm/serve/64/10886395.jpg', u'size': u'medium'},
#            {u'#text': u'http://userserve-ak.last.fm/serve/126/10886395.jpg', u'size': u'large'},
#            {u'#text': u'http://userserve-ak.last.fm/serve/252/10886395.jpg', u'size': u'extralarge'}
#        ]
#    },
#    u'url': u'http://www.last.fm/music/Pennywise/_/Seeing+Red',
#    u'image': [
#        {u'#text': u'http://userserve-ak.last.fm/serve/34s/89522549.png', u'size': u'small'},
#        {u'#text': u'http://userserve-ak.last.fm/serve/64s/89522549.png', u'size': u'medium'},
#        {u'#text': u'http://userserve-ak.last.fm/serve/126/89522549.png', u'size': u'large'},
#        {u'#text': u'http://userserve-ak.last.fm/serve/300x300/89522549.png', u'size': u'extralarge'}
#    ],
#    u'mbid': u'217acea4-7be6-4a3e-bbd6-01dadaa5f49f',
#    u'date': {u'uts': u'1374468657', u'#text': u'22 Jul 2013, 04:50'}
#}

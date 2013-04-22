#!/usr/bin/python
"""
library dependencies:
sudo apt-get install python-requests

to include in another python file:
from video_request import *
"""
import requests
import json

# track represents a string query as if you were searching for the video
# something along the lines of artist song_title
# eg. video_request("fleet foxes montezuma")
# function returns
def video_request(track):

    #initialize vars
    query = ""
    viewCount = 0
    likeCount = 0
    i = 0

    # set to however many vids you want to sum the statistics for
    max_results = 1

    # replace spaces with %20 to format to an https request
    for word in track.split():
        query += word + "%20"

    # send off packaged request you YouTube API
    videos = requests.get(
        "https://gdata.youtube.com/feeds/api/videos?v=2&alt=jsonc&q="+
        query+
        "&max-results="
        +str(max_results)).json

    # sum the stats
    while i < max_results:
        viewCount += int(videos['data']['items'][i]['viewCount'])
        likeCount += int(videos['data']['items'][i]['likeCount'])
        i += 1

    return viewCount, likeCount
    #return viewCount, rating


def read_songs():
    songs  = json.load(open('song_info.json'))
    return songs

youtube_vids = []
songs = read_songs()

views = json.load(open('view_and_like_count.json'))
i = 0
for view in views:
    if view['artist'] == 'mastodon' and view['name'] == 'Deep Sea Creature':
        print view['likeCount']
        print view['viewCount']

    #print view['likeCount']
    #print view['viewCount']
    #print view['name']
    #print view['artist']
    #print ""
"""
i = 0
for song in songs:
    print i
    i += 1
    try:
        #print i
        video = {}
        video['artist'] = song['artist']
        video['name'] = song['name']
        #video['hotness'] = song['hotness']
        video['viewCount'] = video_request(str(song['artist'])+" "+str(song['name']))[0]
        video['likeCount'] = video_request(str(song['artist'])+" "+str(song['name']))[1]
        youtube_vids.append(video)
        #print video
        #i += 1
    except:
        "uh oh"
        #json.dump(youtube_vids,w)

json.dump(youtube_vids,w)

w.close()
"""


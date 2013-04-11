#!/usr/bin/python
"""
library dependencies:
sudo apt-get install python-requests

to include in another python file:
from video_request import *
"""
import requests

# track represents a string query as if you were searching for the video
# something along the lines of artist song_title
# eg. video_request("fleet foxes montezuma")
# function returns
def video_request(track):

    #initialize vars
    query = ""
    viewCount = 0
    #rating = 0.0
    i = 0

    # set to however many vids you want to sum the statistics for
    max_results = 3

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
        #rating += float(videos['data']['items'][i]['rating'])
        i += 1

    return viewCount
    #return viewCount, rating

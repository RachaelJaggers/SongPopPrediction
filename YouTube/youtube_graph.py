#!/usr/bin/python
from numpy import *
import matplotlib
from pylab import *
import matplotlib.pyplot as plt
import json

hotness = []
viewCount = []

def read_data():
    songs = []
    for line in open('view_count.json'):
        hot_flag = False
        view_flag = False
        for word in line.split():
            if hot_flag:
                word = word.replace('},','')
                word = word.replace('}][{"track":','')
                word = word.replace('}]','')
                hotness.append(float(word))
            if view_flag:
                word = word.replace(',','')
                viewCount.append(int(word))
            if 'hotness' in word:
                hot_flag = True
            else:
                hot_flag = False
            if 'viewCount' in word:
                view_flag = True
            else:
                view_flag = False
            #print word
            #print word
            #print viewCount[0]
            #viewCount = viewCount[0].replace(', "','')
            #print viewCount
            #for hotness in viewCount.split('hotness'):
            #    print hotness

            #for hotness in viewCount.split('hotness":'):
                #print hotness
        songs.append(line)
    #for song in songs[:2]:
        #print song
    #songs  = json.load(open('view_count.json'))
    return songs

read_data()
plt.scatter(hotness,viewCount)
plt.show()
"""
hotness = []
viewCount = []
songs = read_data()
for song in songs[:3]:
    print song['hotness']
    print song['viewCount']
    #hotness.append(song['hotness'])
    #viewCount.append(song['viewCount'])

plt.scatter(hotness,viewCount)
plt.show()
"""

import csv
import math
import os
import json
import sys
import hdf5_getters as h5get
import numpy as np

w = open('song_info.json','w')

def calc_poffpop(song):
	retval = 0.0;
	#print "Calc: ", song.hotness, " + ", song.chart_score
	retval = 0.3*float(song.hotness) + 0.7*float(song.chart_score)
	return retval

class Song:
	name = ""
	artist = ""
	year = 0; #Quantity in given year
	hotness = 0;
	chart_score = 0;

	pop_score = 0.0;


h5 = h5get.open_h5_file_read("subset_msd_summary_file.h5")
numSongs = h5get.get_num_songs(h5)

#all_chart_info = {}

"""
with open('tsort-chart-2-2-0007.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	reader.next();
	for row in reader:
		#print row
		artist = row[0]
		title = row[1]
		score = row[4]

		all_chart_info[(artist,title)] = score;
"""

print "Done loading chart info"

song_list = []
j = 0

for i in range(0, numSongs):
	j += 1
	#print 
	track = {}
	#Handle each one
	year = h5get.get_year(h5, i)
	if year < 1980 or year > 2010:
		continue;

	song = Song()
	#song.year = year
	#song.hotness = h5get.get_song_hotttnesss(h5, i)

	#print "Hotness: ", song.hotness;
	#if math.isnan(song.hotness):
	#	song.hotness = 0.0;

	song.artist = h5get.get_artist_name(h5, i)
	song.name = h5get.get_title(h5, i)
	#track['track'] = str(song.artist) + " " + str(song.name)
	#track['hotness'] = float(song.hotness)
	track['artist'] = song.artist
	track['name'] = song.name
	song_list.append(track)
	#song.pop_score = calc_poffpop(song)
	#print "Poff Score", song.pop_score
	#all_songs.append(song)
	#print all_songs

json.dump(song_list,w)
w.close()
"""

sorted(all_songs, key=lambda song: song.pop_score)

for x in all_songs:
	print x.name, " - ", x.artist, ": ", x.hotness#, "/", x.chart_score, "/", x.pop_score
	break;
"""

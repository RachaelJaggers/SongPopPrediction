import csv, math, os, sys, json, operator
import hdf5_getters as h5get
import numpy as np
#import matplotlib
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

def calc_poffpop(song):
    retval = 0.0
    #print "Calc: ", song.chart_score, " + ", song.yt_score
    #retval = 0.1*float(song.hotness) + 0.2*float(song.chart_score) + 0.7*float(song.yt_score)
    retval = 0.5*float(song.chart_score) + 0.5*float(song.yt_score)
    #if retval > 1:
    #    print retval
    return retval

class Song:
	name = ""
	artist = ""
	year = 0 #Quantity in given year
	hotness = 0
	chart_score = 0
	pop_score = 0.0

def read_youtube():
    f = open('youtube_songs.csv')
    views = []
    for song in f.readlines():
        view = {}
        song = song.strip()
        view['artist'] = song.split(',')[0]
        view['name'] = song.split(',')[1]
        view['viewCount'] = song.split(',')[2]
        view['likeCount'] = song.split(',')[3]
        views.append(view)
    
    f.close()
    return views

upper_songs = {}

def write_to_csv(song):
    youtube_file = open("poff.csv","a")
    file_writer = csv.writer(youtube_file)
    file_writer.writerow([upper_songs[(song.artist,song.name)][0],upper_songs[(song.artist,song.name)][1],song.year,song.pop_score])
    youtube_file.close()

#read_youtube()
youtube_file = open("poff.csv","w")
youtube_file.close()

all_songs = []
songs_80s = []
songs_90s = []
songs_00s = []
top_10_songs = []

#h5 = h5get.open_h5_file_read("subset_msd_summary_file.h5")
#numSongs = h5get.get_num_songs(h5)


all_chart_info = {}

#YOUTUBE STUFF
views = read_youtube()
numSongs = len(views)
#views = json.load(open('view_and_like_count.json'))
view_counts = {}
view_likes = {}
song_year = {}


min_count = float(1000000000)
min_likes = float(1000000000)
max_count = float(-1)
max_likes = float(-1)

i = 0
with open('tsort-chart-2-2-0007.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        #print row
        artist = row[0] 
        title = row[1]
        year = row[3]
        #print year
        #print "artist: " + artist.lower() + " song: " + title.lower()
        score = row[4]
        if year != 'unknown':
            all_chart_info[(artist.lower(),title.lower())] = score
            song_year[(artist.lower(),title.lower())] = year
    
print "Done loading chart info"

songs_with_hot = []
songs_with_chart = []
songs_with_both = []
viewCount = {}
min_score = 20.0
max_score = -1.0


max_count = 520998780
max_likes = 7484252
min_count = 1
min_likes = 1

top_songs = {}

for view in views:
    artist = view["artist"].lower()
    
    song_name = view['name'].lower()
    upper_songs[(artist,song_name)] = (view["artist"],view["name"])
    #print "artist: " + artist + " song: " + song
    count = float(view['viewCount'])
    likes = float(view['likeCount'])
    view_counts[(artist,song_name)] = float(count)
    view_likes[(artist,song_name)] = float(likes)
    

    #if likes > max_likes:
    #    max_likes = likes

    #if likes < min_likes:
    #    min_likes = likes

    #if count > max_count:
    #    max_count = count

    #if count < min_count:
    #    min_count = count

    song = Song()
    song.artist = artist
    song.name = song_name
    song.likes = 0.0
    song.views = 0.0
    views = float(view_counts[(song.artist, song.name)])
    likes = float(view_likes[(song.artist, song.name)])
    if (song.artist, song.name) in all_chart_info:
        song.chart_score = float(all_chart_info[(song.artist, song.name)])/16.0
        val = float(view_likes[(song.artist, song.name)])
        if val > max_likes:
            val = max_likes
        song.likes = (val - min_likes)/(max_likes-min_likes)
        val = float(view_counts[(song.artist, song.name)])
        if val > max_count:
            val = max_count
        song.views = (val - min_count)/(max_count-min_count)
        try:
            song.year = song_year[(song.artist, song.name)]
        except:
            song.year = 0
        song.yt_score = 0.8*song.views + 0.2*song.likes

        #        if song.yt_score > 1:
        #            print song.yt_score

        #if song.chart_score > 10:
        #    print song.chart_score
        song.pop_score = calc_poffpop(song)
        #if song.yt_score > .17:
            #print song.artist + " " + song.name + " " + str(song.yt_score) + " " + str(song.chart_score)
        #if song.pop_score > .69:
            #print song.artist + " " + song.name + " " + str(views) + " " + str(likes)
        #if song.pop_score > 1:
        #    print song.pop_score
        write_to_csv(song)
        top_songs[(song.artist,song.name)] = song.pop_score

#print sorted(top_songs.iteritems(), key=operator.itemgetter(1), reverse = True)[:25]
#print sorted(view_likes.iteritems(), key=operator.itemgetter(1), reverse = True)[:50]
print sorted(top_songs.iteritems(), key=operator.itemgetter(1), reverse = True)[:50]

print "finished"
        
"""

#for view in views:
	#Handle each one
	#year = h5get.get_year(h5, i)
	#if year < 1980 or year > 2010:
	#	continue;

	#song = Song()
	#song.year = year

	#song.tempo = h5get.get_tempo(h5, i)
	#song.duration = h5get.get_duration(h5, i) 
	#song.key = h5get.get_key(h5, i)
	#song.energy = h5get.get_energy(h5, i)
	#song.time_sig = h5get.get_time_signature(h5,i)
	#song.mode = h5get.get_mode(h5,i)

	#song.hotness = h5get.get_song_hotttnesss(h5, i)
	#print "Hotness: ", song.hotness;
	#if math.isnan(song.hotness):
	#	song.hotness = 0.1;

	#song.artist = h5get.get_artist_name(h5, i)

	#song.name = h5get.get_title(h5, i)

	#if (song.artist.lower(), song.name.lower()) in all_chart_info:
	#	song.chart_score = float(all_chart_info[(song.artist.lower(), song.name.lower())])
	#	print " Got us some data! ", song.artist, " -- ", song.name, ": ", song.chart_score
	#else:
		#song.chart_score = float('nan')
	#	song.chart_score = 0.0

	song.likes = 0.0
	song.views = 0.0

	if(song.artist.lower(), song.name.lower()) in view_likes:
		val = float(view_likes[(song.artist.lower(), song.name.lower())])
		song.likes = (val - min_likes)/(max_likes-min_likes)

	if(song.artist.lower(), song.name.lower()) in view_counts:
		val = float(view_counts[(song.artist.lower(), song.name.lower())])
		song.views = (val - min_count)/(max_count-min_count)

	song.yt_score = 0.8*song.views + 0.2*song.likes

	song.pop_score = calc_poffpop(song)

	if song.pop_score > max_score:
		max_score = song.pop_score;

	if song.pop_score < min_score:
		min_score = song.pop_score;

	#print "Poff Score", song.pop_score
	# if math.isnan(song.hotness) == False:
	# 	songs_with_hot.append(song)

	# if math.isnan(song.chart_score) == False:
	# 	songs_with_chart.append(song)

	# if math.isnan(song.hotness) == False and math.isnan(song.chart_score) == False:
	# 	songs_with_both.append(song)

	if song.year >= 1980 and song.year < 1990:
		songs_80s.append(song);

	if song.year >= 1990 and song.year < 2000:
		songs_90s.append(song);

	if song.year >= 2000:
		songs_00s.append(song);

	all_songs.append(song)

#Normalize everything
for x in all_songs:
	x.pop_score = (x.pop_score - min_score)/(max_score-min_score)

all_songs.sort(key=operator.attrgetter('pop_score'));
all_songs.reverse();

for i in range(0,len(all_songs)/10):
	top_10_songs.append(all_songs[i])

for i in range(0,20):
	song = all_songs[i];
	print song.name, " - ", song.artist, ": ", song.pop_score, "(", song.yt_score, ")";


with open('songs.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in all_songs:
		spamwriter.writerow([s.year, s.name, s.artist, s.pop_score, s.duration, s.tempo, s.energy, s.key, s.time_sig])

with open('songs.arff', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in all_songs:
		spamwriter.writerow([s.year, s.pop_score, s.duration, s.tempo, s.energy, s.key, s.time_sig, song.mode])

with open('songs_80s.arff', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in songs_80s:
		spamwriter.writerow([s.year, s.pop_score, s.duration, s.tempo, s.energy, s.key, s.time_sig, song.mode])

with open('songs_90s.arff', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in songs_90s:
		spamwriter.writerow([s.year, s.pop_score, s.duration, s.tempo, s.energy, s.key, s.time_sig, song.mode])

with open('songs_00s.arff', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in songs_00s:
		spamwriter.writerow([s.year, s.pop_score, s.duration, s.tempo, s.energy, s.key, s.time_sig, song.mode])

with open('songs_top.arff', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in top_10_songs:
		spamwriter.writerow([s.year, s.pop_score, s.duration, s.tempo, s.energy, s.key, s.time_sig, song.mode])

"""

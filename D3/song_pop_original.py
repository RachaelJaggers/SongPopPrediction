import csv
import math
import os
import sys
import hdf5_getters as h5get
import numpy as np
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import json
import operator

def calc_poffpop(song):
	retval = 0.0;
	#print "Calc: ", song.hotness, " + ", song.chart_score, " + ", song.yt_score;
	retval = 0.1*float(song.hotness) + 0.2*float(song.chart_score) + 0.7*float(song.yt_score)
	if retval > 1:
		print retval
	return retval

class Song:
	name = ""
	artist = ""
	year = 0; #Quantity in given year
	hotness = 0;
	chart_score = 0;

	pop_score = 0.0;

all_songs = []
songs_80s = []
songs_90s = []
songs_00s = []
top_10_songs = []

h5 = h5get.open_h5_file_read("subset_msd_summary_file.h5")
numSongs = h5get.get_num_songs(h5)

all_chart_info = {}

#YOUTUBE STUFF
views = json.load(open('view_and_like_count.json'))
view_counts = {}
view_likes = {}

min_count = 1000000000;
min_likes = 1000000000;
max_count = -1;
max_likes = -1;

for view in views:
	artist = view["artist"].lower()
	song = view['name'].lower();
	count = view['viewCount'];
	likes = view['likeCount'];
	view_counts[(artist,song)] = count;
	view_likes[(artist,song)] = likes;

	if likes > max_likes:
		max_likes = likes;

	if likes < min_likes:
		min_likes = likes;

	if count > max_count:
		max_count = count;

	if count < min_count:
		min_count = count;

with open('tsort-chart-2-2-0007.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	reader.next();
	for row in reader:
		#print row
		artist = row[0]
		title = row[1]
		score = row[4]

		all_chart_info[(artist.lower(),title.lower())] = score;

print "Done loading chart info"

songs_with_hot = []
songs_with_chart = []
songs_with_both = []

min_score = 20.0;
max_score = -1.0;
print numSongs
for i in range(0, numSongs):
	#Handle each one
	year = h5get.get_year(h5, i)
	if year < 1980 or year > 2010:
		continue;

	song = Song()

	song.year = year

	song.tempo = h5get.get_tempo(h5, i)
	song.duration = h5get.get_duration(h5, i) 
	song.key = h5get.get_key(h5, i)
	song.energy = h5get.get_energy(h5, i)
	song.time_sig = h5get.get_time_signature(h5,i)
	song.mode = h5get.get_mode(h5,i);

	song.hotness = h5get.get_song_hotttnesss(h5, i)
	#print "Hotness: ", song.hotness;
	if math.isnan(song.hotness):
		song.hotness = 0.1;

	song.artist = h5get.get_artist_name(h5, i)

	song.name = h5get.get_title(h5, i)

	if (song.artist.lower(), song.name.lower()) in all_chart_info:
		song.chart_score = float(all_chart_info[(song.artist.lower(), song.name.lower())]);
		print " Got us some data! ", song.artist, " -- ", song.name, ": ", song.chart_score
	else:
		#song.chart_score = float('nan');
		song.chart_score = 0.0;

	song.likes = 0.0;
	song.views = 0.0;

	if(song.artist.lower(), song.name.lower()) in view_likes:
		val = float(view_likes[(song.artist.lower(), song.name.lower())]);
		song.likes = (val - min_likes)/(max_likes-min_likes);

	if(song.artist.lower(), song.name.lower()) in view_counts:
		val = float(view_counts[(song.artist.lower(), song.name.lower())]);
		song.views = (val - min_count)/(max_count-min_count);

	song.yt_score = 0.8*song.views + 0.2*song.likes;

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
	#print song.name, " - ", song.artist, ": ", song.pop_score, "(", song.yt_score, ")";


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

# x = []
# y = []
# for e in songs_with_both:
# 	x.append(e.hotness)
# 	y.append(e.chart_score)

# fig = Figure(figsize=(6,6))

# canvas = FigureCanvas(fig)
# ax = fig.add_subplot(111)
# ax.set_title("Comparison of Popularity Metrics", fontsize=12)
# ax.set_xlabel("Hotness Metric")
# ax.set_ylabel("Chart Pop Metric")
# ax.scatter(x, y, s=10, color='violet')

# fit = np.polyfit(np.array(x),np.array(y),1)
# fit_fn = np.poly1d(fit)
# #ax.plot([70, 70], [100, 250], 'k-', lw=2)

# ax.plot(x, fit_fn(x), 'k-', lw=2)

# canvas.print_figure('comparison.png', dpi=700)


# hots = []
# for e in songs_with_hot:
# 	hots.append(e.hotness)
# fig = plt.figure()
# plt.title('Song Hotness Scores')
# plt.boxplot(hots)
# fig.savefig('Hotness', dpi=fig.dpi)

# charts = []
# for e in songs_with_chart:
# 	charts.append(e.chart_score)
# fig = plt.figure()
# plt.title('Song Chart Scores')
# plt.boxplot(charts)
# fig.savefig('Chart Scores', dpi=fig.dpi)

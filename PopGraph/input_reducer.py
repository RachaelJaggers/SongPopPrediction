#File takes output generated by Rachael and breaks it up a little bit

import csv
import math
import os
import sys
import numpy as np
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import json
import operator


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


min_score = 20.0;
max_score = -1.0;
with open('poff.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		#print row
		song = Song()

		song.artist = row[0]
		song.name = row[1]
		song.year = int(row[2])
		song.pop_score = float(row[3])
		print "Song:", song.year
		if song.year < 1980 or song.year > 2010:
			continue;

		print "Adding song!"
		if song.pop_score > max_score:
			max_score = song.pop_score;

		if song.pop_score < min_score:
			min_score = song.pop_score;

		if song.year >= 1980 and song.year < 1990:
			songs_80s.append(song);

		if song.year >= 1990 and song.year < 2000:
			songs_90s.append(song);

		if song.year >= 2000:
			songs_00s.append(song);

		all_songs.append(song)

for x in all_songs:
	x.pop_score = (x.pop_score - min_score)/(max_score-min_score)

all_songs.sort(key=operator.attrgetter('pop_score'));
all_songs.reverse();

for i in range(0,len(all_songs)/10):
	top_10_songs.append(all_songs[i])

with open('top_songs.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in top_10_songs:
		spamwriter.writerow([s.year, s.name, s.artist, s.pop_score])

with open('80s_songs.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in songs_80s:
		spamwriter.writerow([s.year, s.name, s.artist, s.pop_score])

with open('90s_songs.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in songs_90s:
		spamwriter.writerow([s.year, s.name, s.artist, s.pop_score])

with open('00s_songs.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for s in songs_00s:
		spamwriter.writerow([s.year, s.name, s.artist, s.pop_score])

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

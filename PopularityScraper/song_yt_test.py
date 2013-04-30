import json
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


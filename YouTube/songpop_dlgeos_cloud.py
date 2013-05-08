import csv, json, urllib2, cloud, sys
from time import sleep
from sets import Set
from collections import Counter

rows = []
#Import the data from the DATA (csv) file
#Must decode when necessary
def import_data():
    #Import the data from the exported file
    global headers, rows
    f = open("songs.csv")
    reader = csv.reader(f, delimiter="|")
    for row in reader:
        try:
            test = row[0].split(',')
            if len(test) == 2:
                rows.append(test)
        except:
            print "problem with comma"
    f.close()

def import_distances():
    try:
        f = open("youtube.json")
        content = json.loads(f.read())
        f.close()
        return content
    except:
        print "Error importing distances"
        return {}

def save_distances(distances):
    youtube_file = open("youtube_songs.csv","a")
    file_writer = csv.writer(youtube_file)
    file_writer.writerow([distances['song_title'],distances['artist_name'],distances['viewCount'],distances['likeCount']])
    youtube_file.close()
    #f = open("youtube.json", "a")
    #f.write(json.dumps(distances))
    #f.close()

def row_to_url(row):
    song = row[0] + ' ' + row[1]
    query = ''
    for word in song.split():
        query += word + "%20"

    url = "https://gdata.youtube.com/feeds/api/videos?v=2&alt=jsonc&q="
    url += query
    url += "&max-results=1"
    return url


def download(rows):
    res = []
   # print "hey there"
    #print rows
    for row in rows:
        url = row_to_url(row)
        video = {}
        print url
        resp = json.loads(urllib2.urlopen(url).read())
        video["song_title"] = row[0]
        video["artist_name"] = row[1]
        try:
            video["viewCount"] = int(resp['data']['items'][0]['viewCount'])
            video["likeCount"] = int(resp['data']['items'][0]['likeCount'])
        except:
            video["viewCount"] = 0
            video["likeCount"] = 0
        res.append(video)        
        
        #Only download the data if everything is fine
        #if resp["status"] != "OK":
            #break
        #sleep(0.05)
    return res


def run():
    #Import the data we need
    import_data()
    global rows
    
    #This was to convert the csvfile with commas as delimiters to "|" as delimiters
    """
    output = open("output.csv", "wb")
    rowwriter = csv.writer(output, delimiter='|')
    for row in rows:
        if len(row) != 5:
            print "Skipping row with len " + str(len(row))
            continue
        a = row[0]+","+row[1]
        b = row[2]+","+row[3]
        walk = row[4]
        rowwriter.writerow([a, b, walk])
    output.close()
    print "Done"
    exit()
    """
    distances = import_distances()
    #print "rows:"
    #print rows
    #Find the distances from the csv file not in the json file
    print "Finding distances which need to be downloaded"
    needed_rows = []
    ig = 0
    #Find which distances still need to be downloaded
    for row in rows:
        #print row
        song_title = row[0]
        artist_name = row[1]
        #walk = row[2]
        
        #If it's in distances, then it's been processed and we don't need it
        if song_title in distances and artist_name in distances[song_title]:# and walk in distances[a][b]:
            continue
        needed_rows.append(row)
    
    #Print the results
    print "There are a total of {0:,d} songs.".format(len(rows))
    print "There are {0:,d} downloaded songs.".format(sum([len(d) for d in distances]))
    print "Ignored {0:,d} songs since len != 3.".format(ig)
    print "There are {0:,d} songs needing to be processed.".format(len(needed_rows))
    
    len_needed_rows = len(needed_rows)
    
    if len_needed_rows <= 0:
        print "Done"
        exit()
    
    #Figure out how many jobs I want to create and how many requests per job
    job_count = int(sys.argv[1])
    req_per_row = int(sys.argv[2])
    
    #Probably an easier way to do this...
    #For each job, add the requests to that array and append it to job_rows
    print "Generating data for {0} jobs".format(job_count)
    job_rows = []
    for i in xrange(0, job_count):
        job = []
        while len(job) < req_per_row and len(needed_rows) > 0:
            job.append(needed_rows.pop())
        job_rows.append(job)
        
        if len(needed_rows) == 0:
            break
    
    #Print status of jobs
    print "Created {0} jobs with {1} songs each, so {2} songs to be processed.".format(len(job_rows),req_per_row,sum([len(job) for job in job_rows]))
    
    #Now actually map them to run in the cloud
    #The "s1" type gives unique IP addresses per job. Eek
    print "Creating job map"
    #print job_rows
    jids = cloud.map(download, job_rows, _type="s1")
    
    print "Waiting for jobs to complete."
    
    #The possible statuses and the statuses we are waiting for
    possible_job_statutes = ["waiting", "queued", "processing", "done", "error", "killed", "stalled"]
    pending_job_statuses = Set(["waiting", "queued", "processing"])
    
    #Keep looping until no job statuses are in the pending_job_statuses
    statuses = []
    while True:
        statuses = cloud.status(jids)
        tally = Counter()
        for status in statuses:
            tally[status] += 1
        print "Status of jobs: " + str(tally)
        
        #If none of the statuses are in pending_job_statuses, we are done!
        if len(pending_job_statuses.intersection(Set(statuses))) == 0:
            break
        
        #Wait for 5 seconds between checks
        sleep(5)
    
    #Now loop through the jobs and retrieve the results
    saved = 0
    for index in xrange(0, len(statuses)):
        print "Working on job {0} of {1}".format(index+1, len(statuses))
        jid = jids[index]
        status = statuses[index]
        
        #If it's not "done", then there must have been an error
        if status != "done":
            print "Status of jid {0} = {1}.".format(jid, status)
            continue
        
        results = cloud.result(jid)
        print "There are {0} results.".format(len(results))
        for result in results:
            #Make sure we aren't over the limits or nothing went wrong
            #if result["status"] != "OK":
            #    print('result["status"] == ' + result["status"])
            #    continue
            #elem = result["rows"][0]["elements"][0]
            #if elem["status"] != "OK":
            #    print('elem["status"] == ' + elem["status"])
            #    continue
            
            #dist = elem["distance"]["value"]
            #dur = elem["duration"]["value"]
            #a = result["artist_name"]
            #b = result["b"]
            #walk = result["walk"]
            
            #if a not in distances:
            #    distances[a] = {}
            #if b not in distances[a]:
            #    distances[a][b] = {}
            
            #distances[a][b][walk] = {"walk":walk,"distance":dist,"duration":dur,"a":a,"b":b}
            song = {'artist_name':result['artist_name'],'song_title':result['song_title'],'viewCount':result['viewCount'],'likeCount':result['likeCount']}
            #print song
            saved += 1
        
            try:
                #print song['viewCount']
                if song['viewCount'] > 0:
                    save_distances(song)
                    #print song
            except:
                print "Couldn't save distances."
    
    print "Saved {0:,d} distance with {1:,d} remaining".format(saved, len_needed_rows-saved)
 
def run_ip():
    
    #Figure out how many jobs I want to create and how many requests per job
    job_count = int(sys.argv[1])
    
    job_rows = range(0, job_count)
    
    #Now actually map them to run in the cloud
    #The "s1" type gives unique IP addresses. Eek
    print "Creating job map for {0} jobs.".format(len(job_rows))
    jids = cloud.map(download_ip, job_rows, _type="s1")
    
    print "Waiting for jobs to complete."
    
    #The possible statuses and the statuses we are waiting for
    possible_job_statutes = ["waiting", "queued", "processing", "done", "error", "killed", "stalled"]
    pending_job_statuses = Set(["waiting", "queued", "processing"])
    
    #Keep looping until no job statuses are in the pending_job_statuses
    statuses = []
    while True:
        statuses = cloud.status(jids)
        tally = Counter()
        for status in statuses:
            tally[status] += 1
        print "Status of jobs: " + str(tally)
        
        #If none of the statuses are in pending_job_statuses, we are done!
        if len(pending_job_statuses.intersection(Set(statuses))) == 0:
            break
        
        #Wait for 5 seconds between checks
        sleep(5)
    
    #Now loop through the jobs and retrieve the results
    ip_counter = Counter()
    results = cloud.result(jids)
    for result in results:
        ip_counter[result] += 1
    
    print "IP Addresses: " + str(ip_counter)
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Please pass in the number of jobs to run and then the number of distances per job as parameters."
        exit()
    f = open("youtube_songs.csv",'w')
    f.close()
    #import_data()
    #download(rows)
    run()
    #run_ip()

#!/usr/bin/python
"""
follow http://docs.picloud.com/prereqs.html for system requirements
file is still incomplete 4/21
"""
import json, requests, cloud
from time import sleep
from sets import Set
from collections import Counter

def run():
    #Import the data we need        
    
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
    print "Created {0} jobs with {1} distances each, so {2} distances to be processed.".format(len(job_rows),req_per_row,sum([len(job) for job in job_rows]))
    
    #Now actually map them to run in the cloud
    #The "s1" type gives unique IP addresses per job. Eek
    print "Creating job map"
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
            if result["status"] != "OK":
                print('result["status"] == ' + result["status"])
                continue
            elem = result["rows"][0]["elements"][0]
            if elem["status"] != "OK":
                print('elem["status"] == ' + elem["status"])
                continue
            
            dist = elem["distance"]["value"]
            dur = elem["duration"]["value"]
            a = result["a"]
            b = result["b"]
            walk = result["walk"]
            
            if a not in distances:
                distances[a] = {}
            if b not in distances[a]:
                distances[a][b] = {}
            
            distances[a][b][walk] = {"walk":walk,"distance":dist,"duration":dur,"a":a,"b":b}
            saved += 1
        
        try:
            save_distances(distances)
        except:
            print "Couldn't save distances."
    
    print "Saved {0:,d} distance with {1:,d} remaining".format(saved, len_needed_rows-saved)

import csv, math, os, sys, json, operator
from operator import itemgetter
"""
"rMVMP":104747.5,"fulldate":20120515,"NAME":"Facebook","rMVOP":104100,"Obs":2438,"BHRET3":0}
"rMVMP":5010.53,"fulldate":20091006,"NAME":"Verisk Analytics ","rMVOP":4144.05,"Obs":2430,"BHRET3":79.94121969
"rMVMP":396.19,"fulldate":20110503,"NAME":"Boingo Wireless ","rMVOP":439.128,"Obs":2431,"BHRET3":-14.7107438
"rMVMP":1471.68,"fulldate":20120301,"NAME":"Yelp ","rMVOP":898.1,"Obs":2432,"BHRET3":-12.12367779
"rMVMP":11243.66,"fulldate":20110524,"NAME":"Yandex NV","rMVOP":8031.19,"Obs":2433,"BHRET3":-42.89392379
"rMVMP":962.57,"fulldate":20110719,"NAME":"Zillow ","rMVOP":538.201,"Obs":2434,"BHRET3":12.66424378
"rMVMP":507.75,"fulldate":20111018,"NAME":"ZELTIQ Aesthetics ","rMVOP":425.854,"Obs":2435,"BHRET3":-66.19354839
"rMVMP":6643.76,"fulldate":20111215,"NAME":"Zynga ","rMVOP":6993.43,"Obs":2436,"BHRET3":-13.47368421
"rMVMP":86.21,"fulldate":20091020,"NAME":"ZST Digital Networks ","rMVOP":95.7891,"Obs":2437,"BHRET3":-100

2438
1974-2012

"""

def read_youtube():
    f = open('poff_50_50.csv')
    songs = []
    for song in f.readlines():
        view = {}
        song = song.strip()
        view['artist'] = song.split(',')[0]
        view['song'] = song.split(',')[1]
        view['year'] = song.split(',')[2]
        view['pop'] = song.split(',')[3]
        songs.append(view)
    
    f.close()
    return songs

def edit_html():
    f = open('index.html', 'r')
    w = open('new_index.html','w')
    ret_list = []
    songs = read_youtube()
    songs = sorted(songs, key=itemgetter('pop'), reverse = True)[:1000]
    flag = False
    for line in f.readlines():
        if 'nytg.ipoData' in line:
            if flag == False:
                flag = True
                i = 0   
                year = 0
                date = 0
                for word in line.split('},{'):
                    obj = {}
                    i += 1
                    #print "printing keys"
                    try:
                        #print [for key in word.split(',')].split(':')[1]]
                        temp = []
                        for key in word.split(','):
                            temp.append(key.split(':')[1])
                        
                        obj['rMVMP'] = float(songs[i]['pop'])
                        # huge = 32703
                        obj['fulldate'] = int(songs[i]['year'])*10000 + 101
                        #obj['NAME'] = temp[2]
                        obj['NAME'] = songs[i]['artist'] + " -- " + songs[i]['song']
                        
                         
                        obj['rMVOP'] = float(songs[i]['pop'])*30000.0 - 5000.0
                        #huge = 27706
                        obj['Obs'] = int(temp[4])
                        obj['BHRET3'] = float(temp[5])
                        if 'Relax' in obj['NAME']:
                            print obj
                        if 'Pearl Jam -- Given' in obj['NAME']:
                            print obj
                        ret_list.append('{"rMVMP":'+str(obj['rMVMP'])+','+'"fulldate":'+str(obj['fulldate'])+','+'"NAME":"'+str(obj['NAME'])+'",'+'"rMVOP":'+str(obj['rMVOP'])+','+'"Obs":'+str(obj['Obs'])+','+'"BHRET3":'+str(obj['BHRET3'])+"}")
                        #print obj
                    #year += 1
                    except:
                        j = 34
                        #"not using this"
                    #if year < 70:
                    #    obj['fulldate'] = 20120515
                    #else:
                    #    seventy = 0
                    
                    
                #break
                #print i
                add = ''
                for item in ret_list:
                    add += item + ','
                add = add[:-1]
                #add = add.replace(" ",'')
                #print add
                #add = str(ret_list).replace('"',"")
                #add = add.replace("'",'"')
                #add = add.replace(' ','')
                w.write('\tnytg.ipoData = ['+add+'];\n')
                #w.write('nytg.ipoData='+str(ret_list))
               
                #w.write(line)
            else:
                w.write(line)
        else:
            w.write(line)
            
    f.close()
    w.close()



edit_html()

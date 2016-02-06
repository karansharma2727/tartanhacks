import os
import random
import json
import datetime
import csv

from pydub import AudioSegment

#Make a mix when called
def makemix():

    startseg = [0]
    endseg = []
    fadeoutarr = [0] 
  
    #Get ten songs
    songlist = getSongs("")

    #Make the segments for the 10 songs
    for index in range(len(songlist)-1):
        (starttime, endtime, fadeout) = nextTransition(songlist[index][1], songlist[index+1][1])
        startseg.append(starttime)
        endseg.append(endtime)
        fadeoutarr.append(fadeout)

    endseg.append(0)
    (mix,mixjson) = makesegments(songlist, startseg, endseg, fadeoutarr)
      
    #Create and export the mix
    st = str(datetime.datetime.now())
    mix.export(st+".mp3",format="mp3")

    with open(st+".json", 'w') as outfile:
         json.dump(mixjson, outfile)

#Make full segment 
def makesegments(fullsongarr, startseg, endseg, fadeout):

    songseg = []
    fadeoutarr = []
    songnames = []
    #Makes the segment of the full songs
    for index in range(len(fullsongarr)):
        song = AudioSegment.from_mp3(fullsongarr[index][0])
    	seg1 = makeseg(song, startseg[index], endseg[index])
	songseg.append(seg1)
        songnamepre = fullsongarr[index][0].split("/",)[-1:]
        songname = songnamepre[0].split(".")[0]
        songnames.append(songname)

    return combinemix(songseg, fadeout, songnames)

#Given a full song makes a segment from the song
def makeseg(fullsong, startseg, endseg):

    if (endseg == 0):
        endseg = len(fullsong);
    songfirstchop = fullsong[:endseg]

    songsecondchop = songfirstchop[(startseg-endseg):]

    return songsecondchop

#Song Array of Segments and fadetimes
def combinemix(songarr, fadeoutarr, songnames):

    jsondic = {}
    #loop through the songs combining them
    newseg = songarr[0]
    for index in range(len(songarr)-1):
        newseg = newseg.append(songarr[index+1], crossfade=fadeoutarr[index+1])
        s = len(newseg)/1000
        m,s = divmod(s,60)
        jsondic[songnames[index]] = str(m)+":"+str(s)

    return (newseg,jsondic)

# Know what drop comes next, TODO: Randomize transitions
def nextTransition(s1, s2):
    (sb1, bar1, d1, b1, eb1) = tuple(s1)
    (sb2, bar2, d2, b2, eb2) = tuple(s2)

    # Get time for a single bar in song 1
    barLen1 = (d1 - bar1)

    # Check how many bars are in breakdown in song 1
    barsToEB1 = (b1 - eb1) / barLen1
    
    # Bars in build up of song 2
    barLen2 = (d2 - bar2)
    barsToD2 = (d2 - sb2) / barLen2

    # Build up time matches break down time 
    # Just put the build during break down.
    if round(barsToEB1) == round(barsToD2):
        startTime2 = sb2
        endTime1 = eb1
        fadeOut = sb2 - d2

    # Build up time shorter than breakdown
    # Just put the build during break down.
    elif round(barsToEB1) > round(barsToD2):
        startTime2 = sb2
        breakdownLength = d2 - sb2
        endTime1 = b1 + breakdownLength
        fadeOut = sb2 - d2
        
    # Build up time less than break down time.
    # Just mix in D2 after fixing bars
    else:
        extraBuildUp = (d2 - sb2) - (eb1 - b1)
        startTime2 = sb2 + extraBuildUp
        endTime1 = eb1
        fadeOut = eb1 - b1
 
   
    return (startTime2, endTime1, fadeOut)

def getSongs(genre):
    path = os.getcwd() + "/music/" + "Deep House/"
    jsons = filter(lambda x : x[-5:] == ".json", os.listdir(path))
    
    firstSong = random.choice(jsons)
    firstJSON = json.load(open(path + firstSong))
    
    jsonMaps = map(lambda x : (x, json.load(open(path + x))), jsons)

    res = [(firstSong, firstJSON["cues"])]
    last = (firstSong, firstJSON)
    jsonMaps.remove(last)

    for i in range(1, 9):
        # Get next sont
        nextUp = nextSong(last[1]["bpm"], last[1]["key"], jsonMaps)

        if not nextUp:
            print "Outta songs"
            return map(lambda (a,b) : (path + (a[:-5]) + ".mp3", b),res)
        
        # Remove it from the list of possible songs
        jsonMaps.remove(nextUp)

        # Add to result, and set last song
        res += [(nextUp[0], nextUp[1]["cues"])]
        last = nextUp

    return map(lambda (a,b) : (path + (a[:-5]) + ".mp3", b),res)

def nextSong(bpm, key, jsonMaps):
    bpmRange = [bpm - 5, bpm + 5]
    
    keyNum = int(key[:-1]) 
    possibleKeyNum = [keyNum % 12 + 1, (keyNum - 2) % 12 + 1]
    possibleKey = map(lambda x: str(x) + key[-1] ,possibleKeyNum) + [str(keyNum) + "A", str(keyNum) + "B"]
    
    # Jsons where bpm and key are bounded
    boundBPM = filter(lambda (x,d) : d["bpm"] >= bpmRange[0]
                                 and d["bpm"] <= bpmRange[1], jsonMaps)
    boundKey = filter(lambda (x,d) : d["key"] in possibleKey, boundBPM)

    if len(boundKey) == 0:
        return None
    
    res = random.choice(boundKey)
    return res


csvfile = open('Funk Cues.csv', 'r')

def getMilliSeconds(s):
    r1 = s.split(":")
    sec = int(r1[0])
    msec = float(r1[1])
    return int(((60 * sec) + msec) * 1000)

reader = csv.DictReader(csvfile)
for row in reader:
    SB = getMilliSeconds(row["Start Build"])
    M4 = getMilliSeconds(row["4 Measures"])
    D = getMilliSeconds(row["Drop"])
    B = getMilliSeconds(row["Breakdown"])
    EB = getMilliSeconds(row["End Breakdown"])

    
    jsonfile = open(row["Song"][:-4] + '.json', 'w')
    json.dump({"key" : row["Key"], "bpm" : int(row["Tempo"]),
               "cues" : [SB, M4, D, B, EB]}, jsonfile)  

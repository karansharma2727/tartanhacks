import datetime
import os
import glob

from pydub import AudioSegment

#Return the newest mix
def latestmix():
    return max(glob.iglob('*.[Mm][Pp]3'), key=os.path.getctime)

#Make a mix when called
def makemix():

    fullsongarr = []
    starseg = []
    endseg = []
    fadeout = [] 
 
    nextSong
       
    #Create and export the mix
    st = str(datetime.datetime.now())
    mix.export(st+".mp3",format="mp3")

#Make full segment 
def makesegments(fullsongarr, startseg, endseg, fadeout):

    songseg = []
    fadeoutarr = []
    #Makes the segment of the full songs
    for index in range(len(fullsongarr)):
    	seg1 = makeseg(fullsongarr[index], startseg[index], endseg[index])
	songseg.add(seg1)
        fadeoutarr(fadeout[index]-startseg[index])

    return combinemix(songseg, fadeoutarr)

#Given a full song makes a segment from the song
def makeseg(fullsong, startseg, endseg):

    songfirstchop = fullsong[:endseg]
    songsecondchop = songfirstchop[(startseg-endseg):]

    return songsecondchop

#Song Array of Segments and fadetimes
def combinemix(songarr, fadeoutarr):

    #loop through the songs combining them
    newseg = songarr[0]
    for index in range(len(songarr)):
        newseg = newseg.append(songarr[index+1], crossfade=fadeoutarr[index+1])

    return newseg

def nextSong(s1, s2):
    (sb1, bar1, d1, b1, eb1) = s1
    (sb2, bar2, d2, b2, eb2) = s2

    # Get time for a single bar in song 1
    barLen1 = (d1 - bar1)

    # Check how many bars are in breakdown in song 1
    barsToEB1 = (b1 - eb1) / barLen1
    
    # Bars in build up of song 2
    barLen2 = (d2 - bar2)
    barsToD2 = (sb - d2) / barLen2

    # Build up time matches break down time (or breakdown is longer)
    # Just put the build during break down.
    if round(barsToEB1) <= round(barsToD2):
	startTime = sb2
        endTime = None
        fadeOut = sb2 - d2

    # Build up time less than break down time.
    # Just mix in D2 after fixing bars
    elif barsToEB1 < barsToD2:
        offset = (d2 - sb2) - (eb1 - b1)
        startTime = sb2 + offset
        endTime = None
        fadeOut = eb1 - b1
    return (starTime, endTime, fadeOut)

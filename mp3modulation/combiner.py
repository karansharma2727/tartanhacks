from pydub import AudioSegment

def makemix():

    fullsongarr = []
    starseg = []
    endseg = []
    fadeout = [] 
    

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
    
    return (starTime2, endTime1, fadeOut)

import os
import codecs

# Entry class
class entry:
    def __init__(self,filename,name,writtenDate,year,month,day,time,location,songsList,showList,header,body,editLog,backdated,version,backDate = None):
        # input parameters
        self.filename = filename
        self.id = name
        self.writtenDate = writtenDate
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.location = location
        self.sotd = songsList
        self.show = showList
        self.header = header
        self.body = body
        self.editLog = editLog
        self.backdated = backdated
        self.version = version
        self.backDate = backDate
        # other variables
        self.wordcount = len(self.body.split())
        self.charcount = len(self.body)     #including spaces
        templocations = self.location.split("-->")
        self.locations = []
        for loc in templocations:
            self.locations.append(loc.strip())
    def __str__(self):
        return self.id + " <entry class>"
    def countWords(self):
        return len(self.body.split())
    def listSongs(self):
        for song in self.sotd:
            print(song)

class song:
    def __init__(self,songLine):
        self.songLine = songLine
        self.attr = []
        self.artists = []
        if songLine[0] == "(" and songLine[1].isdigit():
            self.title = songLine
            self.attr
        if "*" in songLine:
            self.attr.append("starred")
            for char in songLine:
                if char == "*":
                    songLine = songLine[1:]
        if ",\"" not in songLine:
            self.title = songLine
            self.attr.append("format anomaly: no quotes")
        else:
            splitSong = songLine.strip().split(",\"")
            self.title = splitSong[0].strip().strip("\"")
            splitArtists = splitSong[1].split(",")
            for artist in splitArtists:
                if "[" in artist:
                    artistAttr = artist.split("[")
                    self.artists.append(artistAttr[0].strip())
                    self.attr.append(artistAttr[1].strip().strip("]"))
                elif "(" in artist:
                    artistAttr = artist.split("(")
                    self.artists.append(artistAttr[0].strip())
                    self.attr.append(artistAttr[1].strip().strip(")"))
                else:
                    self.artists.append(artist.strip())

    def __str__(self):
        return "Title: {}\nArtists: {}\nAttributes: {}".format(self.title,self.artists,self.attr)


# Loop through entries
filesList = os.listdir("entries")
zournal = {}
anomalies = []

for file in filesList:
    if ".md" in file:   # Change this if you change the format you want to be analyzing
        text = codecs.open("entries/" + file,"r","utf-8")
        bigstr = text.read()
        text.close()
        sections = bigstr.split("```")
        header = sections[1].strip()
        headerLines = sections[1].strip().split("\n")
        body = sections[2].strip()
        try:
            editLog = sections[3].strip()
        except:
            editLog = "Not found."
        # Analyze header (metadata)
        if "written" in headerLines[0].lower():
            backdated = True
            writtenDate = headerLines[0].split()[1]
            try:
                writtenTime = headerLines[0].split()[2] + " " + headerLines[0].split()[3]
            except:
                anomalies.append((file,"date error"))
            backDate = headerLines[1].split()[1]
            headerLines = headerLines[2:]
            year = backDate.split("/")[2]
            month = backDate.split("/")[0]
            day = backDate.split("/")[1]
            name = year.strip()[2:4] + month + day
        else:
            backdated = False
            writtenDate = headerLines[0].split()[0]
            writtenTime = headerLines[0].split()[1] + " " + headerLines[0].split()[2]
            headerLines = headerLines[1:]
            year = writtenDate.split("/")[2]
            month = writtenDate.split("/")[0]
            day = writtenDate.split("/")[1]
            name = year.strip()[2:4] + month + day
        """
        # name/id assignment based on file name (not date)
        name = ""
        for char in file:
            if char.isdigit():
                name += char
        """
        if "location" in headerLines[1].lower():
            location = headerLines[1].split(":")[1].strip()
        else:
            if "location" in headerLines[0].lower():
                location = headerLines[0].split(":")[1].strip()
        # generate songs of the day list
        songsList = []
        for songLine in headerLines[3:]:
            songLine = songLine.strip()
            if "current show:" not in songLine.lower():
                if songLine[0] != "(":
                    songsList.append(song(songLine.strip()))
            else:
                break
        
        # version assignment
        if int(name) < 201005:
            version = "1.0.0"
        elif int(name) < 210108:
            version = "1.1.0"
        elif int(name) < 210829:
            version = "1.2.0"
        elif int(name) < 220107:
            version = "1.2.1"
        elif int(name) < 220308:
            version = "1.3.0"
        elif int(name) < 220512:
            version = "1.4.0"
        else:
            version = editLog.split("\n")[1].split(":")[1].strip()
        
        # generate current show(s) list
        showsList = []
        for line in headerLines:
            if "current show:" in line.lower():
                showsList1 = line.strip("current show: ").split(",")
                for show in showsList1:
                    if show != "N/A":
                        showsList.append(show.strip("Current show:").strip("current show:").strip())
        if backdated:
            entryObject = entry(file,name,writtenDate,year,month,day,writtenTime,location,songsList,showsList,header,body,editLog,backdated,version,backDate)
        else:
            entryObject = entry(file,name,writtenDate,year,month,day,writtenTime,location,songsList,showsList,header,body,editLog,backdated,version)
        if name not in zournal:
            zournal[name] = entryObject
        else:
            anomalies.append(file,"duplicate date/id error","duplicate file: " + zournal[name].filename)

if len(anomalies) != 0:
    print("Anomalies detected: " + str(anomalies))

# Analysis Loops
"""
#Most common artists
artFreq = {}
for entry in zournal:
    for song in zournal[entry].sotd:
        for artist in song.artists:
            if artist in artFreq:
                artFreq[artist] += 1
            else:
                artFreq[artist] = 1
artistFreqList = list(artFreq.items())
artistFreqList.sort(key = lambda t: t[1])
artistFreqList.reverse()
for num in range(10):
    print(artistFreqList[num])

# Most common words
wordDict = {}
for entry in zournal:
    words = zournal[entry].body.split()
    for word in words:
        if word.lower() in wordDict:
            wordDict[word.lower()] += 1
        else:
            wordDict[word.lower()] = 1
wordFreqList = list(wordDict.items())
wordFreqList.sort(key = lambda t: t[1])
wordFreqList.reverse()
for num in range(0):
    print(wordFreqList[num])


#How many times a word has been used
target = "nora" #all lower case
targetCount = 0
for entry in zournal:
    for word in zournal[entry].body.split():
        if word.lower() == target:
            targetCount += 1
print(targetCount)


#First use of word
target = "cam"
targetList = []
for entry in zournal:
    for word in zournal[entry].body.split():
        if word.lower() == target.lower():
            if zournal[entry].id not in targetList:
                targetList.append(zournal[entry].id)
for index,entry in enumerate(targetList):
    targetList[index] = int(entry)
targetList.sort()
print(targetList[0])

# Print all locations
for entry in zournal:
    print(zournal[entry].id + " - " + zournal[entry].location + " - " + str(zournal[entry].locations))

# Location frequency
locDict = {}
for entry in zournal:
    for location in zournal[entry].locations:
        if location.lower() in locDict:
            locDict[location.lower()] += 1
        else:
            locDict[location.lower()] = 1
print(locDict)
"""

print(zournal["211227"].sotd())
print(zournal["220117"].sotd())

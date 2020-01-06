from urllib.request import Request, urlopen
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
import pafy
import sys
import re

def getVideoTitle(idVideo):
    url = 'https://www.youtube.com/watch?v='+idVideo
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup = soup.findAll(id="eow-title")
    soup = str(soup)

    clean = re.compile("<.*?>")
    title = re.sub(clean, '', soup)

    title = title.strip("[").strip("]").strip("*\n").strip(" ")
    return title[:-1]


def getVideoDescription(idVideo):
    url = 'https://www.youtube.com/watch?v='+idVideo

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    for p in soup.findAll('p', attrs={'id': 'eow-description'}):
        desc = p.text
        return desc


# return in array format, [0]=hour, [1]=minutes, [2]=seconds
def getVideoDuration(idVideo):
    url = 'https://www.youtube.com/watch?v='+idVideo

    video = pafy.new(url)
    time = video.duration

    return time.split(':')


def getPlaylistDuration(urlPlaylist):
    arrayLinks = getPlaylistLinks(urlPlaylist)
    plDuration = timedelta(hours=0, minutes=0, seconds=0)
    
    for link in arrayLinks:
        videoDuration = getVideoDuration(link)
        plDuration += timedelta(hours=int(videoDuration[0]), minutes=int(videoDuration[1]), seconds=int(videoDuration[2]))
        print(plDuration)
    return plDuration


# return array links
def getPlaylistLinks(urlPlaylist):
    videoLinks = []
    sourceCode = requests.get(urlPlaylist).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    domain = 'https://www.youtube.com'
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            videoLinks.append(href[9:20])
    return videoLinks

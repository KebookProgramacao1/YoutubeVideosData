from urllib.request import Request, urlopen
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
    saida = re.sub(clean, '', soup)

    saida = saida.strip("[").strip("]").strip("*\n").strip(" ")
    return saida[:-1]


def getVideoDescription(idVideo):
    url = 'https://www.youtube.com/watch?v='+idVideo

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    for p in soup.findAll('p', attrs={'id': 'eow-description'}):
        saida = p.text
        return saida


def getVideoDuration(idVideo):
    url = 'https://www.youtube.com/watch?v='+idVideo

    video = pafy.new(url)
    video = video.duration
    video = video.split(':')

    if int(video[0]) <= 0:
        video = video[1]+':'+video[2]
    else:
        video = video[0]+':'+video[1]+':'+video[2]
    return video

     
def getPlaylistLinks(urlPlaylist):
    sourceCode = requests.get(urlPlaylist).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    domain = 'https://www.youtube.com'
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            print(link.string.strip())
            print(domain + href + '\n')

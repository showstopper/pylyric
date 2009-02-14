# -*- coding: utf-8 -*-

import urllib2
import xmlparsing



BASEURL = "http://lyricwiki.org/api.php"
SONG    = "&song="
ARTIST  = "&artist="
FORMAT  = "&fmt="
FUNC    = "?func="
      

def fetch_song(artist, song, fmt="xml"):
    
    func = "getSong"
    artist = artist.replace(" ", "_")
    
    song = song.replace(" ", "_")
    
    f = urllib2.urlopen("".join([BASEURL, FUNC, func, ARTIST, 
                        artist.encode("utf-8"), SONG, song.encode("utf-8"), FORMAT, fmt]))
    data = f.read()
    f.close()
    return data

def get_song(artist, title):
    
    xml_lyric = fetch_song(artist, title)
    lyric = xmlparsing.parse_song_file(xml_lyric)
    song = xmlparsing.Song(artist_name=artist, 
                                  title=title, 
                                  lyric=lyric
                                 )
    return  lyric
       
def fetch_albums(artist, fmt="xml"):
      
    func = "getSong"
    artist = artist.replace(" ", "_")
    url = "".join([BASEURL, FUNC, func, ARTIST,
                         artist, FORMAT, fmt])
    print url
    return load_link(url)
        
def get_albums(artist):
    
    xml_lyric = fetch_albums(artist)
    
    return xmlparsing.parse_disco(xml_lyric)
  
def load_link(url):
    
    f = urllib2.urlopen(url.encode("utf-8"))
    data = f.read()
    f.close()
    return data   



    

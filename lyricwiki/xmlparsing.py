# -*- coding: utf-8
from xml.etree import cElementTree as etree
import lyricwiki



class Artist(object):
    
    def __init__(self, artist_name):
        
        self.name = artist_name
        self.albums = {}

class Album(object):
    
    def __init__(self, artist_name, album_name):
        
        self.artist_name = artist_name
        self.album_name = album_name
        self.songs = {}

class Song(object):
    
    def __init__(self, artist_name, title, album_name=None, lyric=None):
        
        self.artist_name = artist_name
        self.title = title
        self.album_name = album_name
        self._lyric = lyric
        
    @property
    def lyric(self):
        
        if not self._lyric:
            self._lyric = lyricwiki.get_song(self.artist_name, self.title)
        return self._lyric

class Xml_Album_Object(object):
    
    def __init__(self, album_object, song_objects):
        self.album_object = album_object
        self.song_objects = song_objects
        self.album_name = album_object.text
        
def parse_song_file(xml_file):
    
    xml_object = etree.fromstring(xml_file)
    return xml_object.findtext("lyrics")
    
def _get_album_objects(xml_object):
    
    album_objects = xml_object.find("albums")
    for index, album in enumerate(album_objects):
        if album.tag == "album":
            yield Xml_Album_Object(album, album_objects.getchildren()[index+3])
            
def parse_disco(xml_file):
    
    xml_object = etree.fromstring(xml_file)
    artist_name = xml_object.findtext("artist")
    artist = Artist(artist_name)
   
    for album_object in _get_album_objects(xml_object):
        album_name = album_object.album_name
        if not album_name in artist.albums:
            artist.albums[album_name] = (Album(artist_name, album_name))
                
        for song in album_object.song_objects.getchildren():
            print song.text
            artist.albums[album_name].songs[song.text] = Song(artist_name=artist_name, 
                                                                  album_name=album_name, 
                                                                  title=song.text
                                                                )
                    
    return artist
    

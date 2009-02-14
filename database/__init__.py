#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import os.path
import shelve
import codecs

DBNAME = "lyric.db"
PATH = os.path.join(os.getenv("HOME"),".pylyric")

def escape_decorator(target):
    
    def wrapper(**kwargs):
        
        if not kwargs.get("artist"):
            raise KeyError()
        
        for key in kwargs:
            if not key == "lyric":
                kwargs[key] = replace(kwargs[key])
            
        return target(artist=kwargs.get("artist"), 
                      album=kwargs.get("album"), 
                      song=kwargs.get("song"), 
                      lyric=kwargs.get("lyric")
                     )
    def replace(string):
       
        replace_chars = {"Ä" : "Ae", 
                         "ä" : "ae", 
                         "Ö" : "Oe", 
                         "ö" : "oe",
                         "Ü" : "Ue",
                         "ü" : "ue"
                        }
        string = string.replace(" ", "_")
        string = string.replace("/", "_")
        for char in replace_chars:
            string = string.replace(char, replace_chars[char])
        return string
        
    return wrapper
            
def path_decorator(target):
    
    def wrapper(**kwargs):
        
        artist = kwargs.get("artist")
        if not os.path.isdir(os.path.join(PATH, artist)):
            os.mkdir(os.path.join(PATH, artist))
        if kwargs.get("album"):
            album = kwargs.get("album")
            
            if not os.path.isdir(os.path.join(PATH, artist, album)):
                os.mkdir(os.path.join(PATH, artist, album))
        return target(artist=kwargs.get("artist"), 
                      album=kwargs.get("album"), 
                      song=kwargs.get("song"), 
                      lyric=kwargs.get("lyric")
                    )
    return wrapper


@escape_decorator 

def _lyric_exists(**kwargs):
    
    artist = kwargs.get("artist")
    song = kwargs.get("song")
    album = kwargs.get("album")
    path = kwargs.get("path")
    
    if path:
        return os.path.isfile(path)
    else:
        
        if album:
            return os.path.isfile(generate_path(artist=artist, album=album, song=song))
        else:
            return os.path.isfile(generate_path(artist=artist, song=song))
    
        
@escape_decorator
@path_decorator
     
def write_lyric(**kwargs):
    
    if not kwargs.get("song"):
        raise KeyError()
    if not kwargs.get("lyric"):
        kwargs["lyric"] = "Not found"
    artist_path = os.path.join(PATH, kwargs["artist"])
    
    if not _lyric_exists(artist=kwargs["artist"], 
                         song=kwargs["song"], 
                         album=kwargs["album"]
                        ):
        if kwargs.get("album"):    
            
            lyric_path = os.path.join(PATH, 
                                      kwargs["artist"], 
                                      kwargs["album"], 
                                      kwargs["song"],
                                    )
            with codecs.open(lyric_path , "wb", "utf-8") as f:
                f.write(kwargs["lyric"])
        
        else:
            lyric_path = os.path.join(PATH, 
                                      kwargs["artist"],
                                      kwargs["song"]
                                    )
            with codecs.open(lyric_path , "wb", "utf-8") as f:
                f.write(kwargs["lyric"])


@escape_decorator

def get_lyrics(**kwargs):
    if not kwargs.get("song"):
        raise KeyError
    path = generate_path(artist=kwargs.get("artist"), song=kwargs.get("song"), album=kwargs.get("album"))
    if not _lyric_exists(artist=kwargs.get("artist"), album=kwargs.get("album"), song=kwargs.get("song")):
        lyric = "Not found"
    else:
        with codecs.open(path , "rb", "utf-8") as f:
            lyric = f.read()
    return lyric
 
@escape_decorator

def generate_path(**kwargs):
    if not kwargs.get("song"):
        raise KeyError
    if kwargs.get("album"):
        path = os.path.join(PATH, kwargs.get("artist"), kwargs.get("album"), kwargs.get("song"))
    else:
        path = os.path.join(PATH, kwargs.get("artist"), kwargs.get("song"))
                              
    return path
    

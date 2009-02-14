#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       unbenannt.py
#       
#       Copyright 2009  <yannic@hiac>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
import os.path
import shelve
import codecs

DBNAME = "lyric.db"
PATH = os.path.join(os.getenv("HOME"),".pylyric")

def escape_decorator(target):
    
    def wrapper(**kwargs):
        
        if not "artist" in kwargs:
            raise KeyError() # there HAS TO BE an artist ;=)
        for key in kwargs:
            if key =="lyric":
                pass
            else:
                kwargs[key] = replace(kwargs[key])
        
        return target(artist=kwargs.get("artist"), 
                      album=kwargs.get("album"), 
                      song=kwargs.get("song"), 
                      lyric=kwargs.get("lyric")
                    )
    
    def replace(string):
        string = string.replace(" ", "_")
        string = string.replace("/", "_")
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
    
    if not "song" in kwargs:
        raise KeyError()
    if kwargs.get("album"):
        return os.path.isfile(os.path.join(PATH, 
                                           kwargs["artist"], 
                                           kwargs["album"], 
                                           kwargs["song"]
                                          ))
    else:
        return os.path.isfile(os.path.join(PATH, 
                                           kwargs["artist"], 
                                           kwargs["song"]
                                        ))
@escape_decorator
@path_decorator        
def write_lyric(**kwargs):
    
    if not "song" in kwargs or not "lyric" in kwargs:
        raise KeyError()
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


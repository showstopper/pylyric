#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import database
import lyricwiki



PATH = os.path.join(os.getenv("HOME"),".pylyric")

def init():
    if not os.path.isdir(PATH):
        os.mkdir(PATH)

def main():
    
    init()
    artist = raw_input("Artist: ")
    a = lyricwiki.get_albums(artist)
    
    # the following code loads the lyrics of the disco of an artist and save it to ~./pylyric 
    
    for album in a.albums:
       
        for song in a.albums[album].songs:
            
            print "lyric:", a.albums[album].songs[song].lyric
            database.write_lyric(artist=a.name, song=a.albums[album].songs[song].title, lyric=a.albums[album].songs[song].lyric, album=album)
   
   
if __name__ == '__main__':
    main()

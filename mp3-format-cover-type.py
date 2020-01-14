#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import eyed3
import time

REMOVE_TAG_ID3V1 = False
REMOVE_TAG_GENRE = False
REMOVE_TAG_ALBUM = False
REMOVE_TAG_ALBUM_ARTIST = False

err = 0
suc = 0
inv = 0

t0 = time.time()
for path, subdirs, files in os.walk(os.getcwd()):
    for name in files:
        if os.path.isfile(os.path.join(path, name)) and name.lower().endswith(".mp3"):
            tempname = "mytemp.mp3"
            os.chdir(path)
            try:
                if os.path.exists(tempname):
                    os.remove(tempname)
                os.rename(name, tempname)
                audio = eyed3.load(tempname)
                if audio == None or audio.tag.images == None:
                    raise
                if REMOVE_TAG_ID3V1:
                    audio.tag.remove(tempname, version=eyed3.id3.ID3_V1, preserve_file_time=True)
                if REMOVE_TAG_GENRE:
                    audio.tag.genre = None
                if REMOVE_TAG_ALBUM:
                    audio.tag.album = None
                if REMOVE_TAG_ALBUM_ARTIST:
                    audio.tag.album_artist = None
                audio.tag.save()
                description = audio.tag.images[0].description
                removed = audio.tag.images.remove(description)
                if removed.picture_type == eyed3.id3.frames.ImageFrame.OTHER:
                    inv = inv+1
                    raise
                audio.tag.images.set(0, removed.image_data, removed.mime_type, description)
                audio.tag.save()
                suc = suc+1
            except:
                err = err+1
            os.rename(tempname, name)
t0 = time.time()-t0

print("Total files     : %d" % (suc+err))
print("  Success       : %d" % (suc))
print("  Invalid       : %d" % (inv))
print("  Error         : %d" % (err-inv))
print("Total time      : %fs" % (t0))


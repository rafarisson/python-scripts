#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install eyed3

import os
import eyed3
import time

REMOVE_TAG_ID3V1 = True
REMOVE_TAG_GENRE = True
REMOVE_TAG_ALBUM = True
REMOVE_TAG_ALBUM_ARTIST = True
CONVERT_TAG_TO_FILENAME = True

proc = {}

t0 = time.time()
for path, subdirs, files in os.walk(os.getcwd()):
	for name in files:
		if os.path.isfile(os.path.join(path, name)) and name.lower().endswith(".mp3"):
			status = { 'status': 'W', 'error': None, 'name': '' }
			tempname = 'mytemp.mp3'
			try:
				os.chdir(path)
				if os.path.exists(tempname):
					os.remove(tempname)
				os.rename(name, tempname)
				audio = eyed3.load(tempname)
				if audio != None:
					if REMOVE_TAG_ID3V1:
						audio.tag.remove(tempname, version=eyed3.id3.ID3_V1, preserve_file_time=True)
					if REMOVE_TAG_GENRE:
						audio.tag.genre = None
					if REMOVE_TAG_ALBUM:
						audio.tag.album = None
					if REMOVE_TAG_ALBUM_ARTIST:
						audio.tag.album_artist = None
					audio.tag.save()
					if audio.tag.images != None and len(audio.tag.images) > 0:
						description = audio.tag.images[0].description
						removed = audio.tag.images.remove(description)
						if removed.picture_type != eyed3.id3.frames.ImageFrame.OTHER:
							audio.tag.images.set(0, removed.image_data, removed.mime_type, description)
							audio.tag.save()
							status['status'] = 'C'
						else:
							status['status'] = 'I'
					else:
						status['status'] = 'N'
					status['name'] = name;
					if CONVERT_TAG_TO_FILENAME:
						status['name'] = audio.tag.title + ' - ' + audio.tag.artist + '.mp3'
						if name != status['name']:
							status['status'] += 'R'
					os.rename(tempname, status['name'])
			except Exception as e:
				status['status'] = 'E'
				status['error'] = str(e)
			proc[name] = status
t0 = time.time()-t0

print('--------------------------------------')
print('total time:', t0)
print('total files:', len(proc))
for k in proc:
	e = ''
	if proc[k]['error'] != None:
		e = '** ' + proc[k]['error']
	print('  {:5s}{:70s} {:s}'.format(proc[k]['status'], proc[k]['name'], e))
print('--------------------------------------')


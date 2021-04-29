#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install eyed3

import argparse
import eyed3
from pathlib import Path

parser = argparse.ArgumentParser(description='mp3 tags for Renault navmedia')
parser.add_argument('path',
					nargs='?',
					action='store',
					default='.',
					help='path or mp3 files')
parser.add_argument('-p',
					action='store_true',
					dest='preserve_id3v1',
					help='preserve id3v1 tags')

args = parser.parse_args();

# on exception, see terminal messages
wait_input = False;

for p in args.path:
	p = Path(p)
	if not p.exists():
		continue
	files = (p.is_file() and p.exists()) and [p] or p.glob('**/*.mp3')
	for f in files:
		try:
			audio = eyed3.load(f)
			if audio is not None:
				if not args.preserve_id3v1:
					audio.tag.remove(f, version=eyed3.id3.ID3_V1, preserve_file_time=True)
				if audio.tag.images is not None and len(audio.tag.images) > 0:
					for i in audio.tag.images:
						i.description = ''
						if i.picture_type is not eyed3.id3.frames.ImageFrame.OTHER:
							i.picture_type = eyed3.id3.frames.ImageFrame.OTHER
				audio.tag.album_artist = None
				audio.tag.genre = None
				audio.tag.save(preserve_file_time=True)
				tag_filename = audio.tag.title + ' - ' + audio.tag.artist
				if Path(f).stem != tag_filename:
					audio.rename(tag_filename, preserve_file_time=True);
			print('{0} -> ok'.format(f));
		except Exception as e:
			wait_input = True
			print('{0} -> error: {1}'.format(f, str(e)))

# no exception, bye
if wait_input:
	input()

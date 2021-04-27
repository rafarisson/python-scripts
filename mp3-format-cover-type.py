#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install eyed3

import argparse
import eyed3
import pathlib

parser = argparse.ArgumentParser(description='mp3 tags for Renault navmedia')
parser.add_argument('files',
					action='store',
					nargs='+',
					help='mp3 files')
parser.add_argument('-t', 
					action='store_true',
					dest='preserve_filename',
					help='preserve file name (disable convert tag \'title - artist\' to file name)')
parser.add_argument('-p',
					action='store_true',
					dest='preserve_id3v1',
					help='preserve id3v1 tags')

args = parser.parse_args();

# on exception, see terminal messages
wait_input = False;

for f in args.files:
	try:
		audio = eyed3.load(f)
		if audio is not None:
			if not args.preserve_id3v1:
				audio.tag.remove(f, version=eyed3.id3.ID3_V1, preserve_file_time=True)
			if audio.tag.images is not None and len(audio.tag.images) > 0:
				for i in audio.tag.images:
					if i.picture_type is not eyed3.id3.frames.ImageFrame.OTHER:
						i.picture_type = eyed3.id3.frames.ImageFrame.OTHER
			audio.tag.save(preserve_file_time=True)
			if not args.preserve_filename:
				tag_filename = audio.tag.title + ' - ' + audio.tag.artist
				if pathlib.Path(f).stem != tag_filename:
					audio.rename(tag_filename, preserve_file_time=True);
		print(f + ' -> ok');
	except Exception as e:
		wait_input = True
		print(f + ' -> error: ' + str(e))

# no exception, bye
if wait_input:
	input()

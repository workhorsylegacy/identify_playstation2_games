#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os
import json
import read_udf

# Load the database
with open('official_ps2_db.json', 'rb') as f:
	official_db = json.loads(f.read())

# All possible serial number prefixes
# Sorted by the number of games that use that prefix
PREFIXES = [
	'SLPM', # 2616 games
	'SLES', # 2420 games
	'SCES', # 2387 games
	'SLUS', # 1857 games
	'SLPS', # 1171 games
	'SCUS', # 386 games
	'SCPS', # 284 games
	'SCAJ', # 217 games
	'SLKA', # 122 games
	'SLAJ', # 65 games
	'SCKA', # 46 games
	'TCPS', # 31 games
	'SCED', # 13 games
	'SLED', # 6 games
	'PBPX', # 3 games
	'TCES', # 2 games
	'PAPX', # 1 game
	'PBPS', # 1 game
	'PCPX', # 1 game
]

def get_playstation2_game_info(file_name):
	# Skip if not an ISO
	if not os.path.splitext(file_name.lower())[1] == '.iso':
		return None

	# Look at each file in the ISO
	root_directory = None
	try:
		root_directory = read_udf.read_udf_file(file_name)
	except:
		return None
		
	for sub_entry in root_directory.all_entries:

		# Sanitize the file name with the serial number
		serial_number = sub_entry.file_identifier.upper().replace('.', '').replace('_', '-')

		# Skip if the serial number has an invalid prefix
		if serial_number.split('-')[0] not in PREFIXES:
			continue

		# Skip if unknown serial number
		if serial_number not in official_db:
			continue

		# Look up the proper name
		proper_name = official_db[serial_number]

		return (serial_number, proper_name)

	return None

games = "E:/Sony/Playstation2/"
for root, dirs, files in os.walk(games):
	for file in files:
		# Get the full path
		entry = root + '/' + file

		# Skip if not an ISO
		if not os.path.splitext(entry.lower())[1] == '.iso':
			continue

		info = get_playstation2_game_info(entry)
		print(info)

		
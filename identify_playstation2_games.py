#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (c) 2015, Matthew Brennan Jones <matthew.brennan.jones@gmail.com>
# A module for identifying Sony Playstation 2 games with Python 2 & 3
# It uses a MIT style license
# It is hosted at: https://github.com/workhorsy/identify_playstation2_games
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys, os
import json
import read_udf

# Load the databases
with open('db_playstation2_official_au.json', 'rb') as f:
	db_playstation2_official_au = json.loads(f.read())

with open('db_playstation2_official_eu.json', 'rb') as f:
	db_playstation2_official_eu = json.loads(f.read())

with open('db_playstation2_official_jp.json', 'rb') as f:
	db_playstation2_official_jp = json.loads(f.read())

with open('db_playstation2_official_ko.json', 'rb') as f:
	db_playstation2_official_ko = json.loads(f.read())

with open('db_playstation2_official_us.json', 'rb') as f:
	db_playstation2_official_us = json.loads(f.read())


# FIXME: Update this to have more prefixes and the new count
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
		raise Exception("Not an ISO file.")

	# Look at each file in the ISO
	root_directory = None
	try:
		root_directory = read_udf.read_udf_file(file_name)
	except:
		raise Exception("Failed to read as a DVD ISO.")
		
	for sub_entry in root_directory.all_entries:

		# Sanitize the file name with the serial number
		serial_number = sub_entry.file_identifier.upper().replace('.', '').replace('_', '-')

		# Skip if the serial number has an invalid prefix
		if serial_number.split('-')[0] not in PREFIXES:
			continue

		# Look up the proper name
		proper_name = None
		if serial_number not in db_playstation2_official_au:
			proper_name = db_playstation2_official_au[serial_number]
		elif serial_number not in db_playstation2_official_eu:
			proper_name = db_playstation2_official_eu[serial_number]
		elif serial_number not in db_playstation2_official_jp:
			proper_name = db_playstation2_official_jp[serial_number]
		elif serial_number not in db_playstation2_official_ko:
			proper_name = db_playstation2_official_ko[serial_number]
		elif serial_number not in db_playstation2_official_us:
			proper_name = db_playstation2_official_us[serial_number]

		# Skip if unknown serial number
		if not proper_name:
			continue

		return (serial_number, proper_name)

	raise Exception("Failed to find game in database.")



		
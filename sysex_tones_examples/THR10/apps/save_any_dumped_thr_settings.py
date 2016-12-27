#!/usr/bin/env python
""" Example app that waits indefinitely, listening to the THR device, and saves any settings dumps to files with numbered prefixes.

	Turn the device off when you want to exit the app.
"""

# Copyright (c) 2016
#
# This project is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.


import sys
import errno

from sysex_tones.THR10 import THR10


def save_settings_dumps( infilename, outfilename, savefilenamepostfix ):
	""" Save settings dumps to N_savefilenamepostfix. """
	thr = THR10( infilename, outfilename )
	thr.open_infile_wait_indefinitely()
	thr.request_current_settings()
	count = 0
	while thr:
		# read settings dumps
		# first the inital requested dump
		# then any dumps occuring when pressing preset buttons on the THR device
		try:
			attempt = thr.extract_dump()
			# only save settings dumps
			if attempt:
				# output settings into a numbered file
				savefilename = '%i_%s' % (count, savefilenamepostfix)
				savefile = open( savefilename, 'wb' )
				savefile.write( bytearray( attempt['dump'] ) )
				savefile.close()
				savefile = None
				count += 1
		except IOError as error:
			if error.errno == errno.ENODEV: # device disconnected
				thr.close_infile()
				thr = None


if __name__ == '__main__':
	if len( sys.argv ) == 4:
		save_settings_dumps( sys.argv[1], sys.argv[2], sys.argv[3] )
	else:
		print( 'Usage: %s MIDIINPUTDEVFILENAME MIDIOUTPUTDEVFILENAME OUTPUTFILENAMEPOSTFIX' % (sys.argv[0]) )


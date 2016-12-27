#!/usr/bin/env python
""" Example app that listens for MIDI from the THR device, displaying any recognized MIDI as settings text.

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

import sysex_tones
import sysex_tones.THR

from sysex_tones.THR10 import THR10


def process_file( infilename ):
	""" Listen to the THR device via the infilename, output any data sent by the device. """
	thr = THR10()
	thr.open_infile_wait_indefinitely( infilename )
	recognized = [sysex_tones.THR.CONSTANTS.THR10_MODEL_NAME]
	model = ''
	context = ''
	while thr:
		try:
			# break the stream up into SysEx commands and process each one
			for sysex in thr.extract_sysex_from_infile():
				heartbeat = thr.find_thr_heartbeat_model( sysex )
				if heartbeat: # the heartbeat happens about twice a second, when device is connected
					if not model: # only show model name once
						model = heartbeat
						print( 'Model %s' % (model) )
						if model not in recognized:
							print( '%s are not recognized.' % (model) )
				else: # it isn't a device heartbeat, maybe it's settings data
					detected = thr.detect_midi_dump( sysex )
					if detected: # it's a dump of complete current settings
						thr.print_sysex_data( sysex, detected['data'] )
					else: # maybe it's a settings command (probably an on-amp change)
						command = thr.find_thr_command( sysex, context )
						if command:
							print( 'THR command', command )
							if 'context' in command: # used to track 'sub' commands, if possible
								context = command['context']
						else:
							print( 'unrecognized', context, sysex_tones.convert_bytes_to_hex_string( sysex ) )
		except IOError as error:
			if error.errno != errno.EAGAIN: # device disconnected
				thr.close_infile()
				thr = None


if __name__ == '__main__':
	if len( sys.argv ) > 1:
		process_file( sys.argv[1] )
	else:
		print( 'Usage: %s MIDIINPUTDEVFILENAME' % (sys.argv[0]) )


#!/usr/bin/env python
""" Example app that reads the current THR device settings, changes the name of the settings, and writes it back to the device. """

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
import sysex_tones.THR10


def change_settings_name( infilename, outfilename, newsettingsname ):
	""" Ask the THR device for a settings dump, change the name in it, and write it back to the device. """
	newname = sysex_tones.convert_from_stream( newsettingsname.strip() )
	# ask the device to send a dump of the current settings, so the Name can be changed
	thr = sysex_tones.THR10.THR10( infilename, outfilename )
	thr.open_infile_wait_indefinitely()
	thr.request_current_settings()
	while thr:
		try:
			attempt = thr.extract_dump()
			if attempt:
				# print it out, before the change, for visual double checking
				thr.print_sysex_data( attempt['sysex'], attempt['dump'] )
				# replace old name with new name
				newsysex = sysex_tones.THR.change_name_of_settings( newname, attempt['sysex'] )
				# verify the change
				detected = thr.detect_midi_dump( newsysex )
				if detected:
					# print it out again, after the change, for visual double checking
					thr.print_sysex_data( newsysex, detected['data'] )
					# send the updated data to the device, to set the new name
					thr.write_data_to_outfile( newsysex )
					thr.close_infile()
					thr = None
					break # leave the loop, now that the name has been changed
		except IOError as error: # device disconnected
			if error.errno == errno.ENODEV and thr:
				thr.close_infile()
				thr = None


if __name__ == '__main__':
	if len( sys.argv ) == 4:
		change_settings_name( sys.argv[1], sys.argv[2], sys.argv[3] )
	else:
		print( 'Usage: %s MIDIINPUTDEVFILENAME MIDIOUTPUTDEVFILENAME "new settings name"' % (sys.argv[0]) )


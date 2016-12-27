#!/usr/bin/env python
""" Example app that converts text settings files into MIDI bytes and sends it to the THR device. """

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

from sysex_tones.THR10 import THR10


def write_to_midi( outfilename, infilenames ):
	""" Send converted settings text from infilenames to outfilename as MIDI. """
	thr = THR10()
	thr.open_outfile( outfilename )
	for infilename in infilenames:
		thr.write_text_to_midi( infilename )
	thr.close_outfile()


if __name__ == '__main__':
	if len( sys.argv ) >= 3:
		write_to_midi( sys.argv[1], sys.argv[2:] )
	else:
		print( 'Usage: %s MIDIOUTPUTDEVFILENAME configfilenames' % (sys.argv[0]) )


#!/usr/bin/env python
""" Example app that displays text settings conversions of THR settings files, dump files, or files containing THR SysEx commands. """

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


def process_files( infilenames ):
	""" Convert each infilenames into text settings. """
	thr = THR10()
	for infilename in infilenames:
		lines = thr.convert_infile_to_text( infilename )
		if lines:
			for line in lines:
				print( line )
		else:
			print( 'No THR SysEx found.' )


if __name__ == '__main__':
	if len( sys.argv ) >= 2:
		process_files( sys.argv[1:] )
	else:
		print( 'Usage: %s inputfilenames' % (sys.argv[0]) )


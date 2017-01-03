""" Interfaces for managing MIDI devices via SysEx control messages. """

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


__version__ = '0.0.2'


from sysex_tones.BasicIO import BasicIO

import os as _os
import time as _time
import fcntl as _fcntl
import select as _select
import collections as _collections

import sysex_tones.CONSTANTS as _CONSTANTS


def ternary_operator( state, nonzero, zero ):
	""" Returns nonzero if state is, otherwise zero if state is not. """
	return nonzero if state else zero


def get_minmax( value, minimum, maximum ):
	""" Check minimum <= value >= maximum, set to upper or lower limit if out of bounds, then return value. """
	retval = value
	if value < minimum:
		retval = minimum
	if value > maximum:
		retval = maximum
	return retval


def convert_to_midi_int( i ):
	""" Convert i (max 0x3fff) into a MIDI int (7 bit bytes). """
	return ((i & 0x3f80) << 1) | (i & 0x007f)


def convert_from_midi_int( midiint ):
	""" Convert midiint, a MIDI int (7 bit bytes), into an int (max 0x3fff). """
	return (((midiint & 0x7f00) >> 1) | (midiint & 0x007f))


def convert_from_midi_int_ints( data ):
	""" Convert data (two bytes in MIDI int format) into an int. """
	return (((data[0] & 0x007f) << 7) | (data[1] & 0x007f))


def convert_from_midi_to_string( data ):
	""" Convert data into a string, truncate on first '\0' (if present), ignore any ASCII values less than ord( ' ' ) and greater than ord( '~' ). """
	low = ord( ' ' )
	high = ord( '~' )
	if 0 in data:
		data = data[:data.index( 0 )]
	return ''.join( [chr( x ) for x in data if x >= low and x <= high] )


def convert_bytes_to_hex_string( data ):
	""" Convert data into a string of space delimited text hex values. """
	return ' '.join( ['%02x' % (b) for b in data] )


def convert_to_stream( data ):
	""" Convert data into a bytearray, for .write() compatibility. """
	return bytearray( data )


def convert_from_stream( string ):
	""" Convert a string from a stream, via .read(), into a list of bytes. """
	return [ord( c ) for c in string]


def extract_settings( text ):
	""" Parse text, returning extracted settings labels and their associated values.

	a format example (text LABEL and VALUENAMES are not case sensitive, when parsed)

	LABEL: VALUENAME 1, FLOATING POINT VALUENAME 2.3, SPECIAL VALUENAME text
	# ignored (blank lines are ignored too)
	ANOTHERLABEL: ETC ..., SPACES ALLOWED IN LABELS not_values

	"""
	text = text.strip()
	setting = ''
	valuelist = ''
	values = _collections.OrderedDict()
	if text and not text.startswith( '#' ): # ignore blank lines, config comments begin with #
		(setting, valuelist) = text.split( ':', 1 )
		setting = setting.strip().lower()
		valuelist = valuelist.strip()
		if setting != 'name':
			for valuepair in valuelist.split( ',' ):
				pair = valuepair.strip().rsplit( ' ', 1 )
				valuename = pair[0].strip().lower()
				if len( pair ) == 1:
					values[valuename] = None
				else:
					val = pair[1].strip()
					if '.' in val and val.strip( '.' ).isdigit():
						try:
							val = float( val )
						except ValueError:
							pass
					elif val.isdigit():
						try:
							val = int( val )
						except ValueError:
							pass
					values[valuename] = val
	return (setting, valuelist, values)


def extract_midi_sysex( data ):
	""" Returns a list of individual SysEx commands found in data. """
	retval = []
	index = 0
	count = len( data )
	while index < count:
		if data[index] == _CONSTANTS.SYSEX_START[0]:
			start = index
			index += 1
			while index < count:
				if data[index] == _CONSTANTS.SYSEX_STOP[0]:
					retval.append( data[start:index + 1] )
					break
				index += 1
		index += 1
	return retval


def extract_command_payload( data, commandprefix ):
	""" If data is a sysex command, and has a commandprefix, return the contents of the command. """
	retval = []
	if data[-1] == _CONSTANTS.SYSEX_STOP[0]:
		count = len( commandprefix )
		if data[:count] == commandprefix:
			retval = data[count:-1]
	return retval


def read_from_stream( inputfile, maxsize=4096 ):
	""" Read at most maxsize bytes from inputfile. """
	return convert_from_stream( inputfile.read( maxsize ) )


def extract_sysex_from_stream( inputfile, maxsize=4096 ):
	""" Return a list sysex commands extracted from inputfile, after reading at most maxsize bytes. """
	return extract_midi_sysex( read_from_stream( inputfile, maxsize ) )


def is_data_available( infile, timeout=0.3 ):
	""" Check infile for available data, using timeout to wait for n.n seconds, returning an empty sequence if no data is available. """
	return _select.select( [infile], [], [], timeout ) # check for available data


def open_output_stream( filename ):
	""" Open filename for unbuffered output. """
	return open( filename, 'wb', 0 )


def open_input_stream( filename ):
	""" If possible, open the filename for unbuffered and non-blocking reading. """
	retval = None
	if _os.path.exists( filename ) and _os.access( filename, _os.R_OK ):
		retval = open( filename, 'rb', 0 )
		flags = _fcntl.fcntl( retval, _fcntl.F_GETFL ) | _os.O_NONBLOCK
		_fcntl.fcntl( retval, _fcntl.F_SETFL, flags )
	return retval


def open_input_wait_indefinitely( filename, delay=0.3 ):
	""" Attempt to open filename for unbuffered and unblocked reading, waiting for n.n delay seconds between attempts (to avoid CPU waste). """
	retval = None
	while not retval:
		retval = open_input_stream( filename )
		if not retval:
			_time.sleep( delay ) # wait before trying again
	return retval


def settings_to_string( prefix, label, settings, values ):
	""" Convenience function that formats long settings strings. """
	retval = '%s%s: ' % (prefix, label)
	count = 0
	limit = len( settings )
	if len( values ) < limit:
		limit = len( values )
	while count < limit:
		form = '%s%s'
		if count > 0:
			retval += ', '
		valtype = type( values[count] )
		if valtype == str:
			if settings[count]:
				form += ' %s'
			else:
				form += '%s'
		elif valtype == int:
			form += ' %i'
		retval = form % (retval, settings[count], values[count])
		count += 1
	return retval


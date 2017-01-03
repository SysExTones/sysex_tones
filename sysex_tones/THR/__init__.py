""" Manage THR settings via MIDI SysEx. """

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


from sysex_tones.THR.THR import THR

import os as _os

from sysex_tones.THR import CONSTANTS as _THR_CONSTANTS


def calculate_checksum( data ):
	""" Calculate the Yamaha checksum. """
	return (((~sum( data )) + 1) & 0x7f)


def is_valid_checksum( data, checksum ):
	""" Check the validity of the Yamaha checksum. """
	return checksum == calculate_checksum( data )


def is_known_size( size ):
	""" Check if size is a typical THR dump or settings file size, return the size if valid, otherwise return 0. """
	retval = 0
	if size in [_THR_CONSTANTS.THR_DUMP_SIZE, _THR_CONSTANTS.THR_FILE_SIZE, _THR_CONSTANTS.THR_SYSEX_SIZE]:
		retval = size
	return retval


def get_known_file_size( filename ):
	""" Check if the file named filename is less than or equal to typical THR dump or settings file sizes, return the size if valid, otherwise return 0. """
	return is_known_size( _os.stat( filename ).st_size )


def change_name_of_settings( name, data ):
	""" Replace the old name with a new name in the THR MIDI data, returns an altered copy of data. """
	retval = data[:] # make a copy of the data
	offset = _THR_CONSTANTS.THR_DUMP_OFFSET
	low = ord( ' ' )
	high = ord( '~' )
	size = len( name )
	count = 0
	# copy the name, truncating if too long
	while count < size and count < _THR_CONSTANTS.THR_SETTINGS_NAME_SIZE:
		val = name[count]
		if val == 0:
			break
		if val >= low and val <= high:
			retval[count + offset] = name[count]
		count += 1
	# set any remaining trailing old name data to '\0'
	while count < _THR_CONSTANTS.THR_SETTINGS_NAME_SIZE:
		retval[count + offset] = 0
		count += 1
	# update the checksum, now that the name has been changed
	offset = len( _THR_CONSTANTS.THR_DUMP_HEADER_PREFIX )
	retval[-2] = calculate_checksum( retval[offset:-2] )
	return retval


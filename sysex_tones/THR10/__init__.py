""" Manage THR10 settings via MIDI SysEx. """

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


from sysex_tones.THR10.THR10 import THR10

import struct as _struct

import sysex_tones as _sysex_tones

from sysex_tones import CONSTANTS as _CONSTANTS
from sysex_tones.THR import CONSTANTS as _THR_CONSTANTS
from sysex_tones.THR10 import CONSTANTS as _THR10_CONSTANTS
from sysex_tones.THR10 import convert_data as _convert_data


def convert_text_to_midi( string ):
	""" Convert string into a list of MIDI commands. """
	retval = []
	(setting, valuelist, values) = _sysex_tones.extract_settings( string )
	if setting in _THR_CONSTANTS.THR_STREAM_SYSTEM_COMMANDS:
		valuelist = valuelist.lower()
		retval += _THR_CONSTANTS.THR_SYSTEM_COMMAND_PREFIX
		retval += _THR_CONSTANTS.THR_STREAM_SYSTEM_COMMANDS[setting][valuelist]
		retval += _THR_CONSTANTS.THR_SYSEX_STOP
	elif setting in _THR10_CONSTANTS.THR10_STREAM_COMMANDS:
		subkey = None
		for key in values.keys():
			if subkey:
				value = values[key]
				if value != None:
					retval += _THR_CONSTANTS.THR_COMMAND_PREFIX
					retval += _THR10_CONSTANTS.THR10_STREAM_SUBCOMMANDS[subkey][key]
					if key == 'ratio': # special case for text value
						low = 0
						high = len( _THR10_CONSTANTS.THR10_RATIO_NAMES ) - 1
						val = _THR10_CONSTANTS.THR10_RATIO_NAMES.index( value.lower() )
						retval += [_sysex_tones.get_minmax( val, low, high )]
					elif key == 'knee': # special case for text value
						low = 0
						high = len( _THR10_CONSTANTS.THR10_KNEE_NAMES ) - 1
						val = _THR10_CONSTANTS.THR10_KNEE_NAMES.index( value.capitalize() )
						retval += [_sysex_tones.get_minmax( val, low, high )]
					elif len( _THR10_CONSTANTS.THR10_STREAM_SUBCOMMANDS[subkey][key] ) == 1: # MIDI int
						low = _THR10_CONSTANTS.THR10_STREAM_SUBLIMITS[subkey][key][0]
						high = _THR10_CONSTANTS.THR10_STREAM_SUBLIMITS[subkey][key][1]
						val = _sysex_tones.get_minmax( value, low, high )
						vab = _struct.pack( '!I', _sysex_tones.convert_to_midi_int( val ) )
						retval += [vab[2], vab[3]]
					else: # MIDI byte, max 0x7f
						low = _THR10_CONSTANTS.THR10_STREAM_SUBLIMITS[subkey][key][0]
						high = _THR10_CONSTANTS.THR10_STREAM_SUBLIMITS[subkey][key][1]
						retval += [_sysex_tones.get_minmax( value, low, high )]
					retval += _THR_CONSTANTS.THR_SYSEX_STOP
			else:
				value = values[key]
				if value == None:
					retval += _THR_CONSTANTS.THR_COMMAND_PREFIX
					retval += _THR10_CONSTANTS.THR10_STREAM_COMMANDS[setting][key]
					retval += _THR_CONSTANTS.THR_SYSEX_STOP
				else:
					retval += _THR_CONSTANTS.THR_COMMAND_PREFIX
					retval += _THR10_CONSTANTS.THR10_STREAM_COMMANDS[setting][key]
					if len( _THR10_CONSTANTS.THR10_STREAM_COMMANDS[setting][key] ) == 1: # MIDI int
						low = _THR10_CONSTANTS.THR10_STREAM_LIMITS[setting][key][0]
						high = _THR10_CONSTANTS.THR10_STREAM_LIMITS[setting][key][1]
						val = _sysex_tones.get_minmax( value, low, high )
						vab = _struct.pack( '!I', _sysex_tones.convert_to_midi_int( val ) )
						retval += [vab[2], vab[3]]
					else: # MIDI byte, max 0x7f
						low = _THR10_CONSTANTS.THR10_STREAM_LIMITS[setting][key][0]
						high = _THR10_CONSTANTS.THR10_STREAM_LIMITS[setting][key][1]
						retval += [_sysex_tones.get_minmax( value, low, high )]
					retval += _THR_CONSTANTS.THR_SYSEX_STOP
			if key in _THR10_CONSTANTS.THR10_STREAM_SUBCOMMANDS:
				subkey = key
	return retval


def convert_midi_dump_to_text( data ):
	""" Convert MIDI data into a list of settings strings. """
	retval = []
	comment = '# '
	retval.append( _convert_data.name_data_to_string( data ) )
	retval.append( _convert_data.amp_data_to_string( data, comment ) )
	retval.append( _convert_data.control_data_to_string( data ) )
	retval.append( _convert_data.cab_data_to_string( data, comment ) )
	retval += _convert_data.compressor_data_to_strings( data, comment )
	retval += _convert_data.modulation_data_to_strings( data, comment )
	retval += _convert_data.delay_data_to_strings( data, comment )
	retval += _convert_data.reverb_data_to_strings( data, comment )
	retval += _convert_data.gate_data_to_strings( data, comment )
	return retval


def convert_to_text( data ):
	""" Convert data into text settings. """
	retval = []
	if _sysex_tones.THR.is_known_size( len( data ) ):
		detected = _sysex_tones.THR.THR.detect_midi_dump( data )
		if detected:
			for line in convert_midi_dump_to_text( detected['data'] ):
				retval.append( line )
		else:
			for line in convert_midi_dump_to_text( data ):
				retval.append( line )
	else:
		context = None
		for sysex in _sysex_tones.extract_midi_sysex( data ):
			if sysex:
				command = _sysex_tones.THR10.THR10.find_thr_command( sysex, context )
				if command:
					retval.append( command )
					if 'context' in command:
						context = command['context']
					else:
						context = None
				elif sysex == _THR10_CONSTANTS.THR10_SETTINGS_REQUEST:
					retval.append( 'THR10 request settings command' )
	return retval


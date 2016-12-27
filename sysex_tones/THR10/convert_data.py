""" Functions that convert THR10 block data into settings strings. """

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


import sysex_tones as _sysex_tones

from sysex_tones.THR import CONSTANTS as _THR_CONSTANTS
from sysex_tones.THR10 import CONSTANTS as _THR10_CONSTANTS

from sysex_tones import get_minmax as _get_minmax
from sysex_tones.THR10.CONSTANTS import THR10_STREAM_LIMITS as _THR10_STREAM_LIMITS
from sysex_tones.THR10.CONSTANTS import THR10_STREAM_SUBLIMITS as _THR10_STREAM_SUBLIMITS


def _minmax_limits( val, key, keykey ):
	""" Convenience function to save some typing, calls get_minmax() with THR10_STREAM_LIMITS minimum and maximum. """
	minmax = _THR10_STREAM_LIMITS[key][keykey]
	return _get_minmax( val, minmax[0], minmax[1] )


def _minmax_sublimits( val, key, keykey ):
	""" Convenience function to save some typing, calls get_minmax() with THR10_STREAM_SUBLIMITS minimum and maximum. """
	minmax = _THR10_STREAM_SUBLIMITS[key][keykey]
	return _get_minmax( val, minmax[0], minmax[1] )


def name_data_to_string( data ):
	""" Convert data into a Name: string. """
	name = data[:_THR_CONSTANTS.THR_SETTINGS_NAME_SIZE]
	name = _sysex_tones.convert_from_midi_to_string( name )
	return 'Name: %s' % (name)


def amp_data_to_string( data, comment ):
	""" Convert data into an Amp: string, or a commented error string. """
	retval = ''
	label = 'Amp'
	try:
		retval = '%s: %s' % (label, _THR10_CONSTANTS.THR10_AMP_NAMES[data[128]])
	except IndexError:
		retval = '%sBad %s index %i?' % (comment, label, data[128])
	return retval


def control_data_to_string( data ):
	""" Convert data into a Control: string. """
	label = 'Control'
	key = label.lower()
	settings = [
		'Gain',
		'Master',
		'Bass',
		'Middle',
		'Treble',
	]
	values = [
		_minmax_limits( data[129], key, settings[0].lower() ),
		_minmax_limits( data[130], key, settings[1].lower() ),
		_minmax_limits( data[131], key, settings[2].lower() ),
		_minmax_limits( data[132], key, settings[3].lower() ),
		_minmax_limits( data[133], key, settings[4].lower() ),
	]
	return _sysex_tones.settings_to_string( '', label, settings, values )


def cab_data_to_string( data, comment ):
	""" Convert data into a Cab: string, or a commented error string. """
	retval = ''
	label = 'Cab'
	try:
		retval = '%s: %s' % (label, _THR10_CONSTANTS.THR10_CAB_NAMES[data[134]])
	except IndexError:
		retval = '%sBad %s index %i?' % (comment, label, data[134])
	return retval


def compressor_data_to_strings( data, comment ):
	""" Convert data into Compressor: strings, commented strings, or commented error strings. """
	retval = []
	label = 'Compressor'
	compressorstate = _sysex_tones.ternary_operator( data[159], 'Off', 'On' )
	retval.append( '%s: %s' % (label, compressorstate) )
	prefix = _sysex_tones.ternary_operator( compressorstate == 'On', '', comment )
	compressortype = data[144]
	if compressortype == 0:
		key = 'stomp'
		settings = [
			'',
			'Sustain',
			'Output',
		]
		values = [
			_THR10_CONSTANTS.THR10_COMPRESSOR_NAMES[compressortype],
			_minmax_sublimits( data[145], key, settings[1].lower() ),
			_minmax_sublimits( data[146], key, settings[2].lower() ),
		]
		retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	elif compressortype == 1:
		key = 'rack'
		ratio = 'UNKNOWN'
		knee = 'UNKNOWN'
		try:
			ratio = _THR10_CONSTANTS.THR10_RATIO_NAMES[data[149]]
		except IndexError:
			retval.append( '%sBad ratio index %i?' % (comment, data[149]) )
		try:
			knee = _THR10_CONSTANTS.THR10_KNEE_NAMES[data[150]]
		except IndexError:
			retval.append( '%sBad knee index %i?' % (comment, data[150]) )
		settings = [
			'',
			'Threshold',
			'Attack',
			'Release',
			'Ratio',
			'Knee',
			'Output',
		]
		values = [
			_THR10_CONSTANTS.THR10_COMPRESSOR_NAMES[compressortype],
			_minmax_sublimits( data[146], key, settings[1].lower() ),
			_minmax_sublimits( data[147], key, settings[2].lower() ),
			_minmax_sublimits( data[148], key, settings[3].lower() ),
			ratio,
			knee,
			_minmax_sublimits( _sysex_tones.convert_from_midi_int_ints( data[151:153] ), key, settings[6].lower() ),
		]
		retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	else:
		retval.append( '%sUnknown %s type %i?' % (comment, label, compressortype) )
	return retval


def modulation_data_to_strings( data, comment ):
	""" Convert data into Modulation: strings, commented strings, or commented error strings. """
	retval = []
	label = 'Modulation'
	modulationstate = _sysex_tones.ternary_operator( data[175], 'Off', 'On' )
	retval.append( '%s: %s' % (label, modulationstate) )
	prefix = _sysex_tones.ternary_operator( modulationstate == 'On', '', comment )
	modulationtype = data[160]
	if modulationtype == 0:
		key = 'chorus'
		settings = [
			'',
			'Speed',
			'Depth',
			'Mix',
		]
		values = [
			_THR10_CONSTANTS.THR10_MODULATION_NAMES[modulationtype],
			_minmax_sublimits( data[161], key, settings[1].lower() ),
			_minmax_sublimits( data[162], key, settings[2].lower() ),
			_minmax_sublimits( data[163], key, settings[3].lower() ),
		]
		retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	elif modulationtype == 1:
		key = 'flanger'
		settings = [
			'',
			'Speed',
			'Manual',
			'Depth',
			'Feedback',
			'Spread',
		]
		values = [
			_THR10_CONSTANTS.THR10_MODULATION_NAMES[modulationtype],
			_minmax_sublimits( data[161], key, settings[1].lower() ),
			_minmax_sublimits( data[162], key, settings[2].lower() ),
			_minmax_sublimits( data[163], key, settings[3].lower() ),
			_minmax_sublimits( data[164], key, settings[4].lower() ),
			_minmax_sublimits( data[165], key, settings[5].lower() ),
		]
		retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	elif modulationtype == 2:
		key = 'tremelo'
		settings = [
			'',
			'Freq',
			'Depth',
		]
		values = [
			_THR10_CONSTANTS.THR10_MODULATION_NAMES[modulationtype],
			_minmax_sublimits( data[161], key, settings[1].lower() ),
			_minmax_sublimits( data[162], key, settings[2].lower() ),
		]
		retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	elif modulationtype == 3:
		key = 'phaser'
		settings = [
			'',
			'Speed',
			'Manual',
			'Depth',
			'Feedback',
		]
		values = [
			_THR10_CONSTANTS.THR10_MODULATION_NAMES[modulationtype],
			_minmax_sublimits( data[161], key, settings[1].lower() ),
			_minmax_sublimits( data[162], key, settings[2].lower() ),
			_minmax_sublimits( data[163], key, settings[3].lower() ),
			_minmax_sublimits( data[164], key, settings[4].lower() ),
		]
		retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	else:
		retval.append( '%sUnknown %s type %i?' % (comment, label, modulationtype) )
	return retval


def delay_data_to_strings( data, comment ):
	""" Convert data into Delay: strings, or commented strings. """
	retval = []
	label = 'Delay'
	delaystate = _sysex_tones.ternary_operator( data[191], 'Off', 'On' )
	retval.append( '%s: %s' % (label, delaystate) )
	key = label.lower()
	prefix = _sysex_tones.ternary_operator( delaystate == 'On', '', comment )
	settings = [
		'Time',
		'Feedback',
		'High Cut',
		'Low Cut',
		'Level',
	]
	values = [
		_minmax_limits( _sysex_tones.convert_from_midi_int_ints( data[177:179] ), key, settings[0].lower() ),
		_minmax_limits( data[179], key, settings[1].lower() ),
		_minmax_limits( _sysex_tones.convert_from_midi_int_ints( data[180:182] ), key, settings[2].lower() ),
		_minmax_limits( _sysex_tones.convert_from_midi_int_ints( data[182:184] ), key, settings[3].lower() ),
		_minmax_limits( data[184], key, settings[4].lower() ),
	]
	retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	return retval


def reverb_data_to_strings( data, comment ):
	""" Convert data into Reverb: strings, commented strings, or commented error strings. """
	retval = []
	label = 'Reverb'
	reverbstate = _sysex_tones.ternary_operator( data[207], 'Off', 'On' )
	retval.append( '%s: %s' % (label, reverbstate) )
	key = label.lower()
	prefix = _sysex_tones.ternary_operator( reverbstate == 'On', '', comment )
	reverbtype = data[192]
	if reverbtype in [0, 1, 2]:
		settings = [
			'',
			'Time',
			'Pre',
			'Low Cut',
			'High Cut',
			'High Ratio',
			'Low Ratio',
			'Level',
		]
		values = [
			_THR10_CONSTANTS.THR10_REVERB_NAMES[reverbtype],
			_minmax_limits( _sysex_tones.convert_from_midi_int_ints( data[193:195] ), key, settings[1].lower() ),
			_minmax_limits( _sysex_tones.convert_from_midi_int_ints( data[195:197] ), key, settings[2].lower() ),
			_minmax_limits( _sysex_tones.convert_from_midi_int_ints( data[197:199] ), key, settings[3].lower() ),
			_minmax_limits( _sysex_tones.convert_from_midi_int_ints( data[199:201] ), key, settings[4].lower() ),
			_minmax_limits( data[201], key, settings[5].lower() ),
			_minmax_limits( data[202], key, settings[6].lower() ),
			_minmax_limits( data[203], key, settings[7].lower() ),
		]
		retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	elif reverbtype == 3:
		settings = [
			'',
			'Reverb',
			'Filter',
		]
		values = [
			_THR10_CONSTANTS.THR10_REVERB_NAMES[reverbtype],
			_minmax_limits( data[193], key, settings[1].lower() ),
			_minmax_limits( data[194], key, settings[2].lower() ),
		]
		retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	else:
		retval.append( '%sUnknown %s type %i?' % (comment, label, reverbtype) )
	return retval


def gate_data_to_strings( data, comment ):
	""" Convert data into Gate: strings, or commented strings. """
	retval = []
	label = 'Gate'
	gatestate = _sysex_tones.ternary_operator( data[223], 'Off', 'On' )
	retval.append( '%s: %s' % (label, gatestate) )
	key = label.lower()
	prefix = _sysex_tones.ternary_operator( gatestate == 'On', '', comment )
	settings = [
		'Threshold',
		'Release',
	]
	values = [
		_minmax_limits( data[209], key, settings[0].lower() ),
		_minmax_limits( data[210], key, settings[1].lower() ),
	]
	retval.append( _sysex_tones.settings_to_string( prefix, label, settings, values ) )
	return retval


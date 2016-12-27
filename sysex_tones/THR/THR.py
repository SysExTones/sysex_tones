""" Public interface for managing THR settings via MIDI SysEx. """

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

from sysex_tones import CONSTANTS as _CONSTANTS
from sysex_tones.THR import CONSTANTS as _THR_CONSTANTS

from sysex_tones import BasicIO as _BasicIO


class THR( _BasicIO ):
	""" Manage THR settings via MIDI SysEx. """


	def __init__( self, infilename=None, outfilename=None ):
		""" The infilename and outfilename arguments should be MIDI device filenames, or contain MIDI SysEx data. """
		_BasicIO.__init__( self, infilename, outfilename )


	def extract_dump( self ):
		""" Extract a settings dump from self.infile, returning a dictionary containing ['sysex'] and ['dump'] if found. """
		retval = {}
		for sysex in self.extract_sysex_from_infile():
			detected = self.detect_midi_dump( sysex )
			# skip device heartbeats, only process a settings dump
			if detected:
				retval['sysex'] = sysex
				retval['dump'] = detected['data']
				break
		return retval


	@classmethod
	def detect_midi_dump( cls, data ):
		""" Check data for known types of THR MIDI data. """
		retval= []
		if len( data ) == _THR_CONSTANTS.THR_FILE_SIZE:
			unknownprefix = data[:len( _THR_CONSTANTS.THR_UNKNOWN_PREFIX )]
			if unknownprefix == _THR_CONSTANTS.THR_UNKNOWN_PREFIX:
				retval = {
					'type': 'ydl',
					'data': data[_THR_CONSTANTS.THR_FILE_OFFSET:],
				}
		elif len( data ) == _THR_CONSTANTS.THR_DUMP_SIZE:
			if data[-1] == _CONSTANTS.SYSEX_STOP[0]:
				# -2 is the list offset for the checksum byte
				payload = data[len( _THR_CONSTANTS.THR_DUMP_HEADER_PREFIX ):-2]
				if _sysex_tones.THR.is_valid_checksum( payload, data[-2] ):
					header = data[:len( _THR_CONSTANTS.THR_DUMP_HEADER )]
					if header == _THR_CONSTANTS.THR_DUMP_HEADER:
						retval = {
							'type': 'dump',
							'data': data[_THR_CONSTANTS.THR_DUMP_OFFSET:-2],
						}
		return retval

	@staticmethod
	def find_thr_heartbeat_model( data ):
		""" Returns a THR model name, if data is a device heartbeat. """
		retval = ''
		heartbeat = data[:len( _THR_CONSTANTS.THR10_HEARTBEAT )]
		if heartbeat == _THR_CONSTANTS.THR5_HEARTBEAT:
			retval = _THR_CONSTANTS.THR5_MODEL_NAME
		elif heartbeat == _THR_CONSTANTS.THR10_HEARTBEAT:
			retval = _THR_CONSTANTS.THR10_MODEL_NAME
		elif heartbeat == _THR_CONSTANTS.THR10X_HEARTBEAT:
			retval = _THR_CONSTANTS.THR10X_MODEL_NAME
		elif heartbeat == _THR_CONSTANTS.THR10C_HEARTBEAT:
			retval = _THR_CONSTANTS.THR10C_MODEL_NAME
		elif heartbeat == _THR_CONSTANTS.THR5A_HEARTBEAT:
			retval = _THR_CONSTANTS.THR5A_MODEL_NAME
		return retval


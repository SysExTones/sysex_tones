""" Public interface for managing THR10 settings via MIDI SysEx. """

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

from sysex_tones.THR import THR as _THR


class THR10( _THR ):
	""" Manage THR10 settings via MIDI SysEx. """


	def __init__( self, infilename=None, outfilename=None ):
		""" The infilename and outfilename arguments should be MIDI device filenames, or contain MIDI SysEx data. """
		_THR.__init__( self, infilename, outfilename )


	def request_current_settings( self, outfilename=None ):
		""" Return a list of text strings describing THR10 settings, setting self.outfilename if present. """
		retval = []
		opened = False
		if outfilename:
			self.open_outfile( outfilename )
			opened = True
		elif not self.outfile:
			self.open_outfile()
			opened = True
		if self.outfile:
			request = _sysex_tones.convert_to_stream( _sysex_tones.THR10.CONSTANTS.THR10_SETTINGS_REQUEST )
			self.outfile.write( request )
		if opened:
			self.close_outfile()
		return retval


	def convert_infile_to_text( self, infilename=None ):
		""" Convert the THR device data read from self.infilename into text settings, setting self.infilename if present. """
		retval = []
		opened = False
		if infilename:
			self.open_infile( infilename )
			opened = True
		elif not self.infile:
			self.open_infile()
			opened = True
		if self.infile:
			data = _sysex_tones.read_from_stream( self.infile )
			retval = _sysex_tones.THR10.convert_to_text( data )
		if opened:
			self.close_infile()
		return retval


	def convert_infile_to_midi( self, infilename=None ):
		""" Convert self.infilename text into MIDI data, setting self.infilename if present. """
		retval = []
		opened = False
		if infilename:
			self.open_infile( infilename )
			opened = True
		elif not self.infile:
			self.open_infile()
			opened = True
		if self.infile:
			for line in self.infile.readlines():
				command = _sysex_tones.THR10.convert_text_to_midi( line )
				if command:
					retval += command
		if opened:
			self.close_infile()
		return retval


	def write_data_to_outfile( self, data ):
		""" Write data to self.outfile. """
		opened = False
		if not self.outfile:
			self.open_outfile()
			opened = True
		if self.outfile:
			_THR.write_data_to_outfile( self, _sysex_tones.convert_to_stream( data ) )
		if opened:
			self.close_outfile()


	def write_text_to_midi( self, infilename=None ):
		""" Read from infilename or self.infile, convert to MIDI data, write converted data to self.outfile. """
		self.write_data_to_outfile( self.convert_infile_to_midi( infilename ) )


	@staticmethod
	def print_sysex_data( sysex=None, data=None ):
		""" Print the sysex and data, sysex in hexadecimal and data converted, to config statements. """
		if sysex:
			print( _sysex_tones.convert_bytes_to_hex_string( sysex ) )
		if data:
			for line in _sysex_tones.THR10.convert_midi_dump_to_text( data ):
				print( line )


	@staticmethod
	def find_thr_command( data, context=None ):
		""" Search data for known THR commands, with an option context for subcommands, and return a dictionary of search results. """
		retval = {}
		found = _sysex_tones.extract_command_payload( data, _THR_CONSTANTS.THR_COMMAND_PREFIX )
		if found:
			# FIX: this reverse lookup is verbose, and comprehension+lambda obtuse
			for control in _THR10_CONSTANTS.THR10_STREAM_COMMANDS:
				for name in _THR10_CONSTANTS.THR10_STREAM_COMMANDS[control]:
					command = _THR10_CONSTANTS.THR10_STREAM_COMMANDS[control][name]
					if found[:len( command )] == command:
						retval['control'] = control
						retval['name'] = name
						size = len( found ) - len( command )
						if size == 0:
							if name in _THR10_CONSTANTS.THR10_STREAM_SUBCOMMANDS:
								retval['context'] = name
						elif size == 1:
							minmax = _THR10_CONSTANTS.THR10_STREAM_LIMITS[control][name]
							retval['value'] = _sysex_tones.get_minmax( found[-1], minmax[0], minmax[1] )
						elif size == 2:
							minmax = _THR10_CONSTANTS.THR10_STREAM_LIMITS[control][name]
							retval['value'] = _sysex_tones.get_minmax( _sysex_tones.convert_from_midi_int_ints( found[-size:] ), minmax[0], minmax[1] )
						else:
							retval = {}
					if retval:
						break
				if retval:
					break
		else:
			found = _sysex_tones.extract_command_payload( data, _THR_CONSTANTS.THR_SYSTEM_COMMAND_PREFIX )
			if found:
				# FIX: this reverse lookup is verbose, and comprehension+lambda obtuse
				for control in _THR_CONSTANTS.THR_STREAM_SYSTEM_COMMANDS:
					for name in _THR_CONSTANTS.THR_STREAM_SYSTEM_COMMANDS[control]:
						command = _THR_CONSTANTS.THR_STREAM_SYSTEM_COMMANDS[control][name]
						if found[:len( command )] == command:
							retval['control'] = control
							retval['name'] = name
							size = len( found ) - len( command )
							if size == 0:
								pass
							elif size == 1:
								minmax = _THR10_CONSTANTS.THR10_STREAM_LIMITS[control][name]
								retval['value'] = _sysex_tones.get_minmax( found[-1], minmax[0], minmax[1] )
							elif size == 2:
								minmax = _THR10_CONSTANTS.THR10_STREAM_LIMITS[control][name]
								retval['value'] = _sysex_tones.get_minmax( _sysex_tones.convert_from_midi_int_ints( found[-size:] ), minmax[0], minmax[1] )
							else:
								retval = {}
						if retval:
							break
					if retval:
						break
		if not retval and context:
			if context in _THR10_CONSTANTS.THR10_STREAM_SUBCOMMANDS:
				control = context
				# FIX: this reverse lookup is verbose, and comprehensions+lambda obtuse
				for name in _THR10_CONSTANTS.THR10_STREAM_SUBCOMMANDS[control]:
					command = _THR10_CONSTANTS.THR10_STREAM_SUBCOMMANDS[control][name]
					if found[:len( command )] == command:
						retval['control'] = control
						retval['name'] = name
						retval['context'] = context
						size = len( found ) - len( command )
						if size == 0:
							pass
						elif size == 1:
							minmax = _THR10_CONSTANTS.THR10_STREAM_SUBLIMITS[control][name]
							retval['value'] = _sysex_tones.get_minmax( found[-size], minmax[0], minmax[1] )
						elif size == 2:
							minmax = _THR10_CONSTANTS.THR10_STREAM_SUBLIMITS[control][name]
							retval['value'] = _sysex_tones.get_minmax( _sysex_tones.convert_from_midi_int_ints( found[-size:] ), minmax[0], minmax[1] )
						else:
							retval = {}
					if retval:
						break
		return retval


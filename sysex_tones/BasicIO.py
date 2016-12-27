""" Public interface for managing basic IO via MIDI SysEx. """

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


class BasicIO( object ):
	""" Manage basic IO via MIDI SysEx. """

	infilename = None
	outfilename = None
	infile = None
	outfile = None


	def __init__( self, infilename=None, outfilename=None ):
		""" The infilename and outfilename arguments should be MIDI device filenames, or contain MIDI SysEx data. """
		self.set_infilename( infilename )
		self.set_outfilename( outfilename )


	def set_infilename( self, infilename ):
		""" Set self.infilename, close self.infile (if open). """
		self.close_infile()
		self.infilename = infilename


	def set_outfilename( self, outfilename ):
		""" Set self.outfilename, close self.outfile (if open). """
		self.close_outfile()
		self.outfilename = outfilename


	def open_infile( self, infilename=None ):
		""" Open self.infile, setting self.infilename if preset, after old closing self.infile (if open). """
		self.close_infile()
		if infilename:
			self.set_infilename( infilename )
		self.infile = _sysex_tones.open_input_stream( self.infilename )


	def open_infile_wait_indefinitely( self, infilename=None ):
		""" Open self.infile (wait indefinitely for it to be available), setting self.infilename if present, after old closing self.infile (if open). """
		self.close_infile()
		if infilename:
			self.set_infilename( infilename )
		self.infile = _sysex_tones.open_input_wait_indefinitely( self.infilename )


	def open_outfile( self, outfilename=None ):
		""" Open self.outfile, setting self.outfilename if present, after old closing self.outfile (if open). """
		self.close_outfile()
		if outfilename:
			self.set_outfilename( outfilename )
		self.outfile = _sysex_tones.open_output_stream( self.outfilename )


	def close_infile( self ):
		""" Close self.infile (if open). """
		if self.infile:
			self.infile.close()
			self.infile = None


	def close_outfile( self ):
		""" Close self.outfile (if open). """
		if self.outfile:
			self.outfile.close()
			self.outfile = None


	def write_data_to_outfile( self, data ):
		""" Write data to self.outfile. """
		self.outfile.write( _sysex_tones.convert_to_stream( data ) )


	def extract_sysex_from_infile( self ):
		""" Read sysex from self.infile (if data is available)."""
		retval = []
		if _sysex_tones.is_data_available( self.infile ):
			retval = _sysex_tones.extract_sysex_from_stream( self.infile )
		return retval


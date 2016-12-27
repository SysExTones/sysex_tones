""" Constants for Yamaha THR series modeling amplifiers. """

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


import sysex_tones.CONSTANTS as _CONSTANTS


# Yamaha THR model names
THR5_MODEL_NAME = 'THR5'
THR10_MODEL_NAME = 'THR10'
THR10X_MODEL_NAME = 'THR10X'
THR10C_MODEL_NAME = 'THR10C'
THR5A_MODEL_NAME = 'THR5A'


# empirical THR sizes and offsets
THR_DUMP_SIZE = 276
THR_DUMP_OFFSET = 18
THR_FILE_SIZE = 265
THR_FILE_OFFSET = 9
THR_SYSEX_SIZE = 256
THR_SETTINGS_NAME_SIZE = 64


# Yamaha MIDI Manufacturer SysEx ID via https://www.midi.org/specifications/item/manufacturer-id-numbers
YAMAHA_MIDI_ID = [0x43]
YAMAHA_DEVICE_ID = [0x7d]

# Yamaha THR model identifiers https://www.yamaha.com/thr/
YAMAHA_THR5 = [0x30]
YAMAHA_THR10 = [0x31]
YAMAHA_THR10X = [0x32]
YAMAHA_THR10C = [0x33]
YAMAHA_THR5A = [0x34]

# Yamaha flavors of MIDI SYSEX data demarcation
THR_SYSEX_START = _CONSTANTS.SYSEX_START + YAMAHA_MIDI_ID + YAMAHA_DEVICE_ID
THR_SYSEX_STOP = _CONSTANTS.SYSEX_STOP

# MIDI bytes lacking specific specification
THR_UNKNOWN_DUMP_PREFIX = [0x02, 0x0c]
THR_UNKNOWN_DUMP_POSTFIX = [0x00, 0x00, 0x7f, 0x7f]
THR_UNKNOWN_COMMAND_PREFIX = [0x41, 0x30]
THR_UNKNOWN_PREFIX = [0x44, 0x54, 0x41]
THR_UNKNOWN_POSTFIX = [0x41, 0x6c, 0x6c, 0x50]

# Yamaha THR MIDI stream commands
THR_DUMP_HEADER_PREFIX = THR_SYSEX_START + [0x00] + THR_UNKNOWN_DUMP_PREFIX
THR_COMMAND_PREFIX = THR_SYSEX_START + [0x10] + THR_UNKNOWN_COMMAND_PREFIX + [0x01]
THR_SETTINGS_REQUEST_PREFIX = THR_SYSEX_START + [0x20] + THR_UNKNOWN_PREFIX
THR_SYSTEM_COMMAND_PREFIX = THR_SYSEX_START + [0x30] + THR_UNKNOWN_COMMAND_PREFIX
THR_HEARTBEAT_PREFIX = THR_SYSEX_START + [0x60] + THR_UNKNOWN_PREFIX

THR_DUMP_HEADER = THR_DUMP_HEADER_PREFIX + THR_UNKNOWN_PREFIX + [0x31] + THR_UNKNOWN_POSTFIX + THR_UNKNOWN_DUMP_POSTFIX

# Yamaha THR heartbeats, sent by the device at regular intervals (about twice a second)
THR5_HEARTBEAT = THR_HEARTBEAT_PREFIX + YAMAHA_THR5 + THR_SYSEX_STOP
THR10_HEARTBEAT = THR_HEARTBEAT_PREFIX + YAMAHA_THR10 + THR_SYSEX_STOP
THR10X_HEARTBEAT = THR_HEARTBEAT_PREFIX + YAMAHA_THR10X + THR_SYSEX_STOP
THR10C_HEARTBEAT = THR_HEARTBEAT_PREFIX + YAMAHA_THR10C + THR_SYSEX_STOP
THR5A_HEARTBEAT = THR_HEARTBEAT_PREFIX + YAMAHA_THR5A + THR_SYSEX_STOP


# Yamaha MIDI values for system settings
# list length indicates size of MIDI variable values: 3=none, 2=byte, 1=int
THR_STREAM_SYSTEM_COMMANDS = {
	'wide': {
		'on': [0x00, 0x00],
		'off': [0x00, 0x01],
	},
	'lamp': {
		'on': [0x01, 0x00],
		'off': [0x01, 0x01],
	},
}


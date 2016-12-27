""" Constants for Yamaha THR10 modeling amplifiers. """

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


from sysex_tones.THR import CONSTANTS as _THR_CONSTANTS


# Yamaha THR MIDI stream commands
THR10_SETTINGS_REQUEST = _THR_CONSTANTS.THR_SETTINGS_REQUEST_PREFIX + _THR_CONSTANTS.YAMAHA_THR10 + _THR_CONSTANTS.THR_UNKNOWN_POSTFIX + _THR_CONSTANTS.THR_SYSEX_STOP # is this specific to the THR10 or does 0x31 just happen to be part of the UNKNOWN MIDI?


# Yamaha THR10 settings labels, in lists, to retain index order
THR10_AMP_NAMES = ['Clean', 'Crunch', 'Lead', 'BritHi', 'Modern', 'Bass', 'Aco', 'Flat']
THR10_CAB_NAMES = ['US4x12', 'US2x12', 'Brit4x12', 'Brit2x12', '1x12', '4x10', 'None']
THR10_COMPRESSOR_NAMES = ['Stomp', 'Rack']
THR10_MODULATION_NAMES = ['Chorus', 'Flanger', 'Tremelo', 'Phaser']
THR10_REVERB_NAMES = ['Hall', 'Room', 'Plate', 'Spring']
THR10_RATIO_NAMES = ['1:1', '1:4', '1:8', '1:12', '1:20', '1:inf']
THR10_KNEE_NAMES = ['Soft', 'Medium', 'Hard']


# Yamaha THR10 MIDI values for settings
# list length indicates size of MIDI variable values: 3=none, 2=byte, 1=int

THR10_STREAM_COMMANDS = {
	'amp': {
		THR10_AMP_NAMES[0].lower(): [0x00, 0x00, 0x00], # Clean
		THR10_AMP_NAMES[1].lower(): [0x00, 0x00, 0x01], # Crunch
		THR10_AMP_NAMES[2].lower(): [0x00, 0x00, 0x02], # Lead
		THR10_AMP_NAMES[3].lower(): [0x00, 0x00, 0x03], # BritHi
		THR10_AMP_NAMES[4].lower(): [0x00, 0x00, 0x04], # Modern
		THR10_AMP_NAMES[5].lower(): [0x00, 0x00, 0x05], # Bass
		THR10_AMP_NAMES[6].lower(): [0x00, 0x00, 0x06], # Aco
		THR10_AMP_NAMES[7].lower(): [0x00, 0x00, 0x07], # Flat
	},
	'control': {
		'gain': [0x01, 0x00],
		'master': [0x02, 0x00],
		'bass': [0x03, 0x00],
		'middle': [0x04, 0x00],
		'treble': [0x05, 0x00],
	},
	'cab': {
		THR10_CAB_NAMES[0].lower(): [0x06, 0x00, 0x00], # US4x12
		THR10_CAB_NAMES[1].lower(): [0x06, 0x00, 0x01], # US2x12
		THR10_CAB_NAMES[2].lower(): [0x06, 0x00, 0x02], # Brit4x12
		THR10_CAB_NAMES[3].lower(): [0x06, 0x00, 0x03], # Brit2x12
		THR10_CAB_NAMES[4].lower(): [0x06, 0x00, 0x04], # 1x12
		THR10_CAB_NAMES[5].lower(): [0x06, 0x00, 0x05], # 4x10
		THR10_CAB_NAMES[6].lower(): [0x06, 0x00, 0x06], # None
	},
	'compressor': {
		'on': [0x1f, 0x00, 0x00],
		'off': [0x1f, 0x00, 0x7f],
		THR10_COMPRESSOR_NAMES[0].lower(): [0x10, 0x00, 0x00], # Stomp
		THR10_COMPRESSOR_NAMES[1].lower(): [0x10, 0x00, 0x01], # Rack
	},
	'modulation': {
		'on': [0x2f, 0x00, 0x00],
		'off': [0x2f, 0x00, 0x7f],
		THR10_MODULATION_NAMES[0].lower(): [0x20, 0x00, 0x00], # Chorus
		THR10_MODULATION_NAMES[1].lower(): [0x20, 0x00, 0x01], # Flanger
		THR10_MODULATION_NAMES[2].lower(): [0x20, 0x00, 0x02], # Tremelo
		THR10_MODULATION_NAMES[3].lower(): [0x20, 0x00, 0x03], # Phaser
	},
	'delay': {
		'on': [0x3f, 0x00, 0x00],
		'off': [0x3f, 0x00, 0x7f],
		'time': [0x31],
		'feedback': [0x33, 0x00],
		'high cut': [0x34],
		'low cut': [0x36],
		'level': [0x38, 0x00],
	},
	'reverb': { # what about a reverb delay value? 0x44?
		'on': [0x4f, 0x00, 0x00],
		'off': [0x4f, 0x00, 0x7f],
		THR10_REVERB_NAMES[0].lower(): [0x40, 0x00, 0x00], # Hall
		THR10_REVERB_NAMES[1].lower(): [0x40, 0x00, 0x01], # Room
		THR10_REVERB_NAMES[2].lower(): [0x40, 0x00, 0x02], # Plate
		THR10_REVERB_NAMES[3].lower(): [0x40, 0x00, 0x03], # Spring
		'time': [0x41],
		'reverb': [0x41, 0x00],
		'filter': [0x42, 0x00],
		'pre': [0x43],
		'low cut': [0x45],
		'high cut': [0x47],
		'high ratio': [0x49, 0x00],
		'low ratio': [0x4a, 0x00],
		'level': [0x4b, 0x00],
	},
	'gate': {
		'on': [0x5f, 0x00, 0x00],
		'off': [0x5f, 0x00, 0x7f],
		'threshold': [0x51, 0x00],
		'release': [0x52, 0x00],
	},
}


THR10_STREAM_SUBCOMMANDS = {
	THR10_COMPRESSOR_NAMES[0].lower(): { # Stomp
		'sustain': [0x11, 0x00],
		'output': [0x12, 0x00],
	},
	THR10_COMPRESSOR_NAMES[1].lower(): { # Rack
		'threshold': [0x11],
		'attack': [0x13, 0x00],
		'release': [0x14, 0x00],
		'ratio': [0x15, 0x00],
		'knee': [0x16, 0x00],
		'output': [0x17],
	},
	THR10_MODULATION_NAMES[0].lower(): { # Chorus
		'speed': [0x21, 0x00],
		'depth': [0x22, 0x00],
		'mix': [0x23, 0x00],
	},
	THR10_MODULATION_NAMES[1].lower(): { # Flanger
		'speed': [0x21, 0x00],
		'manual': [0x22, 0x00],
		'depth': [0x23, 0x00],
		'feedback': [0x24, 0x00],
		'spread': [0x25, 0x00],
	},
	THR10_MODULATION_NAMES[2].lower(): { # Tremelo
		'freq': [0x21, 0x00],
		'depth': [0x22, 0x00],
	},
	THR10_MODULATION_NAMES[3].lower(): { # Phaser
		'speed': [0x21, 0x00],
		'manual': [0x22, 0x00],
		'depth': [0x23, 0x00],
		'feedback': [0x24, 0x00],
	},
}


# Yamaha THR10 lower/upper limits for MIDI variable values

THR10_STREAM_LIMITS = {
	'control': {
		'gain': [0, 100],
		'master': [0, 100],
		'bass': [0, 100],
		'middle': [0, 100],
		'treble': [0, 100],
	},
	'delay': {
		'time': [1, 9999],
		'feedback': [0, 100],
		'high cut': [1000, 16001],
		'low cut': [21, 8000],
		'level': [0, 100],
	},
	'reverb': {
		'time': [3, 200],
		'reverb': [0, 100],
		'filter': [0, 100],
		'pre': [1, 2000],
		'low cut': [21, 8000],
		'high cut': [1000, 16001],
		'high ratio': [1, 10],
		'low ratio': [1, 14],
		'level': [0, 100],
	},
	'gate': {
		'threshold': [0, 100],
		'release': [0, 100],
	},
}


THR10_STREAM_SUBLIMITS = {
	THR10_COMPRESSOR_NAMES[0].lower(): { # Stomp
		'sustain': [0, 100],
		'output': [0, 100],
	},
	THR10_COMPRESSOR_NAMES[1].lower(): { # Rack
		'threshold': [0, 600],
		'attack': [0, 100],
		'release': [0, 100],
		'ratio': [0, 5],
		'knee': [0, 2],
		'output': [0, 600],
	},
	THR10_MODULATION_NAMES[0].lower(): { # Chorus
		'speed': [0, 100],
		'depth': [0, 100],
		'mix': [0, 100],
	},
	THR10_MODULATION_NAMES[1].lower(): { # Flanger
		'speed': [0, 100],
		'manual': [0, 100],
		'depth': [0, 100],
		'feedback': [0, 100],
		'spread': [0, 100],
	},
	THR10_MODULATION_NAMES[2].lower(): { # Tremelo
		'freq': [0, 100],
		'depth': [0, 100],
	},
	THR10_MODULATION_NAMES[3].lower(): { # Phaser
		'speed': [0, 100],
		'manual': [0, 100],
		'depth': [0, 100],
		'feedback': [0, 100],
	},
}



BEATS_PER_ROW =  64.0 # must be float


HEX_TO_NOTE_DICT = {
    "0":"A",
    "1":"B",
    "2":"C",
    "3":"D",
    "4":"E",
    "5":"F",
    "6":"G",
    "7": "REST"
}

NOTE_TO_HEX_DICT = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "REST": 7
}

MAJOR_DEGREE_TO_CHORD = ['MAJOR', 'MINOR', 'MINOR', 'MAJOR', 'MAJOR', 'MINOR', 'DIMINISHED']
MINOR_DEGREE_TO_CHORD = ['MINOR', 'DIMINISHED', 'MAJOR', 'MINOR', 'MINOR', 'MAJOR', 'MAJOR']

NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
MIDI_OFFSET = 12

MAJOR_SCALE_PATTERN = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE_PATTERN = [0, 2, 3, 5, 7, 8, 10]

NOTE_DURATIONS = [1,2,4,8,16,32,64]

DURATION_TO_STR = {
    1:"1/64",
    2:"1/32",
    4:"1/16",
    8:"1/8",
    16:"1/4",
    32:"1/2",
    64:"1/1"
}

MAX_BPM = 140
MIN_BPM = 80


from constants import MAJOR_DEGREE_TO_CHORD, MINOR_DEGREE_TO_CHORD, NOTE_TO_HEX_DICT, HEX_TO_NOTE_DICT, NOTE_DURATIONS, DURATION_TO_STR, BEATS_PER_ROW, NOTES_FLAT, NOTES_SHARP, MIDI_OFFSET
from math import floor
from random import randint

def note_to_midi(name, octave, sharp=True):
    if name == 'REST':
        return 0
    notes = NOTES_SHARP if sharp else NOTES_FLAT
    return MIDI_OFFSET + octave*12 + notes.index(name)

def midi_to_note(midi, sharp=True):
    notes = NOTES_SHARP if sharp else NOTES_FLAT
    return (notes[(midi - MIDI_OFFSET) % len(notes)], floor((midi - MIDI_OFFSET) / len(notes)))


def find_max_norm_dir(n):
    if n < NOTE_DURATIONS[0]:
        raise Exception('n smaller than smallest note duration!!')
    for i,d in enumerate(NOTE_DURATIONS):
        if n == d:
            return d
        if n < d:
            return NOTE_DURATIONS[i - 1]

class Note:
    def __init__(self, name, octave, sharp=True, rest=False) -> None:
        self.rest = rest
        if name == 'REST':
            self.rest = True
        if not rest:
            self.name = name
            self.octave = octave
            self.sharp=sharp
            self.midi = note_to_midi(name, octave, sharp=self.sharp)
        else:
            self.name = 'REST'
            self.octave = -1
            self.midi = 0
    def relative(self, semisteps: int):
        self.midi += semisteps
        n, o = midi_to_note(self.midi)
        self.name = n
        self.octave = o
    def __str__(self) -> str:
        return f"{self.name}{self.octave}" if not self.rest else "<REST>"

"""
Represents chords
Inversions are 1, 2, or 3 (NOT zero-indexed)
Flavor is MAJOR or MINOR
root should be a Note class type

This class is really supposed to just be READONLY after setting.
If you want to do different stuff, just use the static get_triad method
"""
class Chord:
    def __init__(self, root: Note, flavor, inversion=1, is_sharp=True) -> None:
        self.root = root
        self.flavor = flavor
        self.inversion = inversion
        self.is_sharp = is_sharp
        self.notes = self.get_triad(root, flavor, inversion=inversion, is_sharp=self.is_sharp)

    @staticmethod
    def get_triad(root: Note, flavor, inversion=1, is_sharp=True):
        triad = [root]
        third = Note(root.name, root.octave, sharp=is_sharp)
        fifth = Note(root.name, root.octave, sharp=is_sharp)
        fifth.relative(7)
        if flavor == 'MAJOR':
            third.relative(4)
        elif flavor == 'MINOR':
            third.relative(3)
        elif flavor == 'DIMINISHED':
            third.relative(3)
            fifth.relative(-1)
        else:
            raise Exception(f"Chord flavor `{flavor}` not recognized!")
        triad += [third, fifth]
        inversion_idx = inversion - 1
        triad = triad[inversion_idx:] + triad[:inversion_idx]
        return triad

    def get_distance(self, notes):
        distances = []
        for note in notes:
            if note.rest:
                continue
            min_dist = min(map(lambda x: abs((x.midi % 12) - (note.midi % 12)), self.notes))
            distances.append(min_dist)
        distance = sum(distances) / len(distances)
        return distance
    
    def __str__(self) -> str:
        return f"{self.root.name} {self.flavor[:3]} {self.inversion}"
        
class ChordMoment:
    def __init__(self, chord: Chord, duration) -> None:
        self.chord = chord
        self.duration = duration
    def __str__(self) -> str:
        return f"({self.duration}){self.chord}"

class Moment:
    def __init__(self, duration, note: Note) -> None:
        self.duration = duration
        self.note = note

    def duration_to_note_length(self):
        if DURATION_TO_STR.get(self.duration) is not None:
            return DURATION_TO_STR.get(self.duration)
        dur_str = '('
        dur_left = self.duration
        while dur_left > 0:
            norm_dur = find_max_norm_dir(dur_left)
            dur_str += DURATION_TO_STR.get(norm_dur) + '+'
            # print(f"{dur_left} - {norm_dur} = {dur_left - norm_dur}")
            dur_left -= norm_dur
        if dur_str[-1] == '+':
            dur_str = dur_str[:-1] # drop extra plus
        dur_str += ')'
        return dur_str

    def __str__(self) -> str:
        d = self.duration
        if DURATION_TO_STR.get(d) is not None:
            d = DURATION_TO_STR.get(self.duration)
        return f"{self.duration_to_note_length()}{self.note}"

"""
Holds global info like key, tempo, etc
Also includes the note/note durations
"""

class Score:

    def __init__(
        self,
        root,
        hex_to_note_dict=HEX_TO_NOTE_DICT,
        note_to_hex_dict=NOTE_TO_HEX_DICT,
        name='default',
        tempo=120,
        mode='MINOR',
        is_sharp=True
    ) -> None:
        self.score = []
        self.chords = []
        self.root = root
        self.hex_to_note_dict = hex_to_note_dict
        self.note_to_hex_dict = note_to_hex_dict
        self.name = name
        self.tempo = tempo
        self.key_mode = mode
        self.chord_flavors = MINOR_DEGREE_TO_CHORD if mode == 'MINOR' else MAJOR_DEGREE_TO_CHORD
        self.key_chords = []
        self.is_sharp = is_sharp
        for chord, flavor in zip(note_to_hex_dict.keys(), self.chord_flavors):
            self.key_chords.append(Chord(Note(chord, 4, sharp=self.is_sharp), flavor, is_sharp=self.is_sharp))

    def add_phrase(self, durations, notes) -> None:
        if len(durations) != len(notes):
            raise Exception("Length mismatch between notes and durations for phrase")
        moments = []
        for duration, note_pack in zip(durations, notes):
            note = Note(note_pack[0], note_pack[1], sharp=self.is_sharp)
            moments.append(Moment(duration, note))
        self.score += moments

    # will wipe and regenerate chords, based on current value of self.score
    def generate_chords(self):
        self.chords = [] # reset chords
        measure_counter = 0.0
        curr_time = 0.0
        moment: Moment
        curr_moment_notes = []
        curr_chord_length = 0.
        inversion_counter = 1
        max_chord_length = BEATS_PER_ROW # maybe use this later
        for moment in self.score:
            curr_time += moment.duration
            measure_counter += moment.duration
            curr_chord_length += moment.duration
            curr_moment_notes.append(moment.note)
            if measure_counter >= BEATS_PER_ROW: # account for rounding errors? this is very hacky
                min_dist = float('inf')
                min_dist_chord = self.key_chords[0]
                chord: Chord
                for chord in self.key_chords:
                    d = chord.get_distance(curr_moment_notes)
                    if d < min_dist:
                        min_dist = d
                        min_dist_chord = chord
                if len(self.chords) > 0:
                    if self.chords[-1].chord.root == min_dist_chord.root:
                        inversion_counter += 1 # randint(1,2)
                        if inversion_counter > 3:
                            inversion_counter = 1
                        # make chord cohere to 
                        self.chords.append(
                            ChordMoment(
                                Chord(min_dist_chord.root,
                                      min_dist_chord.flavor,
                                      inversion=inversion_counter,
                                      is_sharp=self.is_sharp
                                ),
                                curr_chord_length
                            )
                        )
                    else:
                        inversion_counter = 1
                        self.chords.append(ChordMoment(min_dist_chord, curr_chord_length))
                else:
                    self.chords.append(ChordMoment(min_dist_chord, curr_chord_length))
                curr_moment_notes = []
                measure_counter = 0.
                curr_chord_length = 0.

        

    def describe(self):
        notes_dict = dict.fromkeys(self.note_to_hex_dict, 0)
        s = f"Root: {self.root}\n"
        total_dur_counter = 0.0
        moment: Moment
        for moment in self.score:
            total_dur_counter += moment.duration
            notes_dict[moment.note.name] += 1
        s += 'Note Counts:\n'
        for k,v in notes_dict.items():
            s += f"  {k} = {v}\n"
        s += f"Duration: {total_dur_counter / 64.} measures"
        print(s)
        return(s)
    def __str__(self) -> str:
        s = f"Root: {self.root}\n"
        measure_counter = 0.0
        line_counter = 0
        total_dur_counter = 0.0
        for moment in self.score:
            s += str(moment) + ' '
            measure_counter += moment.duration
            total_dur_counter += moment.duration
            if measure_counter >= 64:
                s += '| '
                measure_counter = 0
                line_counter += 1
            if line_counter >= 4:
                s += '\n'
                line_counter = 0
        s += f"\nDuration: {total_dur_counter / 64.} measures"
        return s

        

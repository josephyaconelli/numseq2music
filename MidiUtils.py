import sys
from midiutil.MidiFile import MIDIFile
from math import floor
from Score import ChordMoment, Score, Moment
from constants import BEATS_PER_ROW, NOTES_FLAT, NOTES_SHARP, MIDI_OFFSET
import pygame
import time

divisor = BEATS_PER_ROW / 16.0

def make_midi(score: Score, filename="output.midi"):
    name = score.name
    tempo = score.tempo
    
    mf = MIDIFile(1)
    track = 0
    time = 0
    
    mf.addTrackName(track, time, name)
    mf.addTempo(track, time, tempo)

    channel = 0
    volume = 80 

    moment: Moment
    for moment in score.score:
        if not moment.note.rest:
            pitch = moment.note.midi
            duration = moment.duration / (BEATS_PER_ROW / divisor) # BEATS_PER_ROW is 1 measure, assuming 4/4, we want one beat = 1/4*measure
            mf.addNote(track, channel, pitch, time, duration, volume)
        time += duration

    # write chords
    time = 0
    cm: ChordMoment
    volume = 80
    for cm in score.chords:
        duration = cm.duration / (BEATS_PER_ROW / divisor)
        min_midi_val = 0
        for note in cm.chord.notes:
            midi_note = note.midi
            if midi_note < min_midi_val:
                midi_note += 12
            min_midi_val = midi_note
            if midi_note < 48: # arbitrary cut off because some chords were way too low. TODO: make configurable
                midi_note += 12
            mf.addNote(track, channel, midi_note - 24, time, duration, volume) # do chords 2 octaves lower
        time += duration
    with open(filename, 'wb') as outf:
        mf.writeFile(outf)


def play_midi(score):
    try:
        freq = 44100
        bitsize = -16
        channels = 1
        buffer = 1024
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(0.8)
        filename="tempfile_forplay.midi"
        make_midi(score, filename=filename)
        clock = pygame.time.Clock()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        time.sleep(1)
        pygame.mixer.music.stop()
        sys.exit()
    except:
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
    raise SystemExit



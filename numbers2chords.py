import sys
from math import floor
from constants import NOTES_SHARP, NOTE_TO_HEX_DICT, HEX_TO_NOTE_DICT
from helpers import get_key_notes

# from https://stackoverflow.com/a/10322018
def get_bits(n):
  return [int(digit) for digit in bin(n)[2:]]

def get_hex(n):
  return [str(digit) for digit in hex(n)[2:]]

"""
This function should be used to generate notes for a given time step.
The array of notes (n>=1) are intended to all fit w/i that time step
The idea here is that a hex digit is mapped to a note in one of two ways...
  1. if the digit is in {a-f, 0}, then return the corresponding note (A-G)
  2. if the digit is in {1-9}, then it is a relative leap from prev_note, calculated as prev_note + digit
Note that option 2 will sometimes spill over a single note, thats why the function should always return an array
The digits should be resolved until you have an array of notes (all in {a-f, 0})

Example:
digit=0x3, prev_note=F
next_note = hex(digit+prev_note) = 0x13
now recursively call hex_to_notes(0x1, F)
  yields hex(0x1 + F) = 0x10
    hex_to_notes(0x1, F)
then hex_to_notes(0x3)
"""
def hex_to_notes(digit, prev_note, octave=0, hex_to_note_dict=HEX_TO_NOTE_DICT, note_to_hex_dict=NOTE_TO_HEX_DICT, notes=NOTES_SHARP): # hex can have 1-to-many with notes
  if hex_to_note_dict.get(digit) is not None:
    new_octave = octave
    if int(str(prev_note), 16) != 7 and int(str(digit), 16) != 7:
      note_loc = 0
      prev_note_loc = 0
      if digit is not None:
        note_loc = notes.index(hex_to_note_dict.get(digit))
      if prev_note is not None:
        prev_note_int = int(str(prev_note), 16)
        prev_note_loc = notes.index(hex_to_note_dict.get(str(prev_note_int)))

      adjusted_diff = (min(prev_note_loc, note_loc) + len(notes)) - max(prev_note_loc, note_loc)
      diff = abs(note_loc - prev_note_loc)
      if diff > adjusted_diff:
        if prev_note_loc < note_loc:
          new_octave -= 1
        else:
          new_octave += 1
    return [(hex_to_note_dict.get(digit), new_octave)]
  else: # This means its not a-f or 0 (so its 1-9)

    # This old way increases octave as we go (i believe)
    # new_octave = floor((prev_note + float(int(digit, 16))) / len(note_to_hex_dict)) + octave
    # This new way should choose the octave for the note that minimizes distance w/ prev note
    return hex_to_notes(hex((prev_note + int(digit, 16)) % len(note_to_hex_dict))[2], hex(int(digit, 16) % len(note_to_hex_dict)), octave=octave, hex_to_note_dict=hex_to_note_dict, note_to_hex_dict=note_to_hex_dict, notes=notes)


if __name__ == "__main__":
  root = 'A'
  note_to_hex_dict = get_key_notes(root, 'MINOR')

  if len(sys.argv) < 3:
    print("Usage: python3 number2chord.py [-b | -h | -n] <base 10 number>")
    sys.exit()

  flag = sys.argv[1]
  if flag == '-b' or flag == '--bits':
    num = int(sys.argv[2])
    print(get_bits(num))
  elif flag == '-h' or flag == '--hex':
    num = int(sys.argv[2])
    print(get_hex(num))
  elif flag == '-n' or flag == '--notes':
    num = int(sys.argv[2])
    hex_num = get_hex(num)
    notes = ['A']
    for digit in hex_num:
      notes.append(hex_to_notes(digit, note_to_hex_dict.get('A')))
    print(notes)



from constants import BEATS_PER_ROW, NOTE_DURATIONS, NOTES_SHARP, NOTES_FLAT, MAJOR_SCALE_PATTERN, MINOR_SCALE_PATTERN
import urllib.request

# mode is MINOR or MAJOR
def get_key_notes(root, mode, is_sharp=True):
    scale_notes = NOTES_SHARP if is_sharp else NOTES_FLAT
    start_index = scale_notes.index(root)
    all_notes = scale_notes if is_sharp else NOTES_FLAT
    scale_pattern = MAJOR_SCALE_PATTERN if mode == "MAJOR" else MINOR_SCALE_PATTERN
    key_notes = []
    for i in scale_pattern:
        key_notes.append(all_notes[(i + start_index) % len(all_notes)])
    note_to_hex_dict = {}
    hex_to_note_dict = {}
    for i, note in enumerate(key_notes):
        note_to_hex_dict[note] = i
        hex_to_note_dict[str(i)] = note
    note_to_hex_dict["REST"] = 7
    hex_to_note_dict["7"] = "REST"

    return (key_notes, note_to_hex_dict, hex_to_note_dict)

def scrape_oeis(seq_name="A356116"):
    url = f"https://oeis.org/{seq_name}/list"
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    start_idx = mystr.index("[")
    end_idx = mystr.index("]")
    num_str = mystr[start_idx:end_idx]
    clean_str = num_str.replace("\n", "")
    res = [int(i) for i in clean_str.split(",") if i.isdigit()]
    return res
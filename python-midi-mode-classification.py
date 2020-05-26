import pygame.midi

def print_devices():
    for n in range(pygame.midi.get_count()):
        print (n,pygame.midi.get_device_info(n))

if __name__ == '__main__':
    pygame.midi.init()
    print_devices()

scales = {"chromatic": [0,1,2,3,4,5,6,7,8,9,10,11], "major": [0,2,4,5,7,9,11], 
"majorPentatonic": [0,2,4,7,9], "minor": [0,2,3,5,7,8,10], "aeolian": [0,2,3,5,7,8,10], 
"minorPentatonic": [0,3,5,7,10], "mixolydian": [0,2,4,5,7,9,10], "melodicMinor": [0,2,3,5,7,9,11], 
"melodicMajor": [0,2,4,5,7,8,11], "harmonicMinor": [0,2,3,5,7,8,11], "harmonicMajor": [0,2,4,5,7,8,11], 
"dorian": [0,2,3,5,7,9,10], "dorian2": [0,1,3,5,6,8,9,11], "diminished": [0,1,3,4,6,7,9,10], 
"egyptian": [0,2,5,7,10], "yu": [0,3,5,7,10], "zhi": [0,2,5,7,9], "phrygian": [0,1,3,5,7,8,10], 
"prometheus": [0,2,4,6,11], "indian": [0,4,5,7,10], "locrian": [0,1,3,5,6,8,10], 
"locrianMajor": [0,2,4,5,6,8,10], "lydian": [0,2,4,6,7,9,11], "lydianMinor": [0,2,4,6,7,8,10], 
"custom": [0,2,3,5,6,9,10], "hungarianMinor": [0,2,3,6,7,8,11], "romanianMinor": [0,2,3,6,7,9,10], 
"chinese": [0,4,6,7,11], "wholeTone": [0,2,4,6,8,10], "halfWhole": [0,1,3,4,6,7,9,10], 
"wholeHalf": [0,2,3,5,6,8,9,11], "bebopMaj": [0,2,4,5,7,8,9,11], "bebopMin": [0,2,3,4,5,9,10], 
"bebopDom": [0,2,4,5,7,9,10,11], "bebopMelMin": [0,2,3,5,7,8,9,11], "blues": [0,3,5,6,7,10], 
"minMaj": [0,2,3,5,7,9,11], "susb9": [0,1,3,5,7,9,10], "lydianAug": [ 0,2,4,6,8,9,11], 
"lydianDom": [0,2,4,6,7,9,10], "melMin5th": [0,2,4,5,7,8,10], "halfDim": [0,2,3,5,6,8,10], "altered": [0,1,3,4,6,8,10]}

midi_note_status = {}
for x in range(0, 128):
    midi_note_status[x] = 0

def midinum_to_pitch_class(number):
    notes = [*range(0, 13, 1)]
    return notes[number%12]

# Order pitches (forked from music21 library)
def get_normal_form(raw_midi_notes):
    pitch_class_list = []
    for i in range(len(raw_midi_notes)):
        pitch_class_list.append(midinum_to_pitch_class(raw_midi_notes[i]))
    print('Unsorted pitches: Not Unique:')
    print(pitch_class_list)
    sorted_pitch_class_list = sorted(pitch_class_list)
    # Remove duplicates
    unique_pitch_class_list = [sorted_pitch_class_list[0]]
    for i in range(1, len(sorted_pitch_class_list)):
        if sorted_pitch_class_list[i] != sorted_pitch_class_list[i - 1]:
            unique_pitch_class_list.append(sorted_pitch_class_list[i])
    interval_list = []
    for i in range(1, len(unique_pitch_class_list)):
        lPC = (unique_pitch_class_list[i] - unique_pitch_class_list[i - 1]) % 12
        interval_list.append(lPC)
    interval_list.append((unique_pitch_class_list[0] - unique_pitch_class_list[-1]) % 12)
    # Make list of rotations
    rotation_list = []
    for i in range(0, len(interval_list)):
        b = interval_list.pop(0)
        interval_list.append(b)
        interval_tuple = tuple(interval_list)
        rotation_list.append(interval_tuple)
    # Sort list of rotations.
    # First entry will be the geometric normal form arranged intervals
    new_rotation_list = sorted(rotation_list)
    # Take that first entry and assign it as the PCIs that we will want for our chord
    geom_norm_chord = new_rotation_list[0]
    # Create final form of Geometric Normal Chord by starting at pc 0 and
    # assigning the notes based on the intervals we just discovered.
    geom_norm_chord_pitches = []
    interval_sum = 0
    for i in range(0, len(geom_norm_chord)):
        geom_norm_chord_pitches.append(interval_sum)
        interval_sum += geom_norm_chord[i]
    print('Normal Form:')
    print(geom_norm_chord_pitches)
    return(geom_norm_chord_pitches)


def dict_to_list(dict_obj, callback):
    new_list = []
    # Iterate over all the items in dictionary
    for (key, value) in dict_obj.items():
        # Check if item satisfies the given condition then add to list
        if callback((key, value)):
            new_list.append(key)
    return new_list


def read_input(input_device):
    midi_note_status = {}
    for x in range(0, 128):
        midi_note_status[x] = 0

    while True:
        if input_device.poll():
            # Midi format =  [[[status, data1, data2, data3], timestamp], ...]
            event = input_device.read(1)[0]
            # Ignore miscellaneous MIDI events
            # https://www.midi.org/specifications-old/item/table-2-expanded-messages-list-status-bytes
            if event[0][0] < 240:
                note_number = event[0][1]
                velocity = event[0][2]
                midi_note_status[note_number] = velocity
                # Select active MIDI notes
                midi_notes = dict_to_list(midi_note_status, lambda elem : elem[1] != 0)
                print('MIDI Note Number(s):')
                print(midi_notes)
                if len(midi_notes) > 0:
                    get_normal_form(midi_notes)
                print("----------------------")

if __name__ == '__main__':
    pygame.midi.init()
    my_input = pygame.midi.Input(1)
    read_input(my_input)

'''
Next steps:
[] Organize data for normal form for specific recognized chords
    - Common name (E.g Maj7)
        - Is there an MIR style guide for this?
        - Want to be able to output current Chord Symbol / Mode for other players to see
    - Start at triads, include 7ths and available tensions
        [] Everything from "Ideal Soloing Scales"
        [] More basic three-note chords
        [] Available tensions
        [] Substitutions

        Possible solution to root identifier problem:
            - Maybe modify get_normal_form function to pair pitch classes with normal form #s?
                - This way I can simply identify which digit of the normal form notation I want 
                to be the root (in the switch/case) and retrieve it

[] Switch/case-like logic for chords and ideal soloing scales
    - https://www.geeksforgeeks.org/switch-case-in-python-replacement/
    - Have ordered lists of ideal soloing scales based on personal preference from most consonant to most dissonant

[] Else: fallback on list matching?
    - https://www.techbeamers.com/program-python-list-contains-elements/


Other tasks:
[] Compare against previous state?
[] Apply deeper logic for 7th chords from Jim Knapp's book

Controllers:
- Expression pedal sweeps through consonant => dissonant spectrum for each sonority
- Logidy button resets analysis (by default, held over if still applicable)
- Logidy button goes back to previous analysis
- Logidy button freezes analysis

'''
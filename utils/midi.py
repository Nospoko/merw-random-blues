import numpy as np
from utils.MidiFile3 import MIDIFile
from matplotlib import pyplot as plt

# TODO make transition from ticks to seconds possible

def matrix_to_midi(notes, filename = 'matrix.mid', tempo = 60):
    """ Note format: PITCH|START|DURATION|VOLUME """
    # Midi file with one track
    mf = MIDIFile(1)

    track = 0
    time = 0
    mf.addTrackName(track, time, filename[7:-4])

    # Default
    # FIXME tempo -- time relation is not well defined
    mf.addTempo(track, time, tempo)
    channel = 0

    time_per_tick = 2**-5

    for note in notes:
        pitch = int(note[0])
        start = note[1] * time_per_tick
        stop  = note[2] * time_per_tick
        vol   = int(note[3])
        mf.addNote(track, channel, pitch, start, stop, vol)

    # Save as file
    with open(filename, 'wb') as fout:
        mf.writeFile(fout)

def test():
    """ Example usage """
    nof_notes = 100
    cosy_fun = lambda jt: np.cos(2*jt) * np.cos(5*jt)
    picz_fun = lambda it: np.floor(30.0 * cosy_fun(4.0 * it/nof_notes))
    pitches = [80 + picz_fun(it) for it in range(nof_notes)]
    times   = [0 + 16 * it for it in range(nof_notes)]
    durations = [16 for _ in range(nof_notes)]
    volumes = [40 + 0.3 * it for it in range(nof_notes)]

    # Create note array
    notes = np.array([pitches, times, durations, volumes]).transpose()

    # Change to file
    matrix_to_midi(notes, 'yo.mid')

    # return notes

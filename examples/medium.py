import os
import numpy as np
from tqdm import tqdm
from utils import midi as um
from utils import graphs as ug
from walkers import merw as wm
from utils import harmony as uh
from matplotlib import pyplot as plt

def doubly_accented_blues_variable_key():
    # Manage files
    folder = 'tmp'
    name = 'example009'
    hi_path = os.path.join(folder, name + '_hi.mid')
    bass_path = os.path.join(folder, name + '_bass.mid')
    song_path = os.path.join(folder, name + '.mid')
    graph_path = os.path.join(folder, name + '.svg')

    # This coud be just a list of vertex values
    # Initialize the duration walker
    duration_values = [4, 8, 16, 24, 32, 40, 48, 56, 64]
    duration_values = [x / 8. for x in duration_values]
    duration_graph = {
            0: [1, 2, 3, 4, 8],
            1: [0, 2, 4],
            2: [0, 1, 3, 5],
            3: [2, 3, 4],
            4: [3, 4, 5, 6, 7, 8],
            5: [3, 4, 5, 6],
            6: [0, 1, 2, 7, 8],
            7: [4, 6, 8, 0, 1],
            8: [0, 1, 2, 4, 5]
            }

    ug.show_graph(duration_graph,
                  duration_values,
                  savepath = graph_path)

    # First vertex
    initial_id = 0
    duration_walker = wm.GraphWalker(duration_graph,
                                     duration_values,
                                     initial_id)

    # Initialize the c-minor pentatonic walker
    blues_grid = [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0]
    blues_keys = uh.grid2keys(blues_grid)

    # Split low and high keys
    nof_lows = 18
    nof_highs = 25

    # Prepare tha bassist
    bass_keys = blues_keys[:nof_lows]
    bass_graph = ug.linear_graph_no_loops(bass_keys)

    bass_walker = wm.GraphWalker(bass_graph,
                                 bass_keys,
                                 12)

    # Prepare the soloist
    blues_keys = blues_keys[-nof_highs:]
    blues_graph = ug.linear_graph_no_loops(blues_keys)

    pitch_walker = wm.GraphWalker(blues_graph,
                                  blues_keys,
                                  initial_id)
    # Accent distances
    accent_graph = {
            0: [1, 2, 3, 4, 5, 6],
            1: [4],
            2: [0, 3, 5],
            3: [0, 4, 6],
            4: [0, 5],
            5: [3],
            6: [0]
            }
    accent_values = accent_graph.keys()
    accent_walker = wm.CuntdownWalker(accent_graph,
                                      accent_values)

    bass_accents = [1 + it for it in range(3, 10)]
    accent_walker_2 = wm.CuntdownWalker(accent_graph,
                                        bass_accents)

    key_count_values = [8 + 2 * it for it in range(7)]

    key_count = wm.CuntdownWalker(accent_graph,
                                  key_count_values)
    scale_step_graph = {
            0: [0, 1, 2],
            1: [0, 1, 2],
            2: [0],
            }

    # It's the I - IV - V graph
    scale_step_values = [0, 5, 7]
    key_walker = wm.GraphWalker(scale_step_graph,
                                scale_step_values)

    # Typicall
    volume_walker = wm.VolumeWalker()

    # Those help to keep the bass legato
    bit = -1
    bass_sta = 0

    # Iterator and container
    sta = 0
    notes = []
    bass_notes = []
    for it in tqdm(range(10000)):
        # Change keys
        if key_count.take_step() and True:
            key = key_walker.next_value()
            grid = np.roll(blues_grid, key)
            keys = uh.grid2keys(grid)

            # Cut out the lower regions
            hi_keys = keys[-nof_highs:]
            pitch_walker.values = hi_keys

            # Cut out the higher regions
            lo_keys = keys[:nof_lows]
            bass_walker.values = lo_keys

        # Make the note components
        vol = volume_walker.next_value()
        pitch = pitch_walker.next_value()
        dur = duration_walker.next_value()

        if accent_walker.take_step():
            vol -= 5
            note = [pitch + 12, sta, dur, vol]
            notes.append(note)

        if accent_walker_2.take_step():
            vol -= 5
            bass = bass_walker.next_value()

            # If not empty
            if bass_notes:
                # Hold the previous notes up to now
                bas_dur = sta - bass_notes[-1][1]
                bass_notes[-1][2] = bas_dur
                bass_notes[-2][2] = bas_dur

            note = [bass, sta, dur, vol]
            bass_notes.append(note)
            note = [bass + 12, sta, dur, vol]
            bass_notes.append(note)

        note = [pitch, sta, dur, vol]
        notes.append(note)

        sta += dur

    # Make the bass notes ring till the end
    # note_sta + note_dur - bass_sta
    bas_dur = notes[-1][1] + notes[-1][2] - bass_notes[-1][1]
    bass_notes[-1][2] = bas_dur
    bass_notes[-2][2] = bas_dur

    # Full song in one file
    full_notes = notes + bass_notes

    notes = np.array(notes)
    full_notes = np.array(full_notes)
    bass_notes = np.array(bass_notes)

    um.matrix_to_midi(notes, hi_path)
    um.matrix_to_midi(bass_notes, bass_path)
    um.matrix_to_midi(full_notes, song_path)

    return song_path, bass_path, hi_path


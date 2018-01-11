import numpy as np
import itertools as itr

class ChordGenerator(object):
    """ Will create any kind of triad with any kind of addition """
    def __init__(self):
        """ For now this is just shitload of chords wrapper """
        # Create basic triads for the base C scale
        # Major           [C, -, D, -, E, F, -, G, -, A, -, H]
        self.full_scale = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]

        self.triads = {
                      # [C, -, D, -, E, F, -, G, -, A, -, H]
                    1 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                    2 : [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                    3 : [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    4 : [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                    5 : [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    6 : [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                    7 : [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
                    }

        self.sextic = {
                      # [C, -, D, -, E, F, -, G, -, A, -, H]
                    1 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                    2 : [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                    3 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    4 : [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                    5 : [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    6 : [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
                    7 : [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
                    }

        self.septimic = {
                      # [C, -, D, -, E, F, -, G, -, A, -, H]
                    1 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    2 : [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                    3 : [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                    4 : [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
                    5 : [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
                    6 : [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                    7 : [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
                    }

        self.nonic = {
                      # [C, -, D, -, E, F, -, G, -, A, -, H]
                    1 : [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                    2 : [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0],
                    3 : [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1],
                    4 : [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
                    5 : [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                    6 : [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                    7 : [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
                    }

    def get_triad(self, which):
        """ Simple triads """
        return self.triads[which]

    def get_nonic(self, which):
        """ Get chord with added ninth """
        return self.nonic[which]

    def get_sextic(self, which):
        """ With sext """
        return self.sextic[which]

    def get_septimic(self, which):
        """ With seventh """
        return self.septimic[which]

def piano_keys():
    """ MIDI note numbers for typical 8-octave keybord go 21::108 """
    values = range(21, 109)

    return values

def grid2keys(grid):
    """Change a octave grid into a full keyboard graph

    Args:
        grid (list of int): Representation of the steps of the
            middle octave that will be allowed in the graph.
    Returns:
        keys (list of int): All of the possible MIDI keys
            allowed on the interaction grid

    """
    piano = piano_keys()

    # We need to make sure, that by defualt
    # the first step of the grid is the note C
    first_step = piano[0] % len(grid)
    grid_shift = len(grid) - first_step
    rolled_grid = np.roll(grid, grid_shift)

    # Iterate cyclically (?) over the rolled_grid     
    cycle = itr.cycle(rolled_grid)

    values = []
    for value in piano:
        in_grid = cycle.next()
        if in_grid == 1:
            values.append(value)

    return values

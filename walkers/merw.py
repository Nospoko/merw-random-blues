import numpy as np
import itertools as itr
import scipy.linalg as lg
from utils import graphs as ug
from utils import probability as up
from matplotlib import pyplot as plt

class MerwWalker(object):
    """ Most abstract maximal enthropy random walker """
    def __init__(self, values, first_id=0):
        """ quo vadis """
        # Values to walk over, by default we should get
        # a infinite well potential situation over those
        self.values     = values
        self.size       = len(self.values)

        # This is the walking space
        self.id_space = range(self.size)

        # TODO fiddle with that also
        self.max_dist = 2

        # This is the walking element
        self.current_id = first_id

        # Init histogram container
        self.histogram = np.zeros_like(self.values)
        self.histogram[self.current_id] += 1

        # Initialize probability matrices
        self.make_S()

    def set_values(self, values):
        """ And update updatebles """
        self.values     = values
        self.size       = len(values)
        self.id_space   = range(self.size)

        # Re-init histogram container
        self.histogram = np.zeros_like(self.values)

        # Recalculate probabilities
        self.make_S()

    def make_A(self):
        """ Prepare A-matrix """
        A = np.zeros((self.size, self.size))

        # TODO This param should be manipulated!
        max_dist = self.max_dist

        # Create interaction matrix A
        for it in range(self.size):
            for jt in range(it - max_dist, it + max_dist + 1):
                if jt >= 0 and jt < self.size:
                    A[it, jt] = self.A_it_jt(it, jt)
        self.A = A

    def A_it_jt(self, it, jt = 0):
        """ This defines merw-interactions """
        return 1

    def make_S(self):
        """ Transition probabilities matrix """
        self.make_A()
        S = np.zeros_like(self.A)

        # FIXME
        # Assuming this is always
        # if self.symmetric == False:

        # Find eigenvalues and eigenvectors
        d, V = lg.eig(self.A)

        # We are guaranteed to be in the Reals
        # So we can switch explicitily
        d = d.real
        V = V.real
        # Find the maximum eigenvalue
        imax = np.argmax(d)
        d = np.max(d)
        # and the corresponding eigenvector
        V = V[:, imax]

        for it in range(self.size):
            for jt in range(self.size):
                if V[it] != 0:
                    S[it,jt] = V[jt]/V[it] * self.A[it,jt]/d
        self.S = S

    def get_histogram(self):
        """ Research helper """
        return self.id_space, self.histogram

    def show_histogram(self):
        """ Pretty please keep plots pretty """
        plt.bar(self.values, self.histogram, color = 'k', alpha = 0.5)
        plt.show()

    def current_value(self):
        """ No movement here """
        return self.values[self.current_id]

    def next_value(self):
        """ Make a merw step """
        probabilities = self.S[self.current_id, :]

        # Get next ID
        next_id = up.randomly_draw(self.id_space, probabilities)
        self.current_id = next_id

        # Update histogram
        self.histogram[self.current_id] += 1

        # Return value
        return self.values[self.current_id]

    # FIXME those are not most abstract
    def set_interaction_grid(self, grid):
        """ This defines possible transitions """
        # Something like:
        # grid = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1] * 8
        self.interaction_grid = grid

class GraphWalker(MerwWalker):
    def __init__(self, graph, values, initial = None):
        """ Konstruktor """
        # number of vertices
        self.graph     = graph
        self.n_vert    = len(graph)

        # First position on the graph
        if initial is None:
            initial = 0

        # Init parent
        MerwWalker.__init__(self, values, initial)

    def make_A(self):
        """ Prepare adjacency matrix """
        A = np.zeros((self.size, self.size))

        for it in range(self.size):
            for jt in range(self.size):
                    A[it, jt] = self.A_it_jt(it, jt)
        self.A = A

    def A_it_jt(self, it, jt):
        """ Graph version of A matrix """
        # vertices numeration starts from 1
        if jt in self.graph[it]:
            # if there is an edge from it to jt
            return 1
        else:
            # no edge
            return 0

class CuntdownWalker(GraphWalker):
    def __init__(self, graph, values):
        GraphWalker.__init__(self, graph, values)
        self.cunter = self.next_value()

    def take_step(self):
        if self.cunter == 0:
            self.cunter = self.next_value()
            return True
        else:
            self.cunter -= 1
            return False

class VolumeWalker(GraphWalker):
    def __init__(self, volume = 80):
        # Make the volume graph
        vol_min = 60
        vol_max = 110

        self.volumes = range(vol_min, vol_max)[::4]
        graph = {}
        graph = ug.linear_graph_no_loops(self.volumes)

        # Init parent
        first_id = self.volumes.index(volume)
        GraphWalker.__init__(self,
                             graph,
                             self.volumes,
                             first_id)

class LinearWalker(GraphWalker):
    """
    This is a genral walker for the 'inifinite box' potential
    value_space (list of value): acting as a position parameter
    """
    def __init__(self, value_space, first):
        self.value_space = value_space
        graph = {}
        for it in range(len(self.value_space)):
            if it == 0:
                # Cut on the left
                graph[it] = [it, it + 1]
            elif it == len(self.value_space) - 1:
                # Cut on the right
                graph[it] = [it - 1, it]
            else:
                graph[it] = [it - 1, it, it + 1]

        # Init parent
        first_id = self.value_space.index(first)
        GraphWalker.__init__(self, first_id, graph)

    def next(self):
        # .next_vertex() actually
        next_it = self.next_value()
        # Here is the value
        value = self.value_space[next_it]

        return value

class LinePotentialWalker(LinearWalker):
    def __init__(self, potential, value_space, first):
        """
        Args:
            potential (arr): exp(-V)
            value_space (arr): Those values are used as vertices
                of the graph that is used to perform the merw on.
            first (vertex value): Initial position of the walker
        """
        self.potential = np.exp(-potential)

        # Init parent
        LinearWalker.__init__(self, value_space, first)

    def set_potential(self, potential):
        self.potential = np.exp(-potential)
        self.make_S()

    def make_A(self):
        """ Prepare adjacency matrix (figures as Mij in j.d. work) """
        A = np.zeros((self.size, self.size))

        for it in range(self.size):
            for jt in range(self.size):
                    A[it, jt] = self.A_it_jt(it, jt) * self.potential[it]
        self.A = A

import numpy as np
import igraph as ig

def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges

def show_graph(graph, values, savepath = None):
    nverts = len(graph)
    edges = generate_edges(graph)

    print('Number of vertices:', nverts)
    print('Number of edges:', len(edges))

    g = ig.Graph(directed = True)
    g.add_vertices(len(graph))
    g.add_edges(edges)

    g.vs["label"] = values
    g.vs["size"]  = [70 for it in range(g.vcount())]
    g.vs['color'] = ['#00FFFF' for _ in range(g.vcount())]
    # layout = g.layout_kamada_kawai()
    layout = g.layout_lgl()
    # layout = g.layout_reingold_tilford_circular()

    # Save to disk
    if savepath:
        ig.plot(g,
                savepath,
                layout = layout,
                bbox = (800, 300),
                margin = 70)
    # Or show on screen
    else:
        ig.plot(g,
                layout = layout,
                bbox = (500, 500),
                margin = 70).show()

def linear_graph(values):
    graph = {}
    for it in range(len(values)):
        if it == 0:
            # Cut on the left
            graph[it] = [it, it + 1]
        elif it == len(values) - 1:
            # Cut on the right
            graph[it] = [it - 1, it]
        else:
            graph[it] = [it - 1, it, it + 1]

    return graph

def linear_graph_no_loops(values):
    graph = {}
    for it in range(len(values)):
        if it == 0:
            # Cut on the left
            graph[it] = [it + 1]
        elif it == len(values) - 1:
            # Cut on the right
            graph[it] = [it - 1]
        else:
            # Without loops you cant repeat
            graph[it] = [it - 1, it + 1]

    return graph

def linear_graph_random_loops(values, prob = 0.5):
    graph = {}
    for it in range(len(values)):
        if it == 0:
            # Cut on the left
            graph[it] = [it, it + 1]
        elif it == len(values) - 1:
            # Cut on the right
            graph[it] = [it - 1, it]
        else:
            if np.random.random() > prob:
                graph[it] = [it - 1, it, it + 1]
            else:
                graph[it] = [it - 1, it + 1]

    return graph

def show_purgatory():
    scale_step_graph = {
            0: [0, 1, 2],
            1: [0, 1, 2],
            2: [0],
            }

    # It's the I - IV - V graph
    scale_step_values = [0, 5, 7]

    savepath = 'tmp/scale_steps.svg'
    show_graph(scale_step_graph,
               scale_step_values,
               savepath = savepath)

    # return duration_graph, duration_values

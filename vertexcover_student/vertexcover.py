#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Nicolas Golenvaux <nicolas.golenvaux@uclouvain.be>"""
from search import *
import sys


class VertexCover(Problem):

    def successor(self, state):
        for u in state.cover:
            state_cover_except_u = list(
                filter(u.__ne__, state.cover)
            )
            for v in state.not_cover:
                state_not_cover_except_v = list(
                    filter(v.__ne__, state.not_cover)
                )
                yield (None, State(state.k,
                                   state.vertices,
                                   state.edges,
                                   state_cover_except_u+[v],
                                   state_not_cover_except_v+[u]))

    def value(self, state):
        reached_nodes = set()
        for v in state.cover:
            reached_nodes.update(state.vertices[v])
        return len(reached_nodes)


class State:

    def __init__(self, k, vertices, edges, cover=None, not_cover=None):
        self.k = k
        self.n_vertices = len(vertices)
        self.n_edges = len(edges)
        self.vertices = vertices
        self.edges = edges
        if cover is None:
            self.cover = self.build_init_cover()
        else:
            self.cover = cover
        if not_cover is None:
            self.not_cover = [v for v in range(
                self.n_vertices) if v not in self.cover]
        else:
            self.not_cover = not_cover

    def build_init_cover(self):
        return list(range(self.k))
        # vertices_degrees = {k: len(v) for k, v in self.vertices.items()}
        # return sorted(vertices_degrees,
        #               key=vertices_degrees.__getitem__, reverse=True)[:self.k]

    def __str__(self):
        s = ''
        for v in sorted(self.cover):
            s += ' ' + str(v)
        return s


def read_instance(instanceFile):
    file = open(instanceFile)
    line = file.readline()
    k = int(line.split(' ')[0])
    n_vertices = int(line.split(' ')[1])
    n_edges = int(line.split(' ')[2])
    vertices = {}
    for i in range(n_vertices):
        vertices[i] = []
    edges = {}
    line = file.readline()
    while line:
        [edge, vertex1, vertex2] = [int(x) for x in line.split(' ')]
        vertices[vertex1] += [edge]
        vertices[vertex2] += [edge]
        edges[edge] = (vertex1, vertex2)
        line = file.readline()
    return k, vertices, edges


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    for _ in range(limit):
        if callback is not None:
            callback(current)

        best_neighbor = None
        for neighbor in current.expand():
            if best_neighbor is None \
                    or neighbor.value() > best_neighbor.value():
                best_neighbor = neighbor
        current = best_neighbor

        if current.value() > best.value():
            best = current
    return best


class MyPriorityQueue(PriorityQueue):
    def peek(self):
        if self.order == min:
            return self.A[0].elem()
        else:
            return self.A[len(self)-1].elem()

    def get_random(self):
        return random.choice(self.A).elem()


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    for _ in range(limit):
        if callback is not None:
            callback(current)

        def neighbors_priority(neighbor):
            return neighbor.value()

        top5_best_neighbors = MyPriorityQueue(f=neighbors_priority)
        for neighbor in current.expand():
            if len(top5_best_neighbors) < 5:
                top5_best_neighbors.append(neighbor)
                continue
            if neighbor.value() > top5_best_neighbors.peek().value():
                top5_best_neighbors.pop()
                top5_best_neighbors.append(neighbor)
        if len(top5_best_neighbors) > 0:
            current = top5_best_neighbors.get_random()

        if current.value() > best.value():
            best = current
    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1], info[2])
    vc_problem = VertexCover(init_state)
    step_limit = 100
    node = randomized_maxvalue(vc_problem, step_limit)
    state = node.state
    print(state)
    # node = randomized_maxvalue(vc_problem, step_limit)
    # state = node.state
    # print(state, vc_problem.value(state))

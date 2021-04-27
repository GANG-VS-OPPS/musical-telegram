'''Module with Graph ADT.'''

from typing import Iterator


class Vertex:
    '''
    Class representation of graph vertex.
    '''

    def __init__(self, value):
        '''
        Initialize a vertex with a value and a dictionary of connections.
        '''
        self._val = value
        self._connections = {}

    @property
    def value(self):
        '''
        Return the value stored in the vertex.
        '''
        return self._val

    @property
    def connections(self) -> dict:
        '''
        Return a dictionary of connections of the vertex.
        '''
        return self._connections

    def get_cost(self, neighbour) -> int:
        '''
        Return the cost of connection from current vertex to the given one.
        '''
        return self._connections[neighbour]

    def add_connection(self, neighbour, cost=0):
        '''
        Connect the given vertex to the current vertex.
        '''
        self._connections[neighbour] = cost

    def __hash__(self):
        '''
        Hash the current vertex.
        '''
        return hash(self._val)

    def __str__(self) -> str:
        '''
        Return a string representation of the vertex.
        '''
        vertex_info = f'Vertex: {str(self._val)}'
        connections_info = f'Connections: {str([adjacent_vertex.value for adjacent_vertex in self._connections])}'
        return '\n'.join((vertex_info, connections_info))


class GraphADT:
    '''
    Class representation of a graph ADT.
    '''

    def __init__(self):
        '''
        Initialize a graph with an empty dictionary of vertices.
        '''
        self.vertices = {}

    @property
    def num_vertices(self) -> int:
        '''
        Return the number of vertices in the graph.
        '''
        return len(self.vertices)

    def add_vertex(self, value) -> Vertex:
        '''
        Add a vertex with the given value to the graph.
        '''
        new_vertex = Vertex(value)
        self.vertices[value] = new_vertex

        return new_vertex

    def __contains__(self, vertex: Vertex) -> bool:
        '''
        Return True if the given vertex is in the graph, False otherwise.
        '''
        return hash(vertex) in self.vertices

    def add_edge(self, vertex_1: Vertex, vertex_2: Vertex, cost: int = 0):
        '''
        Add an edge from vertex_1 to vertex_2 in the graph.
        '''
        if vertex_1 not in self.vertices:
            self.add_vertex(vertex_1)

        if vertex_2 not in self.vertices:
            self.add_vertex(vertex_2)

        self.vertices[vertex_1].add_connection(self.vertices[vertex_2], cost)

    def __iter__(self) -> Iterator:
        '''
        Return an iterator through vertices of the graph.
        '''
        return iter(self.vertices.values())


if __name__ == '__main__':
    # Create a graph
    graph = GraphADT()

    # Add vertices to the graph
    for num in range(6):
        graph.add_vertex(num)

    # Add edges to the graph
    graph.add_edge(0, 1, 5)
    graph.add_edge(0, 5, 2)
    graph.add_edge(1, 2, 4)
    graph.add_edge(2, 3, 9)
    graph.add_edge(3, 4, 7)
    graph.add_edge(3, 5, 3)
    graph.add_edge(4, 0, 1)
    graph.add_edge(5, 4, 8)
    graph.add_edge(5, 2, 1)

    # Print information about all vertices
    for vertex in graph:
        print(vertex)
        print()

    # Print all edges
    for vertex in graph:
        for connection in vertex.connections:
            print(f"({vertex.value}, {connection.value})")

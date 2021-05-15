from graph import Vertex, GraphADT

graph = GraphADT()

# Add vertices to the graph
music_lst = ["Ugo", "Choke", "Forgotten Souls", "Ode", "Believe Me", "On the Inside", "Spinning", "End", "Lake", "No Way Out"]
for song in music_lst:
    graph.add_vertex(song)

# Add edges to the graph
graph.add_edge(music_lst[0], music_lst[8], 5)
graph.add_edge(music_lst[0], music_lst[3], 2)
graph.add_edge(music_lst[1], music_lst[2], 4)
graph.add_edge(music_lst[1], music_lst[0], 9)
graph.add_edge(music_lst[2], music_lst[7], 7)
graph.add_edge(music_lst[3], music_lst[4], 3)
graph.add_edge(music_lst[4], music_lst[1], 1)
graph.add_edge(music_lst[4], music_lst[5], 8)
graph.add_edge(music_lst[5], music_lst[6], 1)
graph.add_edge(music_lst[7], music_lst[1], 1)
graph.add_edge(music_lst[7], music_lst[8], 1)

def find_songs(song):
    for vertex in graph:
        if vertex.value == song:
            return [connection.value for connection in vertex.connections]

# find connected songs
song = "Ugo"
print(find_songs(song))

# input song that does not exists
song1 = "Cats"
print(find_songs(song1))

# input song that has no connections
song2 = "No Way Out"
print(find_songs(song2))

from queue import Queue

nodes_list = {
    "A": ["D","F"],
    "B": ["A","C"],
    "C": ["E","A"],
    "D": ["C","F"],
    "E": ["G","H"],
    "F": ["A","F"],
    "G": ["D","B"],
    "H": ["A","F"],
}

visited = {}
parent  = {}
level   = {} # distance 

result = []

queue = Queue()


for node in nodes_list:
    visited[node] = False
    parent[node]  = None
    level[node]   = -1


visited['A'] = True
level['A'] = 0
queue.put('A')
result = ['A']

while not queue.empty():
    curr_node = queue.get() # remove and return element
    for child in nodes_list[curr_node]:
        if not visited[child]:
            visited[child] = True
            parent[child]  = curr_node
            level[child]   = level[curr_node] + 1
            queue.put(child)
            result.append(child)

print(result)
import heapq

with open("task15/input.txt") as f:
    data = f.read()
    lines = data.splitlines()

width = len(lines[0])
height = len(lines)

class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.neighbors = []

    def add_neighbor(self, neighbor, cost):
        self.neighbors.append((neighbor, cost))

    def __repr__(self) -> str:
        return f"{self.pos}"

    def __str__(self) -> str:
        return f"{self.pos}"

    def __lt__(self, other):
        return True

nodes = {}

for y in range(height):
    for x in range(width):
        value = int(lines[y][x])
        node = Node((x, y), value)
        nodes[(x, y)] = node

def enlarge(graph: dict):
    for i in range(1, 5):
        for x in range(width):
            for y in range(height):
                pos = ((i * width) + x, y)
                org = nodes[(x, y)]
                value = (org.value + i - 1) % 9 + 1
                graph[pos] = Node(pos, value)

    for i in range(1, 5):
        for x in range(width * 5):
            for y in range(height):
                pos = (x, (i * height) + y)
                org = nodes[(x, y)]
                value = (org.value + i - 1) % 9 + 1
                graph[pos] = Node(pos, value)

enlarge(nodes)
width *= 5
height *= 5

for y in range(height):
    for x in range(width):
        node = nodes[(x, y)]

        def add_neighbor(pos):
            n = nodes[pos]
            node.add_neighbor(n, n.value)

        if y != 0:
            add_neighbor((x, y - 1))
        if x != 0:
            add_neighbor((x - 1, y))
        if y != height - 1:
            add_neighbor((x, y + 1))
        if x != width - 1:
            add_neighbor((x + 1, y))

def print_nodes(graph: dict):
    for y in range(height):
        for x in range(width):
            n = graph[(x, y)]
            print(n.value, end="")
        print()

# print_nodes(nodes)
# print()

def dijkstra(graph: dict, start, end):
    unvisited = set(graph.values())
    visited = set()

    heap = []
    distances = {d: float('inf') for d in unvisited}
    predecessors = {}

    distances[start] = 0
    heapq.heappush(heap, (0, start))

    while heap:
        distance, current = heapq.heappop(heap)

        if current in visited:
            continue

        for neighbor, neighbor_distance in current.neighbors:
            new_distance = distance + neighbor_distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current

                heapq.heappush(heap, (new_distance, neighbor))
        
        visited.add(current)
        unvisited.remove(current)

    p = end
    weights = []
    while p != start:
        # print(f"{p.name} -> {p.value}")
        weights.append(p.value)
        p = predecessors[p]
    print(sum(weights))

start = nodes[(0,0)]
end = nodes[(width - 1, height - 1)]
dijkstra(nodes, start, end)
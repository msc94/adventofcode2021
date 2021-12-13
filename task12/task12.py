from collections import Counter

class Node:
    def __init__(self, name: str):
        self.name = name
        self.adjacency_list = set()

    def add_adjacent(self, name: str):
        self.adjacency_list.add(name)

    def __repr__(self) -> str:
        return self.name


with open("task12/input.txt") as f:
    data = f.read()
    lines = data.splitlines()

nodes = dict()

for l in lines:
    parts = l.split("-")
    nodes.setdefault(parts[0], Node(parts[0])).add_adjacent(parts[1])
    nodes.setdefault(parts[1], Node(parts[1])).add_adjacent(parts[0])

def should_visit(name: str, visited: list):
    if name.isupper():
        return True

    ctr = Counter(visited)
    if ctr[name] == 0:
        return True

    if (name == "start" or name == "end"):
        return ctr[name] == 0

    one_small_visited_twice = any([n.islower() and k > 1 for n, k in ctr.items()])
    if not one_small_visited_twice and ctr[name] == 1:
        return True

    return False

def dfs(start: Node, end: Node, visited: list) -> list:
    if start == end:
        return [visited + [end.name]]

    visited.append(start.name)

    routes = []
    for n in start.adjacency_list:
        if should_visit(n, visited):
            new_routes = dfs(nodes[n], end, visited[:])
            routes.extend(new_routes)

    return routes


routes = dfs(nodes["start"], nodes["end"], [])

# for r in routes:
#     for n in r:
#         print(n + ",", end="")
#     print()

print(f"{len(routes)} routes")

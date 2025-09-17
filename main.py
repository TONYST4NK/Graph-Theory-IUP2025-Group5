from collections import defaultdict

# nodes = [1, 2, 3, 4]
# edges = [(1, 2), (2, 3), (3, 4), (4, 1)]

nodes = [1, 2, 3, 4]
edges = [(1, 2), (3, 4)]

# nodes = []
# edges = []


def build_graph(nodes, edges):
    adj = defaultdict(list)
    edge_count = defaultdict(int)

    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        key = frozenset({u, v})
        edge_count[key] += 1

    for n in nodes:
        adj.setdefault(n, [])
    return adj, edge_count


def euler_possible_and_start(nodes, adj):
    deg = {n: len(adj[n]) for n in nodes}
    odd = [n for n in nodes if deg[n] % 2 == 1]
    nonzero = [n for n in nodes if deg[n] > 0]

    if nonzero:
        stack = [nonzero[0]]
        visited = set()
        while stack:
            x = stack.pop()
            if x in visited:
                continue
            visited.add(x)
            for nb in adj[x]:
                if nb not in visited:
                    stack.append(nb)
        if any((n not in visited) for n in nonzero):
            return False, None, odd

    if len(odd) == 0:
        start = nonzero[0] if nonzero else None
        return True, start, odd
    if len(odd) == 2:
        return True, odd[0], odd
    return False, None, odd


def hierholzer(start, adj, edge_count):
    if start is None:
        return []

    iter_pos = {n: 0 for n in adj}
    stack = [start]
    circuit = []

    while stack:
        u = stack[-1]
        pos = iter_pos[u]

        while pos < len(adj[u]):
            v = adj[u][pos]
            key = frozenset({u, v})
            if edge_count.get(key, 0) > 0:
                edge_count[key] -= 1
                iter_pos[u] = pos + 1
                stack.append(v)
                break
            else:
                pos += 1
                iter_pos[u] = pos
        else:
            circuit.append(stack.pop())

    circuit.reverse()
    return circuit


adj, edge_count = build_graph(nodes, edges)


possible, start, odd = euler_possible_and_start(nodes, adj)
if not possible:
    print("euler path not found")
else:
    path = hierholzer(start, adj, edge_count.copy())
    if len(edges) == 0:
        print(path)
    elif path and len(path) == len(edges) + 1:
        print(path)
    else:
        print("euler path not found")

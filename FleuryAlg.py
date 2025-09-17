from collections import defaultdict

class Graph:
    def __init__(self):
        self.adj = defaultdict(list)
        self.edges = {}  # edge_id -> (u, v)
        self.used = set()  # used edge ids
        self._eid = 0

    def add_edge(self, u, v):
        eid = self._eid
        self._eid += 1
        self.edges[eid] = (u, v)
        self.adj[u].append((v, eid))
        self.adj[v].append((u, eid))

    def total_edges(self):
        return len(self.edges)

    def dfs_count(self, v, visited):
        """Count reachable vertices from v using only unused edges."""
        visited.add(v)
        count = 1
        for nbr, eid in self.adj[v]:
            if eid in self.used:
                continue
            if nbr not in visited:
                count += self.dfs_count(nbr, visited)
        return count

    def is_connected(self, start):
        """Check connectivity for vertices with non-zero degree."""
        non_zero = [n for n in self.adj if len(self.adj[n]) > 0]
        if not non_zero:
            return True
        if start is None:
            start = non_zero[0]
        visited = set()
        reachable = self.dfs_count(start, visited)
        return reachable == len(non_zero)

    def is_valid_next_edge(self, u, eid):
        """Return True if edge eid (u--v) can be chosen next (not a bridge unless unavoidable)."""
        # Count unused edges from u
        unused_from_u = [ee for nbr, ee in self.adj[u] if ee not in self.used]
        if len(unused_from_u) == 0:
            return False  # no edge to take
        if len(unused_from_u) == 1:
            return True  # must take the only edge

        # Count reachable vertices before removing edge
        visited_before = set()
        count1 = self.dfs_count(u, visited_before)

        # Temporarily mark edge as used
        self.used.add(eid)

        visited_after = set()
        count2 = self.dfs_count(u, visited_after)

        # Restore the edge
        self.used.remove(eid)

        # If removing the edge reduces reachable count, it's a bridge
        return count1 == count2

    def print_euler_util(self, u, path):
        for nbr, eid in list(self.adj[u]):
            if eid in self.used:
                continue
            if self.is_valid_next_edge(u, eid):
                # use the edge
                self.used.add(eid)
                path.append(nbr)
                self.print_euler_util(nbr, path)

    def find_euler(self):
        # find vertices with odd degree
        odd_vertices = [v for v in self.adj if len(self.adj[v]) % 2 == 1]

        if len(odd_vertices) == 0:
            # choose a vertex with non zero degree as start
            start = next((n for n in self.adj if len(self.adj[n]) > 0), None)
            kind = "Eulerian Circuit"
        elif len(odd_vertices) == 2:
            start = odd_vertices[0]
            kind = "Eulerian Path"
        else:
            print("Euler path not found")
            return

        if start is None:
            # empty graph (no edges)
            print("Euler path not found")
            return

        # graph must be connected (ignore zero degree vertices)
        if not self.is_connected(start):
            print("Euler path not found")
            return

        path = [start]
        self.print_euler_util(start, path)

        if len(self.used) != self.total_edges():
            # not all edges were used -> something wrong / disconnected
            print("Euler path not found")
            return

        print(f"{kind}:")
        print(" -> ".join(path))


# MAIN
nodes = input("Enter nodes: ").split()
edges = input("Enter edges (ex : A-B B-C C-A): ").split()

g = Graph()
for edge in edges:
    u, v = edge.split('-')
    g.add_edge(u.strip(), v.strip())

g.find_euler()

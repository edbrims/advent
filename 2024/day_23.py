from utils import get_input
from collections import defaultdict

use_real = True
example_input = '''
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''

class Cluster:
    def __init__(self, nodes):
        self.nodes = nodes

    def __repr__(self):
        return f"{",".join(sorted(list(self.nodes)))}"

    def __eq__(self, __value: object) -> bool:
        return self.nodes == __value.nodes

    def __hash__(self) -> int:
        return self.__repr__().__hash__()

connections = defaultdict(lambda: set())
t_nodes = set()
lines = get_input(use_real, example_input, __file__)
for line in lines:
    nodes = line.split("-")
    connections[nodes[0]].add(nodes[1])
    connections[nodes[1]].add(nodes[0])
    for node in nodes:
        if node[0] == "t":
            t_nodes.add(node)

def find_t_triangles(connections, t_nodes):
    triangles = set()
    for t in t_nodes:
        neighbours = connections[t]
        for neighbour in neighbours:
            for neighbour_of_neighbour in connections[neighbour]:
                if neighbour_of_neighbour in neighbours:
                    triangle = Cluster({t, neighbour, neighbour_of_neighbour})
                    triangles.add(triangle)
    return triangles

triangles = find_t_triangles(connections, t_nodes)

def find_clusters_of_size(connections, size, smaller_clusters):
    clusters = set()
    for cluster in smaller_clusters:
        for extra_node in connections.keys():
            for cluster_node in cluster.nodes:
                if cluster_node not in connections[extra_node]:
                    break
            else:
                new_cluster = Cluster(cluster.nodes.union({extra_node}))
                clusters.add(new_cluster)

    return clusters

def find_largest_cluster(connections):
    clusters = {Cluster({k}) for k in connections.keys()}
    size = 1

    while clusters:
        size += 1
        new_clusters = find_clusters_of_size(connections, size, clusters)
        print(f"{size}: {len(new_clusters)}")
        if not new_clusters:
            (largest_cluster,) = clusters
            return largest_cluster
        clusters = new_clusters

print(f"Part 1: {len(triangles)}") # 1423
print(f"Part 2: {find_largest_cluster(connections)}") # gt,ha,ir,jn,jq,kb,lr,lt,nl,oj,pp,qh,vy

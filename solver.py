import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys

def solve(G):
    unexplored = []
    start_vertex = list(G.nodes())[0]
    tree = nx.Graph()
    tree.add_node(start_vertex)
    for vertex in G.neighbors(start_vertex):
        unexplored.append(vertex)
    current_node = start_vertex
    while current_node != None:
        next_node = choose_best_neighbor(G, tree)
        current_node = next_node
        if current_node != None:
            for vertex in G.neighbors(current_node):
                if vertex not in unexplored:
                    if vertex not in tree.nodes():
                        unexplored.append(vertex)
            unexplored.remove(current_node)

    return remove_leaves(G, tree)

def choose_best_neighbor(G, tree):
    least_pairwise_distance = float('inf')
    least_pairwise_neighbor = None
    least_pairwise_vertex = None
    for t in tree.nodes():
       for n in list(G.neighbors(t)):
            if n not in tree.nodes():
                edge_weight = G[t][n]['weight']
                tree.add_edge(t, n, weight=edge_weight)
                pairwise_distance = average_pairwise_distance_fast(tree)
                if pairwise_distance < least_pairwise_distance:
                    least_pairwise_vertex = t
                    least_pairwise_neighbor = n
                    least_pairwise_distance = pairwise_distance
                tree.remove_node(n) 
    if (least_pairwise_vertex != None and least_pairwise_neighbor != None):
        edge_weight = G[least_pairwise_vertex][least_pairwise_neighbor]['weight']
        tree.add_edge(least_pairwise_vertex, least_pairwise_neighbor, weight=edge_weight)
    return least_pairwise_neighbor

def remove_leaves(G, tree):
    all_leaves = []
    new_leaves = find_new_leaves(tree, [],  all_leaves)
    for leaf in new_leaves:
        cost_with_leaf = average_pairwise_distance_fast(tree)
        for neighbor in tree.neighbors(leaf):
            neighbor_leaf = neighbor
        tree.remove_node(leaf) 
        cost_without_leaf = average_pairwise_distance_fast(tree)
        if (nx.is_dominating_set(G, tree.nodes())):
             if cost_with_leaf < cost_without_leaf:
                 edge_weight = G[neighbor_leaf][leaf]['weight']
                 tree.add_edge(neighbor_leaf, leaf, weight=edge_weight)
        else:
            edge_weight = G[neighbor_leaf][leaf]['weight']
            tree.add_edge(leaf, neighbor_leaf, weight=edge_weight)
        new_leaves.remove(leaf)
        new_leaves = find_new_leaves(tree, new_leaves, all_leaves)
    return tree

def find_new_leaves(tree, new_leaves, all_leaves):
    for v in tree.nodes():
        if tree.degree(v) == 1 and v not in all_leaves:
            all_leaves.append(v)
            new_leaves.append(v)
    return new_leaves



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

#if __name__ == '__main__':
#    assert len(sys.argv) == 2
#    path = sys.argv[1]
#    G = read_input_file(path)
#    T = solve(G)
#    assert is_valid_network(G, T)
#    print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#    write_output_file(T, 'out/test.out')

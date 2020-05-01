import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys


# def solve(G):
 

# Start at any vertex v. 
# Explores all its neighbors and go to the one with the least pairwise 
# distance. 
# Continue until we find the whole tree. 
# Remove the leaves iff it reduces the overall cost 
# (prevents us from removing something <1). 
# Repeat for all vertices. Compare the graphs and return 
# the one with the least cost

def solve(G):
    unexplored = []
    start_vertex = list(G.nodes())[0]
    tree = nx.Graph()
    tree.add_node(start_vertex)
    for vertex in G.nodes():
    	unexplored.append(vertex)
    current_node = start_vertex
    while unexplored:
        next_node = choose_best_neighbor(G, current_node, tree, unexplored)
        tree.add_edge(current_node, next_node)
        current_node = next_node
    return remove_leaves(tree)

def choose_best_neighbor(G, v, tree, unexplored):
    least_pairwise_distance = float('inf')
    least_pairwise_neighbor = None
    for n in G.neighbors(v):
    	tree.add_edge(v, n)
    	pairwise_distance = average_pairwise_distance(tree)
    	if pairwise_distance < least_pairwise_distance:
    		least_pairwise_neighbor = n
    		least_pairwise_distance = pairwise_distance
    	tree.remove_node(n) 
    	if n in unexplored:
    		unexplored.remove(n)
    return least_pairwise_neighbor

def remove_leaves(tree):
    leaves = []
    for v in nodes(tree):
    	if degree(v) == 1:
    		leaves.append(v)
    for leaf in leaves:
    	previous_cost = average_pairwise_distance(tree)
    	neighbor_leaf = G.neighbors(leaf)
    	tree.remove_node(leaf)
    	if average_pairwise_distance(tree) > previous_cost:
    		tree.add_edge(leaf, neighbor_leaf)
    return tree


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
	assert len(sys.argv) == 2
	path = sys.argv[1]
	G = read_input_file(path)
	T = solve(G)
	assert is_valid_network(G, T)
	print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
	write_output_file(T, 'out/test.out')

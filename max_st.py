from parse import *
import networkx as nx
from solver import *
import os

if __name__ == "__main__":
    output_dir = "outputs"
    input_dir = "inputs/large"
    counter = 0
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        G = read_input_file(f"{input_dir}/{input_path}")
        T = solve(G)
        print(counter)
        print(graph_name)
        counter += 1
        assert is_valid_network(G, T)
        write_output_file(T, f"outputs/{graph_name}.out")

#     G = read_input_file(f"{input_dir}/small-circle.in")
#     T = solve(G)
#     assert is_valid_network(G, T)
#     write_output_file(T, f"outputs/small-circle.out")

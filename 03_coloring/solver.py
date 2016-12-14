#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    A = np.zeros((node_count,edge_count))
    for i in range(edge_count):
        A[edges[i][0],i] = 1
        A[edges[i][1],i] = -1

    edges_per_node = []
    for i in range(node_count):
        edges_per_node.append(sum(abs(A[i][:])))
    print(edges_per_node)
    color_vector = np.ones((node_count))
    color_check  = np.dot(color_vector,A)

    # print(A)
    # while any(node == 0 for node in color_check):
    for i in range(2,400):
        # print(color_vector)
        # print(color_check)

        max_index = edges_per_node.index(max(edges_per_node))
        edges_per_node[max_index]-=1
        color_vector[max_index]+=1
        color_check  = np.dot(color_vector,A)
        print(color_check.tolist().count(0))

    # print(edges_per_node)
    # build a trivial solution
    # every node has its own color
    solution = map(int, color_vector.tolist())#range(0, node_count)
    solution = list(item-1 for item in solution)
    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

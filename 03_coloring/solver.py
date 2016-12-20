#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

class colorNode(object):
    "objet representing node and the available soultion space left for it"
    def __init__(self,index,totalNodes,conectedNodes):
        # self.__init__()
        self.index         = index
        self.availableSet  = set(range(totalNodes))
        self.conectedNodes = conectedNodes
        self.color         = None
        self.decided       = False

def solve_it(input_data):
    lines = input_data.split('\n')
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    nodeList = []
    for i in range(node_count):
        nodeList.append(colorNode(i,node_count,set()))

    checkMetrix = np.zeros((node_count,edge_count))
    for i in range(edge_count):
        nodeList[edges[i][0]].conectedNodes.add(nodeList[edges[i][1]])
        nodeList[edges[i][1]].conectedNodes.add(nodeList[edges[i][0]])
        checkMetrix[edges[i][0]][i] =  1
        checkMetrix[edges[i][1]][i] = -1

    nodeList = sorted(nodeList, key=lambda colorNode:len(colorNode.conectedNodes), reverse=True)

    for node in nodeList:
        if not node.decided:
            unnavailableSet=set()
            for neighbour in node.conectedNodes:
                if neighbour.decided:
                    unnavailableSet.add(neighbour.color)
            node.availableSet = node.availableSet.difference(unnavailableSet)
            node.color = min(node.availableSet)
            node.decided=True

    # print( ' '.join(map(str, [node.index for node in nodeList])))
    # print( ' '.join(map(str, [node.color for node in nodeList])))
    # print( ' '.join(map(str, [len(node.conectedNodes) for node in nodeList])))


    nodeList = sorted(nodeList, key=lambda colorNode:colorNode.index)

    solution = [node.color for node in nodeList]
    if 0 in (np.dot(np.array(solution),checkMetrix)):
        print("ALAAAARM!!!!")

    output_data = str(len(set(solution))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        # file_location ="data/gc_4_1"
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

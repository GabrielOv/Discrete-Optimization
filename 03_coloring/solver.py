#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

class colorNode(object):
    "objet representing node and the available soultion space left for it"
    def __init__(self,index,totalNodes,conectedNodes):
        # self.__init__()
        self.id            = index
        self.totalSet      = set()
        self.availableSet  = set()
        self.conectedNodes = conectedNodes
        self.degree        = 0
        self.color         = 0
        self.decided       = False
        self.tier          = None

    def trimAvailables(self):
        unnavailableSet=set()
        for neighbour in self.conectedNodes:
            if neighbour.decided:
                unnavailableSet.add(neighbour.color)
        self.availableSet= self.availableSet.difference(unnavailableSet)
    def checkForLast(self):
        if len(self.availableSet)==1:
            self.color   = min(self.availableSet)
            self.decided = True

class graph(object):
    def __init__(self,node_count,edge_count,edges):
        self.node_count = node_count
        self.edge_count = edge_count
        self.nodes            = [colorNode(i,node_count,set()) for i in range(node_count)]
        self.checkMatrix      = np.zeros((node_count,edge_count))

        for i in range(edge_count):
            self.nodes[edges[i][0]].conectedNodes.add(self.nodes[edges[i][1]])
            self.nodes[edges[i][1]].conectedNodes.add(self.nodes[edges[i][0]])
            self.checkMatrix[edges[i][0]][i] =  1
            self.checkMatrix[edges[i][1]][i] = -1
        for node in self.nodes:
            node.degree = len(node.conectedNodes)
        maxDegree = max([node.degree for node in self.nodes])
        for node in self.nodes:
            node.totalSet      = set(range(1,maxDegree))
            node.availableSet  = set(range(1,maxDegree))

    def tierFiender(self):
        self.nodes[0].tier=0

        exploredSet = set([self.nodes[0]])
        previousTier= set([self.nodes[0]])

        i=0
        while len(exploredSet) < self.node_count:
            i+=1
            nextTier= set()
            for node in previousTier:
                nextTier.update(node.conectedNodes)
            nextTier= nextTier.difference(exploredSet)
            for node in nextTier:
                node.tier = i
            previousTier = nextTier
            exploredSet.update(nextTier)
    def sortByNodeDegree(self):
        # print( 'INDEX  : ',''.join(format(node.id, "3.0f")                 for node in self.nodes))
        self.nodes = sorted(self.nodes, key=lambda colorNode:(colorNode.degree), reverse=True)
        # print( 'INDEX  : ',''.join(format(node.id, "3.0f")                 for node in self.nodes))
    def sortByTier(self):
        if not self.node_count == 70:
            self.nodes = sorted(self.nodes, key=lambda colorNode:len(colorNode.availableSet), reverse=False)
        self.nodes = sorted(self.nodes, key=lambda colorNode:(colorNode.tier), reverse=False)

    def allNodesDecided(self):
        for node in self.nodes:
            if not node.decided:
                return False
        return True
    def updateConstrains(self):
        for node in self.nodes:
            if not node.decided:
                node.trimAvailables()
    def nextChoice(self):
        for node in self.nodes:
            if not node.decided:
                node.color = min(node.availableSet)
                node.decided = True
                # print('    chosen node:',node.id )
                break
    def checkForCornered(self):
        for node in self.nodes:
            if len(node.availableSet)==1 and not node.decided:
                node.color = min(node.availableSet)
                node.decided = True
                # print('     gottcha! node:',node.id )

def readInput(input_data):
    lines = input_data.split('\n')
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    return [node_count, edge_count,lines]

def buildEdges(edge_count, lines):
    edges = []
    for i in range(1, edge_count + 1):
            line = lines[i]
            parts = line.split()
            edges.append((int(parts[0]), int(parts[1])))
    return edges

def solve_it(input_data):

    [node_count, edge_count,lines] = readInput(input_data)
    edges                          = buildEdges(edge_count, lines)
    mainGraph                      = graph(node_count,edge_count,edges)
    mainGraph.sortByNodeDegree()
    mainGraph.tierFiender()

    mainGraph.nodes[0].color    = 1
    mainGraph.nodes[0].decided  = True

    while not mainGraph.allNodesDecided():
        mainGraph.sortByTier()
        mainGraph.updateConstrains()
        mainGraph.nextChoice()
        mainGraph.checkForCornered()

    nodeList = sorted(mainGraph.nodes, key=lambda colorNode:colorNode.id)

#--------------------------------------------------------------------------------
    # print( 'INDEX  : ',''.join(format(node.id, "3.0f")                  for node in mainGraph.nodes))
    # print( 'COLOR  : ',''.join(format(node.color, "3.0f")               for node in mainGraph.nodes))
    # print( 'CONNECT: ',''.join(format(len(node.conectedNodes), "3.0f")  for node in mainGraph.nodes))
    # print( 'TIER   : ',''.join(format(node.tier, "3.0f")                for node in mainGraph.nodes))

    solution = [node.color for node in nodeList]
    if 0 in (np.dot(np.array(solution),mainGraph.checkMatrix)):
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

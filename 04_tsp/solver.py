#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import argparse
import csv
from ortools.constraint_solver import pywrapcp
# You need to import routing_enums_pb2 after pywrapcp!
from ortools.constraint_solver import routing_enums_pb2

# parser = argparse.ArgumentParser()
# parser.add_argument('--tsp_size', default = 10, type = int, help='Size of Traveling Salesman Problem instance.')
# parser.add_argument('--tsp_use_random_matrix', default=True, type=bool, help='Use random cost matrix.')
# parser.add_argument('--tsp_random_forbidden_connections', default = 0, type = int, help='Number of random forbidden connections.')
# parser.add_argument('--tsp_random_seed', default = 0, type = int, help = 'Random seed.')
# parser.add_argument('--light_propagation', default = False, type = bool, help = 'Use light propagation')
# parser.add_argument('--data_file', default = False, type = str, help = 'This test requires an input file')

# Cost/distance functions.
class point(object):
    def __init__(self,index,xCoord,yCoord):
        self.id = index
        self.x  = xCoord
        self.y  = yCoord
    def pointAsArray(self):
        return (np.array([self.x, self.y]))
    def distanceTo(self,otherPoint):
        return math.sqrt((self.x - otherPoint.x)**2 + (self.y - otherPoint.y)**2)

class RandomMatrix(object):
    """Random matrix."""
    def __init__(self,input_data):
        """Initialize random matrix."""
        self.points = loadInputFromFile(input_data)
        self.matrix = {}
        for from_node in range(len(self.points)):
            self.matrix[from_node] = {}
            for to_node in range(len(self.points)):
                if from_node == to_node:
                    self.matrix[from_node][to_node] = 0
                else:
                    self.matrix[from_node][to_node] = Distance(self.points[from_node],self.points[to_node])
        # print(self.matrix)

    def Distance(self, from_node, to_node):
        return self.matrix[from_node][to_node]

def Distance(i, j):
  return i.distanceTo(j)
def csvOutput(matrix, routeList):
    with open('ordered.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for index in routeList[1:]:
            point = matrix.points[int(index)]
            spamwriter.writerow([point.x,point.y])

def loadInputFromFile(input_data):
    lines = input_data.split('\n')
    nodeCount = int(lines[0])
    points = []
    line = lines[1]
    parts = line.split()
    if nodeCount < 20000:
        for i in range(1,nodeCount+1):
            line = lines[i]
            parts = line.split()
            points.append(point(i,float(parts[0]), float(parts[1])))
        return points
    else:
        for i in range(1,nodeCount+1):
            line = lines[i]
            parts = line.split()
            points.append(point(i,float(parts[0]), float(parts[1])))
        return points


def solve_it(input_data):
  # Create routing model
  # if args.tsp_size > 0:
    # TSP of size args.tsp_size
    # Second argument = 1 to build a single tour (it's a TSP).
    # Nodes are indexed from 0 to parser_tsp_size - 1, by default the start of
    # the route is node 0.
    matrix = RandomMatrix(input_data)
    tsp_size=len(matrix.points)
    routing = pywrapcp.RoutingModel(tsp_size, 1, 0)

    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    # Setting first solution heuristic (cheapest addition).
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Setting the cost function.
    # Put a callback to the distance accessor here. The callback takes two
    # arguments (the from and to node inidices) and returns the distance between
    # these nodes.

    matrix_callback = matrix.Distance
    tsp_use_random_matrix = True
    if tsp_use_random_matrix:
      routing.SetArcCostEvaluatorOfAllVehicles(matrix_callback)
    else:
      routing.SetArcCostEvaluatorOfAllVehicles(Distance)
    # Forbid node connections (randomly).
    rand = random.Random()
    rand.seed(1)# rand.seed(args.tsp_random_seed)
    forbidden_connections = 0
    while forbidden_connections < 0:# while forbidden_connections < args.tsp_random_forbidden_connections:
        from_node = rand.randrange(tsp_size - 1)
        to_node = rand.randrange(tsp_size - 1) + 1
        if routing.NextVar(from_node).Contains(to_node):
            print('Forbidding connection ' + str(from_node) + ' -> ' + str(to_node))
            routing.NextVar(from_node).RemoveValue(to_node)
            forbidden_connections += 1

    # Solve, returns a solution if any.
#    assignment = routing.SolveWithParameters(search_parameters)
    assignment = routing.Solve()
    if assignment:
        # Solution cost.
        # print(assignment.ObjectiveValue())
        # Inspect solution.
        # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
        route_number = 0
        node = routing.Start(route_number)
        route = ''
        while not routing.IsEnd(node):
            route += ' '+ str(node)
            node = assignment.Value(routing.NextVar(node))
        # route += '0'
        nodeList = route.split()[1:]
        # totalDistance = assignment.ObjectiveValue() + matrix.points[int(nodeList[0])].distanceTo(matrix.points[int(nodeList[-1])])
        # print(totalDistance)
        output_data = '%.2f' % assignment.ObjectiveValue() + ' ' + str(0) + '\n'
        output_data += route
        # output_data += ' '.join(map(str, solution))
        csvOutput(matrix,route.split(' '))
        return output_data

    else:
        print('No solution found.')
  # else:
  #   print('Specify an instance greater than 0.')

if __name__ == '__main__':

    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) > 1:
#         file_location = sys.argv[1].strip()
#         with open(file_location, 'r') as input_data_file:
#             input_data = input_data_file.read()
#         print(solve_it(input_data))
#     else:
#         print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

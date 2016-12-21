#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
from collections import namedtuple
import csv

class point(object):
    def __init__(self,index,xCoord,yCoord):
        self.id = index
        self.x  = xCoord
        self.y  = yCoord
    def pointAsArray(self):
        return (np.array([self.x, self.y]))

class cloud(object):
    def __init__(self):
        self.nodeCount = 0
        self.points = []
        # self.allPoints  = set()
        self.usedPoints  = set()
        self.unmappedPoints = set()
        self.ordered   = []
        self.maxX      = 0
        self.minX      = 0
        self.maxY      = 0
        self.minY      = 0
    def loadInputFromFile(self,input_data):
        lines = input_data.split('\n')
        self.nodeCount = int(lines[0])

        line = lines[1]
        parts = line.split()
        self.points.append(point(1,float(parts[0]), float(parts[1])))
        self.maxX=float(parts[0])
        self.minX=float(parts[0])
        self.maxY=float(parts[1])
        self.minY=float(parts[1])
        for i in range(2,len(lines)-1):
            line = lines[i]
            parts = line.split()
            self.points.append(point(i,float(parts[0]), float(parts[1])))
            if float(parts[0]) > self.maxX: self.maxX = float(parts[0])
            if float(parts[0]) < self.minX: self.minX = float(parts[0])
            if float(parts[1]) > self.maxY: self.maxY = float(parts[1])
            if float(parts[1]) < self.minY: self.minY = float(parts[1])

        self.usedPoints      = set()
        self.unmappedPoints = set(self.points)
    def loadInputFromList(self,pointList):
        self.nodeCount = len(pointList)
        self.points = pointList
        self.maxX=self.points[0].x
        self.minX=self.points[0].x
        self.maxY=self.points[0].y
        self.minY=self.points[0].y

        for i in range(1, len(pointList)):
            if pointList[i].x > self.maxX: self.maxX=pointList[i].x+1
            if pointList[i].x < self.minX: self.minX=pointList[i].x-1
            if pointList[i].y > self.maxY: self.maxY=pointList[i].y+1
            if pointList[i].y < self.minY: self.minY=pointList[i].y-1

        self.usedPoints      = set()
        self.unmappedPoints = set(self.points)
    def pointChosen(self,point):
        self.ordered.append(point)
        self.usedPoints.update([point])
        self.unmappedPoints.discard(point)
    def evaluateDistances(self,point):
        distances = []
        for p in self.unmappedPoints:
            distances.append((length(p.pointAsArray(), point.pointAsArray()),p))

        distances = sorted(distances, key=getKey)
        return(distances[0][1])
    def totalDistance(self):
        totalDistance = 0
        for i in range(len(self.points)-1):
            totalDistance += length(self.ordered[i].pointAsArray(),self.ordered[i+1].pointAsArray())
        totalDistance += length(self.ordered[-1].pointAsArray(),self.ordered[0].pointAsArray())
        return totalDistance

def getKey(item):
    return item[0]
def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
def idForFarthest(cloud):
    pointCloud = []
    for point in cloud.points:
        pointCloud.append(point.pointAsArray())
    centerPoint = np.mean(pointCloud, axis = 0)
    distancesToCenter=[]
    for point in pointCloud:
        distancesToCenter.append(length(point,centerPoint))
    index_max = np.argmax(distancesToCenter)
    return index_max
def csvOutput(cloud):
    with open('ordered.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for point in cloud.ordered:
            spamwriter.writerow([point.x,point.y])
def greddyForProximity(dataSet):
    startPoint = dataSet.points[idForFarthest(dataSet)]
    dataSet.pointChosen(startPoint)
    while dataSet.unmappedPoints:
        dataSet.pointChosen(dataSet.evaluateDistances(dataSet.ordered[-1]))
    solution = [p.id for p in dataSet.ordered]
    obj = (dataSet.totalDistance())
    return [solution, obj]
def trivialSolution(dataSet):
    solution = [p.id for p in dataSet.points]
    dataSet.ordered = dataSet.points
    obj = (dataSet.totalDistance())
    return [solution, obj]
def binarizer(dataSet,resolution):

    xLength = dataSet.maxX-dataSet.minX
    xSpan   = xLength/resolution
    yLength = dataSet.maxY-dataSet.minY
    ySpan   = yLength/resolution
    limitsX = [(dataSet.minX+i*xSpan) for i in range(resolution+1)]
    limitsY = [(dataSet.minY+i*ySpan) for i in range(resolution+1)]

    bins = []
    for i in range(resolution):
        for j in range(resolution):
            auxPointList = []
            auxCloud = cloud()
            mappedSet=set()
            for point in dataSet.unmappedPoints:
                if point.x >= limitsX[i] and point.x <= limitsX[i+1]:
                    if point.y >= limitsY[j] and point.y <= limitsY[j+1]:
                        auxPointList.append(point)
            if auxPointList:
                auxCloud.loadInputFromList(auxPointList)
            bins.append(auxCloud)

    startPoint   = bins[0].points[idForFarthest(bins[0])]
    solutionList = []

    orderList = []
    for i in range(resolution**2):
        if (math.floor(i/resolution) % 2 == 0):
            orderList.append(i)
        else:
            orderList.append(math.floor(i/resolution)*resolution-1+resolution-i%resolution)

    print(orderList)
    for i in orderList:#range(0,len(bins)):
        bins[i].pointChosen(startPoint)
        while bins[i].unmappedPoints:
            bins[i].pointChosen(bins[i].evaluateDistances(bins[i].ordered[-1]))
        startPoint = bins[i].ordered[-1]

    finalOrder = [bins[0].ordered[0]]
    # for group in bins:
    for i in orderList:
        finalOrder += bins[i].ordered[1:]

    # print(len(finalOrder))
    dataSet.ordered = finalOrder

    solution = [p.id for p in dataSet.ordered]

    obj = (dataSet.totalDistance())
    return [solution, obj]


def solve_it(input_data):

    dataSet = cloud()
    dataSet.loadInputFromFile(input_data)

    # [solution, obj] = greddyForProximity(dataSet)
    # [solution, obj] = trivialSolution(dataSet)
    [solution, obj] = binarizer(dataSet,10)
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    csvOutput(dataSet)
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

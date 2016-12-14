#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import math
from numpy import dot
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def int2bin(i,padTo):
    padTo = int(math.sqrt(padTo))
    s = []
    while i:
        if i & 1 == 1.0:
            s = [1] + s
        else:
            s = [0] + s
        i =int(i/2)

    r = [0]*(padTo-len(s))
    return r+s
def brute_force(items,capacity):
    #for item in items:
    valueList =[]
    weightList=[]
    for item in items:
        valueList.append(item.value)
        weightList.append(item.weight)
    print(capacity)
    print(valueList)
    print(weightList)

    allCombos = pow(len(items),2)

    valueCombos=[]
    weightCombos=[]

    for i in range(allCombos):
        weightCombos.append(dot(int2bin(i,allCombos),weightList))
        if weightCombos[-1] <= capacity:
            valueCombos.append(dot(int2bin(i,allCombos),valueList))
        else:
            valueCombos.append(0)

    max_index = valueCombos.index(max(valueCombos))
    print(capacity-weightCombos[max_index])
    print(max(valueCombos))
    return [valueCombos[max_index],weightCombos[max_index],int2bin(max_index,allCombos),1]
def simpleGreddy(items,capacity):

    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return [value,weight,taken,0]
def orderlyGreddy(items,capacity):

    value = 0
    weight = 0
    taken = [0]*len(items)

    def getKey(item):
        # print(item.index,"  ",item.density*(1+0.001*(item.weight/capacity)))
        return item.density*(1+0.0001*(1-item.weight/capacity))
    items = sorted(items, key = getKey, reverse=True)
    # for item in items:
    #     print(item.index,"  ",item.weight,"  ",item.density)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return [value,weight,taken,0]
def depthFirst_trimer(items,capacity):
    Node = namedtuple("Node", ['tier', 'value', 'room', 'estimate','taken'])

    value = 0
    weight = 0
    taken = [0]*len(items)
    # def getKey(item):
    #     return item.density
    # items = sorted(items, key = getKey, reverse=True)
    indexList=[]
    valueList =[]
    weightList=[]
    densityList=[]
    for item in items:
        indexList.append(item.index)
        weightList.append(item.weight)
        valueList.append(item.value)
        densityList.append(item.density)

    averageRemainingDensity =[]
    for i in range(len(items)):
        averageRemainingDensity.append(sum(item.density*item.weight for item in items[i:])/sum(item.weight for item in items[i:]))

    def evaluate_options(valueList,weightList,averageRemainingDensity,combo,tier,capacity):
        room = capacity - dot(combo,weightList)
        if room < 0:
            return [0, 0, 0, False]

        value = dot(combo,valueList)
        estimate = value + averageRemainingDensity[tier]*room
        return [value, room, estimate, True]
    # [value, room, estimate, True] = evaluate_options(valueList,weightList,averageRemainingDensity,node.taken)
    # for tier in range(len())

    return [value,weight,taken,0]
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    start_time = time.time()
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float(parts[0])/float(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    # value1 = 0
    # weight1 = 0
    # taken1 = []
    #
    # value2 = 0
    # weight2 = 0
    # taken2= []

    [value1,weight1,taken1,optimal1] = simpleGreddy(items,capacity)
    [value2,weight2,taken2,optimal2] = orderlyGreddy(items,capacity)

    if value1 > value2:
        [value,weight,taken,optimal]=[value1,weight1,taken1,optimal1]
    else:
        [value,weight,taken,optimal]=[value2,weight2,taken2,optimal2]

    #[value,weight,taken,optimal] = brute_force(items,capacity)
    #[value,weight,taken,optimal] = average_density_trimer(items,capacity)

    # prepare the solution in the specified output format
    print(weight, "/", capacity)
    output_data = str(value) + ' ' + str(optimal) + '\n'
    output_data += ' '.join(map(str, taken))
    # print("--- %s seconds ---" % (time.time() - start_time))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

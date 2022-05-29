#!/usr/bin/python

#
# Use the neighbour joining algorithm to build a tree
#

import sys
import numpy as np
import scipy as scipy
import itertools
import sys
max = sys.maxsize

def calculateQ(d):
    r = d.shape[0]
    q = np.zeros((r,r))
    for i in range(r):
        for j in range(r):
            if i == j:
                q[i][j] = 0
            else:
                sumI = 0
                sumJ = 0
                for k in range(r):
                    sumI += d[i][k]
                    sumJ += d[j][k]
                q[i][j] = (r-2) * d[i][j] - sumI - sumJ

    return q

def findLowestPair(q):
    r = q.shape[0]
    minVal = max
    for i in range(0,r):
        for j in range(i,r):
            if (q[i][j] < minVal):
                minVal = q[i][j]
                minIndex = (i,j)
    return minIndex


def doDistOfPairMembersToNewNode(i,j,d):
    r = d.shape[0]
    sumI = 0
    sumJ = 0
    for k in range(r):
        sumI += d[i][k]
        sumJ += d[j][k]

    dfu = (1.0 / (2.0 * (r - 2.0))) * ((r - 2.0) * d[i][j] + sumI - sumJ)
    dgu = (1.0 / (2.0 * (r - 2.0))) * ((r - 2.0) * d[i][j] - sumI + sumJ)

    return (dfu,dgu)

def calculateNewDistanceMatrix(f,g,d):
    print (d)
    r = d.shape[0]
    nd = np.zeros((r-1,r-1))

    # Copy over the old data to this matrix
    ii = jj = 1
    for i in range(0,r):
        if i == f or i == g:
            continue
        for j in range(0,r):
            if j == f or j == g:
                continue
            nd[ii][jj] = d[i][j]
            jj += 1
        ii += 1
        jj = 1
            
    # Calculate the first row and column
    ii = 1
    for i in range (0,r):
        if i == f or i == g:
            continue
        nd[0][ii] = (d[f][i] + d[g][i] - d[f][g]) / 2.
        nd[ii][0] = (d[f][i] + d[g][i] - d[f][g]) / 2.
        ii += 1

    return nd
    
def doNeighbourJoining(d):
    labels = ["A","B","C","D","E","F","G","H"]
    
    while d.shape[0] > 1:
        q = calculateQ(d)
        lowestPair = findLowestPair(q)
        print ("Joining")
        print (lowestPair[0])
        print (lowestPair[1])
        # newlabel = "%s%s" % (labels[lowestPair[0]], labels[lowestPair[1]])
        # print "lowestPair[0]=%i\tlowestPair[1]=%i" % (lowestPair[0], lowestPair[1])
        # print labels
        # print newlabel
        # del labels[lowestPair[0]]
        # del labels[lowestPair[1]]
        # labels.insert(0,newlabel)

        i = lowestPair[0]
        j = lowestPair[1]
        
        pairDist = doDistOfPairMembersToNewNode(i,j,d)
        d = calculateNewDistanceMatrix(i,j,d)
        # print d

        
    
    
def run(distMatrix):
    doNeighbourJoining(distMatrix)
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print ("Usage: neighbour-joining.py")
        sys.exit(1)


try:
    file = open("3.in")
    print("this file exist")
except:
    print("Error reading input file")


distMatrix = np.array([[0, 6, 4, 12, 11], [6, 0, 5, 13, 11], [4, 5, 0, 12, 10], [12, 13, 12, 0, 11], [11, 11, 10, 11, 0]])
   
   
        
run(distMatrix)
#!/usr/bin/python

#
# Use the neighbour joining algorithm to build a tree
#


fileCount = 1; 
clusterCount = 1;

import sys
import numpy as np
import math
import time
import random
import scipy as scipy
import itertools
import sys
import os
max = sys.maxsize

def dist(seq1, seq2):
    # Helper method for finding distances
    
    distance  = 0
    for x, y in zip(seq1, seq2):
        if x != y: 
            distance += 1
    return distance

def distance_matx(sequences):
    # Do the comparisons and create distance matrix
    # Takes a list of sequences
    # Returns an integer distance matrix
    
    # Empty matrix
    distance_matrix = np.zeros((len(sequences), len(sequences)), dtype=int)
    
    # Do the comparisons
    x, y = 0, 0
    for seqA in sequences:
        for seqB in sequences:
            score = dist(seqA, seqB)
            distance_matrix[x][y] = score
            y += 1
        x += 1
        y = 0

    return distance_matrix

def tril_matx(dist_matx):
    # Make it lower triangular by replacing upper tri w/ inf
    # removes duplicates and diagonal 0s
    
    dist_matx = dist_matx.astype(float)
    dist_matx[np.triu_indices(dist_matx.shape[0], 0)] = float("inf")
    
    return dist_matx

def min_cell(matx):
    # Takes a matrix
    # Return a list of tuples, with all indicies containing min value.
    
    mins = []
    # Use np to find a min
    min_dist = matx[np.unravel_index(np.argmin(matx, axis=None), matx.shape)]
    
    # Check if there's any other minima
    for i in range(len(matx)):
        for j in range(len(matx)):
            if matx[i][j] == min_dist:
                mins.append((i,j)) 
    
    return mins



def dist(seq1, seq2):
    # Helper method for finding distances
    
    distance  = 0
    for x, y in zip(seq1, seq2):
        if x != y: 
            distance += 1
    return distance

def distance_matx(sequences):
    # Do the comparisons and create distance matrix
    # Takes a list of sequences
    # Returns an integer distance matrix
    
    # Empty matrix
    distance_matrix = np.zeros((len(sequences), len(sequences)), dtype=int)
    
    # Do the comparisons
    x, y = 0, 0
    for seqA in sequences:
        for seqB in sequences:
            score = dist(seqA, seqB)
            distance_matrix[x][y] = score
            y += 1
        x += 1
        y = 0

    return distance_matrix

def tril_matx(dist_matx):
    # Make it lower triangular by replacing upper tri w/ inf
    # removes duplicates and diagonal 0s
    
    dist_matx = dist_matx.astype(float)
    dist_matx[np.triu_indices(dist_matx.shape[0], 0)] = float("inf")
    
    return dist_matx

def min_cell(matx):
    # Takes a matrix
    # Return a list of tuples, with all indicies containing min value.
    
    mins = []
    # Use np to find a min
    min_dist = matx[np.unravel_index(np.argmin(matx, axis=None), matx.shape)]
    
    # Check if there's any other minima
    for i in range(len(matx)):
        for j in range(len(matx)):
            if matx[i][j] == min_dist:
                mins.append((i,j)) 
    
    return mins

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
        nd[0][ii] = (d[f][i] + d[g][i] - d[f][g]) / 2.0
        nd[ii][0] = (d[f][i] + d[g][i] - d[f][g]) / 2.0
        ii += 1

    return nd
    
def doNeighbourJoining(d):
       print("this is d",d);
       fileCount = 1;
        # Save this matrix, d, into an output file e.g "neighborMatrix.o1" or "neighborMatrix.o2" etc.
        # Use 
        # #write a matrix to the file ##
        #print("Outputfile matrixCount: ");
       print("Outputfile" + str(clusterCount) + ":");
       out1 = "Cluster.o" + str(clusterCount);
        #out1 = "matrixCount.o"
       print(out1);
       print("");
       if not os.path.isfile(out1):
            open(out1,'w').close();
    
       out = open(out1, 'w');
       out.write(str(fileCount-1));

        # write the matrix count to the file ##
       print("Outputfile mergeCount: ");
       out1 = "mergeCount.o";
       print(out1);
       print("");


       if not os.path.isfile(out1):
            open(out1, 'w').close();
    
       out = open(out1,'w');
       out.write(str(clusterCount));
       
        ## 
       while d.shape[0] > 1:
        q = calculateQ(d)
        print("this is q:",q)

        ### this code is finding the first lowest pair ###
        lowestPair = findLowestPair(q)
        print ("Joining")
        print (lowestPair[0])
        print (lowestPair[1])
        i = lowestPair[0]
        j = lowestPair[1]
        
        pairDist = doDistOfPairMembersToNewNode(i,j,d)
        d = calculateNewDistanceMatrix(i,j,d)
        print("this is a matrix",d)
        fileCount = 1;
        # Save this matrix, d, into an output file e.g "neighborMatrix.o1" or "neighborMatrix.o2" etc.
        # Use 
        # #write a matrix to the file ##
        #print("Outputfile matrixCount: ");
        print("Outputfile" + str(clusterCount) + ":");
        out1 = "Cluster.o" + str(clusterCount);
        #out1 = "matrixCount.o"
        print(out1);
        print("");
        if not os.path.isfile(out1):
            open(out1,'w').close();
    
        out = open(out1, 'w');
        out.write(str(fileCount-1));

        # write the matrix count to the file ##
        print("Outputfile mergeCount: ");
        out1 = "mergeCount.o";
        print(out1);
        print("");


        if not os.path.isfile(out1):
            open(out1, 'w').close();
    
        out = open(out1,'w');
        out.write(str(clusterCount));
  # increment matrix count after file is outputed. 
  #  matrixCount = matrixCount + 1;

        
    


 ### trying to read the file from here ###
try:
    file = open("3.in")
    print("this file exist")
except:
    print("Error reading input file")

in_sequences = []
in_seq_labels = []

# Assumes format of header line followed by sequence line
while True:
    seq_name = file.readline().strip(">\n") # Read header, strip stuff
    sequence = file.readline().strip() # Read sequence, strip newline
    if not sequence: break
    # sequences[seq_name] = sequence # Add to dict
    in_sequences.append(sequence)
    in_seq_labels.append(seq_name)

print("Sequences read: ")
print(in_sequences)
print(in_seq_labels)


int_dist_matx = distance_matx(in_sequences)
print("Question 1a:")
print(int_dist_matx)





 ### this is the main method where we start running of the neighbour joining methods ##   
def run(distMatrix):
    doNeighbourJoining(distMatrix)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print ("Usage: neighbour-joining.py")
        sys.exit(1)


    

#distMatrix = np.array([[0, 6, 4, 12, 11], [6, 0, 5, 13, 11], [4, 5, 0, 12, 10], [12, 13, 12, 0, 11], [11, 11, 10, 11, 0]])
   
   
        
#run(distMatrix)



run(int_dist_matx)










### this code is used for creating the tree ###
class Node:
    '''
    Simple binary tree node with name + height
    also left_height and right_height functions to return height - child height
    if you want getters and setters write them your own damn self
    '''
        
    def __init__(self, name, height, left=None, right=None):
        self.name = name
        self.height = height
        self.left = left
        self.right = right

    def left_height(self):
        """
        Returns edge length btwn self and left child
        """
        
        if self.left is not None:
            return self.height - self.left.height
        else:
            return 0
    
    def right_height(self):
        """
        Returns edge length btwn self and right child
        """
        
        if self.right is not None:
            return self.height - self.right.height
        else:
            return 0
    
    def __str__(self):
        """
        Recursively prints tree structure
        """
        
        if self.left is not None:
            # Has children
            return ("({ln}:{lh}{lr})({rn}:{rh}{rr})".format(

                    ln=self.left.name,
                    lh=round(self.left_height(),1),
                    lr=self.left.__str__(),
                    rn=self.right.name,
                    rh=round(self.right_height(),1),
                    rr=self.right.__str__()
                    ))
        else:
            return ""

    

    def traverse(self):
	        """
	        Unused, lol
	        """
	        if self.left is not None:
	            self.left.traverse()
	        if self.right is not None:
	            self.right.traverse()
	        print(self.__str__())
	    
def round_down_1_dp(num):
	    """ 
	    Does some rounding-down chicanery because the numbers weren't quite right
	    """
	    return math.floor(num*10) / 10

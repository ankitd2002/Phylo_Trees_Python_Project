#!/usr/bin/python

#
# Use the neighbour joining algorithm to build a tree
#


fileCount = 1; 
clusterCount = 1;
matrixCount = 0;
iteration = 0;
originalMatrix = [];
temp = [];
mergedAlready = "";

import sys
import numpy as np
import math
import time
import random
import scipy as scipy
import itertools
import sys
import os
import filegen;


from ete3 import Tree
from skbio import DistanceMatrix
from skbio.tree import nj

max = sys.maxsize



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


def printSaveTree():
    pass;


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

    print("Min Val: " + str(minVal));

    return minIndex


def doDistOfPairMembersToNewNode(i,j,d):
    r = d.shape[0]
    sumI = 0
    sumJ = 0


    global fileCount;
    global matrixCount;
    global clusterCount;

    for k in range(r):
        sumI += d[i][k]
        sumJ += d[j][k]

    if((2.0 * (r - 2.0)) != 0):

        dfu = (1.0 / (2.0 * (r - 2.0))) * ((r - 2.0) * d[i][j] + sumI - sumJ)
        dgu = (1.0 / (2.0 * (r - 2.0))) * ((r - 2.0) * d[i][j] - sumI + sumJ)

        print("Matrix #" + str(fileCount) + "\n",d)


        return (dfu,dgu);

    else:



        # Write matrix count to a file
        matrixCount = fileCount-1;
        print("There are: " + str(matrixCount) + " matrices");

        print("Outputfile matrixCount:");
        out1 = "matrixCount.o";
        print(out1);
        print("");

        if not os.path.isfile(out1):
            open(out1, 'w').close();

        out = open(out1, 'w');
        out.write(str(matrixCount));


        # Write matrix merge count to a file
        clusterCount = fileCount-1;
        print("There are: " + str(clusterCount) + " clusters");

        print("Outputfile mergeCount:");
        out1 = "mergeCount.o";
        print(out1);
        print("");

        if not os.path.isfile(out1):
            open(out1, 'w').close();

        out = open(out1, 'w');
        out.write(str(clusterCount));






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


def doNeighbourJoining(d, seq_labels):

    print("this is the distance Matrix: d\n",d);
    
    filegen.makeXML_blank("./trees/tree0.xml")
    filegen.makePNG("./trees/tree0.xml",
                    "./trees/tree0")


    global fileCount;
    global clusterCount;
    global originalMatrix;
    global iteration;
    global originalMatrix;
    global mergedAlready;


    originalMatrix = d;


    leaf_nodes = [] 

    for sequence in seq_labels:
        leaf_nodes.append(Node(sequence, 0))


    # Save this matrix, d, into an output file e.g "neighborMatrix.o1" or "neighborMatrix.o2" etc.
    print("Outputfile" + str(fileCount) + ":");
    out1 = "Matrix.o" + str(fileCount);
    print(out1);
    print("");
    if not os.path.isfile(out1):
        open(out1,'w').close();

    out = open(out1, 'w');
    out.write(str(d.tolist()));

    fileCount = fileCount + 1;

    # Temporary merged sequences/clusters list
    global temp;


    temp2 = [];

    for i in range(len(originalMatrix)):
        temp2.append(i+1);


    ## 
    while d.shape[0] > 1:

        q = calculateQ(d)
        print("this is q:\n",q)
        # Save this matrix, q, into an output file e.g "neighborMatrix.o1" or "neighborMatrix.o2" etc.
        print("Outputfile" + str(fileCount-1) + ":");
        out1 = "qMatrix.o" + str(fileCount-1);
        print(out1);
        print("");
        if not os.path.isfile(out1):
            open(out1,'w').close();

        out = open(out1, 'w');
        out.write(str(q.tolist()));        


        ### this code is finding the first lowest pair ###
        lowestPair = findLowestPair(q)
        print ("Joining:")
        print (lowestPair[0])
        print (lowestPair[1])
        i = lowestPair[0]
        j = lowestPair[1]

        print("Iteration " + str(iteration) + " ---------------------------------------------------");

        # If first iteration, write the index of the original matrix as first merged clusters
        if(iteration == 0):

            # Write merged clusters to file
            clusterRes = str(i+1) + " " + str(j+1);
            print("Outputfile " + str(clusterCount) +":");
            out1 = "Cluster.o" + str(clusterCount);
            print(out1);
            print("");

            if not os.path.isfile(out1):
                open(out1, 'w').close();

            out = open(out1, 'w');
            out.write(str(clusterRes));

            L = clusterRes.split();
            temp.append(L);


            mergedAlready = mergedAlready + clusterRes;


        # Else, we need to find out what clusters are being merged, get it from temp list;
        else:
            
            # If i is 0, use temp list and previous iteration's results
            if(i == 0):

                # Previous Cluster String
                c1 = str(temp[iteration-1][0]) + str(temp[iteration-1][1]);

                # New cluster/sequence to merge with
                c2 = "";
                temp3 = [];

                for val in temp2:

                    if str(val) not in mergedAlready:

                        temp3.append(val);

                c2 = str(temp3[j-1]);


                # Write merged clusters to file
                clusterRes = c1 + " " + c2;
                print("Outputfile " + str(clusterCount) +":");
                out1 = "Cluster.o" + str(clusterCount);
                print(out1);
                print("");

                if not os.path.isfile(out1):
                    open(out1, 'w').close();

                out = open(out1, 'w');
                out.write(str(clusterRes));

                L = clusterRes.split();
                temp.append(L);

                mergedAlready = mergedAlready + clusterRes;



            # Else, use original matrix (hard stuff)
            else:
                pass;



        # Honestly this code is not even used anywhere. Use it to output files.
        pairDist = doDistOfPairMembersToNewNode(i,j,d)
        
        d = calculateNewDistanceMatrix(i,j,d)
        # Save this matrix, d, into an output file e.g "neighborMatrix.o1" or "neighborMatrix.o2" etc.
        print("Outputfile" + str(fileCount) + ":");
        out1 = "Matrix.o" + str(fileCount);
        print(out1);
        print("");
        if not os.path.isfile(out1):
            open(out1,'w').close();

        out = open(out1, 'w');
        out.write(str(d.tolist()));

        # Increment Everything
        fileCount = fileCount + 1;
        clusterCount = clusterCount + 1;
        iteration = iteration + 1;
        


 ### this is the main method where we start running of the neighbour joining methods ##   
def run(distMatrix, seq_labels):
    doNeighbourJoining(distMatrix, seq_labels)



def runNeighbour(filename):

    ### trying to read the file from here ###
    try:
        file = open(filename)
        print("this file exist")

        # Write filename to a file
        print("Outputfile " + str("3.in") +":");
        out1 = "inputFileName.o";
        print(out1);
        print("");

        if not os.path.isfile(out1):
            open(out1, 'w').close();

        out = open(out1, 'w');
        out.write(str("3.in"));

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
    print("Distance Matrix:");
    print(int_dist_matx)




    # Start
    run(int_dist_matx, in_seq_labels);


    # Testing
    # data = int_dist_matx;
    # ids = ["S1", "S2", "S3", "S4", "S5"];

    # dm = DistanceMatrix(data, ids);

    # tree = nj(dm);
    # print(tree.ascii_art());




# runNeighbour("3.in");




# http://scikit-bio.org/docs/0.2.1/generated/skbio.tree.nj.html

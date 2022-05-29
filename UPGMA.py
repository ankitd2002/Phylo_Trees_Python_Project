import numpy as np;
import math;
import os;
import filegen;
import random;
import ast;


iteration = 0;
 

fileCount = 1; 
clusterCount = 1;
sequenceCount = 0;



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


def displayMatrixFileOutput():

    print("");

    # Get the amount of matrices file count
    file = open("matrixCount.o");

    for line in file:
        matrix_Count = int(line);

    maxLength = 0;
    index = 1;


    # Loop through all these matrices files and create a a new row ontop that shows merged/unmerged sequencnes
    for i in range(matrix_Count):

        # Row or Column Sequence Labeled Matrix
        temp1 = [];

        # Non-Sequence Labeled Matrix
        temp2 = [];
        res = [];

        file = open("Matrix.o" + str(i+1));

        for line in file:
            temp2 = ast.literal_eval(line);



        # First Matrix Case
        if(i+1 == 1):

            maxLength = len(temp2);

            # Insert row labels
            for i in range(len(temp2[0])):

                temp1.append("S" + str(i+1));
            
            res.append(temp1);


            for row in temp2:
                res.append(row);


            # Insert column labels
            for i in range(len(res[0]) + 1):
                
                if(i == 0):

                    res[i].insert(0, "  ");

                else:
                    res[i].insert(0, str(res[0][i]));


        # Not first test Matrix
        else:



            # Open Cluster file
            file = open("Cluster.o" + str(i));

            countTemp = i + 1;

            mergeSequences = [];

            for line in file:
                mergeSequences = line.split();


            # Name first (0th) Column the first string in the file
            # print("---------->" + str(mergeSequences));
            temp1.append("S" + str(mergeSequences[0] + str(mergeSequences[1])));


            # Insert row labels
            # The rest are named chronologically from the remaining seuquence numbers that haven't been merged
            for i in range(maxLength):

                # If the string is not in the merged string
                if(str(i+1) not in temp1[0]):
                    temp1.append("S" + str(i+1));

            res.insert(0, temp1);

            for row in temp2:
                res.append(row);

            # Insert column labels
            x = 0;
            for row in res:
                
                if(x == 0):

                    row.insert(0, "  ");

                else:
                    row.insert(0, str(res[0][x]));

                x = x + 1;



        # Write matrix to file
        out1 = "displayMatrix.o" + str(index);

        if not os.path.isfile(out1):
            open(out1, 'w').close();

        out = open(out1, 'w');
        out.write(str(res));

        index = index + 1;




def matrixFileOutput(Matrix):

    global fileCount;

    res = (Matrix.tolist());

    # Write matrix to file
    print("Outputfile " + str(fileCount) +":");
    out1 = "Matrix.o" + str(fileCount);
    print(out1);
    print("");

    if not os.path.isfile(out1):
        open(out1, 'w').close();

    out = open(out1, 'w');
    out.write(str(res));

    fileCount = fileCount + 1;

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
    distance_matrix = np.zeros((len(sequences), len(sequences)), dtype=int);
    
    # Do the comparisons
    x, y = 0, 0
    for seqA in sequences:
        for seqB in sequences:
            score = dist(seqA, seqB)
            distance_matrix[x][y] = score
            y += 1
        x += 1
        y = 0

    matrixFileOutput(distance_matrix);

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

def round_down_1_dp(num):
    """ 
    Does some rounding-down chicanery because the numbers weren't quite right
    """
    return math.floor(num*10) / 10

def UPGMA(matx, seq_labels, debug=False):
    """
    Does UPGMA.
    Takes a distance matrix, a list of sequence labels, and a debug param which defaults to false.
    Makes a bunch of files, idk yet there's a lot going on
    Returns a node, which is the root of the tree produced via UPGMA.
    """

    global clusterCount;

    # INITIALIZE
    
    # Create leaf nodes for sequences
    leaf_nodes = [] 
    for sequence in seq_labels:
        leaf_nodes.append(Node(sequence, 0))
    
    # Integers are no good here
    matx = matx.astype(float)
    
    # TODO: the first tree, which should just be blank
    """
    if debug == True:
        print(seq_labels)
        print(matx)
        print("\n")
    """

    filegen.makeXML_blank("./trees/tree0.xml")
    filegen.makePNG("./trees/tree0.xml",
                    "./trees/tree0")

    # ITERATE
    while len(seq_labels) > 2:

        # Find pair with minimum distance. (Just take the first one, who cares)
        min_pair = min_cell(tril_matx(matx))[0]
        seq_i_idx, seq_j_idx = min_pair
        if seq_i_idx > seq_j_idx: # Put them in ascending order
            seq_i_idx, seq_j_idx = seq_j_idx, seq_i_idx
            
        # Get dij
        dij = matx[seq_i_idx][seq_j_idx]
        if debug == True:
            print("dij = " + str(dij))
        
        # Delete the i,j rows + cols        
        matx_reduced = np.delete(matx, (seq_i_idx, seq_j_idx), 0)
        matx_reduced = np.delete(matx_reduced, (seq_i_idx, seq_j_idx), 1)
        
        # Prepend an empty row and col for new cluster
        new_row = np.zeros(len(matx_reduced), dtype=float)
        matx_reduced = np.vstack((new_row, matx_reduced))
        new_col = np.zeros((len(matx_reduced), 1), dtype=float)
        matx_reduced = np.hstack((new_col, matx_reduced))
        
        # Get the values needed to make averages
        # This code is awful I'm so sorry
        some_list = matx[seq_i_idx]
        some_list = np.delete(some_list, (seq_i_idx, seq_j_idx))
        some_lisp = matx[seq_j_idx]
        some_lisp = np.delete(some_lisp, (seq_i_idx, seq_j_idx))
        
        # Calculate averages and put em in the new matrix
        for i in range(0, len(some_list)):
            avg = (some_list[i] + some_lisp[i]) / 2
            matx_reduced[0][i+1] = avg
            matx_reduced[i+1][0] = avg
            if debug == True:
                print(str(some_list[i]) + " + " + str(some_lisp[i]) + " / 2 = " + str(avg))
        
        # Reassign matrix for next iter
        matx = matx_reduced
        
        # Define label for new cluster k
        k_label = "S" + seq_labels[seq_i_idx].strip("S") + seq_labels[seq_j_idx].strip("S")


        # Write merged clusters to file
        clusterRes = str(seq_labels[seq_i_idx].strip("S")) + " " + str(seq_labels[seq_j_idx].strip("S"));
        print("Outputfile " + str(clusterCount) +":");
        out1 = "Cluster.o" + str(clusterCount);
        print(out1);
        print("");

        if not os.path.isfile(out1):
            open(out1, 'w').close();

        out = open(out1, 'w');
        out.write(str(clusterRes));


        # Remove merged sequence labels from list and add the merged one
        del seq_labels[seq_j_idx]; del seq_labels[seq_i_idx]
        seq_labels.insert(0, k_label)

        # Create node, assign height and children
        new_node = Node(k_label, round(round_down_1_dp(dij / 2),1), leaf_nodes[seq_i_idx], leaf_nodes[seq_j_idx])
        del leaf_nodes[seq_j_idx]; del leaf_nodes[seq_i_idx]
        leaf_nodes.insert(0, new_node)

        filegen.makeXML(new_node, "./trees/tree{}.xml".format(str(clusterCount)))
        filegen.makePNG("./trees/tree{}.xml".format(str(clusterCount)),
                        "./trees/tree{}".format(str(clusterCount)))

        # Increment
        clusterCount += 1


        # New Matrix Created
        matrixFileOutput(matx);
        

    # TERMINATE
    
    # Only 2 clusters remain
    # Define label for root cluster k
    # Get distance, create final node

    k_label = "S" + seq_labels[0].strip("S") + seq_labels[1].strip("S")


    # Write merged clusters to file
    clusterRes = str(seq_labels[0].strip("S")) + " " + str(seq_labels[1].strip("S"));
    print("Outputfile " + str(clusterCount) +":");
    out1 = "Cluster.o" + str(clusterCount);
    print(out1);
    print("");

    if not os.path.isfile(out1):
        open(out1, 'w').close();

    out = open(out1, 'w');
    out.write(str(clusterRes));



    dij = matx[0][1]
    root = Node(k_label, (dij / 2), leaf_nodes[0], leaf_nodes[1])

    filegen.makeXML(root, "./trees/tree{}.xml".format(str(clusterCount)))
    filegen.makePNG("./trees/tree{}.xml".format(str(clusterCount)),
                    "./trees/tree{}".format(str(clusterCount)))


    return root
    

def runUPGMA(fileName):

    try:
        file = open(fileName)

        # Write filename to a file
        print("Outputfile " + str(fileName) +":");
        out1 = "inputFileName.o";
        print(out1);
        print("");

        if not os.path.isfile(out1):
            open(out1, 'w').close();

        out = open(out1, 'w');
        out.write(str(fileName));



    except:
        print("Error reading input file")

    in_sequences = []
    in_seq_labels = []

    # Read input file for sequences and their names
    # Assumes format of header line followed by sequence line (FASTA-style)
    while True:
        seq_name = file.readline().strip(">\n") # Read header, strip stuff
        sequence = file.readline().strip() # Read sequence, strip newline
        if not sequence: break

        in_sequences.append(sequence)
        in_seq_labels.append(seq_name)

    print("Sequences read: ")
    print(in_sequences)
    print(in_seq_labels)

    # Question A:
    int_dist_matx = distance_matx(in_sequences)
    print("Question 1a:")
    print(int_dist_matx)

    # Copies so if you run it again it's not brank
    matx_copy = int_dist_matx.copy()
    labels_copy = in_seq_labels.copy()

    # Change debug to True for step-by-step
    root = UPGMA(matx_copy, labels_copy, debug=True)

    print("\nQuestion B: ")
    print(root.name + root.__str__())


    # Write matrix count to a file
    print("Outputfile matrixCount:");
    out1 = "matrixCount.o";
    print(out1);
    print("");

    global fileCount;

    if not os.path.isfile(out1):
        open(out1, 'w').close();

    out = open(out1, 'w');
    out.write(str(fileCount-1));



    # Write matrix merge count to a file
    print("Outputfile mergeCount:");
    out1 = "mergeCount.o";
    print(out1);
    print("");

    if not os.path.isfile(out1):
        open(out1, 'w').close();

    out = open(out1, 'w');
    out.write(str(clusterCount));




    # Write displayed matrices
    displayMatrixFileOutput();





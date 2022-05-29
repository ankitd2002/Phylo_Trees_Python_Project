
import numpy as np
import math
import random


fileCount = 1; 




try:
    file = open("3.in")
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

# Question A:
int_dist_matx = distance_matx(in_sequences)
print("Question 1a:")
print(int_dist_matx)


# Write out first matrix
 


class Node:
    
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

def UPGMA(matx, seq_labels, debug=False):
    """
    Does UPGMA.
    Takes a distance matrix, a list of sequence labels, and a debug param which defaults to false.
    Returns a node, which is the root of the tree produced via UPGMA.
    """

    # INITIALIZE
    
    # Create leaf nodes for sequences
    leaf_nodes = [] 
    for sequence in seq_labels:
        leaf_nodes.append(Node(sequence, 0))
    
    # Integers are no good here
    matx = matx.astype(float)
    
    if debug == True:
        print(seq_labels)
        print(matx)
        print("\n")
    
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
        del seq_labels[seq_j_idx]; del seq_labels[seq_i_idx]
        seq_labels.insert(0, k_label)

        # Create node, assign height and children
        new_node = Node(k_label, round(round_down_1_dp(dij / 2),1), leaf_nodes[seq_i_idx], leaf_nodes[seq_j_idx])
        del leaf_nodes[seq_j_idx]; del leaf_nodes[seq_i_idx]
        leaf_nodes.insert(0, new_node)
        
        if debug == True:
            print(matx)
            print(new_node)
            print("\n")
            
    # TERMINATE
    
    # Only 2 clusters remain
    # Define label for root cluster k
    # Get distance, create final node
    k_label = "S" + seq_labels[0].strip("S") + seq_labels[1].strip("S")
    dij = matx[0][1]
    root = Node(k_label, (dij / 2), leaf_nodes[0], leaf_nodes[1])
    
    return root

# Copies so if you run it again it's not brank
matx_copy = int_dist_matx.copy()
labels_copy = in_seq_labels.copy()

# Change debug to True for step-by-step
root = UPGMA(matx_copy, labels_copy, debug=False)

print("\nQuestion B: ")
print(root.name + root.__str__())
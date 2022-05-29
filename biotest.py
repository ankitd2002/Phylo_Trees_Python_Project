import matplotlib
import matplotlib.pyplot as plt
from Bio import Phylo
import numpy as np
import os, os.path

tree = Phylo.read("test.xml", "phyloxml")

Phylo.draw(tree, do_show = False)
plt.savefig("test")

"""
tree = Phylo.read("tree0.xml", "phyloxml")

Phylo.draw(tree, do_show=False)
plt.savefig("yeet0")


tree = Phylo.read("tree1.xml", "phyloxml")
tree.ladderize()  # Flip branches so deeper clades are displayed at top

Phylo.draw(tree, do_show=False)
plt.savefig("yeet1")

tree = Phylo.read("tree2.xml", "phyloxml")

Phylo.draw(tree, do_show=False)
plt.savefig("yeet2")

tree = Phylo.read("tree3.xml", "phyloxml")

Phylo.draw(tree, do_show=False)
plt.savefig("yeet3")

tree = Phylo.read("tree4.xml", "phyloxml")

Phylo.draw(tree, do_show=False)
plt.savefig("yeet4")
"""

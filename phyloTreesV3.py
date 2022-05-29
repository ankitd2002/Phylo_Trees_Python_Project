# Phylogenetic Algorithm Visualization Thing

# Mattias Park

# TODO: (broad strokes here)
# Window + GUI
# Controls for working stepwise through algorithm
# Implementations of algorithms

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import numpy as np
import os
import sys
import time

import UPGMA;
import NeighbourJoining;


class MainMenu():

    # Currently implemented algorithms, for drop-down select
    ALGORITHMS = [
    "UPGMA",
    "NeighborJoining"
    ]

    def __init__(self):

        self.root = Tk()
        self.root.title("PhyloTrees")

        self.width = 1280
        self.height = 720

        self.algorithm = StringVar(self.root)
        self.algorithm.set(MainMenu.ALGORITHMS[0]) # Default to first option on ALGORITHMS list

        self.fasta_file = StringVar(self.root)

        # Frame for a cool graphic
        cool_graphic_frame = Frame(self.root)
        cool_graphic_img = PhotoImage(file="coolGif.gif")
        cool_graphic_label = Label(cool_graphic_frame, image=cool_graphic_img)  

        cool_graphic_frame.pack( side = TOP )
        cool_graphic_label.pack()

        # Frame for some expository text
        expository_text_frame = Frame(self.root)
        expository_text = """              Welcome to PhyloTrees!
                          Please select an algorithm and input file to continue.
                            Created by Mattias Park, Nabil Nazri, Ankit Dahiya"""
        expository_text_label = Label(expository_text_frame, text=expository_text)       
        expository_text_frame.pack( side = LEFT )
        expository_text_label.pack()                   


        # Frame for controls
        controls_frame = Frame(self.root)
        controls_frame.pack( side = RIGHT )

        # Algorithm selection
        algorithm_prompt_label = Label(controls_frame, text="Choose Algorithm:")
        algorithm_prompt_label.pack()

        algorithm_dropdown = OptionMenu(controls_frame, self.algorithm, "UPGMA", "NeighbourJoining")
        algorithm_dropdown.pack()

        # Input file selection
        file_prompt_label = Label(controls_frame, text="Choose FASTA file:")
        file_prompt_label.pack()

        file_choose_button = Button(controls_frame, text="Open", command=self.choose_fasta)
        file_choose_button.pack( side = LEFT )

        # Run
        run_button = Button(controls_frame, text="Go!", command=self.launch)
        run_button.pack( side = RIGHT )

        self.root.mainloop()
        sys.exit()

    def choose_fasta(self):
        # Open a file chooser dialog

        try:
            self.fasta_file.set(filedialog.askopenfilename(initialdir=os.getcwd()))
        except:
            print("oopsies")

    def launch(self):

        if self.fasta_file.get() == "":

            messagebox.showinfo(title="PhyloTrees", message="Please select an input FASTA file.")
            return

        if self.algorithm.get() == "UPGMA":

            UPGMA.runUPGMA(self.fasta_file.get());
            self.root.destroy();
            import UPGMAStep;

        if self.algorithm.get() == "NeighbourJoining":

            NeighbourJoining.runNeighbour(self.fasta_file.get());
            self.root.destroy();
            import NeighbourStep;





MainMenu();
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

import UPGMA


class MainMenu():

    # Currently implemented algorithms, for drop-down select
    ALGORITHMS = [
    "UPGMA",
    "Neighbor-Joining"
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

        algorithm_dropdown = OptionMenu(controls_frame, self.algorithm, "UPGMA", "Neighbor-Joining")
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

            UPGMA.runUPGMA(self.fasta_file.get())
            # time.sleep(2);
            self.root.destroy();
            import UPGMAStep;

        if self.algorithm.get() == "Neighbor-Joining":

            print("Neighbor Joining Not Fully Implemented Yet!");




class UPGMAGUI():


    def __init__(self):

        self.root = Tk() # Must be done first to load images
        self.root.title("UPGMA") # Set a title        

        # Read in the trees (XML? PNG?) and the matrices
        self.trees, self.trees_something = self.read_trees()
        # self.matrices = []
        self.current_step = 0

        # Build the GUI

        self.width = 1280
        self.height = 720

        # Frame for displaying tree + matrix
        frame1 = Frame(self.root)
        frame1.pack(side=TOP)

        # The thing to display the tree image
        self.tree_pic = Label(frame1, image=self.trees[self.current_step])
        self.tree_pic.pack()

        # Frame for controls
        frame2 = Frame(self.root) # Create and add a frame to root
        frame2.pack(side=BOTTOM)

        # The buttons
        btn_prev = Button(frame2, text = "PREV", command = self.prev_step)
        btn_next = Button(frame2, text = "NEXT", command = self.next_step)
        btn_prev.pack()
        btn_next.pack()

        # TODO:
        # - Read the trees and matrices into lists
        # - Setup the GUI
        # - For each step:
        #       - Show tree, matrix
        #       - Show matrix w/ highlights
        #       - Show reduced matrix
        # -

        self.root.mainloop() # Create an event loop 
        self.root.destroy() # Clean up

    def read_trees(self):
        '''
        Read the tree PNGs into a list of Tk image objects and return. 
        Relative path of images defined below- maybe do it somewhere else?
        '''

        tree_pics_img_ref = [] # so they don't get garbage collected
        tree_pics = []
        trees_dir = r'.\trees'

        for filename in os.listdir(trees_dir):
            
            if filename.endswith(".png"):

                img_path = (os.path.join(os.getcwd(), trees_dir, filename))
                try:
                    img = ImageTk.PhotoImage(Image.open(img_path), master=self.root)
                except:
                    print("Error reading {}".format(img_path))
                else:
                    tree_pics.append(img)
                    print("Read {}".format(img_path))

        return tree_pics, tree_pics_img_ref

    def read_matrices(self):
        pass

    def next_step(self):

        if self.current_step < len(self.trees)-1:
            self.current_step += 1
            self.tree_pic.configure(image=self.trees[self.current_step])

    def prev_step(self):

        if self.current_step > 0:
            self.current_step -= 1
            self.tree_pic.configure(image=self.trees[self.current_step])


MainMenu()
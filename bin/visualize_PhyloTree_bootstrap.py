#!/bin/python
# -*- coding: utf-8 -*-
"""

Title: visualize_PhyloTree_base.py
Date: 2024.02.11
Author: Vi Varga

Description:
	This program visualizes an input Newick tree, and outputs the results to 
		an SVG file.

List of functions:
	get_label(leaf): 
		Function to return tip labels as complete names
		Source: https://stackoverflow.com/a/33291465/18382033

List of standard and non-standard modules used:
	sys
	os
	pandas
	Bio.Phylo
	seaborn as sns
	matplotlib.pyplot

Procedure:
	1. Loading required modules & assigning command line arguments.
    2. Loading Newick tree with Biopython. 
	3. Extracting species information in order to color the tree tip labels.
	4. Creating the annotation dataframe with Pandas.
	5. Visualizing the phylogenetic tree.
	6. Writing out results to an SVG file. 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not entirely user-defined, but is instead based 
		on the input filename plus a user-provided extension.
	- Note that the input gene names need to be in the NCBI BLAST format. The 
		editing of species names also assumes the input tree was generated by 
		IQ-TREE.

Usage
	./visualize_PhyloTree_base.py input_tree
	OR
	python visualize_PhyloTree_base.py input_tree

This script was written for Python 3.9.18, in Spyder 5.4.5. 

"""


# Part 1: Import modules & assign command line arguments

# import necessary modules
import sys # allows execution of script from command line
import os # allows access to the operating system
import pandas as pd # allows manipulation of dataframes in Python
from Bio import Phylo # use Biopython to work with phylogenetic trees
import seaborn as sns # use Seaborn for image visualization
import matplotlib.pyplot as plt # use matplotlib to print out plot


# load input file
input_tree = sys.argv[1]
#input_tree = "XP_001322682.1__MSA_IQ.treefile"

# load output file
# set up a file name addition
usr_file_ext = "Vis_boot"
# extract the file basename
base = os.path.basename(input_tree)
outfile_base = os.path.splitext(base)[0]
output_img = outfile_base + '__' + usr_file_ext + '.png'
output_svg = outfile_base + '__' + usr_file_ext + '.svg'


# Part 2: Load Newick tree with Bio.Phylo

# use Biopython to load the Newick tree
spp_tree = Phylo.read(input_tree, "newick")


# Part 3: Extract species information in order to color the tree tip labels

# initialize empty list for tip labels
gene_list = []

# this looping is courtesy of Sandra Viknander!!!
for terminal_node in spp_tree.get_terminals():
	# get a list of objects with information on the tip labels
	# extract the name of the protein
	tip_label = terminal_node.name.rstrip("_")
	# append the tip label to the gene_list
	gene_list.append(tip_label)


# create a an empty list for species IDs
species_list = []

# extract the species IDs from the list
for i in gene_list:
	# loop over the elements of the list one by one
	# save the gene ID to a variable
	gene_id = i
	# split the gene ID into the gene & species
	gene_id_list = gene_id.split("__")
	# get the last element of the list (i.e., the species ID)
	species_id = gene_id_list[-1]
	# add species ID to the species list
	species_list.append(species_id)


# Part 4: Create the annotation dataframe with Pandas

# connect gene names with species IDs by writing the lists to a dataframe
species_df = pd.DataFrame({"Gene_IDs": gene_list, "Species_IDs": species_list})


# count the number of unique species/stains
spp_num = len(pd.unique(species_df.Species_IDs))

# generate list of hex codes matching number of unique species/strains
color_list = sns.color_palette("viridis", spp_num).as_hex()
# ref: https://datascientyst.com/get-list-of-n-different-colors-names-python-pandas/
# ref: https://stackoverflow.com/questions/38249454/extract-rgb-or-6-digit-code-from-seaborn-palette
# ref: https://r02b.github.io/seaborn_palettes/

# write the list of unique species IDs to a list
uniq_spp = pd.unique(species_df.Species_IDs)
# create a dataframe of species/strains to colors
color_df = pd.DataFrame({"Spp_Unique": uniq_spp, "Color_Assoc": color_list})

# now fill in the color information using Pandas merge
merged_df = species_df.merge(color_df, left_on="Species_IDs", right_on="Spp_Unique")
# drop the 
merged_df.drop(['Spp_Unique'], axis=1, inplace=True)

# create dictionary with the gene names associated with hex codes
tip_color_dict = dict(zip(merged_df['Gene_IDs'], merged_df['Color_Assoc']))
# ref: https://saturncloud.io/blog/how-to-create-a-dictionary-of-two-pandas-dataframe-columns


# Part 5: Visualize the phylogenetic tree

# making sure full leaf name is shown
# ref: https://stackoverflow.com/a/33291465/18382033
def get_label(leaf):
	# define a function
	# where the tip labels will be returned as complete names
	return leaf.name


# use matplotlib to print the plot to a file
fig = plt.figure(figsize=(70, 40), dpi=100)
# ref: https://stackoverflow.com/questions/29419973/in-python-how-can-i-change-the-font-size-of-leaf-nodes-when-generating-phylogen

# set axes
tree_axes = fig.add_subplot(1, 1, 1)
# plot the tree
tree_plot = Phylo.draw(spp_tree, label_func=get_label, do_show=False, show_confidence=True, axes=tree_axes, label_colors=tip_color_dict)
# ref: https://stackoverflow.com/questions/33147651/biopython-phylogenetic-tree-edit-labels-in-svg-file
# ref: https://stackoverflow.com/questions/74069786/labels-colors-in-bio-phylo

# print the tree
tree_plot


# Part 6: Write out results to an SVG file

plt.savefig(output_img, dpi='figure', format='png')
# ref: https://stackoverflow.com/questions/24525111/how-can-i-get-the-output-of-a-matplotlib-plot-as-an-svg
plt.savefig(output_svg, dpi='figure', format='svg')

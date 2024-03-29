# -*- coding: utf-8 -*-
#!/bin/python

"""

Title: clean_MSA_seqs.py
Date: 2024.02.12
Author: Vi Varga

Description:
	This program cleans an input FASTA file by replacing spaces in sequence names
		with underscores, and removing non-standard amino acids from the 
		sequence lines. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Determining input & output files. 
	3. Parsing FASTA file and writing out results

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
    - The output file name is based on the input file name. 

Usage
	./clean_MSA_seqs.py input_fasta
	OR
	python clean_MSA_seqs.py input_fasta

Version: 
	This is version 2.0 of this script. An earlier version was used for the 2023
		version of BBT045.
	This script is based on the remove_nonStandardAA.py script, which can be found
		in this GitHub repository: 
		https://github.com/V-Varga/TrichoCompare/tree/main/AncestralStates

This script was written for Python 3.9.18, in Spyder 5.4.5.

"""


# Part 1: Importing necessary modules & assign command-line arguments

# import necessary modules
import sys # allows execution of script from command line


# Part 2: Loading input & output files

# load input and output files
input_fasta = sys.argv[1]
#vinput_fasta = "XP_001322682.1__MSAprep.fasta"
output_fasta = ".".join(input_fasta.split('.')[:-1]) + '_CLEAN.fasta'


# Part 3: Parsing FASTA file & writing out results

# write the program
with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
	# open the input and output files
	for line in infile:
		# iterate through the input file line by line
		if line.startswith(">"):
			# identify the FASTA header lines
			header = line.strip()
			# save the header to a variable without the endline character
			header = header.replace(" ", "_")
			# replace spaces in the header lines with underscores
			header = header.replace(",", "")
			# remove commas in headers - commas can cause problems with TrimAl
			header = header.replace(":", "")
			# remove colons in headers - they cause issues with IQ-TREE
			header = header.replace("=_", "")
			# remove any equal signs in the header as these cause issues with IQ-TREE
			# also need to remove brackets to avoid issues with IQ-TREE
			# but only some of the brackets - species names are also in brackets
			bracket_count = header.count("[")
			# count the number of brackets
			if bracket_count > 1:
				# if there is >1 bracket
				# then need to replace the last set with _
				header = "_".join(header.rsplit("[", 1))
				header = "".join(header.rsplit("]", 1))
				# ref: https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string
				# and simply remove the others
				header = header.replace("[", "").replace("]", "")
			else: 
				# if there is only 1 bracket set
				# simply replace with underscores
				header = header.replace("[", "_").replace("]", "")
			# and write the result to the outfile
			outfile.write(header + "\n")
		else:
			# identify the sequence lines
			sequence = line.strip()
			# remove the "\n" endline character from the end of the sequence lines
			sequence = sequence.upper()
			# make sure all characters are uppercase
			# this should already be the case, but just in case an X is lowercase
			standard_seq = sequence.replace("U", "C")
			# replace the selenocysteines (U) with cysteines (C)
			standard_seq = standard_seq.replace("*", "")
			# remove non-standard * characters
			standard_seq = standard_seq.replace("X", "")
			# remove non-standard X characters
			# now print the standardized amino acid sequence to the outfile
			outfile.write(standard_seq + "\n")

#!/usr/bin/env bash

#SBATCH -A C3SE2023-2-17 -p vera
#SBATCH -n 3
#SBATCH -t 03:00:00
#SBATCH -J iqtree
#SBATCH --mail-user=<WRITE YOUR CHALMERS EMAIL HERE>
#SBATCH --mail-type=ALL
# Set the names for the error and output files
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out


###
#
# Title: sbatch_iqtree.sh
# Date: 2024.02.20
# Author: Vi Varga
#
# Description: 
# This script will run IQ-TREE on C3SE Vera from the phylo-tutorial-env.sif
# Apptainer container file, in order to phylogenetic trees.
# 
# Usage: 
# sbatch sbatch_iqtree.sh
#
###


### Set parameters
# key directory
# CORRECT THIS FILE PATH AS YOU NEED
# MAKE SURE THAT YOUR CLEANED MSA IS IN THIS DIRECTORY
WORKDIR=/cephyr/users/<CID>/Vera/<WORKING DIRECTORY>;

# files used
# location of the container
CONTAINER_LOC=/cephyr/NOBACKUP/groups/bbt045_2024/Phylogeny/phylo-tutorial-env.sif;
# input MSA file
# MAKE SURE YOU WRITE YOUR FILE NAME HERE
MSA_FILE=$WORKDIR/<WRITE YOUR CLEANED MSA FILE NAME HERE>;

# temp files directory variable
WORKING_TMP=$TMPDIR/IQ-TREE_TMP;


### Load modules
module purge
#module load MODULE_NAME/module.version ...;


# Copy relevant files to $TMPDIR
# create a temporary directory to store output files
mkdir $WORKING_TMP;
cd $WORKING_TMP;
# copy the MSA to the temporary directory
cp $MSA_FILE $WORKING_TMP


### Running IQ-TREE
apptainer exec $CONTAINER_LOC iqtree -s $MSA_FILE --prefix <WRITE YOUR FILE BASE NAME HERE> \
-m MFP -seed 12345 -wbtl -T AUTO -ntmax 3;


### Copy relevant files back, SLURM_SUBMIT_DIR is set by SLURM
cp $WORKING_TMP/* $WORKDIR;


# Refs: 
# C3SE container use: https://www.c3se.chalmers.se/documentation/applications/containers/
# IQ-TREE Manual: http://www.iqtree.org/doc/iqtree-doc.pdf
# -s is the option to specify the name of the alignment file that is always required by IQ-TREE to work.
# -m is the option to specify the model name to use during the analysis. 
# The special MFP key word stands for ModelFinder Plus, which tells IQ-TREE to perform ModelFinder 
# and the remaining analysis using the selected model.
# Here, the model to use has been pre-selected: LG+R5
# To make this reproducible, need to use -seed option to provide a random number generator seed.
# -wbtl Like -wbt but bootstrap trees written with branch lengths. DEFAULT: OFF
# -T AUTO: allows IQ-TREE to auto-select the ideal number of threads
# -ntmax: set the maximum number of threads that IQ-TREE c use

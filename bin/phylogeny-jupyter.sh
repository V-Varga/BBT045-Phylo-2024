###
# 
# Title: phylogeny-jupyter.sh
# Date: 2025.02.24
# Author: Vi Varga
#
# Description: 
# This script creates the environment to run JupyterLab on C3SE Vera 
# using the Open OnDemand portal for the Phylogeny tutorial and exercise.
# 
# Usage: 
# You should place this script in your ~/portal/jupyter/ directory.
# If the directory doesn't exist, create it with: 
#   mkdir -p ~/portal/jupyter/
# 
# Acknowledgements: 
# The content of this script is based on the TensorFlow-2.6.0-PyTorch-1.12.1.sh script
# provided by C3SE, which can be found in the /apps/portal/jupyter/ directory.
# 
###

# Ensure we don't have any conflicting modules loaded
ml purge; 

# provide the path to the container
container=/cephyr/NOBACKUP/groups/bbt045_2025/Containers/phylo-tutorial-env-2025.sif;

# You can launch jupyter notebook or lab, but you must specify the config file as below: 
apptainer exec $container jupyter lab --config="${CONFIG_FILE}"; 

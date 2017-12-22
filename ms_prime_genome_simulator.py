import msprime
from pprint import pprint
import numpy
#from pedigree import Individual, Pedigree
from random import choice
import csv
import pandas as pd
import os
import logging
import sys
import pydigree
from  pydigree.simulation.chromosomepool import ChromosomePool
from pydigree.sgs import SGSAnalysis

# Setup logging
logging.basicConfig(level=logging.DEBUG, filename='output.log')

# Run MSPrime simulation of population growth and evolution.
# The parameters here are good defaults for humans.
# To change the number of genotypes output, just change the sample size.
# `tree_sequence` is an object of type msprime.trees.TreeSequence.
tree_sequence = msprime.simulate(sample_size=100, Ne=10000, length=186e6,
    recombination_rate=2e-8, mutation_rate=2e-8)
print("Simulated {} mutations".format(tree_sequence.get_num_mutations()))

# Transform MSPrime population sample from list of individual values for each
# SNP site to list of SNPS for each individual.
snp_sample = []
snp_locations = []
for variant in tree_sequence.variants(): # variants are essentially SNPs
    snp_sample.append(variant.genotypes.tolist())
    snp_locations.append(variant.position)
genomeSample = [list(individual) for individual in zip(*snp_sample)]

# Read in 51 person Amish subpedigree to Pydigree pedigree object.
filename = "amish_pedigree/amish_pedigree_with_ancestors.csv"
ped = pydigree.io.read_ped(filename) # PedigreeCollection object
ped1 = ped['amish'] # Pedigree object

# Create Pydigree Chromosome Template to store simulated MSPrime data and
# associate with the pedigree object.
# TODO: How does MSPrime store chromosome number?
chrom1 = pydigree.ChromosomeTemplate() # Create template
for snp_location in snp_locations: # Fill in with simulated data
    chrom1.add_genotype(map_position=snp_location)
ped1.add_chromosome(chrom1) # Add to the population
#print(ped1.chromosomes.chroms[0].genetic_map) # Comfirm that it worked

pool = ChromosomePool(chromosomes=ped1.chromosomes)
pool.pool = [genomeSample]
ped1.pool = pool
# To look at the first chromosome in the pool: pool.chromosome(0)
# To access values of pedigree pool: ped1.pool.pool
ped1.get_founder_genotypes() # Populate founders genotypes from pool
ped1.get_genotypes() # Populate rest of the trees genotypes from inheritance
#for i in ped1.individuals:
#    print(i.genotypes)# Populate founder genotypes from chromosome pool.

#print(pydigree.ibs())

#foo = SGSAnalysis()
#foo.direct_to_disk("MaybeOutput.txt", ped1)


#TODO:
# Read James Hicks's thesis:
# - 15-34
# - 72-86
# - 100-105
# 114-117

# SGS Analysis (Using Pydigree or Re-implement)
# -- Why do you need these "affected individuals" to do ibd analysis? https://github.com/jameshicks/pydigree/blob/master/scripts/genedrop.py
# -- SGSAnalysis Class, chromwide_ibd method
# Write script to manipulate full amish pedigree into Pydigree format with ancestors
# Try out GERMLINE
# Try out http://genepi.med.utah.edu/~alun/software/docs/SGS.html
# Read about IBD-Groupon and HapFABIA
# Try to understand the significance of: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2914765/
# This might be a useful ovrview: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2831613/
# Published European LD blocks => will SGS come up with the same blocks?
# Interested in getting the number of haplotypes per region:
# - because low number of haplotypes is uncommon.
# - How big is the difference in genome-wide homozygosity between well and unwell individuals?

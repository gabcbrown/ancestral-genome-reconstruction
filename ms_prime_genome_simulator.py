import msprime
from pprint import pprint
import numpy
from random import choice
import csv
import pandas as pd
import os
import logging
import sys
import pydigree
from  pydigree.simulation.chromosomepool import ChromosomePool
from pydigree.sgs import SGSAnalysis
from pydigree.ibs import get_ibs_states
from pydigree.io.plink import write_plink
from pydigree.genotypes import alleles
from helper import visualize
# Setup logging
logging.basicConfig(level=logging.DEBUG, filename='output.log')


# Run MSPrime simulation of population growth and evolution.
# The parameters here are good defaults for humans.
# To change the number of genotypes output, just change the sample size.
# `tree_sequence` is an object of type msprime.trees.TreeSequence.
# Chromosome 4 is length=186e6
tree_sequence = msprime.simulate(sample_size=100, Ne=10000, length=1000,
    recombination_rate=2e-8, mutation_rate=2e-8)
print("Simulated {} mutations".format(tree_sequence.get_num_mutations()))


# Transform MSPrime population sample from list of individual values for each
# SNP site to list of SNPS for each individual.
snp_sample = []
snp_locations = []
for variant in tree_sequence.variants(): # variants are essentially SNPs
    snp_sample.append(variant.genotypes.tolist())
    snp_locations.append(variant.position)
# One instance of the Alleles object corresponds to the haploid alleles of
# one individual. (i.e. the alleles of one of their chromosome copies.)
genomeSample = [alleles.Alleles(individual) for individual in zip(*snp_sample)]


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


#visualize(ped1)
write_plink(ped, "latest", mapfile=True)

#TODO: Line 58 fails if no mutations were generated

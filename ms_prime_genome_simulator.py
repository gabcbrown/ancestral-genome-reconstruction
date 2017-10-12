import msprime
from pprint import pprint
import numpy
from pedigree import Individual
from random import choice
import pandas as pd
import os

# Simulate to n=100 individuals

# Example usage:
# Simulate the coalescent for a sample size of 5 and effective population of
# 1000.
# tree_sequence = msprime.simulate(sample_size=5, Ne=1000, length=1,
#                                  recombination_rate=2e-8, mutation_rate=2e-8)
# tree = next(tree_sequence.trees())
# The function simulate() takes two parameters: base length of the simulated
# sequence and the recombination rate.

# Can configure the population, with initial size, growth rate, sample size

# Can simulate demographic events

# Parallelization is possible with some effort

# This is an object of type msprime.trees.SparseTree
#tree = next(tree_sequence.trees())
#tree.draw('foo.svg')

# Population sizes are assumed to be diploid
# This is an object of type TreeSequence, some useful methods/attributes
# breakpoints() - returns the breakpoints
# get_num_mutations()
# get_num_nodes()
# get_sample

# These are good defaults for humans. Just change the sample size.
# This is an object of type msprime.trees.TreeSequence
tree_sequence = msprime.simulate(sample_size=100, Ne=10000, length=5e3,
    recombination_rate=2e-8, mutation_rate=2e-8)


# Transform msprime population sample from list of individual values for each
# SNP site to list of SNPS for each individual.
SNPSample = []
for variant in tree_sequence.variants(): # variants are essentially SNPs
    SNPSample.append(variant.genotypes.tolist())

genomeSample = [list(individual) for individual in zip(*SNPSample)]
genomeSample = [g[:10] for g in genomeSample] # Limit the genome size to 10 SNPs

'''
# Simple pedigree
a = Individual(genome=[genomeSample[0],genomeSample[1]])
b = Individual(genome=[genomeSample[2],genomeSample[3]])
c = Individual(mother=a, father=b)

c.inherit()
print("Genome A:", a.genome)
print("Genome B:", b.genome)
print("Genome C:", c.genome)'''

# Read in 51 person Amish subpedigree.
with open(os.path.join(os.getcwd(),"amish_pedigree/amish_pedigree.csv"),'r') as f:
    pedigree = pd.read_csv(f)

missing = pedigree.query("MOTHER not in ID or FATHER not in ID")
top_of_pedigree = missing['ID'].tolist()
print(top_of_pedigree)

counter = 0
for i in top_of_pedigree:
    # Create the missing parents, then inherit
    ID1 = "A" + str(counter)
    ID2 = "A" + str(counter + 1)
    counter += 2

    mother = Individual(genome=[genomeSample.pop(), genomeSample.pop()],
                        sex=0, id=ID1)
    father = Individual(genome=[genomeSample.pop(), genomeSample.pop()],
                        sex=1, id=ID2)
    child = Individual(id=i, mother=mother, father=father) #TODO: add sex
    child.inherit()
    print(mother.id, mother.genome)
    print(father.id, father.genome)
    print(child.id, child.genome)
    print('\n')

# TODO:
# Simulate the parents of individuals at the top of the tree.s
# Add mutation.

import msprime
from pprint import pprint
import numpy
from pedigree import Individual, Pedigree
from random import choice
import csv
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
    data = pd.read_csv(f)

# Construct the pedigree
pedigree = Pedigree()

# Find missing ancestors and replace them with new Individual IDs
mother_missing = data.query("MOTHER not in ID")
father_missing = data.query("FATHER not in ID")

counter = 0
for i in mother_missing['ID'].tolist():
    motherID = "A" + str(counter)
    counter += 1
    mother = Individual(genome=[genomeSample.pop(), genomeSample.pop()],
                        sex=1, id=motherID, children=[i])
    pedigree.add_member(mother, ancestor=True)
    data.loc[data["ID"] == i, 'MOTHER'] = motherID

for i in father_missing['ID'].tolist():
    fatherID = "A" + str(counter)
    counter += 1
    father = Individual(genome=[genomeSample.pop(), genomeSample.pop()],
                        sex=0, id=fatherID, children=[i])
    pedigree.add_member(father, ancestor=True)
    data.loc[data["ID"] == i, 'FATHER'] = fatherID

# Add known individuals to the pedigree
for row in data.itertuples():
    ID, father, mother, sex = row[1:5]
    member = Individual(id=ID, mother=mother, father=father, sex=sex)
    if mother in pedigree.ancestors or father in pedigree.ancestors:
        pedigree.add_member(member, root=True)
    else:
        pedigree.add_member(member)

print("Ancestors:", len(pedigree.ancestors))
print("Roots:", len(pedigree.roots))
print("All members:", len(pedigree.members))

# TODO:
# Inherit down the tree
# Add mutation.

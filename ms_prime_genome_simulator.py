import msprime
from pprint import pprint
import numpy
from pedigree import Individual
from random import choice
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

#for variant in tree_sequence.variants(): # variants are essentially SNPs
#    print(variant.index, variant.position, variant.genotypes, sep='\t')
firstSNP = next(tree_sequence.variants()).genotypes
print(firstSNP)
# Simple pedigree
a = Individual(genome=[firstSNP[0],firstSNP[1]])
b = Individual(genome=[firstSNP[2],firstSNP[3]])
c = Individual(mother=a, father=b)

c.inherit()
print(a.genome, b.genome, c.genome)
# TODO:
# Single SNP, Single family
# 10 SNPs, single family simulation with crossover
# Larger pedigree
# Simulate mutation? Not clear if it will be on the SNPs, recombination more important
# 50 core members first

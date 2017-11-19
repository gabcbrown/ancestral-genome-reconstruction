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

# Setup logging
logging.basicConfig(level=logging.DEBUG, filename='output.log')

# Run MSPrime simulation of population growth and evolution.
# The parameters here are good defaults for humans.
# To change the number of genotypes output, just change the sample size.
# `tree_sequence` is an object of type msprime.trees.TreeSequence.
tree_sequence = msprime.simulate(sample_size=100, Ne=10000, length=5e3,
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
ped1 = ped['1'] # Pedigree object

# Create Pydigree Chromosome Template to store simulated MSPrime data and
# associate with the pedigree object.
# TODO: How does MSPrime store chromosome number?
chrom1 = pydigree.ChromosomeTemplate() # Create template
for snp_location in snp_locations: # Fill in with simulated data
    chrom1.add_genotype(map_position=snp_location)
ped1.add_chromosome(chrom1) # Add to the population
print(ped1.chromosomes.chroms[0].genetic_map) # Comfirm that it worked

# Chromosome pool?
pool = ChromosomePool(chromosomes=ped1.chromosomes)
#print(pool.pool)
pool.pool = [genomeSample]
#print(pool.pool)
ped1.pool = pool
#print(pool.chromosomes)
#print(pool.chromosome(0))
#print(pool.get_genotype_set())
#print(ped1.pool.pool)
ped1.get_founder_genotypes() # Populate founders genotypes from pool
ped1.get_genotypes() # Populate rest of the trees genotypes from inheritance
for i in ped1.individuals:
    print(i.genotypes)# Populate founder genotypes from chromosome pool.
#for f, genome in zip(ped1.founders(), genomeSample):
#    for location, g in zip(genome, snp_locations):
#        f.set_genotype(location, g)


#TODO:
# - Prediction
# -- SGSAnalysis Class, chromwide_ibd method

#TODO: This file should describe the format of a "template" that chromosome
# template wants: https://github.com/jameshicks/pydigree/blob/bde42786f81b885e797ee6f370f86489dedb053a/pydigree/io/genomesimla.py
# Assign founders genomes from MS_Prime data.
# need to setup gene pool population.pool. This is what founders are pulled from.
# Figure out what's going on with pools and chromosomes: https://github.com/jameshicks/pydigree/blob/bde42786f81b885e797ee6f370f86489dedb053a/pydigree/simulation/chromosomepool.py
# Then use individual.get_genotyoes()

# Populate down the tree
# Function for recombination:
# https://github.com/jameshicks/pydigree/blob/master/pydigree/recombination.py


'''
# Construct the pedigree
pedigree = Pedigree()

# Find missing ancestors and replace them with new Individual IDs
mother_missing = data.query("MOTHER not in ID")
father_missing = data.query("FATHER not in ID")
print(mother_missing)
print(father_missing)
counter = 0
for i in mother_missing['ID'].tolist():
    motherID = "A" + str(counter)
    counter += 1
    mother = Individual(genome=[genomeSample.pop(), genomeSample.pop()],
                        sex=2, id=motherID, children=[i])
    pedigree.add_member(mother, ancestor=True)
    data.loc[data["ID"] == i, 'MOTHER'] = motherID

for i in father_missing['ID'].tolist():
    fatherID = "A" + str(counter)
    counter += 1
    father = Individual(genome=[genomeSample.pop(), genomeSample.pop()],
                        sex=1, id=fatherID, children=[i])
    pedigree.add_member(father, ancestor=True)
    data.loc[data["ID"] == i, 'FATHER'] = fatherID

# Add known individuals to the pedigree
logging.info(data)
for row in data.itertuples():
    ID, fatherID, motherID, sex = row[1:5]

    # TODO: This makes me mad
    children = []
    for foo in data.itertuples():
        c, f, m = foo[1:4]
        if f == ID or m == ID:
            children.append(c)

    member = Individual(id=ID, mother=motherID,
                        father=fatherID,
                        children=children,
                        sex=sex)

    if motherID in pedigree.ancestors or fatherID in pedigree.ancestors:
        pedigree.add_member(member, root=True)
    else:
        pedigree.add_member(member)


# Check that everything is running smoothly
logging.info("Number of ancestors: {}".format(len(pedigree.ancestors)))
logging.info("Number of roots: {}".format(len(pedigree.roots)))
logging.info("Total number of members: {}".format(len(pedigree.members)))
pedigree.draw_structure()

# Inherit down the tree
pedigree.inherit()

# Check the genomes
for m in pedigree.members:
    logging.info(pedigree.members[m].genome)

# Check the haplotypes:
for h, name in pedigree.haplotypes.items():
    logging.info("Haplotype {}: {}".format(name, h))

breakpoint_indices = []
haplotypes = list(pedigree.haplotypes.keys())
for i in range(0, len(haplotypes[0])-1):
    for j in range(i + 1, len(haplotypes[0])):
        seen = set()
        for m in haplotypes:
            seen.add((m[i], m[j]))

        if seen == set([(0, 0), (0, 1), (1, 0), (1,1)]):
            logging.info("Recombination breakpoint between SNPs {} and {}:".format(i, j))
            breakpoint_indices.append((i, j))
'''

# cuda
#TODO:
# Can we identify regions of the chromosomes that have been passed down from these two individuals to affected individuals in the pedigree
# Phased with ShapeIt
# LD prune
# Valid assumption that all roots come from the same amish population
# How big was the European Amish population that these root individual came from
# LD structure of Amish populations are very similar to the European population
# Rules of inheritance
# Explicitly model each generation (one generation for now)
# Finding recombination breakpoints
# Choosing most likely haplotype
# Look up Identity by Descent
# https://www.ncbi.nlm.nih.gov/pubmed/?term=Li%20X%5BAuthor%5D&cauthor=true&cauthor_uid=25519372

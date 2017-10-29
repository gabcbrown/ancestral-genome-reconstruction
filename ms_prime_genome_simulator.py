import msprime
from pprint import pprint
import numpy
from pedigree import Individual, Pedigree
from random import choice
import csv
import pandas as pd
import os
import logging
import sys

#logging.basicConfig(level=logging.DEBUG)

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

    '''if sex == 2:
        children = data.loc[data["MOTHER"] == i, 'ID'].tolist()
    elif sex == 1:
        children = data.loc[data["FATHER"] == i, 'ID'].tolist()
    '''

    member = Individual(id=ID, mother=motherID,
                        father=fatherID,
                        children=children,
                        sex=sex)

    if motherID in pedigree.ancestors or fatherID in pedigree.ancestors:
        pedigree.add_member(member, root=True)
    else:
        pedigree.add_member(member)


# Check that everything is running smoothly
logging.info("Ancestors: {}".format(len(pedigree.ancestors)))
logging.info("Roots: {}".format(len(pedigree.roots)))
logging.info("All members: {}".format(len(pedigree.members)))
pedigree.draw_structure()

# Inherit down the tree
pedigree.inherit()

for m in pedigree.members:
    logging.info(pedigree.members[m].genome)

#TODO:
# Rules of inheritance
# Explicitly model each generation (one generation for now)
# Finding recombination breakpoints
# Choosing most likely haplotype
# Look up Identity by Descent
# https://www.ncbi.nlm.nih.gov/pubmed/?term=Li%20X%5BAuthor%5D&cauthor=true&cauthor_uid=25519372

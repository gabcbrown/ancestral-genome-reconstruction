# Ancestral Genome Reconstruction - Genome Simulator

## Motivation
We are interested in reconstructing ancestral SNPs for known, highly inter-related pedigrees. This code is the research of Gabriela Brown and Dr. Sara Mathieson at Swarthmore College.

## Installation 
This code uses pipenv to install and manage python dependencies. To install
pipenv, follow the instructions here: TODO: link
OR
run `pip install pipenv` TODO: is this true?

To install dependencies, run
`pipenv install requirements.txt`

## Running the Code TODO: figure out how to format this file
`pipenv run python3 genome_simulator.py [--length chromosome_length] [--help] [--verbose] [--output filename] pedigree_file family_id`  

## Arguments
`pedigree_file` -- Path to the file that specifies the pedigree structure to use
in the simulation.
`family_id` -- The FAMILY_ID of the pedigree in the pedigree_file.
`--length chromosome_length` -- [Optional] Length in base pairs of chromosome to
simulate. Default value is 5000.
`--verbose` -- Increase output verbosity.
`--help` -- Output usage information.
`--output` -- Filename to write output files to (.ped, .map, .pdf).

## Input file format
The pedigree data is supplied by the `pedigree_file` and `family_id` arguments.
The pedigree file should contain a single pedigree in a format similar to TODO.
If you have a TODO format file, run `convert_format.py` to get the right input
format.

The pedigree file must be space delimited, with no header, and have the following columns:

1. FAMILY_ID -- A single word or number per pedigree. This should be the same for every row.
2. INDIVIDUAL_ID -- A unique identifying number.
3. FATHER_ID -- The INDIVIDUAL_ID of the father. Use 0 for unknown/missing individuals.
4. MOTHER_ID -- The INDIVIDUAL ID of the mother. Use 0 for unknown/missing individuals.
5. SEX -- Use 1 for male, 2 for female.

In addition,
1. Every INDIVIDUAL_ID present in the FATHER_ID and MOTHER_ID columns must
also have their own row. The file is space delimited, with no header.
2. The mother and father of an individual must precede the individual in the
dataset.

## Output file format
The simulation will write Plink files to output.map and
output.ped) and visualization files to output.pdf). An
alternate name can be specified with the --output argument.

## Runtime
Some informal experiments have shown that, given a fixed pedigree structure,
the runtime is polynomial on the length of the chromosome being simulated. For
example, if you want to simulate the length of Chromosome 4 (about 190 million
bp), it will take about 20 minutes. If you want to simulate the length of the
entire human genome (about 3 billion bp), it will take about 3 days.

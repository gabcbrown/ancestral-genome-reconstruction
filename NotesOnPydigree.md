NOTE: The docs are here: https://github.com/jameshicks/pydigree/tree/master/doc
IO:
________________________________________________________________________________
Let's start by getting our data into Pydigree. Pydigree can read in a space or
tab separated file with the following columns:
 `PedigreeID` `IndividualID`  `Mother`  `Father`   `Sex`
In the file you pass in, make sure that any IDs that show up in Mother or Father
columns are individuals with their own row in the dataset. If not, make a row
for that individual with values 0 0 for parents. (Put these individuals with no
known parents at the top of the file for clarity).

Now we read in the data using:
`ped = pydigree.io.read_ped(filename)`

In this case, we only had one pedigree in the data set which we gave the name '1'.
However, the variable `ped` output by this method is a PedigreeCollection object.
We therefore need to use `ped1 = ped['1']` to access the actual pedigree.

The variable `ped1` is a Pedigree object, which is what we want. All of the
individuals who had parents 0 0 in the dataset are treated as founders. The call
`ped1.individuals` gives a list of all the individuals in the pedigree, each of
which is an Individual object. We can check these individuals to see if they are
a founder using `individual.is_founder`. Similarly, we can check other features
of ancestry and lineage:
- `ind.parents()` #  tuple of individuals
- `ind.ancestors()` #  collection of individuals
- `ind.descendants()` # collection of individuals
- `ind.siblings()` # collection of individuals
- `ind.matriline()` # collection of individuals
- `ind.patriline()` # collection of individuals
- `ind.depth()` # Depth in the tree. 0 if founder, max(parents) else.

There are also useful methods for simulating reproduction down the tree:
- `ind.get_genotypes()` - has different behavior depending on what type of
  individual it is called on. For founders, if pulls a genotype from the genome
  pool. For everyone else, it recombines and inherits their parent's genomes.
- `ind.gamete()`
- `ind.fertilize(father, mother)`
- `ind.has_genotypes()` # quick check to make sure the individual has a genome.

Now, in order to actually give the individuals genomes, we need to establish
some population-wide classes and organization. Start by giving the Pedigree
population the number of chromosomes it needs. In this case we only need one, so
we will write:
`chrom1 = pydigree.ChromosomeTemplate()
ped1.add_chromosome(chrom1)`

You can easily check how many chromosomes a population currently has using
'ped1.chromosome_count()'. (Pedigree inherits from Population. A population
stores the ChromosomeSet object of ChromosomeTemplates that describe the
chromosome structure of the population. Individuals store the actual values of
the genomes).


________________________________________________________________________________



 Individual - represent the genotype and phenotype of an individual.
  inputs:
  -

Organization of individuals:
Population - represent a group of unrelated individuals.

Pedigree - represent a group of related individuals with known pedigree structure.

PedigreeCollection - represent a collection of pedigrees.


Organization of genetic information:
Alleles - represent a set of alleles for a haploid chromosome

SparseAlleles - a memory-efficient way to store alleles, like above.


Simulation:
There's a lot of simulation stuff for populations, pedigrees, and phenotypes.
ConstrainedMendelianSimulation???

Analysis:
IBD -> SGSAnalysis
HMM
LMM
Coefficient calculation (Kinship, inbreeding...)

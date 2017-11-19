NOTE: The docs are here: https://github.com/jameshicks/pydigree/tree/master/doc

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
We want the chromosome to keep track of SNPs output by an MSPrime simulation. So
we iterate through the SNP locations and add them to the ChromosomeTemplate:
`for snp_location in snp_locations:
    chrom1.add_genotype(map_position=snp_location)`:
ped1.add_chromosome(chrom1)`

`ped1` will store the chromosomes you give it in a `ChromosomeSet` object. (If
you want to see where in the code this happens, Pedigree inherits from
Population, and Population implements this organization.) You can easily check how many chromosomes a population currently has using
`ped1.chromosome_count()`.

Individuals store the values of the genotypes whose structure (SNP location)
is specified by the ChromosomeSet. Normally, Pydigree sets up a `ChromosomePool`
object with its own simulation methods in order to populate individual genotypes.
But we want to use the output of an MSPrime simulation (`genomeSample`) instead,
so the next step is a bit of a hack.

We start by initializing a ChromosomePool object from the population's
ChromosomeSet:
`pool = ChromosomePool(chromosomes=ped1.chromosomes)`

Now, we want to set the ChromosomePool's `pool` attribute to be our MSPrime
data. The `pool` attribute expects a list with the following structure:
`[[Chromosome 1 Pool], [Chromosome 2 Pool], ... , [Chromosome N Pool]]`
Where `[Chromosome i Pool]` has the structure `[[Haplotype 1], [Haplotype 2], ...
, [Haplotype M]]` of the possible haplotypes for the set of SNPs specified in
ChromosomeTemplate. Since we only have one chromosome in this situation, this
is just
`pool.pool = [genomeSample]`

We associate this ChromosomePool with the pedigree:
`ped1.pool = pool`
Now we can populate the founder's genotypes randomly from the chromosome pool:
`ped1.get_founder_genotypes()`
And populate the rest of the individual's genotypes by inheriting from their
parent's genotypes:
`ped1.get_genotypes()`



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

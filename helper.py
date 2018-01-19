import msprime
import graphviz as gv
import pydigree
from  pydigree.simulation.chromosomepool import ChromosomePool
from pydigree.sgs import SGSAnalysis
from pydigree.ibs import get_ibs_states
from pydigree.io.plink import write_plink
from pydigree.genotypes import alleles


class Simulation():

    def __init__(self, verbose=False):
        self.pedigrees = None # Because otherwise we can't output Plink
        self.pedigree = None
        self.genomePool = None
        self.verbose = verbose


    def addPedigree(self, fileName, pedigreeName):
        # Read in 51 person Amish subpedigree to Pydigree pedigree object.
        self.pedigrees = pydigree.io.read_ped(fileName) # PedigreeCollection object
        self.pedigree =self.pedigrees[pedigreeName] # Pedigree object


    def _validatePedigreeFile(self, filename):
        #TODO: Implement and add call in addPedigree
        raise NotImplementedError


    def runSimulation(self, sampleSize=100, chromLength=5000):
        if self.verbose:
            print("Starting simulation")

        # Run MSPrime simulation of population growth and evolution.
        # The parameters here are good defaults for humans.
        # To change the number of genotypes output, just change the sample size.
        # `tree_sequence` is an object of type msprime.trees.TreeSequence.
        # Chromosome 4 is length=186e6
        numMutations = 0
        while numMutations == 0:
            tree_sequence = msprime.simulate(sample_size=sampleSize, Ne=10000,
                length=chromLength, recombination_rate=2e-8, mutation_rate=2e-8)
            numMutations = tree_sequence.get_num_mutations()

        if self.verbose:
            print("Simulated {} mutations".format(numMutations))

        # Transform MSPrime population sample from list of individual values for each
        # SNP site to list of SNPS for each individual.
        snp_sample = []
        snp_locations = []
        for variant in tree_sequence.variants(): # variants are essentially SNPs
            snp_sample.append(variant.genotypes.tolist())
            snp_locations.append(variant.position)
        # One instance of the Alleles object corresponds to the haploid alleles of
        # one individual. (i.e. the alleles of one of their chromosome copies.)
        self.genomePool = [alleles.Alleles(individual) for individual in zip(*snp_sample)]
        self.snpLocations = snp_locations


    def populateGenomes(self):
        # Create Pydigree Chromosome Template to store simulated MSPrime data and
        # associate with the pedigree object.
        # TODO: How does MSPrime store chromosome number?
        chrom1 = pydigree.ChromosomeTemplate() # Create template
        for snp_location in self.snpLocations: # Fill in with simulated data
            chrom1.add_genotype(map_position=snp_location)
        self.pedigree.add_chromosome(chrom1) # Add to the population
        #print(self.pedigree.chromosomes.chroms[0].genetic_map) # Comfirm that it worked

        #TODO: This fails if no mutations were generated
        pool = ChromosomePool(chromosomes=self.pedigree.chromosomes)
        pool.pool = [self.genomePool]
        self.pedigree.pool = pool
        # To look at the first chromosome in the pool: pool.chromosome(0)
        # To access values of pedigree pool: self.pedigree.pool.pool
        self.pedigree.get_founder_genotypes() # Populate founders genotypes from pool
        self.pedigree.get_genotypes() # Populate rest of the trees genotypes from inheritance


    def writePedigreeToPlink(self, fileName):
        if not self.pedigrees:
            raise ValueError("No pedigree defined, cannot write to Plink file.")

        write_plink(self.pedigrees, fileName, mapfile=True)

        if self.verbose:
            print("Plink files written to {}.map and {}.ped".format(fileName,
                                                                    fileName))


    def visualizePedigree(self, fileName):
        if not self.pedigree:
            raise ValueError("No pedigree defined, cannot visualize pedigree.")

        # A nice tutorial on gv: http://matthiaseisen.com/articles/graphviz/
        g = gv.Digraph('pedigree')
        for i in self.pedigree.individuals:
            g.node(str(i.label)) #Otherwise it throws an error
        for i in self.pedigree.individuals:
            for c in i.children:
                g.edge(str(i.label), str(c.label))

        filename = g.render(filename=fileName)

        if self.verbose:
            print("Pedigree visualization written to {}.pdf".format(fileName))

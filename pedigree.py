# TODO:
# More crossover points
from random import choice, uniform
from copy import deepcopy
import graphviz as gv
import logging

class Individual():

    def __init__(self, id=None, mother=None, father=None, children=[], sex=None,
                 genome=[[],[]]):
        self.id = id # TODO: Is this name bad?
        self.mother = mother
        self.father = father
        self.children = children
        self.sex = sex
        self.genome = genome
        self.haplotypes = []
        #self.logger = logging.getLogger(__name__)



    def inherit(self, m, f):
        # FIXME
        #maternal = self._meiosis(self.mother.genome[0], self.mother.genome[1])
        maternal = self._meiosis(m.genome[0], m.genome[1])
        #paternal = self._meiosis(self.father.genome[0], self.father.genome[1])
        paternal = self._meiosis(f.genome[0], f.genome[1])
        self.genome = [maternal, paternal]

    # Takes two homologous chromosomes (hc) and simulates meiosis. Returns a
    # single gamete chromosome. Simulates 1 crossover point.
    def _meiosis(self, hc1, hc2):
        # Randomly chooses an index to crossover at.
        crossoverPoint = choice(range(0,len(hc1)))

        # Simulate Meiosis I with:
        # - each homologous chromosome duplicates itself into two identical
        #   sister chromatids (sc).
        # - One sister chromatid from each homologous chromosome cross over.
        sc1a, sc1b = deepcopy(hc1), deepcopy(hc1)
        sc2a, sc2b = deepcopy(hc2), deepcopy(hc2)
        new_sc1a = sc1a[:crossoverPoint] + sc2a[crossoverPoint:]
        new_sc2a = sc2a[:crossoverPoint] + sc1a[crossoverPoint:]
        gametes = [new_sc1a, sc1b, new_sc2a, sc2b]

        # Simulate mutation in the duplication TODO: Ways to improve this?
        # Mutation method inspired by http://wjidea.github.io/2016/popSim.html
        mutation_rate = 0.0005 # between 10e-3 and 10e-4
        for g in gametes:
            if uniform(0,1.0) < mutation_rate: # Mutation!
                logging.info("Mutation!")
                mutation_locus = choice(range(0,len(g)))
                g[mutation_locus] = 0 if g[mutation_locus] == 1 else 1

        # Simulate Meiosis II with
        # - the now crossed-over homologous chromosomes separate and the cell
        #   divides.
        # - the sister chromatids separate and the cells divide into 4 gametes.
        return choice(gametes)

class Pedigree():

    def __init__(self):
        self.members = {}
        self.roots = {}
        self.ancestors = {}
        self.haplotypes = {}

    def _add_haplotype(self, member):
        for chromosome in member.genome:
            c = tuple(chromosome)
            if c in self.haplotypes:
                # We've already given a name to this haplotype
                haplotype = self.haplotypes[c]
                member.haplotypes.append(haplotype)
            else:
                # Name this new haplotype
                self.haplotypes[c] = len(self.haplotypes) + 1

    def add_member(self, new_member, root=False, ancestor=False):
        self.members[new_member.id] = new_member
        if root == True:
            self.roots[new_member.id] = new_member
        elif ancestor == True:
            self.ancestors[new_member.id] = new_member
            self._add_haplotype(new_member)

    def get_member(self, id):
        try:
            return self.members[id]
        except:
            return None

    def has_member(self, id):
        if id in self.members:
            return True
        return False

    def inherit(self):
        children = []
        for a in self.ancestors:
            children += self.ancestors[a].children

        while len(children) > 0:
            c_id = children.pop(0)
            c = self.members[c_id]
            c.inherit(self.members[c.mother], self.members[c.father])
            self._add_haplotype(c)
            children += c.children


    def draw_structure(self, snp=None):
        # A nice tutorial on gv: http://matthiaseisen.com/articles/graphviz/
        g = gv.Digraph('pedigree')
        for i in self.members:
            g.node(str(i)) #Otherwise it throws an error
        for i in self.members:
            for c in self.members[i].children:
                g.edge(str(i), str(c))

        filename = g.render(filename='visualizePedigree')
        logging.info("Pedigree drawn to {}".format(filename))

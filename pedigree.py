# TODO:
# More crossover points
from random import choice
from copy import deepcopy

class Individual():

    def __init__(self, id=None, mother=None, father=None, children=[], sex=None,
                 genome=[[],[]]):
        self.id = id # TODO: Is this name bad?
        self.mother = mother
        self.father = father
        self.children = children
        self.sex = sex
        self.genome = genome

    def inherit(self):
        maternal = self._meiosis(self.mother.genome[0], self.mother.genome[1])
        paternal = self._meiosis(self.father.genome[0], self.father.genome[1])
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

        # Simulate Meiosis II with
        # - the now crossed-over homologous chromosomes separate and the cell
        #   divides.
        # - the sister chromatids separate and the cells divide into 4 gametes.
        return choice([new_sc1a, sc1b, new_sc2a, sc2b])

class Pedigree():

    def __init__(self):
        self.members = {}
        self.roots = {}
        self.ancestors = {}

    def add_member(self, new_member, root=False, ancestor=False):
        self.members[new_member.id] = new_member
        if root == True:
            self.roots[new_member.id] = new_member
        elif ancestor == True:
            self.ancestors[new_member.id] = new_member

    def get_member(self, id):
        try:
            return self.members[id]
        except:
            return None

    def has_member(self, id):
        if id in self.members:
            return True
        return False

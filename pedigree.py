# TODO:
# More crossover points
from random import choice

class Individual():

    def __init__(self, ID=None, mother=None, father=None, children=[], sex=None,
                 genome=[[],[]]):
        self.id = ID
        self.mother = mother
        self.father = father
        self.children = children
        self.sex = sex
        self.genome = genome

    def inherit(self):
        maternal = self._meiosis(self.mother.genome[0], self.mother.genome[1])
        paternal = self._meiosis(self.father.genome[0], self.father.genome[1])
        self.genome = [maternal, paternal]

    # Takes two homologous chromosomes (hc) and simulates meiosis. Returns a single
    # gamete chromosome. Simulates 1 crossover point.
    def _meiosis(self, hc1, hc2):
        # Randomly chooses an index to crossover at.
        crossoverPoint = choice(range(0,len(hc1)))

        # Simulate Meiosis I with:
        # - each homologous chromosome duplicates itself into two identical
        #   sister chromatids (sc).
        # - One sister chromatid from each homologous chromosome cross over.
        sc1a, sc1b, sc2a, sc2b = hc1, hc1, hc2, hc2 # TODO: make sure this doesn't break
        new_sc1a = sc1a[:crossoverPoint] + sc2a[crossoverPoint:]
        new_sc2a = sc2a[:crossoverPoint] + sc1a[crossoverPoint:]

        # Simulate Meiosis II with
        # - the now crossed-over homologous chromosomes separate and the cell
        #   divides.
        # - the sister chromatids separate and the cells divide into 4 gametes.
        return choice([new_sc1a, sc1b, new_sc2a, sc2b])

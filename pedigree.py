from random import choice

class Individual():

    def __init__(self, mother=None, father=None, children=[], sex=None,
                 genome=[[],[]]):
        self.mother = mother
        self.father = father
        self.children = children
        self.sex = sex
        self.genome = genome

    def inherit(self):
        m = choice([0,1])
        p = choice([0,1])
        matriline = self.mother.genome[m]
        patriline = self.father.genome[p]
        self.genome = [matriline, patriline]

# GENETIC ALGORITHM METHODS.
from abc import ABC, abstractmethod
from random import randint, uniform
from EA import EA
import numpy as np
from random import seed
np.random.seed(111)
seed(111)

class GA(EA, ABC):
    def __init__(self, type_of_genes, lower_bound, upper_bound, pop_size, no_of_genes, xover_model, problem):
        self.type_of_genes = type_of_genes
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.pop_size = pop_size
        self.no_of_genes = no_of_genes
        self.xover_model = xover_model
        super().__init__(problem)

    @abstractmethod
    def evaluate(self, *args):
        pass

    # Generic random population initialisation. Creates either integers or floats, depending on the given type_of_genes.
    def initialise_population(self):
        chromosomes = None # ???
        if self.type_of_genes == "int":
            chromosomes = [[randint(self.lower_bound, self.upper_bound) for _ in range(self.no_of_genes)] for _
                           in range(self.pop_size)]

        elif self.type_of_genes == "float":
            chromosomes = [[uniform(self.lower_bound, self.upper_bound) for _ in range(self.no_of_genes)] for _
                           in range(self.pop_size)]
            # for x in range(len(chromosomes)-90):
            #     for y in range(len(chromosomes[x])):
            #         chromosomes[x][y] = 0.0
            # # Also needs to CHANGE !!!!
            # chromosomes[0][0]=1.0;chromosomes[1][1]=1.0;chromosomes[2][2]=1.0;chromosomes[3][3]=1.0;chromosomes[4][4]=1.0
            # chromosomes[5][5] = 1.0;chromosomes[6][6]=1.0;chromosomes[7][7]=1.0;chromosomes[8][8]=1.0;chromosomes[9][9]=1.0
            # #COMMENT !! ONLY FOR 8 STRATS
            # # chromosomes[8][8]=1.0; chromosomes[9][9] = 1.0;chromosomes[10][10]=1.0;chromosomes[11][11]=1.0

        else:
            print("SHOULD NOT REACH HERE!")
            exit()
        population = [self.Individual(chromosome) for chromosome in chromosomes]

        return population

    # One-point crossover
    def crossover(self, parent1, parent2):
        if self.xover_model == "TwoPoint":
            xover_point_1 = np.random.randint(1, len(parent1) - 1)
            xover_point_2 = np.random.randint(1, len(parent2) - 1)
            # xover_point_1=12
            # xover_point_2=12
            child = []
            if xover_point_1 < xover_point_2:
                for i in range(0, xover_point_1):
                    child.append(parent1[i])
                for i in range(xover_point_1, xover_point_2):
                    child.append(parent2[i])
                for i in range(xover_point_2, len(parent2)):
                    child.append(parent1[i])
            elif xover_point_1 > xover_point_2:
                for i in range(0, xover_point_2):
                    child.append(parent1[i])
                for i in range(xover_point_2, xover_point_1):
                    child.append(parent2[i])
                for i in range(xover_point_1, len(parent2)):
                    child.append(parent1[i])
            elif xover_point_1 == xover_point_2:
                for i in range(0, xover_point_1):
                    child.append(parent1[i])
                for i in range(xover_point_1, len(parent2)):
                    child.append(parent2[i])
            return child
        elif self.xover_model == "OnePoint":
    # def crossover(self, parent1, parent2):
            xover_point = randint(1, len(parent1)-1)
            child = []
            for i in range(0, xover_point):
                child.append(parent1[i])
            for i in range(xover_point, len(parent2)):
                child.append(parent2[i])
            return child

    # Point mutation. Differentiates between integer and float gene types.
    def mutate(self, parent):
        mutation_point = randint(0, len(parent)-1)
        if self.type_of_genes == "int":
            parent[mutation_point] = randint(self.lower_bound, self.upper_bound)
        elif self.type_of_genes == "float":
            parent[mutation_point] = uniform(self.lower_bound, self.upper_bound)

        return parent

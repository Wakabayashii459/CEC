# Port.Optimisation PROBLEM IMPLEMENTATION. ESSENTIALLY THE ONLY THING WE NEED TO DO IS DEFINE THE PROBLEM-SPECIFIC
# FITNESS FUNCTION. ALL OTHER GA FUNCTIONS (E.G. CROSSOVER, MUTATION) ARE WRITTEN IN THE PARENT CLASSES EA AND GA. WE
# CAN OF COURSE OVER-WRITE THEM HERE, IF WE WANT A DIFFERENT IMPLEMENTATION, E.G. A DIFFERENT CROSSOVER OPERATOR.
from EA import Problem, EA
from GA import GA
import numpy as np
import pandas as pd
from random import seed, randint, uniform
import WeightsTraining, WeightsTest
import math


np.seterr(divide='ignore', invalid='ignore')

np.random.seed(111)
seed(111) # Using a seed for reproducibility purposes, as GA is a stochastic algorithm.
nRUNS = 50 ##
POPULATION_SIZE = 100
nGENS = 18  # Number of generations
XOVER_PROB = 0.95
TOURNAMENT_SIZE = 2 #
GENES_TYPE = "float"  # Define the type of the GA genes, if e.g. they will be int or float
LB = 0  # Lower boundary (inclusive) of the potential gene values that are generated
UB = 1  # Upper boundary (inclusive) of the potential ge+ne values that are generated
PROBLEM = Problem.MAXIMISATION  # Setup as maximisation problem
data = np.array(pd.read_csv("returns.csv"))
# expected_returns = np.mean(data, axis=0)
GENES = 5  # Number of genes (cells) in each chromosome !!!!!
XOVER_MODEL = 'OnePoint'
for_debug=1


class PortfolioOptimisation(GA):

    class Individual(EA.Individual):
        #mdd = 0
        number_of_trades = 0
        rate_of_return = 0
        risk = 0
        sharpe_ratio = 0

    def __init__(self):
        super().__init__(type_of_genes=GENES_TYPE, lower_bound=LB, upper_bound=UB,
                         pop_size=POPULATION_SIZE, no_of_genes=GENES, xover_model=XOVER_MODEL, problem=PROBLEM)

    # Problem-specific fitness function calculation. Flag is not used here.
    def evaluate(self, individual, dataset, flag):
        # Some explanations: 1. we do np.array(individual.model), because after xover the individuals end up as list
        # Normally there's no problem, but we cannot do the matrix multiplication for lists, so we convert it to array.
        # 2. We reshape both the weights (individual.model) and the returns arrays, so that their dimensions are
        # compatible for the matrix multiplication. 3. In this simple example, fitness is the return of the portfolio.
        # individual.fitness = return_per_individual[0, 0]  # Obtain the value from the single-element array
        # Weights.get_weights(individual.model)
        if flag == 0:
            WeightsTraining.calculate_sharpe(individual.model)
            individual.fitness = WeightsTraining.sharpeGA_tf
            #individual.mdd = Weights.mddGA
            individual.number_of_trades = WeightsTraining.number_of_tradesGA
            individual.rate_of_return = WeightsTraining.rate_of_return
            individual.risk = WeightsTraining.riskGA
            individual.sharpe_ratio = WeightsTraining.sharpeGA_tf
        else:
            WeightsTest.calculate_sharpe(individual.model)
            individual.fitness = WeightsTest.sharpeGA_tf
            #individual.mdd = Weights_test.mddGA
            individual.number_of_trades = WeightsTest.number_of_tradesGA
            individual.rate_of_return = WeightsTest.rate_of_return
            individual.risk = WeightsTest.riskGA
            individual.sharpe_ratio = WeightsTest.sharpeGA_tf

        if math.isnan(individual.fitness):
            print('Problem!!! There was no trade')
        for_debug=0
        # print(individual.model)
        # for_debug=1 # fitness = sharpe ratio
    # One-point crossover. Overwrites parent method to ensure that weights are always normalised in the [0, 1) range.
    # Strictly speaking, I should have done the same during population initialisation. But it doesn't really matter,
    # as even without normalisation, the weights still show preferences between assets. And during crossover/mutation,
    # I normalise the whole population, so from generation 1 onwards we have normalised weights.
    def crossover(self, parent1, parent2):
        if self.xover_model=='TwoPoint':
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
            return child / np.sum(child)
    #def crossover(self, parent1, parent2):
        elif self.xover_model == 'OnePoint':
            xover_point = randint(1, len(parent1) - 1)
            child = []
            for i in range(0, xover_point):
                child.append(parent1[i])
            for i in range(xover_point, len(parent2)):
                child.append(parent2[i])
            return child / np.sum(child)  # weights normalisation
    # Point mutation. Overwrites parent method to ensure that weights are always normalised in the [0, 1) range.
    def mutate(self, parent):
        mutation_point = randint(0, len(parent) - 1)
        parent_copy = parent.copy()
        parent_copy[mutation_point] = uniform(self.lower_bound, self.upper_bound)

        return parent_copy / np.sum(parent)  # weights normalisation

# Runs the EA algorithm over a number of independent runs and prints and saves results.
if __name__ == '__main__':
    task = PortfolioOptimisation()  # ????
    task.run(population_size=POPULATION_SIZE, xover_prob=XOVER_PROB, tournament_size=TOURNAMENT_SIZE,
             no_of_gens=nGENS, no_of_runs=nRUNS, training_dataset=None, test_dataset=None,
             class_object=PortfolioOptimisation.Individual("")) # check it out again
check_1=0
    # DUMMY TEST DATASET HAS BEEN PASSED ABOVE. SHOULD REPLACE IT WITH AN ACTUAL TEST DATASET.

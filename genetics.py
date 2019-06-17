# Genetic Algorithm
# Attempt to simulate the process of evolution according to natural selection
# Author cyyy

from ctypes import *
from random import random
from random import seed
from os import system

seed(None)

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]

def cpos(x,y):
    STD_OUTPUT_HANDLE = -11
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(x,y))

# return a random integer between a given minimum and maximum number
def scaledRand(mini, maxi):
    value = random()
    return int(mini + (value * (maxi - mini)))

class entity:
    def __init__(self, size, mr):
        self.size = size            # the length of the genes
        self.mutationRate = mr      # the chance that the genes will undergo mutation
        self.fitness = 0            # the fitness score of the entity, the higher, the more chances of being picked in the selection process
        self.genes = ''             
        for i in range(size):
            self.genes += ('abcdefghijklmnopqrstuvwxyz ')[scaledRand(0,27)]

    def mutate(self):
        if random() < self.mutationRate:
            mutationPoint = scaledRand(0, self.size)
            replacement = ('abcdefghijklmnopqrstuvwxyz ')[scaledRand(0, 27)]
            self.genes = self.genes[:mutationPoint] + replacement + self.genes[mutationPoint+1:]

    def crossover(self, inputEntity):
        midpoint = scaledRand(1, self.size)
        child = entity(self.size, self.mutationRate)
        child.genes = self.genes[0:midpoint] + inputEntity.genes[midpoint:]
        child.mutate()
        self.child = child

    def updateFitness(self, target):
        targetGenes = target.genes
        for i in range(self.size):
            if self.genes[i] == targetGenes[i]:
                self.fitness += 1

class evolution:
    def __init__(self, size, target):
        self.size = size
        self.population = []    # size of the pupolation in the evolution
        self.matingPool = []    # list of parents that will undergo selection
        self.bestfit = 0        # the current fittest entity in the population according to the target entity
        self.target = target    # target entity
        self.show = False       
        self.pausable = False
        self.bestEntity = entity(target.size, 0.0)
        for i in range(size):
            self.population.append(entity(target.size, 0.1))

    def addToPool(self, ent):
        for i in range(ent.fitness):
            self.matingPool.append(ent)

    def start(self):
        generation = 0
        fit = False
        while not fit:
            generation += 1
            for ent in self.population:
                ent.updateFitness(self.target)
                if ent.fitness > self.bestfit:
                    self.bestfit = ent.fitness
                    self.bestEntity = ent
            cpos(0,0) # set the cursor position to top left
            print('Generation:    {}'.format(generation))
            print('Best Gene:     {}'.format(self.bestEntity.genes))
            print('Target:        {}'.format(self.target.genes))
            print('Mutation Rate: {}'.format(ent.mutationRate))
            print('\nCurrent Population:\n' if self.show else '\n')
   
            for ent in self.population:
                if self.show:
                    print(ent.genes)
                self.addToPool(ent)
            
            if self.pausable is True:
                print()
                system('pause')
                
            for i in range(self.size):
                if len(self.matingPool) == 0:
                    for i in range(len(self.population)):
                        self.matingPool.append(self.population[i])
                mother = self.matingPool[scaledRand(0, len(self.matingPool))]
                father = self.matingPool[scaledRand(0, len(self.matingPool))]
                mother.crossover(father)
                child = mother.child
                self.population[i] = child
            
            self.matingPool = []
            if self.bestfit == self.target.size:
                fit = True

if __name__ == '__main__':

    # YOU CAN CHANGE THE VALUES FOR EXPERIMENTATION
    # this string is the target value
    # the longer the target the more population you'll need for faster evolution
    # use only small letters and space
    target = 'jan cyrill'
    # mutation rate is the probability that the gene of the entity instance will be changed
    mutationRate = 0.3
    # the population that will try to evolve towards the target string/genes
    population = 40
    # set to true if you want the evolution to pause at every generation
    pausable = True
    # set to true if you want to see the genes of population
    show = True

    # DO NOT MODIFY
    ideal = entity(len(target), mutationRate)   # create instance of the ideal entity
    ideal.genes = target                        # set the ideal entity's gene according to target
    evo = evolution(population, ideal)          # create the evolution environment
    evo.show = show            
    evo.pausable = pausable
    evo.start()                                 # start the simulation

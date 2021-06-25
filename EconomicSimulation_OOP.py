# OOP design with abstraction : implementations are left to concrete classes.
# To add a new functionality, just create a new class that inherits from/implements the generic interface.

import random
from abc import ABC, abstractmethod

#Interfaces/abstractions

class IWealth(ABC):
    @abstractmethod
    def initialize(self, wealth, size):
        pass
    
class IInteraction(ABC):
    @abstractmethod
    def chooseBuyerSeller(self, size):
        pass
            
class ITransaction(ABC):
    @abstractmethod
    def exchange(self, a, b):
        pass
    
class IMetrics(ABC):
    def __init__(self):
        self.value = 0

    @abstractmethod
    def compute(self, arr):
        pass
    
    def display(self):
        print(self.value)
    
class ISimulation(ABC):
    def __init__(self, repartition, interaction, transaction, metric):
        self.repartition = repartition
        self.interaction = interaction
        self.transaction = transaction
        self.metric = metric

    def run(self,pop,wealth,step):
        population = self.repartition.initialize(wealth, pop)
        self.metric.compute(population)
        self.metric.display()
        for _ in range(step):
            ind1, ind2 = self.interaction.chooseBuyerSeller(pop) # Buyer meets sellers
            population[ind1], population[ind2] = self.transaction.exchange(population[ind1], population[ind2]) # They exchange money
        self.metric.compute(population)
        self.metric.display()

# Concrete classes/implementations

class UniformWealth(IWealth): # Same wealth for everyone
    def initialize(self, wealth, size):
        return [wealth for i in range(size)]
    
class RandomWealth(IWealth):  # Random wealth for each individual
    def initialize(self, wealth, size):
        return random.choices(list(range(wealth)), k=size)
    
class FairTransaction(ITransaction):
    def exchange(self, a, b):
        pot = a + b
        split = random.choice(list(range(1, pot)))
        return split, pot - split

class UnFairTransaction(ITransaction):
    def exchange(self, a, b):
        pot = a + b
        split = 0
        return split, pot - split
    
class RandomGuys(IInteraction):
    def chooseBuyerSeller(self, size):
        return random.choices(list(range(size)), k=2)

class NeighborsGuys(IInteraction):
    def chooseBuyerSeller(self, size):
        return random.choices(list(range(size)), k=2)
        # Here you can implement a way to select two neighbors


class Gini(IMetrics):
    def compute(self, arr):
        arr.sort()
        n = float(len(arr))
        self.value = 2.0*sum([(i+1)*w for i, w in enumerate(arr)]) / (n*sum(arr)) - (n+1)/n
    
class Simulation(ISimulation):
    def __init__(self, repartition, interaction, transaction, metric):
        super().__init__(repartition, interaction, transaction, metric)

POP = 1000   # Number of individuals
WEALTH = 100 # Initial wealth of the population
ITER = 10000 # Number of transaction before the simulmation ends

simulation = Simulation(UniformWealth(), RandomGuys(), UnFairTransaction(), Gini()) # Here you can choose how the simulation performs by modifying the constructor and provides the object you want.
simulation.run(POP,WEALTH,ITER)

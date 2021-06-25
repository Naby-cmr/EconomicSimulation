# Functional design : implementations are in functions called when neeeded.

import random

def initialization(size, wealth):
    #arr = [wealth for i in range(size)]              # Same wealth for everyone
    arr = random.choices(list(range(wealth)), k=size) # Random wealth for each individual
    return arr

# Pick two individual randomly
def interaction(size):
    return random.choices(list(range(size)), k=2)

def transaction(a, b):
    pot = a + b
    split = random.choice(list(range(1, pot))) # Split randomly the pot in two
    #split = 0                                 # One takes all
    return split, pot - split

# Computation of Gini parameter
def gini(arr):
    arr.sort()
    n = float(len(arr))
    return 2.0*sum([(i+1)*w for i, w in enumerate(arr)]) / (n*sum(arr)) - (n+1)/n


POP = 1000   # Number of individuals
WEALTH = 100 # Initial wealth of the population
ITER = 10000 # Number of transaction before the simulmation ends

population = initialization(POP, WEALTH) # Initialize population's wealth
print(population)
print(gini(population)) # Initial Gini
for _ in range(ITER):
    ind1, ind2 = interaction(POP) # Buyer meets sellers
    population[ind1], population[ind2] = transaction(population[ind1], population[ind2]) # They exchange money
print(gini(population)) # Final Gini

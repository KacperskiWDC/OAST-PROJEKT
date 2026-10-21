from typing                     import List, Dict

from graph.demand               import Demand
from graph.DemandPathLink       import DemandPath
from graph.link                 import Links

from solution.individual        import Individual, generateIndividual

from algorithm.ParamsImporter   import ParamsImporter

def solver(
    algParams:          ParamsImporter,
    links:              Links,
    demands:            Dict[int, Demand],
    demandPathLink:     Dict
) -> Individual:

    population_size = algParams.getPopulationSize()
    epochs          = algParams.getEpochsNum()
    q               = algParams.getMutationProbabilty()
    p               = algParams.getCrossoverProbabilty()

    P = []
    for _ in range(population_size):
        P.append(generateIndividual(demands=demands))

    
    
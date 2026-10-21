import random
import numpy                    as np
from   copy                     import deepcopy

from collections                import defaultdict
from typing                     import List, Dict

from graph.demand               import Demand
from graph.DemandPathLink       import DemandPath
from graph.link                 import Links

from solution.individual        import Individual, generateIndividual

from algorithm.ParamsImporter   import ParamsImporter


def _evaluate(
    individual: Individual,
    demandPathLink: Dict
) -> int:

    gens = individual.getSolutions()

    link_loads = defaultdict(int)

    for demand_id, chromosome in gens.items():

        for path_id, flow in enumerate(chromosome, start=1):

            demandPath = demandPathLink[demand_id][path_id]

            for link_id in demandPath.links:

                link_loads[link_id] += flow

    if not link_loads:
        return 0

    return max(link_loads.values())

def _tournament(
    scores:  int,
    k:       int=3
) -> int:

    contestants = random.sample(scores, k)

    contestants.sort(
        key=lambda x: x[0]
    )

    return contestants[0][1]

def _crossover(
    parent1: Individual,
    parent2: Individual
):

    g1 = parent1.getSolutions()
    g2 = parent2.getSolutions()

    child1 = {}
    child2 = {}

    for demand_id in g1:

        if random.random() < 0.5:

            child1[demand_id] = deepcopy(g1[demand_id])
            child2[demand_id] = deepcopy(g2[demand_id])

        else:

            child1[demand_id] = deepcopy(g2[demand_id])
            child2[demand_id] = deepcopy(g1[demand_id])

    return (
        Individual(child1),
        Individual(child2)
    )

def _generateChromosome(demand: Demand) -> list[int]:

    chromosome = [0] * demand.maxPaths

    for _ in range(demand.volume):
        path = random.randint(0, demand.maxPaths - 1)
        chromosome[path] += 1

    return chromosome

def _mutate(
    individual: Individual,
    demands:    Dict[int, Demand]
):

    genes = individual.getSolutions()

    demand_id = random.choice(
        list(genes.keys())
    )

    demand = demands[demand_id-1]
    genes[demand_id] = _generateChromosome(
        demand
    )

def solver(
    algParams:          ParamsImporter,
    links:              Links,
    demands:            Dict[int, Demand],
    demandPathLink:     Dict
) -> Individual:

    population_size = algParams.getPopulationSize()
    epochs          = algParams.getEpochsNum()
    crossovers      = algParams.getCrossovers()  
    q               = algParams.getMutationProbabilty()
    p               = algParams.getCrossoverProbabilty()

    P = []
    for _ in range(population_size):
        individual = generateIndividual(demands=demands) 
        P.append(individual)

    best = None
    best_score = np.inf
    for epoch_num in range(epochs):

        O = []

        for _ in range(crossovers):

            parent1 = random.choice(P)
            parent2 = random.choice(P)

            child1, child2 = _crossover(
                parent1,
                parent2
            )

            O.append(child1)
            O.append(child2)

        for individual in O:

            if random.random() < q:
                _mutate(
                    individual,
                    demands
                )

        candidates = []

        for individual in P + O:

            score = _evaluate(
                individual,
                demandPathLink
            )

            candidates.append(
                (score, individual)
            )

            if score < best_score:
                best_score = score
                best = individual

        candidates.sort(
            key=lambda x: x[0]
        )

        P = [
            individual
            for _, individual
            in candidates[:population_size]
        ]

        print(
            f"{epoch_num}: {best_score}"
        )


    return best

    
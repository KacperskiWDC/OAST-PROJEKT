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
        individual = generateIndividual(demands=demands) 
        P.append(individual)
        print(
            _evaluate(individual=individual, demandPathLink=demandPathLink)
        )

    
import  random

from    typing          import List, Dict

from    graph.demand    import Demand

class Individual:

    def __init__(
        self,
        solutions: Dict[int, List[int]]  #int jako klucz
    ) -> None:
        self._solutions = solutions

    def getSolutions(
        self
    ) -> Dict[int, List[int]]:           # słownik byla lista
        return self._solutions
def _generateChromosome(
    demand: Demand
) -> list[int]:

    volume = demand.volume
    maxPaths = demand.maxPaths

    chromosome = [0] * maxPaths

    for _ in range(volume):
        chromosome[random.randint(0, maxPaths - 1)] += 1

    return chromosome

def generateIndividual(
    demands: Dict[int, Demand]={}
) -> Individual:

    solution = {}
    for i, demand in demands.items():
        chromosome = _generateChromosome(demand)
        solution[demand.id] = chromosome

    return Individual(solution)
    
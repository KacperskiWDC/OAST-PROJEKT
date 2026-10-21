import random
import math
import numpy as np
from copy import deepcopy
from collections import defaultdict
from typing import List, Dict

from graph.demand import Demand
from graph.DemandPathLink import DemandPath
from graph.link import Links

from solution.individual import Individual, generateIndividual
from algorithm.ParamsImporter import ParamsImporter


def _evaluate(
        individual: Individual,
        demandPathLink: Dict,
        links: Links,
        problem_type: str
) -> int:
    gens = individual.getSolutions()
    link_loads = defaultdict(int)

    # 1. Obliczanie całkowitego ruchu na każdym łączu
    for demand_id, chromosome in gens.items():
        for path_id, flow in enumerate(chromosome, start=1):
            if flow > 0:  # tylko gdy ruch
                demandPath = demandPathLink[demand_id][path_id]
                for link_id in demandPath.links:
                    link_loads[link_id] += flow

    # 2. Obliczanie funkcji celu
    if problem_type == "DAP":
        max_overload = -float('inf')
        for link_id, link_obj in links.getLink().items():
            # W DAP link_obj.value to liczba modułów (moduleCount)
            capacity = link_obj.value * links.moduleCapacity
            overload = link_loads[link_id] - capacity
            if overload > max_overload:
                max_overload = overload
        return max_overload

    elif problem_type == "DDAP":
        total_cost = 0
        for link_id, link_obj in links.getLink().items():
            # W DDAP link_obj.value to koszt jednego modułu (moduleCost)
            modules_needed = math.ceil(link_loads[link_id] / links.moduleCapacity)
            total_cost += modules_needed * link_obj.value
        return total_cost

    return 0


def _tournament(
        scores: list,
        k: int = 3
):
    contestants = random.sample(scores, k)
    contestants.sort(key=lambda x: x[0])
    return contestants[0][1]


def _crossover(
        parent1: Individual,
        parent2: Individual
):
    g1 = parent1.getSolutions()
    g2 = parent2.getSolutions()

    child1_genes = {}
    child2_genes = {}

    for demand_id in g1:
        if random.random() < 0.5:
            child1_genes[demand_id] = deepcopy(g1[demand_id])
            child2_genes[demand_id] = deepcopy(g2[demand_id])
        else:
            child1_genes[demand_id] = deepcopy(g2[demand_id])
            child2_genes[demand_id] = deepcopy(g1[demand_id])

    return Individual(child1_genes), Individual(child2_genes)


def _mutate(
        individual: Individual,
        demands: Dict[int, Demand]
):
    genes = individual.getSolutions()

    # 1. Losowanie mutacji
    demand_id = random.choice(list(genes.keys()))
    chromosome = genes[demand_id]

    # 2. Ścieżki z ruchem
    active_paths = [i for i, flow in enumerate(chromosome) if flow > 0]

    if not active_paths:
        return

    # 3. Losujemy ścieżke z której zabieramy ruch
    path_from = random.choice(active_paths)

    # 4. Losujemy ścieżkę do której dodajemy ruch
    max_paths = len(chromosome)
    available_targets = [i for i in range(max_paths) if i != path_from]

    if not available_targets:
        return

    path_to = random.choice(available_targets)

    # 5. mutant
    chromosome[path_from] -= 1
    chromosome[path_to] += 1


def solver(
        algParams: ParamsImporter,
        links: Links,
        demands: Dict[int, Demand],
        demandPathLink: Dict,
        problemType: str
) -> Individual:
    population_size = algParams.getPopulationSize()
    epochs = algParams.getEpochsNum()
    crossovers = algParams.getCrossovers()
    q = algParams.getMutationProbabilty()
    p = algParams.getCrossoverProbabilty()


    P = []
    for _ in range(population_size):
        individual = generateIndividual(demands=demands)
        P.append(individual)

    best = None
    best_score = float('inf')

    for epoch_num in range(epochs):
        O = []

        # krzyżowanie
        for _ in range(crossovers):
            parent1 = random.choice(P)
            parent2 = random.choice(P)

            # krzyżowanie odbywa się z prawdopodobieństwem p
            if random.random() < p:
                child1, child2 = _crossover(parent1, parent2)
                O.append(child1)
                O.append(child2)

        # mutacja na potomkach
        for individual in O:
            if random.random() < q:
                _mutate(individual, demands)

        candidates = []

        # Ocena całej puli
        for individual in P + O:
            score = _evaluate(
                individual,
                demandPathLink,
                links,
                problemType
            )

            candidates.append((score, individual))

            if score < best_score:
                best_score = score
                best = individual

        # Selekcja najlepszych N osobników
        candidates.sort(key=lambda x: x[0])

        P = [
            individual
            for _, individual
            in candidates[:population_size]
        ]

        if epoch_num % 10 == 0:
            print(f"Epoka {epoch_num:4d} | Najlepszy wynik ({problemType}): {best_score}")

    print(f"\n--- KONIEC ---")
    print(f"Ostateczny najlepszy wynik: {best_score}")

    return best
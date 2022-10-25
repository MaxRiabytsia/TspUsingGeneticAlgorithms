from __future__ import annotations

import numpy as np
import math

from Path import Path
from City import City


class Population:
    def __init__(self, individuals: np.array):
        self.parents = individuals
        self.size = len(self.parents)
        self.best_path = min(self.parents, key=lambda path: path.length)
        self.offsprings = None

    @staticmethod
    def random(cities: list[City], size: int):
        population = Population(individuals=[Path(np.random.permutation(cities)) for i in range(size)])
        return population

    def get_next_generation(self, selection_rate: float, crossover_rate: float, mutation_rate: float) -> Population:
        self.__elitism_selection(selection_rate)
        self.__crossover(crossover_rate)
        self.__exchange_based_mutation(mutation_rate)
        next_generation = Population(individuals=self.offsprings)
        return next_generation

    def __probability_based_selection(self, selection_rate: float) -> None:
        paths_length = np.array([path.length for path in self.parents])
        paths_scores = 1 / (paths_length - np.min(paths_length) + 1)
        paths_selection_probabilties = paths_scores / np.sum(paths_scores)
        self.parents = np.random.choice(self.parents, p=paths_selection_probabilties,
                                        size=math.ceil(len(self.parents) * selection_rate), replace=False)

    def __elitism_selection(self, selection_rate: float) -> None:
        self.parents = sorted([path for path in self.parents], key=lambda path: path.length)
        self.parents = self.parents[:math.ceil(len(self.parents) * selection_rate)]

    def __tournament_selection(self, selection_rate: float) -> None:
        selected_parents = []
        for i in range(math.ceil(len(self.parents) * selection_rate)):
            parent1, parent2 = np.random.choice(self.parents, 2, replace=False)
            selected_parents.append(parent1 if parent1.length < parent2.length else parent2)
        self.parents = selected_parents

    def __crossover(self, crossover_rate: float) -> None:
        self.offsprings = [*self.parents]
        loop_number = 1
        i, j = 0, loop_number
        while len(self.offsprings) != self.size:
            if j >= len(self.parents):
                loop_number += 1
                if loop_number == j:
                    loop_number = 1
                i, j = 0, loop_number
            child1 = self.__segment_crossover(self.parents[i], self.parents[j], crossover_rate)
            child2 = self.__segment_crossover(self.parents[j], self.parents[i], crossover_rate)
            self.offsprings.append(child1)
            if len(self.offsprings) != self.size:
                self.offsprings.append(child2)
            i += 1
            j += 1

    @staticmethod
    def __segment_crossover(parent1: Path, parent2: Path, crossover_rate: float) -> Path:
        number_of_genes_to_swap = int(len(parent1.ordered_cities) * crossover_rate)
        start_index = np.random.randint(0, len(parent1.ordered_cities) - number_of_genes_to_swap)
        end_index = start_index + number_of_genes_to_swap
        child = Path(np.concatenate(([None] * start_index, parent1.ordered_cities[start_index:end_index],
                                     [None] * (len(parent1.ordered_cities) - end_index))))

        count = 0
        for city in parent2.ordered_cities:
            if city not in child.ordered_cities:
                while child.ordered_cities[count] is not None:
                    count += 1
                child.ordered_cities[count] = city

        return child

    @staticmethod
    def __position_based_crossover(parent1: Path, parent2: Path, crossover_rate: float) -> Path:
        number_of_genes_to_swap = math.ceil(len(parent1.ordered_cities) * crossover_rate)
        child = Path([None] * len(parent1.ordered_cities))
        genes_indeces_from_parent1 = np.random.choice(range(len(parent1.ordered_cities)),
                                                      number_of_genes_to_swap, replace=False)
        for i in genes_indeces_from_parent1:
            child.ordered_cities[i] = parent1.ordered_cities[i]

        count = 0
        for city in parent2.ordered_cities:
            if city not in child.ordered_cities:
                while child.ordered_cities[count] is not None:
                    count += 1
                child.ordered_cities[count] = city

        return child

    def __exchange_based_mutation(self, mutation_rate: float) -> None:
        for path in self.offsprings:
            for i in range(len(path.ordered_cities)):
                if np.random.uniform() < mutation_rate:
                    j = np.random.randint(0, len(path.ordered_cities))
                    path.ordered_cities[i], path.ordered_cities[j] = (
                        path.ordered_cities[j],
                        path.ordered_cities[i]
                    )
            path.recalculate_length()

    def __insert_based_mutation(self, mutation_rate: float) -> None:
        for path in self.offsprings:
            for i in range(len(path.ordered_cities)):
                if np.random.uniform() < mutation_rate:
                    j = np.random.randint(0, len(path.ordered_cities))
                    np.insert(path.ordered_cities, j, path.ordered_cities[i])
            path.recalculate_length()

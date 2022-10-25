import copy
import matplotlib.pyplot as plt

from MapOfCities import MapOfCities
from Population import Population


number_of_cities = 50
population_size = 1000
number_of_generations = 100
selection_rate = 0.1
crossover_rate = 0.3
mutation_rate = 0.05

map_of_cities = MapOfCities(number_of_cities)


def get_parameters_from_user():
    global number_of_cities, population_size, number_of_generations, selection_rate, crossover_rate, mutation_rate
    number_of_cities = int(input("Enter number of cities: "))
    population_size = int(input("Enter population size: "))
    number_of_generations = int(input("Enter number of generations: "))
    selection_rate = float(input("Enter selection rate: "))
    crossover_rate = float(input("Enter crossover rate: "))
    mutation_rate = float(input("Enter mutation rate: "))


def generate_map_of_cities():
    global map_of_cities
    map_of_cities = MapOfCities(number_of_cities)
    print(f"New map for {number_of_cities} cities was successfully generated.")


def show_map_of_cities():
    plt.ion()
    fig = plt.figure()
    map_of_cities.show(fig)

    return fig


def find_optimal_path():
    fig = show_map_of_cities()

    population = Population.random(cities=map_of_cities.cities, size=population_size)
    current_best_path, first_best_generation = population.best_path, 1
    current_best_path.show(fig)

    for generation in range(number_of_generations):
        print(f"======================= Generation {generation + 1} =======================\n"
              f"The best length: {round(population.best_path.length, 2)}\n")
        if population.best_path.length < current_best_path.length:
            current_best_path, first_best_generation = copy.deepcopy(population.best_path), generation
            current_best_path.show(fig)
        population = population.get_next_generation(selection_rate, crossover_rate, mutation_rate)

    current_best_path.show(fig, is_last_gen=True)
    print(f"======================= Result =======================\n"
          f"The best length: {round(current_best_path.length, 2)}\n"
          f"The generation when the length was achieved: {first_best_generation}\n")


def main():
    print("Рябиця Максим Андрійович\n"
          "ІПЗ-21\n")

    get_parameters_from_user()
    global map_of_cities
    map_of_cities = MapOfCities(number_of_cities)

    while True:
        print("\n1. Change parameters\n"
              "2. Generate map of cities\n"
              "3. Show map of citites\n"
              "4. Find optimal path\n"
              "0. Exit\n")

        task_number = int(input("Enter task number: "))
        match task_number:
            case 1:
                get_parameters_from_user()
            case 2:
                generate_map_of_cities()
            case 3:
                plt.close()
                show_map_of_cities()
            case 4:
                plt.close()
                find_optimal_path()
            case 0:
                break


if __name__ == "__main__":
    main()

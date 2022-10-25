import matplotlib.pyplot as plt
import numpy as np

from City import City


class MapOfCities:
    def __init__(self, number_of_cities: int, seed=None):
        self.number_of_cities = number_of_cities
        self.seed = seed
        self.cities = []
        self.__generate_cities_coords()

    def __generate_cities_coords(self) -> None:
        np.random.seed(self.seed)
        for i in range(self.number_of_cities):
            city = City(*np.random.randint(0, 10000, 2))
            self.cities.append(city)
        np.random.seed(None)

    def show(self, fig: plt.figure) -> None:
        for city in self.cities:
            plt.plot(city.x, city.y, color="black", marker="o")
        plt.title(f"Map of {self.number_of_cities} cities")
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.cla()

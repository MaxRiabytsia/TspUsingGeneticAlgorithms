import matplotlib.pyplot as plt
import numpy as np


class Path:
    def __init__(self, ordered_cities: np.array):
        self.ordered_cities = ordered_cities
        self.__length = 0

    def __repr__(self) -> str:
        return f"Path with length {self.length}"

    @property
    def length(self) -> float:
        if self.__length != 0:
            return self.__length

        self.recalculate_length()
        return self.__length

    def recalculate_length(self):
        for i, city in enumerate(self.ordered_cities[:-1]):
            next_city = self.ordered_cities[i+1]
            self.__length += city.distance_to(next_city)
        self.__length += self.ordered_cities[-1].distance_to(self.ordered_cities[0])

    def show(self, fig: plt.figure, is_last_gen: bool = False) -> None:
        if not is_last_gen:
            plt.cla()
        for i, city in enumerate(self.ordered_cities[:-1]):
            next_city = self.ordered_cities[i + 1]
            plt.plot((city.x, next_city.x), (city.y, next_city.y), 'o-', color='black')

        start_city = self.ordered_cities[0]
        last_city = self.ordered_cities[-1]
        plt.plot((start_city.x, last_city.x), (start_city.y, last_city.y), 'o-', color='black')
        plt.title(f"Path with length {round(self.length, 2)}")

        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.show(block=is_last_gen)

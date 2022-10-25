from __future__ import annotations

import numpy as np


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"City at position [{self.x, self.y}]"

    def __eq__(self, other: City) -> bool:
        return isinstance(other, City) and self.x == other.x and self.y == other.y

    def distance_to(self, other: City) -> float:
        return np.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

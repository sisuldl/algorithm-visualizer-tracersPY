import abc
import random
import string
from typing import List, NoReturn, Sequence, Union

_Number = Union[float, int]


class Randomizer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self) -> NoReturn:
        raise NotImplementedError


class Integer(Randomizer):
    def __init__(self, min: int = 1, max: int = 9):
        self._min = min
        self._max = max

    def create(self) -> int:
        return random.randint(self._min, self._max)


class Double(Randomizer):
    def __init__(self, min: _Number = 0, max: _Number = 1):
        self._min = min
        self._max = max

    def create(self) -> float:
        return random.uniform(self._min, self._max)


class String(Randomizer):
    def __init__(self, length: int = 16, letters: Sequence[str] = string.ascii_lowercase):
        self._length = length
        self._letters = letters

    def create(self) -> str:
        text = random.choices(self._letters, k=self._length)
        return "".join(text)


class Array1D(Randomizer):
    def __init__(self, N: int = 10, randomizer: Randomizer = Integer()):
        self._N = N
        self._randomizer = randomizer
        self._sorted = False

    def sorted(self, sorted: bool = True) -> "Array1D":
        self._sorted = sorted
        return self

    def create(self) -> List:
        array = [self._randomizer.create() for _ in range(self._N)]
        if self._sorted:
            array.sort()

        return array


class Array2D(Array1D):
    def __init__(self, N: int = 10, M: int = 10, randomizer: Randomizer = Integer()):
        super().__init__(N, randomizer)
        self._M = M

    def sorted(self, sorted: bool = True) -> "Array2D":
        self._sorted = sorted
        return self

    def create(self) -> List[List]:
        return [super().create() for _ in range(self._N)]


class Graph(Randomizer):
    def __init__(self, N: int = 5, ratio: _Number = 0.3, randomizer: Randomizer = Integer()):
        self._N = N
        self._ratio = ratio
        self._randomizer = randomizer
        self._directed = True
        self._weighted = False

    def directed(self, directed: bool = True) -> "Graph":
        self._directed = directed
        return self

    def weighted(self, weighted: bool = True) -> "Graph":
        self._weighted = weighted
        return self

    def create(self) -> List[List]:
        graph = [[None] * self._N for _ in range(self._N)]
        for i in range(self._N):
            for j in range(self._N):
                if i == j:
                    graph[i][j] = 0
                elif self._directed or i < j:
                    if random.random() >= self._ratio:
                        graph[i][j] = 0
                    elif self._weighted:
                        graph[i][j] = self._randomizer.create()
                    else:
                        graph[i][j] = 1
                else:
                    graph[i][j] = graph[j][i]

        return graph
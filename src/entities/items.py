import random
from typing import Tuple, List

class Items:
    def __init__(self, pacgums: int, matrix: List[List[int]]) -> None:
        self.p_quant = pacgums
        self.matrix = matrix
        self._height = len(self.matrix)
        self._width = len(self.matrix[0])
        self.super_pacgums: List[Tuple[int, int]] = []
        self.pacgums: List[Tuple[int, int]] = []
        self._start_items()

    def _start_items(self) -> None:
        self._create_supergum()
        self._create_gums()

    def _create_supergum(self) -> None:
        coord = [
                (0, 0),
                (0, self._width - 1),
                (self._height - 1, 0),
                (self._height - 1, self._width - 1)
                ]
        for x in coord:
            self.super_pacgums.append(x)

    def _create_gums(self) -> None:
        pos_avaliable: List[Tuple[int, int]] = []
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                if self.matrix[x][y] < 15:
                    if not (x, y) in self.super_pacgums:
                        pos_avaliable.append((x, y))
        random.shuffle(pos_avaliable)
        for x in pos_avaliable:
            if len(self.pacgums) < self.p_quant:
                self.pacgums.append(x)
            else:
                break

    def apply_to_matrix(self
            ) -> List[List[int]]:
        for x, y in self.super_pacgums:
            self.matrix[x][y] += 32
        for x, y in self.pacgums:
            self.matrix[x][y] += 16
        return self.matrix

    def pos_start(self) -> Tuple(int, int):
        pass

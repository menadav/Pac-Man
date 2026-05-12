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
        self.respawn = self.pos_start()
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
                        if not (x, y) == self.respawn:
                            pos_avaliable.append(((x, y), self.matrix[x][y]))
        pos_avaliable.sort(key=lambda x: x[1])
        for x in pos_avaliable:
            if len(self.pacgums) < self.p_quant:
                self.pacgums.append(x[0])
            else:
                break

    def apply_to_matrix(self
            ) -> List[List[int]]:
        for x, y in self.super_pacgums:
            self.matrix[x][y] += 32
        for x, y in self.pacgums:
            self.matrix[x][y] += 16
        return self.matrix

    def pos_start(self) -> Tuple[int, int]:
        center_y = self._height // 2
        center_x = self._width // 2
        if self.matrix[center_y][center_x] < 15:
            return (center_y, center_x)
        pos = [
                (-1, 0),
                (1, 0),
                (0, 1),
                (0, -1)
            ]
        max_radius = max(self._height, self._width)
        for r in range(1, max_radius):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if abs(dx) == r or abs(dy) == r:
                        ny, nx = center_y + dy, center_x + dx
                        if 0 <= ny < self._height and 0 <= nx < self._width:
                            if self.matrix[ny][nx] < 15:
                                return (nx, ny)

        raise ValueError("[Error] No se encontró un pasillo válido en el mapa")

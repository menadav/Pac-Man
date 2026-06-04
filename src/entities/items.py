from typing import List, Tuple


class Items:
    """Manages the spawning, storage, placement, and matrix allocation of game collection items."""

    def __init__(self, pacgums: int, matrix: List[List[int]]) -> None:
        """Initialize dimensions, high score targets, item collections, and calculation vectors."""
        self.p_quant = pacgums
        self.matrix = matrix
        self._height = len(self.matrix)
        self._width = len(self.matrix[0])
        self.super_pacgums: List[Tuple[int, int]] = []
        self.pacgums: List[Tuple[int, int]] = []
        self.respawn = self.pos_start()
        self._start_items()

    def _start_items(self) -> None:
        """Execute automated collection generation processes for supergums and standard pacgums."""
        self._create_supergum()
        self._create_gums()

    def _create_supergum(self) -> None:
        """Anchor special super-pacgums directly onto the extreme four outer boundary corners."""
        coord = [
            (0, 0),
            (0, self._width - 1),
            (self._height - 1, 0),
            (self._height - 1, self._width - 1),
        ]
        for y, x in coord:
            self.super_pacgums.append((y, x))

    def _create_gums(self) -> None:
        """Populate remaining safe open grid corridors with sorted, capped standard pacgum items."""
        pos_avaliable: List[Tuple[Tuple[int, int], int]] = []
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[0])):
                if self.matrix[y][x] < 15:
                    if (y, x) not in self.super_pacgums:
                        if (y, x) != self.respawn:
                            pos_avaliable.append(((y, x), self.matrix[y][x]))
        if self.p_quant <= 0:
            cap = len(pos_avaliable)
        else:
            cap = min(self.p_quant, len(pos_avaliable))
        pos_avaliable.sort(key=lambda item: item[1])
        for entry in pos_avaliable[:cap]:
            self.pacgums.append(entry[0])

    def apply_to_matrix(self) -> List[List[int]]:
        """Inject item cell identifiers directly into the active level coordinate matrix layout."""
        for y, x in self.super_pacgums:
            self.matrix[y][x] += 32
        for y, x in self.pacgums:
            self.matrix[y][x] += 16
        return self.matrix

    def pos_start(self) -> Tuple[int, int]:
        """Find the closest valid open-space tile starting outwards from the exact maze center."""
        center_y = self._height // 2
        center_x = self._width // 2
        if self.matrix[center_y][center_x] < 15:
            return (center_y, center_x)
        max_radius = max(self._height, self._width)
        for r in range(1, max_radius):
            for i in range(-r, r + 1):
                candidates = [
                    (center_y - r, center_x + i),
                    (center_y + r, center_x + i),
                    (center_y + i, center_x - r),
                    (center_y + i, center_x + r)
                ]
                for ny, nx in candidates:
                    if 0 <= ny < self._height and 0 <= nx < self._width:
                        if self.matrix[ny][nx] < 15:
                            return (ny, nx)
        raise ValueError("[Error]")

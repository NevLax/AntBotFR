import csv
from game.Cell import Cell
from game.Package import Package


class Board:
    def __init__(self, colors, targets) -> None:
        self.cells = list()
        self.load_from_file(colors, targets)
        self.size = len(self.cells)
        self.current_player_index = 0

        self.yellow_cells = self.get_cells_by_color('y')
        self.red_cells = self.get_cells_by_color('r')
        self.green_cells = self.get_cells_by_color('a')
        self.blue_cells = self.get_cells_by_color('b')
        self.white_cells = self.get_cells_by_color('w')
        self.occupied_cells = {}

    def __getitem__(self, index):
        return self.cells[index]

    def get_cells_by_color(self, color):
        return [cell for row_cell in self.cells for cell in row_cell if cell.color == color]

    def load_from_file(self, colors_map, targets_map):
        self.cells = []

        colors_map_file = open(colors_map, mode='r')
        targets_map_file = open(targets_map, mode='r')

        color_matrix = csv.reader(colors_map_file)
        target_matrix = csv.reader(targets_map_file)

        for i, (color_row, target_row) in enumerate(zip(color_matrix, target_matrix)):
            self.cells.append([])
            for j, (color, target) in enumerate(zip(color_row, target_row)):
                self.cells[-1].append(Cell(i, j, color=color, target=int(target)))

        colors_map_file.close()
        targets_map_file.close()

        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if (i - 1) >= 0:
                    self.cells[i][j].front = self.cells[i - 1][j]
                if (i + 1) < len(self.cells[i]):
                    self.cells[i][j].back = self.cells[i + 1][j]
                if (j + 1) < len(self.cells[i]):
                    self.cells[i][j].right = self.cells[i][j + 1]
                if (j - 1) >= 0:
                    self.cells[i][j].left = self.cells[i][j - 1]

    def is_occupied(self, new_pos):
        return new_pos in self.occupied_cells

    def occupied(self, new_pos):
        self.occupied_cells[new_pos] = True

    def update_position(self, old_pos, new_pos):
        if self.is_occupied(old_pos):
            del self.occupied_cells[old_pos]
        self.occupied(new_pos)

    def place_package(self, pos):
        package = Package(pos)
        self.cells[pos[1]][pos[0]].package = package
        return package

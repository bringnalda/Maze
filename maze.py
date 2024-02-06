from cell import Cell
import random
import time

class Maze:
    def __init__(
        self,
        x1, y1,
        num_rows, num_cols,
        cell_size_x, cell_size_y,
        win=None,
        seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._seed = 0
        if seed is not None:
            self._seed = random.seed()

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self): 
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.03)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            visit_list = []

            #check left
            if i > 0 and not self._cells[i - 1][j].visited:
                visit_list.append((i-1, j))
            #check right
            if i + 1 < self._num_cols and self._cells[i + 1][j].visited is not True:
                visit_list.append((i+1, j))
            #check up
            if j > 0 and self._cells[i][j-1].visited is not True:
                visit_list.append((i, j-1))
            #check down
            if j + 1 < self._num_rows and self._cells[i][j+1].visited is not True:
                visit_list.append((i, j+1))
            
            if len(visit_list) == 0:
                self._draw_cell(i, j)
                return

            direction_index = random.randrange(len(visit_list))
            next_index = visit_list[direction_index]

            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, x, y):
        self._animate()
        current_cell = self._cells[x][y]
        current_cell.visited = True

        if x == self._num_cols - 1 and y == self._num_rows - 1:
            return True
        
        #check left
        if x > 0 and not current_cell.has_left_wall and not self._cells[x - 1][y].visited:
            result = self._solve_r(x - 1, y)
            self._cells[x][y].draw_move(self._cells[x - 1][y])
            if result:
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x - 1][y], True)

        #check right
        if x < self._num_cols - 1 and not current_cell.has_right_wall and not self._cells[x + 1][y].visited:
            result = self._solve_r(x + 1, y)
            self._cells[x][y].draw_move(self._cells[x + 1][y])
            if result:
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x + 1][y], True)

        #check top
        if y > 0 and not current_cell.has_top_wall and not self._cells[x][y - 1].visited:
            result = self._solve_r(x, y - 1)
            self._cells[x][y].draw_move(self._cells[x][y - 1])
            if result:
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x][y - 1], True)

        #check bottom
        if y < self._num_rows - 1 and not current_cell.has_bottom_wall and not self._cells[x][y + 1].visited:
            result = self._solve_r(x, y + 1)
            self._cells[x][y].draw_move(self._cells[x][y + 1])
            if result:
                return True
            else:
                self._cells[x][y].draw_move(self._cells[x][y + 1], True)

        return False


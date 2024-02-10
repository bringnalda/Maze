from graphics import Window, Line, Point
from maze import Maze

def main():    
    num_rows = 14
    num_cols = 18
    margin = 50
    screen_x = 1000
    screen_y = 800
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)
    is_solvable = maze.solve()

    if is_solvable:
        print("This maze is solvable!")
    else:
        print("This maze is impossible.")

    win.wait_for_close()


main()

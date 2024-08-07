import random

class Computer:
    def make_move(self, board):
        '''
        Determine and return a random move from the available empty cells.

        This method scans the current state of the board for empty cells (represented by 0)
        and selects one at random. If there are no empty cells, it returns None.


        :param board: The current game board, represented as a 2D list
                                     where 0 indicates an empty cell, 1 indicates a cell
                                     occupied by 'X', and 2 indicates a cell occupied by 'O'.
        :return: tuple: A tuple (row, col) representing the coordinates of the randomly selected
               empty cell, or None if no empty cells are available.
        '''
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    empty_cells.append((row, col))
        if empty_cells:
            return random.choice(empty_cells)
        return None
class Board:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def reset(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def draw(self, drawer):
        '''
        Draws the current state of the board on the screen using the provided drawer.

        :param drawer: An instance of the Draw class responsible for rendering the game board and pieces.

            This function clears the previous drawing, redraws the board, and then draws each piece
        based on the current state of the board. Finally, it updates the screen to reflect the changes.
        '''
        drawer.clear()
        drawer.draw_board()
        for row in range(3):
            for col in range(3):
                self.draw_piece(drawer, row, col, self.board[row][col])
        drawer.screen.update()

    def draw_piece(self, drawer, row, col, piece):
        '''
        Draws a game piece on the board using the specified drawer.

        This function determines which piece to draw based on the value of `piece`:
        - If `piece` is 1, it draws an "X" at the specified row and column.
        - If `piece` is 2, it draws a circle at the specified row and column.
        - If `piece` is 0, no piece is drawn (the cell is empty).

        :param drawer: An instance of the `Draw` class responsible for drawing.
        :param row: The row index (0 to 2) where the piece is to be drawn.
        :param col: The column index (0 to 2) where the piece is to be drawn.
        :param piece: The type of piece to be drawn. 1 for "X", 2 for circle, 0 for empty.
        :return:
        '''
        if piece == 0:
            return
        if piece == 1:
            drawer.draw_x(row, col)
        else:
            drawer.draw_circle(row, col)

    def is_full(self):
        '''
        Checks if the board is full (i.e., there are no empty cells).

        This function iterates through each cell of the board and returns `False`
        if any cell contains 0 (indicating an empty cell). If all cells are occupied,
        it returns `True`.

        :return: bool: `True` if the board is full, `False` otherwise.
        '''
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def is_winner(self, piece):
        '''
        This method checks all possible winning conditions in a Tic Tac Toe game:
        1. Any row being completely occupied by the specified piece.
        2. Any column being completely occupied by the specified piece.
        3. The two diagonals being completely occupied by the specified piece.

        :param piece: The piece to check for a win condition (1 for 'X' and 2 for 'O').
        :return: bool: True if the specified piece has won, False otherwise.
        '''
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == piece:
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == piece:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == piece:
            return True
        if self.board[2][0] == self.board[1][1] == self.board[0][2] == piece:
            return True
        return False
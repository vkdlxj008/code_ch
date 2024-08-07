from turtle import Turtle, Screen
import sys
from tkinter import messagebox as mb
from draw import Draw
from board import Board
from computer import Computer

line = Turtle()
screen = Screen()
turn = ''
screen.setup(600, 800)
screen.title("Tic Tac Toe")
screen.setworldcoordinates(-5, -5, 5, 5)
screen.bgcolor("black")
screen.tracer(0, 0)
line.hideturtle()

drawer = Draw()
drawer.draw_board()

board = Board()
computer = Computer()

def draw():
    """
    Clears the screen and redraws the game board and all pieces.
    """
    board.draw(drawer)

def game_over():
    """
    Checks the current state of the game to determine if it is over and what the result is.

    :return: The result of the game.
            - 1 if player 'X' has won.
            - 2 if player 'O' has won.
            - 3 if the game is a tie (board is full and no winner).
            - 0 if the game is still ongoing.
    """
    if board.is_winner(1):
        return 1
    if board.is_winner(2):
        return 2
    if board.is_full():
        return 3
    return 0

def callback_X():
    """
    Displays a message when the player wins and prompts to play again or exit.
    """
    if mb.askyesno('You win', 'Play again?'):
        reset_game()
    else:
        mb.showinfo('Exit', 'ByeBye.')
        sys.exit(0)

def callback_O():
    """
    Displays a message when the player loses and prompts to play again or exit.
    """
    if mb.askyesno('You lose', 'Play again?'):
        reset_game()
    else:
        mb.showinfo('Exit', 'ByeBye.')
        sys.exit(0)

def callback_tie():
    """
    Displays a message when the game ends in a tie and prompts to play again or exit.
    """
    if mb.askyesno('Tied', 'Play again?'):
        reset_game()
    else:
        mb.showinfo('Exit', 'ByeBye.')
        sys.exit(0)

def reset_game():
    """
    Resets the game board and the turn to the initial state.
    If the computer is set to go first, it makes the first move immediately.
    """
    global turn
    board.reset()
    turn = ask_who_first()
    draw()
    if turn == 'o':
        computer_move()

def ask_who_first():
    """
    Prompts the user to choose who should go first: player or computer.
    Uses a message box to get the user's choice and returns the choice.
    """
    result = mb.askquestion('Who Goes First?', 'Do you want to go first? (Yes/No)')
    if result == 'yes':
        mb.showinfo('First Move', 'Okay. You are first.')
        return 'x'
    elif result == 'no':
        mb.showinfo('First Move', 'Okay. The computer is first.')
        return 'o'

def play(x, y):
    """
    Handles a player's move and updates the game state based on the coordinates provided.

    This function translates the screen coordinates `(x, y)` into board coordinates `(row, col)`.
    It checks if the move is valid (i.e., within bounds and on an empty cell). If valid, it updates
    the board with the player's move, switches turns, and updates the display. If the game is over
    after the move, it triggers the appropriate callback function. If the game is still ongoing, it
    initiates the computer's move.

    :param x: The x-coordinate of the click event on the screen.
    :param y: The y-coordinate of the click event on the screen.
    """
    global turn
    row = 3 - int(y + 5) // 2
    col = int(x + 5) // 2 - 1
    if row > 2 or col > 2 or row < 0 or col < 0 or board.board[row][col] != 0:
        return
    if turn == 'x':
        board.board[row][col] = 1
        turn = 'o'
        draw()
        result = game_over()
        if result == 1:
            callback_X()
            return
        elif result == 2:
            callback_O()
            return
        elif result == 3:
            callback_tie()
            return
        if result == 0:
            computer_move()
    elif turn == 'o':
        pass

def computer_move():
    """
    Executes a move for the computer player and updates the game state.

    This function determines a valid move for the computer using the `computer.make_move()` method.
    If a move is found, it updates the board with the computer's move, switches the turn back to the
    player, and updates the display. It then checks if the game has ended and triggers the appropriate
    callback function based on the game result.

    The function does not take any arguments and relies on global variables for game state management.

    Calls:
        - `computer.make_move()`: Determines the computer's move.
        - `draw()`: Updates the game board display.
        - `game_over()`: Checks the game status after the move.
        - `callback_O()`: Called if the computer wins the game.
        - `callback_tie()`: Called if the game ends in a tie.
    """
    global turn
    move = computer.make_move(board.board)
    if move:
        row, col = move
        board.board[row][col] = 2
        turn = 'x'
        draw()
        result = game_over()
        if result == 2:
            callback_O()
        elif result == 3:
            callback_tie()


reset_game()
screen.onclick(play)
screen.mainloop()
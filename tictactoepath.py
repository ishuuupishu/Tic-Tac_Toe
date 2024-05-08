import tkinter as tk
import tkinter.messagebox
import random

# Function to check if a player has won
def check_win(board, player):
    win_positions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    return [player, player, player] in win_positions

# Function to check if the board is full
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True

# Function to check if the game is over
def game_over(board):
    return check_win(board, "X") or check_win(board, "O") or check_draw(board)

# Function to evaluate the board for the AI
def evaluate(board):
    if check_win(board, "X"):
        return -1
    elif check_win(board, "O"):
        return 1
    else:
        return 0

# Minimax algorithm implementation
def minimax(board, depth, is_maximizing):
    if game_over(board) or depth == 0:
        return evaluate(board)
    
    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    print("Maximizing move at depth", depth, ":", (i, j))
                    eval = minimax(board, depth - 1, False)
                    board[i][j] = ""
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    print("Minimizing move at depth", depth, ":", (i, j))
                    eval = minimax(board, depth - 1, True)
                    board[i][j] = ""
                    min_eval = min(min_eval, eval)
        return min_eval

# Function to make AI move
def ai_move(board, player):
    best_eval = float('-inf') if player == "O" else float('inf')
    best_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = player
                eval = minimax(board, 5, player == "O")
                board[i][j] = ""
                if (player == "O" and eval > best_eval) or (player == "X" and eval < best_eval):
                    best_eval = eval
                    best_moves = [(i, j)]
                elif eval == best_eval:
                    best_moves.append((i, j))
    return random.choice(best_moves)

# Function to handle player's move
def player_move(row, col):
    if board[row][col] == "":
        board[row][col] = "X"
        buttons[row][col].config(text="X", state=tk.DISABLED)
        if game_over(board):
            end_game()
        else:
            ai_row, ai_col = ai_move(board, "O")
            board[ai_row][ai_col] = "O"
            buttons[ai_row][ai_col].config(text="O", state=tk.DISABLED)
            if game_over(board):
                end_game()

# Function to simulate AI vs AI game
def ai_vs_ai():
    while not game_over(board):
        ai_row, ai_col = ai_move(board, "X")
        board[ai_row][ai_col] = "X"
        update_buttons()
        if game_over(board):
            end_game()
            return
        ai_row, ai_col = ai_move(board, "O")
        board[ai_row][ai_col] = "O"
        update_buttons()
        if game_over(board):
            end_game()
            return

# Function to update button states
def update_buttons():
    for i in range(3):
        for j in range(3):
            if board[i][j] != "":
                buttons[i][j].config(text=board[i][j], state=tk.DISABLED)

# Function to start AI vs AI game
def start_ai_vs_ai():
    reset_board()
    ai_vs_ai()

# Function to start AI vs Human game
def start_ai_vs_human():
    reset_board()

# Function to reset the board
def reset_board():
    for i in range(3):
        for j in range(3):
            board[i][j] = ""
            buttons[i][j].config(text="", state=tk.NORMAL)

# Function to end the game and show the result
def end_game():
    if check_win(board, "X"):
        tk.messagebox.showinfo("Game Over", "X Wins!")
    elif check_win(board, "O"):
        tk.messagebox.showinfo("Game Over", "O Wins!")
    else:
        tk.messagebox.showinfo("Game Over", "It's a Draw!")

# Function to restart the game
def restart_game():
    reset_board()

# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(background="black")  # Set background color

# Create the board
board = [["" for _ in range(3)] for _ in range(3)]

# Create buttons for the board
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text="", width=8, height=4, command=lambda row=i, col=j: player_move(row, col),
                                  bg="#CCCCCC", fg="#000000", font=('Helvetica', 16, 'bold'), borderwidth=2)
        buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

# Create buttons for game modes with background and foreground color
ai_vs_ai_button = tk.Button(root, text="AI vs AI", command=start_ai_vs_ai, bg="#C0C0C0", fg="#000000", font=('Helvetica', 12, 'bold'))
ai_vs_ai_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

ai_vs_human_button = tk.Button(root, text="AI vs Human", command=start_ai_vs_human, bg="#C0C0C0", fg="#000000", font=('Helvetica', 12, 'bold'))
ai_vs_human_button.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

# Create restart game button
restart_button = tk.Button(root, text="Restart Game", command=restart_game, bg="#404040", fg="#FFFFFF", font=('Helvetica', 12, 'bold'))
restart_button.grid(row=4, column=1, columnspan=1, padx=5, pady=5)

root.mainloop()


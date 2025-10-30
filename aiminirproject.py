import tkinter as tk
import numpy as np
from tkinter import messagebox


board = np.full((3, 3), ' ')


PLAYER = 'X'
AI = 'O'


def check_winner(b):
    for i in range(3):
        if np.all(b[i, :] == PLAYER) or np.all(b[:, i] == PLAYER):
            return PLAYER
        if np.all(b[i, :] == AI) or np.all(b[:, i] == AI):
            return AI
    if b[0,0] == b[1,1] == b[2,2] != ' ':
        return b[0,0]
    if b[0,2] == b[1,1] == b[2,0] != ' ':
        return b[0,2]
    if ' ' not in b:
        return 'Draw'
    return None


def minimax(b, depth, is_maximizing):
    winner = check_winner(b)
    if winner == AI:
        return 1
    elif winner == PLAYER:
        return -1
    elif winner == 'Draw':
        return 0

    if is_maximizing:
        best = -np.inf
        for i in range(3):
            for j in range(3):
                if b[i, j] == ' ':
                    b[i, j] = AI
                    val = minimax(b, depth + 1, False)
                    b[i, j] = ' '
                    best = max(best, val)
        return best
    else:
        best = np.inf
        for i in range(3):
            for j in range(3):
                if b[i, j] == ' ':
                    b[i, j] = PLAYER
                    val = minimax(b, depth + 1, True)
                    b[i, j] = ' '
                    best = min(best, val)
        return best


def ai_move():
    best_score = -np.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i, j] == ' ':
                board[i, j] = AI
                score = minimax(board, 0, False)
                board[i, j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move] = AI
        buttons[move[0]][move[1]].config(text=AI, state="disabled")
    check_game_status()


def player_move(i, j):
    if board[i, j] == ' ':
        board[i, j] = PLAYER
        buttons[i][j].config(text=PLAYER, state="disabled")
        check_game_status()
        if check_winner(board) is None:
            ai_move()


def check_game_status():
    winner = check_winner(board)
    if winner:
        if winner == 'Draw':
            messagebox.showinfo("Game Over", "It's a Draw!")
        else:
            messagebox.showinfo("Game Over", f"{winner} Wins!")
        reset_board()


def reset_board():
    global board
    board = np.full((3, 3), ' ')
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", state="normal")


root = tk.Tk()
root.title("AI Tic-Tac-Toe Game")

tk.Label(root, text="AI Tic-Tac-Toe (Player vs AI)", font=("Arial", 18, "bold"), fg="blue").grid(row=0, column=0, columnspan=3)

buttons = []
for i in range(3):
    row = []
    for j in range(3):
        b = tk.Button(root, text=" ", font=("Arial", 24, "bold"), width=5, height=2,
                      command=lambda i=i, j=j: player_move(i, j))
        b.grid(row=i+1, column=j, padx=5, pady=5)
        row.append(b)
    buttons.append(row)

tk.Button(root, text="Restart", font=("Arial", 12), bg="lightgreen", command=reset_board).grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()

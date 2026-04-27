import tkinter as tk
from tkinter import messagebox
import math

X = "X" # Máy
O = "O" # Người
EMPTY = ""

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY: return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY: return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY: return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY: return board[0][2]
    return None

def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# AI Alpha-Beta cho GUI
def alphabeta_gui(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == X: return 10 - depth
    if winner == O: return -10 + depth
    if is_full(board): return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = X
                    eval = alphabeta_gui(board, depth + 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha: break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = O
                    eval = alphabeta_gui(board, depth + 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha: break
        return min_eval

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Bài 6: Tic-Tac-Toe AI (Alpha-Beta)")
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # Tạo lưới nút bấm
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text="", font=('consolas', 40, 'bold'), width=5, height=2,
                                               command=lambda r=i, c=j: self.human_move(r, c),
                                               bg="white", activebackground="lightgray")
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

    def human_move(self, r, c):
        if self.board[r][c] == EMPTY:
            # Người đi (Chữ O màu Xanh)
            self.board[r][c] = O
            self.buttons[r][c].config(text=O, fg="blue")
            if not self.check_game_over():
                # AI tính toán đi phản hồi
                self.window.update() 
                self.ai_move()

    def ai_move(self):
        best_val = -math.inf
        move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = X
                    move_val = alphabeta_gui(self.board, 0, -math.inf, math.inf, False)
                    self.board[i][j] = EMPTY
                    if move_val > best_val:
                        best_val = move_val
                        move = (i, j)
                        
        if move != (-1, -1):
            r, c = move
            # Máy đi (Chữ X màu Đỏ)
            self.board[r][c] = X
            self.buttons[r][c].config(text=X, fg="red")
            self.check_game_over()

    def check_game_over(self):
        winner = check_winner(self.board)
        if winner:
            messagebox.showinfo("Kết quả", f"Trò chơi kết thúc! {winner} đã giành chiến thắng.")
            self.reset_game()
            return True
        elif is_full(self.board):
            messagebox.showinfo("Kết quả", "Bàn cờ đầy! Kết quả hòa.")
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=EMPTY, bg="white")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()
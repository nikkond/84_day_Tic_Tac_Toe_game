import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QMessageBox, QGridLayout


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Initialize empty board
        self.current_player = 'X'  # Player X starts the game
        self.score = {'X': 0, 'O': 0, 'Tie': 0}  # Initialize score

    def make_move(self, position):
        if self.board[position] == ' ':  # Check if the position is empty
            self.board[position] = self.current_player
            return True
        return False

    def check_winner(self):
        # Define winning combinations
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]  # Return the winner
        if ' ' not in self.board:  # If the board is full and no winner
            return 'Tie'
        return None

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def ai_move(self):
        # Choose the best move using the minimax algorithm
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '  # Undo the move
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, depth, is_maximizing):
        result = self.check_winner()
        if result == 'O':
            return 10 - depth
        elif result == 'X':
            return depth - 10
        elif result == 'Tie':
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '  # Undo the move
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '  # Undo the move
                    best_score = min(score, best_score)
            return best_score


class TicTacToeUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")

        self.game = TicTacToe()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)

        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = QPushButton(' ', self)
                btn.clicked.connect(lambda state, row=i, col=j: self.make_move(row, col))
                grid_layout.addWidget(btn, i, j)
                self.buttons.append(btn)

        self.score_labels = {
            'X': QLabel('Player X: 0', self),
            'O': QLabel('Player O: 0', self),
            'Tie': QLabel('Ties: 0', self)
        }
        for idx, (player, label) in enumerate(self.score_labels.items()):
            grid_layout.addWidget(label, 3, idx)

        self.update_score_labels()

    def make_move(self, row, col):
        if self.game.make_move(row * 3 + col):
            self.update_board()
            winner = self.game.check_winner()
            if winner:
                self.update_score(winner)
                self.show_result(winner)
                self.reset_board()
            else:
                self.game.switch_player()
                if self.game.current_player == 'O':
                    self.ai_move()

    def ai_move(self):
        position = self.game.ai_move()
        self.make_move(position // 3, position % 3)

    def update_board(self):
        for i, btn in enumerate(self.buttons):
            btn.setText(self.game.board[i])

    def update_score_labels(self):
        for player, label in self.score_labels.items():
            label.setText(f"{player}: {self.game.score[player]}")

    def update_score(self, winner):
        if winner == 'Tie':
            self.game.score['Tie'] += 1
        else:
            self.game.score[winner] += 1
        self.update_score_labels()

    def show_result(self, winner):
        if winner == 'Tie':
            QMessageBox.information(self, "Result", "It's a tie!")
        else:
            QMessageBox.information(self, "Result", f"{winner} wins!")

    def reset_board(self):
        self.game.board = [' ' for _ in range(9)]
        self.update_board()
        self.game.current_player = 'X'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicTacToeUI()
    window.show()
    sys.exit(app.exec())

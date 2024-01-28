# game_board.py
import pygame
from minimax import minimax

class GameBoard:
    # Initialize the game board with the given number of rows and columns.
    def __init__(self, rows, cols):
        # Initialize instance variables.
        self.rows = rows
        self.cols = cols
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.player_score = 0
        self.bot_score = 0
        self.game_started = False
        self.game_over = False
        self.winner_message = ""

    # Draw grid lines on the screen to create the Tic Tac Toe board.
    def draw_grid(self, screen, width, height, line_color):
        # Fill the screen with a background color.
        screen.fill((201, 87, 199))
        # Draw horizontal and vertical lines to create the grid.
        for i in range(1, self.cols):
            pygame.draw.line(screen, line_color, (0, i * height // self.cols), (width, i * height // self.cols), 5)
            pygame.draw.line(screen, line_color, (i * width // self.cols, 0), (i * width // self.cols, height), 5)

    # Draw X and O symbols on the screen based on the current state of the game board.
    def draw_symbols(self, screen, width, height, player_x_color, player_o_color):
        # Iterate through each cell in the game board.
        for row in range(self.rows):
            for col in range(self.cols):
                # Draw X symbol if the cell contains 'X', and O symbol if the cell contains 'O'.
                if self.board[row][col] == 'X':
                    # Draw X symbol.
                    x_pos = col * width // self.cols + width // (2 * self.cols)
                    y_pos = row * height // self.rows + height // (2 * self.rows)
                    pygame.draw.line(screen, player_x_color, (x_pos - 50, y_pos - 50), (x_pos + 50, y_pos + 50), 5)
                    pygame.draw.line(screen, player_x_color, (x_pos + 50, y_pos - 50), (x_pos - 50, y_pos + 50), 5)
                elif self.board[row][col] == 'O':
                    # Draw O symbol.
                    x_pos = col * width // self.cols + width // (2 * self.cols)
                    y_pos = row * height // self.rows + height // (2 * self.rows)
                    pygame.draw.circle(screen, player_o_color, (x_pos, y_pos), 50, 5)

    # Check if a move at the given row and column is valid.
    def is_valid_move(self, row, col):
        return self.board[row][col] is None

    # Make a move for the player at the specified row and column.
    def make_player_move(self, row, col):
        # Check if the move is valid and the game is not over.
        if self.is_valid_move(row, col) and not self.game_over:
            # Make the move and check if the game is over.
            self.board[row][col] = 'X'
            if self.is_game_over():
                self.handle_game_over()

    # Make a move for the computer using the minimax algorithm.
    def make_computer_move(self):
        # Check if the game is not over.
        if not self.game_over:
            best_score = float('-inf')
            best_move = None

            # Iterate over each cell in the game board.
            for i in range(self.rows):
                for j in range(self.cols):
                    # Check if the current cell is empty.
                    if self.board[i][j] is None:
                        # Simulate making a move by 'O' in the empty cell.
                        self.board[i][j] = 'O'
                        # Evaluate the score of the current move using the minimax algorithm.
                        score = minimax(self.board, 0, False)  # 0=> current state, False is not a maximizer
                        # Reset the cell to its original state.
                        self.board[i][j] = None

                        # Update the best move if the current move has a higher score.
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)

            # Make the best move for the computer and check if the game is over.
            if best_move:
                self.board[best_move[0]][best_move[1]] = 'O'
                if self.is_game_over():
                    self.handle_game_over()

    # Handle the end of the game, determine the winner, and update scores.
    def handle_game_over(self):
        # Check the winner and update scores accordingly.
        winner = self.check_winner()
        if winner:
            if winner == 'X':
                self.player_score += 1
                self.winner_message = "Player wins!"
            elif winner == 'O':
                self.bot_score += 1
                self.winner_message = "Bot wins!"
            else:
                self.winner_message = "It's a tie!"
        else:
            self.winner_message = "It's a tie!"

        # Set the game over flag to True.
        self.game_over = True

    # Check for a winner by examining rows, columns, and diagonals.
    def check_winner(self):
        # Check each row for a winning combination.
        for i in range(self.rows):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return self.board[i][0]
            # Check each column for a winning combination.
            if self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return self.board[0][i]

        # Check main diagonal for a winning combination.
        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None:
            return self.board[0][0]
        # Check other diagonal for a winning combination.
        if self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return self.board[0][2]
        # If no winning combination is found in rows, columns, or diagonals, return None.

        return None

    # Check if the game is over by examining rows, columns, and diagonals.
    def is_game_over(self):
        for i in range(self.rows):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None or \
                    self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                # If a winning combination or a complete row is found, the game is over.
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None or \
                self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:

            # If a winning combination is found in either diagonal, the game is over.
            return True

        if all(self.board[i][j] is not None for i in range(self.rows) for j in range(self.cols)):
            # If all cells are filled, the game is over.
            return True

        return False

    # Draw the label indicating the winner or tie on the screen.
    def draw_winner_label(self, screen, font):
        winner_text = font.render(self.winner_message, True, (255, 255, 255))
        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2, screen.get_height() // 3))

    # Draw a button for starting a new match on the screen.
    def draw_new_match_button(self, screen, font):
        pygame.draw.rect(screen, (148, 185, 255),
                         (screen.get_width() // 2 - 75, screen.get_height() // 2 - 25, 150, 50))
        new_match_text = font.render("New Match", True, (255, 255, 255))
        screen.blit(new_match_text, (screen.get_width() // 2 - new_match_text.get_width() // 2,
                                     screen.get_height() // 2 - new_match_text.get_height() // 2))

    # Draw a button for returning to the home screen on the screen.
    def draw_home_button(self, screen, font):
        pygame.draw.rect(screen, (148, 185, 255),
                         (screen.get_width() // 2 - 50, screen.get_height() // 2 + 50, 100, 50))
        home_text = font.render("Home", True, (255, 255, 255))
        screen.blit(home_text, (screen.get_width() // 2 - home_text.get_width() // 2,
                                screen.get_height() // 2 + 50 + home_text.get_height() // 2))

    # Draw the start screen with the "Start" button on the screen.
    def draw_start_screen(self, screen, big_font, font):
        # Fill the screen with a background color.
        screen.fill((148, 185, 255))
        # Draw the title text on the screen.
        start_text = big_font.render("Have Fun with TicTacToe!!", True, (255, 255, 255))
        screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, screen.get_height() // 3))
        # Draw the "Start" button on the screen.
        pygame.draw.rect(screen, (148, 185, 255),
                         (screen.get_width() // 2 - 50, screen.get_height() // 2 - 25, 100, 50))
        start_text = font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, (
            screen.get_width() // 2 - start_text.get_width() // 2,
            screen.get_height() // 2 - start_text.get_height() // 2))

    # Update scores based on the winner of the current match.
    def update_scores(self, winner):
        if winner == 'X':
            self.player_score += 1
        elif winner == 'O':
            self.bot_score += 1

    # Reset player and bot scores to zero.
    def reset_scores(self):
        self.player_score = 0
        self.bot_score = 0

    # Draw the scores of the player and bot on the screen.
    def draw_scores(self, screen, font):
        player_text = font.render(f'Player: {self.player_score}', True, (239, 203, 88))
        bot_text = font.render(f'Bot: {self.bot_score}', True, (239, 203, 88))
        screen.blit(player_text, (screen.get_width() - player_text.get_width() - 10, 10))
        screen.blit(bot_text, (10, 10))

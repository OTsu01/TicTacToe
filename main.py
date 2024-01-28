# main.py
import sys
import pygame
from game_board import GameBoard
from minimax import minimax

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 3, 3
BACKGROUND_COLOR = (201, 87, 199)
LINE_COLOR = (239, 203, 88)
PLAYER_X_COLOR = (148, 185, 255)
PLAYER_O_COLOR = (205, 255, 216)
HOME_SCREEN_COLOR = (148, 185, 255)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Create the game board
game_board = GameBoard(ROWS, COLS)

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Set up fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
              # Check if the game started and if the clicked pos is 50px from left of horizon screen  and
            if not game_board.game_started and WIDTH // 2 - 50 <= event.pos[0] <= WIDTH // 2 + 50 and \
               HEIGHT // 2 - 25 <= event.pos[1] <= HEIGHT // 2 + 25:
                # Start button clicked
                game_board.game_started = True
                game_board.game_over = False
                game_board.winner_message = ""
                game_board.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
            elif game_board.game_over and WIDTH // 2 - 75 <= event.pos[0] <= WIDTH // 2 + 75 and \
                 HEIGHT // 2 - 25 <= event.pos[1] <= HEIGHT // 2 + 25:
                # New Match button clicked
                game_board.game_over = False
                game_board.winner_message = ""
                game_board.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
            elif game_board.game_over and WIDTH // 2 - 50 <= event.pos[0] <= WIDTH // 2 + 50 and \
                 HEIGHT // 2 + 50 <= event.pos[1] <= HEIGHT // 2 + 100:
                # Home button clicked
                game_board.game_started = False
                game_board.game_over = False
                game_board.winner_message = ""
                game_board.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

            elif game_board.game_started and event.button == 1:
                # Player's turn
                mouseX, mouseY = event.pos
                clicked_row = mouseY // (HEIGHT // 3)  # output will be row index
                clicked_col = mouseX // (WIDTH // 3)   # output will be col index

                if game_board.is_valid_move(clicked_row, clicked_col) and not game_board.is_game_over():
                    game_board.make_player_move(clicked_row, clicked_col)

                    # Computer's turn
                    game_board.make_computer_move()

                    if game_board.is_game_over():
                        game_board.game_over = True

    # Draw the game board and buttons
    if game_board.game_started:
        game_board.draw_grid(screen, WIDTH, HEIGHT, LINE_COLOR)
        game_board.draw_symbols(screen, WIDTH, HEIGHT, PLAYER_X_COLOR, PLAYER_O_COLOR)
    else:
        game_board.draw_start_screen(screen, big_font, font)

    if game_board.game_over:
        game_board.draw_winner_label(screen, font)
        game_board.draw_new_match_button(screen, font)
        game_board.draw_home_button(screen, font)

    # Draw scores during the game
    game_board.draw_scores(screen, font)

    # Update the display
    pygame.display.flip()

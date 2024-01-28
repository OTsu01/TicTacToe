# Check if the game is over by examining rows, columns, and diagonals.
def is_game_over(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] is not None or \
           board[0][i] == board[1][i] == board[2][i] is not None:
            return True

    if board[0][0] == board[1][1] == board[2][2] is not None or \
       board[0][2] == board[1][1] == board[2][0] is not None:
        return True

    if all(board[i][j] is not None for i in range(3) for j in range(3)):
        return True

    return False

# Check and return the winner ('X', 'O') if there is one, otherwise return None.
def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] is not None:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] is not None:
        return board[0][2]

    return None

# Minimax algorithm for determining the best move for the computer player.
def minimax(board, depth, maximizing_player):
    # Base case: If the game is over, return the evaluation score.
    if is_game_over(board):
        if check_winner(board) == 'X':
            return -1
        elif check_winner(board) == 'O':
            return 1
        else:
            return 0

    if maximizing_player:
        # If it's the maximizing player's turn ('O'), find the maximum evaluation score.
        max_eval = float('-inf') # variable will store the maximum evaluation score among the possible moves.
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:  # if empty
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False) # call recursively minimax with updated board and increasing the level , and
                    board[i][j] = None
                    # Update max_eval to the maximum value between its current value and the evaluation score obtained from the recursive call
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        # If it's the minimizing player's turn ('X'), find the minimum evaluation score.
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True) # we set True because in next level of the tree will be the turn maximizing Player
                    board[i][j] = None
                    min_eval = min(min_eval, eval)
        return min_eval

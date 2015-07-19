"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants
NTRIALS = 100        # Number of trials to run
SCORE_CURRENT = 1.8 # Score for squares played by the current player
SCORE_OTHER = 1.3   # Score for squares played by the other player

def mc_trial(board, player):
    """
    Takes the current board at play and simulates remaining moves until a win 
    or draw. First move starts with specified player
    """
    while board.check_win() == None:
        move_options = board.get_empty_squares()
        next_move_index = random.randrange(0, len(move_options))
        next_move = move_options[next_move_index]
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    Updates a running score board of same size as the game board with scores 
    favoring the winner. If a draw occurs, no scores are added to the score 
    board.
    """
    winner = board.check_win()
    if winner != provided.DRAW:
        loser = provided.switch_player(winner)
        machine_win = (winner == player)
    else:
        loser = None
        machine_win = None
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if machine_win:
                if board.square(row, col) == winner:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == loser:
                    scores[row][col] -= SCORE_OTHER
            elif machine_win != None:
                if board.square(row, col) == winner:
                    scores[row][col] += SCORE_OTHER
                elif board.square(row, col) == loser:
                    scores[row][col] -= SCORE_CURRENT

def get_best_move(board, scores):
    """
    Generates a random next move given the current board and the corresponding 
    score board of same dimensions. The next move is randomly chosen from the 
    board's empty squares that correspond to the highest scores in the score 
    board.
    """
    move_options = board.get_empty_squares()
    if len(move_options) > 0:
        scores_dict = {}
        for idx in range(0, len(move_options)):
            row = move_options[idx][0]
            col = move_options[idx][1]
            if scores_dict.get(scores[row][col]) == None:
                scores_dict[scores[row][col]] = [move_options[idx]]
            else:
                scores_dict[scores[row][col]].append(move_options[idx])
        max_score = max(scores_dict.keys())
        if len(scores_dict[max_score]) > 1:
            next_move_i = random.randrange(0, len(scores_dict[max_score]))
            next_move = scores_dict[max_score][next_move_i]
        else:
            next_move = scores_dict[max_score][0]
        return next_move
    else:
        raise TypeError("Cannot call function on a board with no empty squares")

def mc_move(board, player, trials):
    """
    Returns next move location with highest score given a number of trials over 
    which to simulate the remaining game moves of the current board. The first 
    move is specified by the player.
    """
    dim = board.get_dim()
    scores = [[0 for dummy_row in range(dim)] for dummy_col in range(dim)]
    if len(board.get_empty_squares()) >= 1:
        for dummy_trial in range(0, trials):
            cloned = board.clone()
            mc_trial(cloned, player)
            mc_update_scores(scores, cloned, player)
        move = get_best_move(board, scores)
    return move

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

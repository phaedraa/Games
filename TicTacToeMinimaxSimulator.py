"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as ttt_info

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES
SCORES = {ttt_info.PLAYERX: 1,
          ttt_info.DRAW: 0,
          ttt_info.PLAYERO: -1}

def return_max_score_and_pos(results_array):
    '''
    Finds max score and associated next best move from results_array
    '''
    max_val = -2
    for val_pos in results_array:
        if val_pos[0] > max_val:
            max_val = val_pos[0]
            best_move = val_pos
    return best_move

def return_min_score_and_pos(results_array):
    '''
    Finds max score and associated next best move from results_array
    '''
    min_val = 2
    for val_pos in results_array:
        if val_pos[0] < min_val:
            min_val = val_pos[0]
            best_move = val_pos
    return best_move

def return_opt_score_and_pos(board, player, min_or_max_func):
    '''
    Returns the optimal score and associated next best move for given player,
    depending on an inputted minimization or maximization function.
    '''
    if board.check_win():
        return SCORES[board.check_win()] # (0/1/-1) depending on win/lose/tie
    else:
        results_array = []
        for empty_spot in board.get_empty_squares():
            board_copy = board.clone()
            next_player = ttt_info.switch_player(player)
            board_copy.move(empty_spot[0], empty_spot[1], player)
            result = mm_move(board_copy, next_player)
            if type(result) == int:	
                results_array.append((result, empty_spot))	
            else:
                results_array.append((result[0], empty_spot))
        return min_or_max_func(results_array)

def mm_move(board, player):
    '''
    Returns the next best move and result that would occur given all players
    always choose a move that will cause a win or draw for them. This game
    optimizes for player X to win the game.
    '''
    if player == ttt_info.PLAYERX:
        return return_opt_score_and_pos(board, player, return_max_score_and_pos)
    elif player == ttt_info.PLAYERO:
        return return_opt_score_and_pos(board, player, return_min_score_and_pos)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert type(move) != int, "returned illegal move: no more moves left"
    return move[1]

# ttt_info.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, ttt_info.PLAYERO, move_wrapper, 1, False)

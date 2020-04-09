"""
An AI player for Othello.
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache_board = {}

def eprint(*args, **kwargs):  # you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    # IMPLEMENT
    num_black, num_white = get_score(board)
    if color == 1:
        return num_black - num_white
    else:
        return num_white - num_black


# Better heuristic value of board
def compute_heuristic(board, color):  # not implemented, optional
    # IMPLEMENT
    return 0  # change this!


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching=0):
    # IMPLEMENT
    if caching and (board, color) in cache_board:
        return cache_board[(board, color)]

    possible_moves = get_possible_moves(board, 3 - color)
    if not possible_moves or limit == 0:
        if caching:
            cache_board[(board, color)] = (None, compute_utility(board, color))
        return (None, compute_utility(board, color))
    min_uti = float('inf')
    min_tuple = None
    limit -= 1
    for m in possible_moves:




        new_board = play_move(board, 3 - color, m[0], m[1])
        t = minimax_max_node(new_board, color, limit)

        if t[1] < min_uti:


            min_uti = t[1]
            min_tuple = m
    if caching:
        cache_board[(board, color)] = (min_tuple, min_uti)

    return (min_tuple, min_uti)


def minimax_max_node(board, color, limit, caching=0):  # returns highest possible utility
    # IMPLEMENT
    if caching and (board, color) in cache_board:
        return cache_board[(board, color)]

    possible_moves = get_possible_moves(board, color)
    if not possible_moves or limit == 0:
        utility = compute_utility(board, color)
        if caching:
            cache_board[(board, color)] = (None, utility)
        return (None, utility)
    max_uti = float('-inf')
    max_tuple = None
    limit -= 1
    for m in possible_moves:




        new_board = play_move(board, color, m[0], m[1])
        t = minimax_min_node(new_board, color, limit)

        if t[1] > max_uti:


            max_uti = t[1]
            max_tuple = m
    if caching:
        cache_board[(board, color)] = (max_tuple, max_uti)

    return (max_tuple, max_uti)


def select_move_minimax(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    # IMPLEMENT
    global cache_board
    cache_board = {}
    max_tuple = minimax_max_node(board, color, limit, caching)
    return max_tuple[0]  # change this!


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT
    if caching and (board, color) in cache_board:
        return cache_board[(board, color)]

    possible_moves = get_possible_moves(board, 3 - color)
    if not possible_moves or limit == 0:
        if caching:
            cache_board[(board, color)] = (None, compute_utility(board, color))
        return (None, compute_utility(board, color))
    min_uti = float('inf')
    min_tuple = None
    limit -= 1
    new_moves = []
    for m in possible_moves:
        new_graph = play_move(board, 3 - color, m[0], m[1])
        new_moves.append((m, compute_utility(new_graph, color), new_graph))
    if ordering:
        new_moves.sort(key=lambda tup: tup[1])

    for element in new_moves:
        t = alphabeta_max_node(element[2], color, alpha, beta, limit, caching, ordering)
        if t[1] < min_uti:
            min_tuple = element[0]
            min_uti = t[1]
        beta = min(min_uti, beta)
        if alpha >= beta:
            break
    if caching:
        cache_board[(board, color)] = (min_tuple, min_uti)

    return (min_tuple, min_uti)


def alphabeta_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT
    if caching and (board, color) in cache_board:
        return cache_board[(board, color)]
    possible_moves = get_possible_moves(board, color)
    if not possible_moves or limit == 0:
        if caching:
            cache_board[(board, color)] = (None, compute_utility(board, color))
        return (None, compute_utility(board, color))

    max_uti = float('-inf')
    max_tuple = None
    limit -= 1

    new_moves = []
    for m in possible_moves:
        new_graph = play_move(board, color, m[0], m[1])
        new_moves.append((m, compute_utility(new_graph, color), new_graph))
    if ordering:
        new_moves.sort(key=lambda tup: tup[1], reverse=True)

    for element in new_moves:
        t = alphabeta_min_node(element[2], color, alpha, beta, limit, caching, ordering)
        if t[1] > max_uti:
            max_tuple = element[0]
            max_uti = t[1]
        alpha = max(max_uti, alpha)
        if alpha >= beta:
            break
    if caching:
        cache_board[(board, color)] = (max_tuple, max_uti)

    return (max_tuple, max_uti)  # change this!


def select_move_alphabeta(board, color, limit, caching=0, ordering=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    # IMPLEMENT
    alpha = float('-inf')
    beta = float('inf')

    global cache_board
    cache_board= {}
    max_tuple = alphabeta_max_node(board, color, alpha, beta, limit, caching, ordering)

    return max_tuple[0]  # change this!


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)

    if (minimax == 1):
        eprint("Running MINIMAX")
    else:
        eprint("Running ALPHA-BETA")

    if (caching == 1):
        eprint("State Caching is ON")
    else:
        eprint("State Caching is OFF")

    if (ordering == 1):
        eprint("Node Ordering is ON")
    else:
        eprint("Node Ordering is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1):  # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else:  # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()

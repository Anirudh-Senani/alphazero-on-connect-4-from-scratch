"""
AlphaZero on Connect-4 from Scratch

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - make_empty_board
import numpy as np

def make_empty_board():
    """Return a 6x7 integer numpy array of zeros representing an empty Connect-4 board."""
    # TODO: create a 6x7 integer array of zeros and return it
    return np.zeros((6,7), dtype=int)

# Step 2 - column_top_row
def column_top_row(board, column):
    """Return the lowest empty row in `column`, or -1 if the column is full."""
    # TODO: scan the column from the bottom up and return the first empty row index
    return (board[:,column] == 0).sum() - 1

# Step 3 - drop_piece
def drop_piece(board, column, player):
    # TODO: place `player` in the lowest empty row of `column` and return the new board
    row = column_top_row(board, column)
    if row == -1:
        raise ValueError

    new_board = board.copy()
    new_board[row, column] = player
    return new_board

# Step 4 - column_full
import numpy as np

def column_full(board, column):
    """Return True if `column` has no empty rows left."""
    # TODO: check whether the column can still accept a piece
    return bool(column_top_row(board, column) == -1)

# Step 5 - valid_moves
def valid_moves(board):
    # TODO: return a list of column indices that still have at least one empty row
    rows, cols = board.shape
    return [col for col in range(cols) if not column_full(board, col)]

# Step 6 - four_in_a_row_horizontal
def four_in_a_row_horizontal(board):
    # TODO: scan every row for four consecutive matching non-zero pieces horizontally
    rows, cols = board.shape
    slices = []
    for i in range(cols-3):
        slices.append(board[:, i:i+4])

    win1 = np.full((rows, 4), False)
    win2 = np.full((rows, 4), False)
    for i in range(len(slices)):
        win1 = win1 | np.all(slices[i]==1, axis=-1, keepdims=True)
        win2 = win2 | np.all(slices[i]==2, axis=-1, keepdims=True)

    return 1 if np.any(win1) else 2 if np.any(win2) else 0

# Step 7 - four_in_a_row_vertical
def four_in_a_row_vertical(board):
    # TODO: scan every column for four consecutive matching non-zero pieces vertically
    return four_in_a_row_horizontal(board.T)

# Step 8 - four_in_a_row_diagonal_down_right
def four_in_a_row_diagonal_down_right(board):
    # TODO: scan every down-right diagonal of the 6x7 board for four matching non-zero pieces
    r_idx = np.array([0, 1, 2])[:, None, None]  # shape (3, 1, 1)
    c_idx = np.array([0, 1, 2, 3])[None, :, None] # shape (1, 4, 1)
    diags_idx = np.array([0, 1, 2, 3])[None, None, :] # shape (1, 1, 4)

    # Grid of coordinates
    R_pos = r_idx + diags_idx
    C_pos = c_idx + diags_idx

    # Extract all positive 4-length diagonals: shape (3, 4, 4)
    pos_diags = board[R_pos, C_pos]
    # Check if all 4 elements in the last axis are equal to the first element
    win1 = np.all((pos_diags == pos_diags[:, :, :1]) & (pos_diags==1), axis=2)
    win2 = np.all((pos_diags == pos_diags[:, :, :1]) & (pos_diags==2), axis=2)
    # print(pos_match)
    win1 = np.any(win1)
    win2 = np.any(win2)

    return 1 if win1 else 2 if win2 else 0

# Step 9 - four_in_a_row_diagonal_up_right
def four_in_a_row_diagonal_up_right(board):
    # TODO: scan every up-right diagonal for four consecutive matching non-zero pieces
    r_idx = np.array([3, 4, 5])[:, None, None]  # shape (3, 1, 1)
    c_idx = np.array([0, 1, 2, 3])[None, :, None] # shape (1, 4, 1)
    diags_idx = np.array([0, 1, 2, 3])[None, None, :] # shape (1, 1, 4)

    # Grid of coordinates
    R_pos = r_idx - diags_idx
    C_pos = c_idx + diags_idx

    # Extract all positive 4-length diagonals: shape (3, 4, 4)
    neg_diags = board[R_pos, C_pos]
    # Check if all 4 elements in the last axis are equal to the first element
    win1 = np.all((neg_diags == neg_diags[:, :, :1]) & (neg_diags==1), axis=2)
    win2 = np.all((neg_diags == neg_diags[:, :, :1]) & (neg_diags==2), axis=2)
    # print(pos_match)
    win1 = np.any(win1)
    win2 = np.any(win2)

    return 1 if win1 else 2 if win2 else 0

# Step 10 - check_winner
import numpy as np

def check_winner(board):
    """Return 1 or 2 if that player has four in a row, else 0."""
    # TODO: combine the four direction scans and return the first non-zero result
    hres = four_in_a_row_horizontal(board)
    vres = four_in_a_row_vertical(board)
    rdiag = four_in_a_row_diagonal_up_right(board)
    ldiag = four_in_a_row_diagonal_down_right(board)

    if 1 in (hres, vres, rdiag, ldiag):
        return 1
    elif 2 in (hres, vres, rdiag, ldiag):
        return 2
    else:
        return 0

# Step 11 - board_is_full
def board_is_full(board):
    # TODO: return True when no column has an empty slot left
    return not any(valid_moves(board))

# Step 12 - is_terminal (not yet solved)
# TODO: implement

# Step 13 - other_player (not yet solved)
# TODO: implement

# Step 14 - step_env (not yet solved)
# TODO: implement

# Step 15 - encode_board (not yet solved)
# TODO: implement

# Step 16 - board_to_torch_tensor (not yet solved)
# TODO: implement

# Step 17 - init_conv_backbone (not yet solved)
# TODO: implement

# Step 18 - init_policy_head (not yet solved)
# TODO: implement

# Step 19 - init_value_head (not yet solved)
# TODO: implement

# Step 20 - build_policy_value_net (not yet solved)
# TODO: implement

# Step 21 - policy_value_forward (not yet solved)
# TODO: implement

# Step 22 - action_mask (not yet solved)
# TODO: implement

# Step 23 - masked_policy_logits (not yet solved)
# TODO: implement

# Step 24 - masked_log_softmax (not yet solved)
# TODO: implement

# Step 25 - sample_action_from_policy (not yet solved)
# TODO: implement

# Step 26 - greedy_action_from_policy (not yet solved)
# TODO: implement

# Step 27 - make_mcts_node (not yet solved)
# TODO: implement

# Step 28 - node_q_value (not yet solved)
# TODO: implement

# Step 29 - ucb_score (not yet solved)
# TODO: implement

# Step 30 - select_best_child (not yet solved)
# TODO: implement

# Step 31 - select_leaf (not yet solved)
# TODO: implement

# Step 32 - evaluate_with_network (not yet solved)
# TODO: implement

# Step 33 - expand_node (not yet solved)
# TODO: implement

# Step 34 - backup_value (not yet solved)
# TODO: implement

# Step 35 - run_one_simulation (not yet solved)
# TODO: implement

# Step 36 - run_mcts (not yet solved)
# TODO: implement

# Step 37 - visit_count_policy (not yet solved)
# TODO: implement

# Step 38 - mcts_choose_action (not yet solved)
# TODO: implement

# Step 39 - record_self_play_step (not yet solved)
# TODO: implement

# Step 40 - play_self_play_game (not yet solved)
# TODO: implement

# Step 41 - assign_value_targets (not yet solved)
# TODO: implement

# Step 42 - generate_self_play_batch (not yet solved)
# TODO: implement

# Step 43 - value_loss_mse (not yet solved)
# TODO: implement

# Step 44 - policy_loss_cross_entropy (not yet solved)
# TODO: implement

# Step 45 - l2_regularization_loss (not yet solved)
# TODO: implement

# Step 46 - combined_loss (not yet solved)
# TODO: implement

# Step 47 - encode_batch_states (not yet solved)
# TODO: implement

# Step 48 - iterate_minibatches (not yet solved)
# TODO: implement

# Step 49 - training_step (not yet solved)
# TODO: implement

# Step 50 - training_epoch (not yet solved)
# TODO: implement

# Step 51 - self_play_iteration (not yet solved)
# TODO: implement

# Step 52 - train_loop (not yet solved)
# TODO: implement

# Step 53 - random_policy_action (not yet solved)
# TODO: implement

# Step 54 - greedy_agent_action (not yet solved)
# TODO: implement

# Step 55 - play_one_match (not yet solved)
# TODO: implement

# Step 56 - match_win_rate (not yet solved)
# TODO: implement

# Step 57 - evaluate_against_random (not yet solved)
# TODO: implement


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

# Step 12 - is_terminal
def is_terminal(board):
    # TODO: return (done, winner) using check_winner and board_is_full.
    winner = check_winner(board)
    if winner != 0:
        return (True, winner)
    elif board_is_full(board):
        return (True, 0)
    else:
        return (False, 0)

# Step 13 - other_player
def other_player(player):
    # TODO: return the opponent's player code (1 <-> 2)
    return 2 if player==1 else 1

# Step 14 - step_env
def step_env(board, column, player):
    # TODO: drop piece for player, then return (new_board, done, winner, next_player).
    new_board = drop_piece(board, column, player)
    done, winner = is_terminal(new_board)
    next_player = other_player(player)

    return new_board, done, winner, next_player

# Step 15 - encode_board
def encode_board(board, current_player):
    """Encode a 6x7 board as a (2, 6, 7) float32 tensor from current_player's view."""
    # TODO: build two binary planes (current player, opponent) and stack them
    current_channel = (board==current_player)
    opponent_channel = (board==other_player(current_player))

    return np.stack([current_channel, opponent_channel], dtype=np.float32)

# Step 16 - board_to_torch_tensor
import torch


def board_to_torch_tensor(board, current_player):
    # TODO: encode the board and return it as a float32 torch tensor of shape (1, 2, 6, 7).
    encoding = encode_board(board, current_player)
    encoding = torch.from_numpy(encoding).float()

    return torch.unsqueeze(encoding, 0)

# Step 17 - init_conv_backbone
import torch.nn as nn


def init_conv_backbone(in_channels=2, hidden_channels=16):
    # TODO: Build a small convolutional backbone preserving the 6x7 spatial shape.
    kernel_size = (3, 3)
    model = nn.Sequential(
        nn.Conv2d(in_channels, hidden_channels, kernel_size, padding='same'),
        nn.ReLU(),
        nn.Conv2d(hidden_channels, hidden_channels, kernel_size, padding='same'),
        nn.ReLU()
    )

    return model

# Step 18 - init_policy_head
import torch
import torch.nn as nn

def init_policy_head(hidden_channels=16, num_columns=7):
    """Return an nn.Module mapping (B, hidden_channels, 6, 7) -> (B, num_columns) logits."""
    # TODO: build a small policy head that projects backbone features to column logits
    kernel_size = (1, 1)
    out_channels = hidden_channels//4
    model = nn.Sequential(
        nn.Conv2d(hidden_channels, out_channels, kernel_size, padding='same'),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(out_channels*6*7, num_columns)
    )

    return model

# Step 19 - init_value_head
import torch
import torch.nn as nn

def init_value_head(hidden_channels=16):
    """Return an nn.Module mapping (B, hidden_channels, 6, 7) -> (B, 1) in (-1, 1)."""
    # TODO: build a value head that collapses backbone features to a single bounded scalar per board.
    out_channels = hidden_channels//4
    kernel_size = (1, 1)
    model = nn.Sequential(
        nn.Conv2d(hidden_channels, out_channels, kernel_size, padding='same'),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(out_channels*6*7, 7),
        nn.ReLU(),
        nn.Linear(7, 1),
        nn.Tanh()
    )

    return model

# Step 20 - build_policy_value_net
import torch
import torch.nn as nn


class PolicyValueNet(nn.Module):
    def __init__(self, in_channels, hidden_channels, num_columns):
        super().__init__()
    
        self.backbone = init_conv_backbone(in_channels, hidden_channels)
        self.policy_head = init_policy_head(hidden_channels, num_columns)
        self.value_head = init_value_head(hidden_channels)


    def forward(self, x):
        x = self.backbone(x)
        logits = self.policy_head(x)
        value = self.value_head(x)
        return (logits, value)


def build_policy_value_net(in_channels=2, hidden_channels=16, num_columns=7):
    """Compose backbone + policy head + value head into one nn.Module."""
    # TODO: build an nn.Module with backbone, policy_head, value_head attributes
    return PolicyValueNet(in_channels, hidden_channels, num_columns)

# Step 21 - policy_value_forward
import torch
import torch.nn as nn

def policy_value_forward(net, encoded_board):
    """Run encoded_board (B,2,6,7) through net and return (logits, value)."""
    # TODO: call the network on the encoded board and return its two outputs
    return net(encoded_board)

# Step 22 - action_mask
import numpy as np

def action_mask(board):
    # TODO: return a length-7 boolean mask, True where the column is legal
    mask = np.full(7, False)
    mask[valid_moves(board)] = True
    return mask

# Step 23 - masked_policy_logits
import torch

def masked_policy_logits(logits, mask):
    """Set logits at illegal columns to -inf.

    logits: torch.Tensor of shape (..., 7)
    mask:   bool array/tensor of shape (7,), True = legal
    returns: torch.Tensor of same shape as logits
    """
    # TODO: replace logits at illegal columns with negative infinity
    if len(logits.shape) > 1:
        mask = mask[None, :]
    return torch.where(torch.tensor(mask), logits, -torch.inf)

# Step 24 - masked_log_softmax
import torch

def masked_log_softmax(logits, mask):
    """Log-softmax of logits with illegal columns (mask=False) forced to -inf."""
    # TODO: mask out illegal columns, then apply log-softmax over the last dim.
    masked_logits = masked_policy_logits(logits, mask)
    exp_logits = torch.exp(masked_logits - masked_logits.max(dim=-1, keepdim=True).values)
    probs = exp_logits/exp_logits.sum(axis=-1, keepdim=True)

    return torch.log(probs)

# Step 25 - sample_action_from_policy
import torch

def sample_action_from_policy(logits, mask, temperature=1.0):
    """Sample a legal column from a tempered masked categorical policy."""
    # TODO: scale logits by temperature, mask illegal columns, sample one index
    if temperature <= 0.0:
        temperature = 1.0

    logits /= temperature
    masked_logits = masked_policy_logits(logits, mask)
    dist = torch.softmax(masked_logits, dim=-1)

    return int(torch.multinomial(dist, 1, replacement=False))

# Step 26 - greedy_action_from_policy
import torch

def greedy_action_from_policy(logits, mask):
    """Return the argmax legal column index from masked policy logits."""
    # TODO: mask out illegal columns then return the argmax as a python int
    masked_logits = masked_policy_logits(logits, mask)
    return int(torch.argmax(masked_logits))

# Step 27 - make_mcts_node
def make_mcts_node(prior=0.0, parent=None):
    # TODO: build a dict with prior, visit_count, value_sum, children, and parent fields.
    return dict(
        prior=prior,
        visit_count=0,
        value_sum=0.0,
        children={},
        parent=parent
    )

# Step 28 - node_q_value
def node_q_value(node):
    # TODO: return the mean value Q = value_sum / visit_count, or 0.0 if visit_count == 0
    return node['value_sum']/node['visit_count'] if node['visit_count'] > 0 else 0.0

# Step 29 - ucb_score
import math

def ucb_score(parent, child, c_puct=1.5):
    # TODO: return Q(child) + c_puct * prior * sqrt(N_parent) / (1 + N_child)
    return node_q_value(child) + c_puct * child['prior'] * math.sqrt(parent['visit_count'])/(1 + child['visit_count'])

# Step 30 - select_best_child
def select_best_child(node, legal_actions, c_puct=1.5):
    # TODO: return (action, child) maximizing PUCT among legal children of node.
    action = max(legal_actions, key=lambda x: (ucb_score(node, node['children'][x], c_puct), node['children'][x]['prior']))
    child = node['children'][action]
    return action, child

# Step 31 - select_leaf
def select_leaf(root, c_puct):
    # TODO: walk down the MCTS tree picking the best PUCT child until a non-expanded node is reached
    head = root
    while head.get('is_expanded', False):
        action, head = select_best_child(head, list(head['children'].keys()), c_puct)

    return head

# Step 32 - evaluate_with_network
def evaluate_with_network(net, state, to_play):
    # TODO: run net on encoded state and return (masked priors np.ndarray (7,), value float)
    encoded_board = board_to_torch_tensor(state, to_play)
    net.eval()

    with torch.no_grad():
        logits, value = policy_value_forward(net, encoded_board)
        mask = action_mask(state)
        logprobs = masked_log_softmax(logits, mask)
        priors = torch.exp(logprobs)

    return priors.squeeze(0).numpy(), float(value)

# Step 33 - expand_node
def expand_node(node, priors):
    # TODO: attach a child node for every legal move with the corresponding network prior
    next_player = other_player(node['to_play'])
    node['is_expanded'] = True

    for action in valid_moves(node['board']):
        node['children'][action] = make_mcts_node(priors[action], node)
        node['children'][action]['board'] = drop_piece(node['board'], action, node['to_play'])
        node['children'][action]['to_play'] = next_player
        node['children'][action]['is_expanded'] = False

    return node

# Step 34 - backup_value
def backup_value(leaf, value):
    # TODO: walk from leaf up through parents, updating visit_count and value_sum with alternating signs
    node = leaf
    sign = 1
    node['value_sum'] += sign * value
    node['visit_count'] += 1
    while node['parent'] is not None:
        sign = -sign
        node['parent']['visit_count'] += 1
        node['parent']['value_sum'] += sign * value
        node = node['parent']

# Step 35 - run_one_simulation
def run_one_simulation(root, net, c_puct):
    # TODO: run one MCTS simulation: select a leaf, evaluate, expand if non-terminal, backup.
    leaf = select_leaf(root, c_puct)
    done, winner = is_terminal(leaf['board'])
    if done:
        value = 0.0
        if winner != 0 and winner != leaf['to_play']:
            value = -1.0
        elif winner != 0:
            value = 1.0
        leaf['is_expanded'] = False
    else:
        priors, value = evaluate_with_network(net, leaf['board'], leaf['to_play'])
        leaf = expand_node(leaf, priors)

    backup_value(leaf, value)

# Step 36 - run_mcts
def run_mcts(state, to_play, net, num_simulations, c_puct):
    # TODO: build a fresh root for (state, to_play) and run num_simulations PUCT simulations
    root = make_mcts_node()
    root['board'] = state
    root['to_play'] = to_play

    for _ in range(num_simulations):
        run_one_simulation(root, net, c_puct)

    return root

# Step 37 - visit_count_policy
def visit_count_policy(root, temperature=1.0):
    # TODO: convert root child visit counts into a length-7 probability vector over columns
    if not root['children']:
        return np.full(7, 1/7)
    
    probs = np.zeros(7)
    for child in root['children']:
        probs[child] = root['children'][child]['visit_count']

    if temperature == 0.0:
        ind = np.argmax(probs)
        probs = np.zeros(7)
        probs[ind] = 1.0
    else:
        tempered = probs**(1/temperature)
        probs = tempered/tempered.sum()

    return probs

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

